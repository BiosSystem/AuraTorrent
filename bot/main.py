import asyncio
import functools
import html
import logging
import os
import time
from collections import defaultdict, deque
from typing import Callable, Optional, List, TypedDict

class RssFeed(TypedDict, total=False):
    url: str
    uid: str
    hasError: bool
    isLoading: bool
    articles: List[dict]

class RssRuleDef(TypedDict, total=False):
    enabled: bool
    mustContain: str
    mustNotContain: str
    useRegex: bool
    episodeFilter: str
    smartFilter: bool
    previouslyMatchedEpisodes: List[str]
    affectedFeeds: List[str]
    ignoreDays: int
    lastMatch: str
    addPaused: bool
    assignedCategory: str
    savePath: str

class TorrentData(TypedDict, total=False):
    hash: str
    name: str
    state: str

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Explicit owner takes priority; falls back to the first entry in ALLOWED_USERS.
OWNER_ID = int(os.getenv("OWNER_ID", "0")) or None
ALLOWED_USERS = [int(u.strip()) for u in os.getenv("ALLOWED_USERS", "").split(",") if u.strip()]
ALLOWED_USERS_FILE = os.getenv("ALLOWED_USERS_FILE", "allowed_users.txt")

# Load persisted allowed users if the file exists
if os.path.exists(ALLOWED_USERS_FILE):
    try:
        with open(ALLOWED_USERS_FILE, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped.isdigit():
                    uid = int(stripped)
                    if uid not in ALLOWED_USERS:
                        ALLOWED_USERS.append(uid)
    except OSError as e:
        logger.warning(f"Could not read {ALLOWED_USERS_FILE}: {e}")

QBITTORRENT_URL = os.getenv("QBITTORRENT_URL", "http://localhost:8080")
QBITTORRENT_USER = os.getenv("QBITTORRENT_USER", "admin")
QBITTORRENT_PASS = os.getenv("QBITTORRENT_PASS", "adminadmin")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))

# Per-user command rate limit: at most RATE_LIMIT_MAX commands per
# RATE_LIMIT_WINDOW seconds. Applies to allowed and rejected users alike, so a
# compromised or misbehaving client cannot hammer the qBittorrent API or spam
# unauthorized-access log lines.
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "5"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "10"))
# Minimum seconds between repeated "unauthorized access" alerts sent to the
# owner for the same user id, so a persistent attacker cannot spam the owner.
UNAUTHORIZED_ALERT_COOLDOWN = int(os.getenv("UNAUTHORIZED_ALERT_COOLDOWN", "300"))

# Dispatcher is created at import time; the Bot is created in main() so this
# module can be imported (and unit-tested) without a valid token.
dp = Dispatcher()
bot: Optional[Bot] = None

from enum import Enum

class TorrentState(str, Enum):
    DOWNLOADING = "downloading"
    UPLOADING = "uploading"
    ERROR = "error"
    MISSING_FILES = "missingFiles"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

def handle_transition(prev: TorrentState, new: TorrentState, name: str) -> Optional[str]:
    if prev == TorrentState.DOWNLOADING and new == TorrentState.UPLOADING:
        return _fmt_finished(name)
    if new in (TorrentState.ERROR, TorrentState.MISSING_FILES):
        return _fmt_error(name, new.value)
    return None

# Maps torrent hash -> last known state, used to detect transitions.
known_torrents: dict[str, TorrentState] = {}


def owner_id() -> Optional[int]:
    """Return the primary owner id: explicit OWNER_ID, else first allowed user."""
    if OWNER_ID:
        return OWNER_ID
    return ALLOWED_USERS[0] if ALLOWED_USERS else None


def is_allowed(user_id: int) -> bool:
    if not ALLOWED_USERS:
        logger.warning(f"Blocked command from user {user_id}: ALLOWED_USERS is empty or unset.")
        return False
    return user_id in ALLOWED_USERS


