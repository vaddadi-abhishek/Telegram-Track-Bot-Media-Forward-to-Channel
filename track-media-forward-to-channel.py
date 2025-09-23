import asyncio
import logging
import os
from threading import Thread

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from flask import Flask

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

# --- Configuration ---
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")
bot_usernames_str = os.getenv("BOT_USERNAMES")
invite_link = os.getenv("TARGET_CHANNEL_INVITE")

# --- Validate Configuration ---
if not all([api_id, api_hash, session_string, bot_usernames_str, invite_link]):
    raise ValueError("One or more required environment variables are missing from .env file!")

try:
    api_id = int(api_id)
except ValueError:
    raise ValueError("API_ID must be an integer.")

bot_usernames = [u.strip() for u in bot_usernames_str.split(",")]

# --- Pyrogram & Flask Setup ---
app = Client("media_forwarder", session_string=session_string, api_id=api_id, api_hash=api_hash)
web = Flask(__name__)
TARGET_CHAT_ID = None

@web.route("/")
def index():
    return "Telegram Media Forwarder Bot is running."

@app.on_message(filters.chat(bot_usernames) & filters.media)
async def forward_media(_, message):
    """This function is called when a media message is received from a monitored bot."""
    if not TARGET_CHAT_ID:
        logger.warning("Target chat ID not resolved yet, skipping message.")
        return
    try:
        await message.copy(TARGET_CHAT_ID)
        logger.info(f"✅ Copied media from {message.chat.username} to target channel.")
    except Exception as e:
        logger.error(f"❌ Failed to copy message: {e}")

def run_flask():
    """Runs the Flask web server in a separate thread."""
    port = int(os.environ.get("PORT", 8000))
    web.run(host="0.0.0.0", port=port)

async def main():
    """Main function to start the bot and web server."""
    global TARGET_CHAT_ID

    # Run Flask in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    async with app:
        try:
            chat = await app.join_chat(invite_link)
            TARGET_CHAT_ID = chat.id
            logger.info(f"✅ Successfully joined and set target channel: {chat.title}")
        except UserAlreadyParticipant:
            chat = await app.get_chat(invite_link)
            TARGET_CHAT_ID = chat.id
            logger.info(f"✅ Already in the target channel: {chat.title}")
        except Exception as e:
            logger.error(f"❌ Could not join or get chat: {e}")
            return # Exit if we can't get the target chat

        logger.info("🤖 Telegram Media Forwarder Bot is running...")
        await asyncio.Event().wait() # Keep the client running indefinitely

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
