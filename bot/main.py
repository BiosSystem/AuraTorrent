import asyncio
import logging
import os
import aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERS = [int(u.strip()) for u in os.getenv("ALLOWED_USERS", "").split(",") if u.strip()]
QBITTORRENT_URL = os.getenv("QBITTORRENT_URL", "http://localhost:8080")
QBITTORRENT_USER = os.getenv("QBITTORRENT_USER", "admin")
QBITTORRENT_PASS = os.getenv("QBITTORRENT_PASS", "adminadmin")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Store state for torrents to detect changes
# Dictionary mapping hash to state string
known_torrents = {}

def is_allowed(user_id: int) -> bool:
    return not ALLOWED_USERS or user_id in ALLOWED_USERS

async def get_qbittorrent_session():
    """Authenticate and return an aiohttp session for qBittorrent."""
    session = aiohttp.ClientSession()
    login_url = f"{QBITTORRENT_URL}/api/v2/auth/login"
    data = {'username': QBITTORRENT_USER, 'password': QBITTORRENT_PASS}
    try:
        async with session.post(login_url, data=data) as resp:
            if resp.status == 200:
                return session
            else:
                logger.error(f"Login failed: {resp.status}")
                await session.close()
                return None
    except Exception as e:
        logger.error(f"Connection error: {e}")
        await session.close()
        return None

async def poll_torrents():
    """Background task to poll qBittorrent for torrent state changes."""
    global known_torrents
    
    while True:
        try:
            session = await get_qbittorrent_session()
            if session:
                torrents_url = f"{QBITTORRENT_URL}/api/v2/torrents/info"
                async with session.get(torrents_url) as resp:
                    if resp.status == 200:
                        torrents = await resp.json()
                        current_torrents = {t['hash']: t for t in torrents}
                        
                        # Compare with known torrents
                        for t_hash, t_data in current_torrents.items():
                            name = t_data.get('name', 'Unknown')
                            state = t_data.get('state', 'unknown')
                            
                            if t_hash in known_torrents:
                                prev_state = known_torrents[t_hash]
                                if prev_state != state:
                                    if state == 'uploading' and prev_state == 'downloading':
                                        await broadcast_message(f"✅ **Download Finished:**\n`{name}`")
                                    elif state in ('error', 'missingFiles'):
                                        await broadcast_message(f"⚠️ **Torrent Error:**\n`{name}`\nState: {state}")
                            
                            # Update known state
                            known_torrents[t_hash] = state
                            
                        # Remove deleted torrents
                        known_torrents = {h: s for h, s in known_torrents.items() if h in current_torrents}
                        
                await session.close()
        except Exception as e:
            logger.error(f"Polling error: {e}")
            
        await asyncio.sleep(POLL_INTERVAL)

async def broadcast_message(text: str):
    """Send a message to all allowed users."""
    for user_id in ALLOWED_USERS:
        try:
            await bot.send_message(user_id, text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Failed to send to {user_id}: {e}")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not is_allowed(message.from_user.id):
        await message.reply("⛔ Unauthorized user.")
        return
    await message.reply("🟢 AuraBot is active and monitoring qBittorrent!")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    if not is_allowed(message.from_user.id):
        return
        
    session = await get_qbittorrent_session()
    if not session:
        await message.reply("🔴 Cannot connect to qBittorrent API.")
        return
        
    async with session.get(f"{QBITTORRENT_URL}/api/v2/torrents/info") as resp:
        if resp.status == 200:
            torrents = await resp.json()
            active = sum(1 for t in torrents if t['state'] in ('downloading', 'uploading', 'stalledDL', 'stalledUP'))
            await message.reply(f"📊 **AuraTorrent Status**\nTotal Torrents: {len(torrents)}\nActive: {active}", parse_mode="Markdown")
        else:
            await message.reply("⚠️ Error fetching torrent list.")
    await session.close()

@dp.message(Command("add_user"))
async def cmd_add_user(message: Message):
    """Owner command to add new users dynamically."""
    if len(ALLOWED_USERS) > 0 and message.from_user.id != ALLOWED_USERS[0]:
        await message.reply("⛔ Only the primary owner can add users.")
        return
        
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("Usage: /add_user <user_id>")
        return
        
    new_user = int(parts[1])
    if new_user not in ALLOWED_USERS:
        ALLOWED_USERS.append(new_user)
        # Ideally, we should save this to .env or a database, but we will keep it in memory for now
        await message.reply(f"✅ Added user ID: {new_user}")
    else:
        await message.reply(f"User {new_user} is already allowed.")

async def main():
    logger.info("Starting AuraBot...")
    # Start polling in the background
    asyncio.create_task(poll_torrents())
    # Start bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