# Sliding-window timestamps of recent commands, keyed by Telegram user id.
_command_times: dict[int, deque] = defaultdict(deque)
# Last time an "unauthorized access" alert was sent to the owner, per user id.
_last_unauthorized_alert: dict[int, float] = {}


def is_rate_limited(user_id: int) -> bool:
    """True if this user has exceeded RATE_LIMIT_MAX commands in the current window."""
    now = time.monotonic()
    times = _command_times[user_id]
    while times and now - times[0] > RATE_LIMIT_WINDOW:
        times.popleft()
    if len(times) >= RATE_LIMIT_MAX:
        return True
    times.append(now)
    return False


async def _alert_owner_unauthorized(message: Message) -> None:
    """Notify the owner of a rejected access attempt, throttled per user."""
    user = message.from_user
    now = time.monotonic()
    last = _last_unauthorized_alert.get(user.id, 0.0)
    if now - last < UNAUTHORIZED_ALERT_COOLDOWN:
        return
    _last_unauthorized_alert[user.id] = now

    owner = owner_id()
    if owner is None or bot is None:
        return
    username = f"@{user.username}" if user.username else "no username"
    try:
        await bot.send_message(
            owner,
            f"⛔ <b>Unauthorized access attempt</b>\nUser ID: <code>{user.id}</code> ({html.escape(username)})",
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error(f"Failed to alert owner about unauthorized user {user.id}: {e}")


def guarded(handler: Callable) -> Callable:
    """Decorator applying auth, unauthorized-access alerting, and rate limiting
    to a message handler, in that order, before it runs."""

    @functools.wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        user_id = message.from_user.id
        if not is_allowed(user_id):
            logger.warning(f"Rejected command from unauthorized user {user_id} ({message.from_user.username}).")
            await _alert_owner_unauthorized(message)
            return
        if is_rate_limited(user_id):
            logger.warning(f"Rate-limited user {user_id}: exceeded {RATE_LIMIT_MAX} commands / {RATE_LIMIT_WINDOW}s.")
            await message.reply("⏳ Too many commands, please slow down.")
            return
        return await handler(message, *args, **kwargs)

    return wrapper


def _fmt_finished(name: str) -> str:
    return f"✅ <b>Download Finished:</b>\n<code>{html.escape(name)}</code>"


def _fmt_error(name: str, state: str) -> str:
    return f"⚠️ <b>Torrent Error:</b>\n<code>{html.escape(name)}</code>\nState: {html.escape(state)}"


from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

def _return_none_on_error(retry_state):
    return None

def _return_false_on_error(retry_state):
    return False

class QBittorrentClient:
    """Holds a single authenticated session and re-authenticates only on demand."""

    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
        self._timeout = aiohttp.ClientTimeout(total=15)

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=lambda rs: logger.warning(f"Connection error during login. Retrying... (Attempt {rs.attempt_number})"),
        retry_error_callback=_return_false_on_error
    )
    async def login(self) -> bool:
        """Authenticate against the qBittorrent API, storing the SID cookie."""
        session = await self._ensure_session()
        login_url = f"{QBITTORRENT_URL}/api/v2/auth/login"
        data = {"username": QBITTORRENT_USER, "password": QBITTORRENT_PASS}
        
        async with session.post(login_url, data=data) as resp:
            if resp.status == 200:
                return True
            logger.error(f"Login failed: {resp.status}")
            return False

    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=lambda rs: logger.warning(f"Connection error fetching torrents. Retrying... (Attempt {rs.attempt_number})"),
        retry_error_callback=_return_none_on_error
    )
    async def get_torrents(self) -> Optional[List[TorrentData]]:
        """Fetch the torrent list, re-authenticating once if the session expired."""
        session = await self._ensure_session()
        url = f"{QBITTORRENT_URL}/api/v2/torrents/info"
        
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 403:
                # Cookie expired, re-authenticate and retry
                logger.info("Session expired, forcing re-authentication.")
                if await self.login():
                    # Raise an exception to trigger the tenacity retry loop
                    raise aiohttp.ClientError("Triggering retry after re-authentication")
                return None
            logger.error(f"Failed to fetch torrents: {resp.status}")
            return None


    async def add_feed(self, url: str, path: str = "") -> bool:
        session = await self._ensure_session()
        data = {"url": url, "path": path}
        async with session.post(f"{QBITTORRENT_URL}/api/v2/rss/addFeed", data=data) as resp:
            return resp.status == 200

    async def remove_feed(self, path: str) -> bool:
        session = await self._ensure_session()
        data = {"path": path}
        async with session.post(f"{QBITTORRENT_URL}/api/v2/rss/removeItem", data=data) as resp:
            return resp.status == 200

    async def list_feeds(self) -> dict:
        session = await self._ensure_session()
        async with session.get(f"{QBITTORRENT_URL}/api/v2/rss/items?withData=false") as resp:
            if resp.status == 200:
                return await resp.json()
            return {}

    async def add_rule(self, ruleName: str, ruleDef: dict) -> bool:
        import json
        session = await self._ensure_session()
        data = {"ruleName": ruleName, "ruleDef": json.dumps(ruleDef)}
        async with session.post(f"{QBITTORRENT_URL}/api/v2/rss/setRule", data=data) as resp:
            return resp.status == 200

    async def remove_rule(self, ruleName: str) -> bool:
        session = await self._ensure_session()
        data = {"ruleName": ruleName}
        async with session.post(f"{QBITTORRENT_URL}/api/v2/rss/removeRule", data=data) as resp:
            return resp.status == 200

    async def list_rules(self) -> dict:
        session = await self._ensure_session()
        async with session.get(f"{QBITTORRENT_URL}/api/v2/rss/rules") as resp:
            if resp.status == 200:
                return await resp.json()
            return {}

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()


