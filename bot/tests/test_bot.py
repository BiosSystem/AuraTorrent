import os
import sys

# Import the bot module from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main as bot  # noqa: E402


def test_is_allowed_accepts_listed_user():
    bot.ALLOWED_USERS = [111, 222]
    assert bot.is_allowed(111) is True
    assert bot.is_allowed(222) is True


def test_is_allowed_rejects_unlisted_user():
    bot.ALLOWED_USERS = [111, 222]
    assert bot.is_allowed(999) is False


def test_is_allowed_denies_when_list_empty():
    bot.ALLOWED_USERS = []
    assert bot.is_allowed(111) is False


def test_owner_id_prefers_explicit_env():
    bot.OWNER_ID = 555
    bot.ALLOWED_USERS = [111, 222]
    assert bot.owner_id() == 555


def test_owner_id_falls_back_to_first_allowed():
    bot.OWNER_ID = None
    bot.ALLOWED_USERS = [111, 222]
    assert bot.owner_id() == 111


def test_owner_id_none_when_no_users():
    bot.OWNER_ID = None
    bot.ALLOWED_USERS = []
    assert bot.owner_id() is None


def test_finished_message_escapes_html_metacharacters():
    msg = bot._fmt_finished("Ubuntu <22.04> & More_[x]")
    # Raw angle brackets and ampersands must be escaped so Telegram HTML parsing
    # cannot be broken (or hijacked) by a crafted torrent name.
    assert "<22.04>" not in msg
    assert "&lt;22.04&gt;" in msg
    assert "&amp;" in msg


def test_error_message_escapes_name_and_state():
    msg = bot._fmt_error("bad<name>", "error")
    assert "bad&lt;name&gt;" in msg
    assert "error" in msg


def test_rate_limit_allows_up_to_max_commands():
    bot.RATE_LIMIT_MAX = 3
    bot.RATE_LIMIT_WINDOW = 10
    bot._command_times.clear()
    for _ in range(3):
        assert bot.is_rate_limited(42) is False


def test_rate_limit_blocks_after_max_commands():
    bot.RATE_LIMIT_MAX = 3
    bot.RATE_LIMIT_WINDOW = 10
    bot._command_times.clear()
    for _ in range(3):
        bot.is_rate_limited(42)
    assert bot.is_rate_limited(42) is True


def test_rate_limit_is_isolated_per_user():
    bot.RATE_LIMIT_MAX = 1
    bot.RATE_LIMIT_WINDOW = 10
    bot._command_times.clear()
    assert bot.is_rate_limited(1) is False
    assert bot.is_rate_limited(2) is False
    assert bot.is_rate_limited(1) is True


def test_rate_limit_window_expires_old_entries():
    bot.RATE_LIMIT_MAX = 1
    bot.RATE_LIMIT_WINDOW = 10
    bot._command_times.clear()
    assert bot.is_rate_limited(7) is False
    # Simulate the window having elapsed by backdating the recorded timestamp.
    bot._command_times[7][0] -= bot.RATE_LIMIT_WINDOW + 1
    assert bot.is_rate_limited(7) is False