qbit = QBittorrentClient()


async def poll_torrents() -> None:
    """Background task that polls qBittorrent and reports state transitions."""
    global known_torrents

    await qbit.login()

    while True:
        torrents = await qbit.get_torrents()
        if torrents is not None:
            current_torrents = {t["hash"]: t for t in torrents}

            for t_hash, t_data in current_torrents.items():
                name = t_data.get("name", "Unknown")
                raw_state = t_data.get("state", "unknown")
                state = TorrentState(raw_state)

                if t_hash in known_torrents:
                    prev_state = known_torrents[t_hash]
                    if prev_state != state:
                        msg = handle_transition(prev_state, state, name)
                        if msg:
                            await broadcast_message(msg)

                known_torrents[t_hash] = state

            # Drop torrents that no longer exist
            known_torrents = {h: s for h, s in known_torrents.items() if h in current_torrents}

        await asyncio.sleep(POLL_INTERVAL)


async def broadcast_message(text: str) -> None:
    """Send a message to all allowed users."""
    if bot is None:
        return
    for user_id in ALLOWED_USERS:
        try:
            await bot.send_message(user_id, text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Failed to send to {user_id}: {e}")


@dp.message(Command("start"))
@guarded
async def cmd_start(message: Message):
    await message.reply("🟢 AuraBot is active and monitoring qBittorrent!")


@dp.message(Command("status"))
@guarded
async def cmd_status(message: Message):
    torrents = await qbit.get_torrents()
    if torrents is None:
        await message.reply("🔴 Cannot connect to qBittorrent API.")
        return

    active = sum(1 for t in torrents if t["state"] in ("downloading", "uploading", "stalledDL", "stalledUP"))
    await message.reply(
        f"📊 <b>AuraTorrent Status</b>\nTotal Torrents: {len(torrents)}\nActive: {active}",
        parse_mode="HTML",
    )


@dp.message(Command("add_user"))
async def cmd_add_user(message: Message):
    """Owner command to add new users dynamically.

    Deliberately not gated by is_allowed(): when ALLOWED_USERS is empty and no
    OWNER_ID is set, owner_id() returns None and this becomes the bootstrap
    command that registers the first user. Once an owner exists, only that
    owner may use it. Still rate-limited to slow down id-guessing during the
    open bootstrap window.
    """
    if is_rate_limited(message.from_user.id):
        return

    owner = owner_id()
    if owner is not None and message.from_user.id != owner:
        logger.warning(f"Rejected /add_user from non-owner user {message.from_user.id}.")
        await _alert_owner_unauthorized(message)
        await message.reply("⛔ Only the primary owner can add users.")
        return

    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("Usage: /add_user <user_id>")
        return

    new_user = int(parts[1])
    if new_user not in ALLOWED_USERS:
        ALLOWED_USERS.append(new_user)
        try:
            with open(ALLOWED_USERS_FILE, "a") as f:
                f.write(f"{new_user}\n")
        except OSError as e:
            logger.error(f"Error saving to {ALLOWED_USERS_FILE}: {e}")
        await message.reply(f"✅ Added user ID: {new_user} (persisted)")
    else:
        await message.reply(f"User {new_user} is already allowed.")



@dp.message(Command("add_feed"))
@guarded
async def cmd_add_feed(message: Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        await message.reply("Usage: /add_feed <url> [name]")
        return
    url = parts[1]
    name = parts[2] if len(parts) > 2 else ""
    success = await qbit.add_feed(url, name)
    if success:
        await message.reply(f"✅ Feed added: {url}")
    else:
        await message.reply(f"❌ Failed to add feed: {url}")

@dp.message(Command("remove_feed"))
@guarded
async def cmd_remove_feed(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Usage: /remove_feed <name>")
        return
    name = parts[1]
    success = await qbit.remove_feed(name)
    if success:
        await message.reply(f"✅ Feed removed: {name}")
    else:
        await message.reply(f"❌ Failed to remove feed: {name}")

@dp.message(Command("list_feeds"))
@guarded
async def cmd_list_feeds(message: Message):
    feeds = await qbit.list_feeds()
    if not feeds:
        await message.reply("No feeds found.")
        return
    text = "📡 <b>RSS Feeds</b>\n"
    for path, data in feeds.items():
        url = data.get("url", "")
        text += f"\n• <code>{html.escape(path)}</code> - {html.escape(url)}"
    await message.reply(text, parse_mode="HTML")

@dp.message(Command("add_rule"))
@guarded
async def cmd_add_rule(message: Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.reply("Usage: /add_rule <name> <mustContain>")
        return
    name = parts[1]
    mustContain = parts[2]
    ruleDef: RssRuleDef = {"enabled": True, "mustContain": mustContain}
    success = await qbit.add_rule(name, ruleDef)
    if success:
        await message.reply(f"✅ Rule added: {name}")
    else:
        await message.reply(f"❌ Failed to add rule: {name}")

@dp.message(Command("remove_rule"))
@guarded
async def cmd_remove_rule(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Usage: /remove_rule <name>")
        return
    name = parts[1]
    success = await qbit.remove_rule(name)
    if success:
        await message.reply(f"✅ Rule removed: {name}")
    else:
        await message.reply(f"❌ Failed to remove rule: {name}")

@dp.message(Command("list_rules"))
@guarded
async def cmd_list_rules(message: Message):
    rules = await qbit.list_rules()
    if not rules:
        await message.reply("No rules found.")
        return
    text = "📜 <b>RSS Rules</b>\n"
    for name, data in rules.items():
        mustContain = data.get("mustContain", "")
        text += f"\n• <code>{html.escape(name)}</code>: {html.escape(mustContain)}"
    await message.reply(text, parse_mode="HTML")

async def main() -> None:
    global bot
    logger.info("Starting AuraBot...")
    bot = Bot(token=BOT_TOKEN)
    # Start polling qBittorrent in the background
    asyncio.create_task(poll_torrents())
    try:
        await dp.start_polling(bot)
    finally:
        await qbit.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
