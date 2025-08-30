from pyrogram import Client, filters
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_usernames = [u.strip() for u in os.getenv("BOT_USERNAMES").split(",")]
invite_link = os.getenv("TARGET_CHANNEL_INVITE")
session_string = os.getenv("SESSION_STRING")

if not invite_link:
    raise ValueError("TARGET_CHANNEL_INVITE is missing from .env file!")

app = Client("media_forwarder", session_string=session_string, api_id=api_id, api_hash=api_hash)
web = Flask(__name__)

@web.route("/")
def index():
    return "Telegram Media Forwarder Bot is running."

@app.on_message(filters.chat(bot_usernames) & filters.media)
async def forward_media(client, message):
    try:
        try:
            await client.join_chat(invite_link)
        except Exception as e:
            if "USER_ALREADY_PARTICIPANT" not in str(e):
                print(f"⚠️ Join error: {e}")

        chat = await client.get_chat(invite_link)
        await message.copy(chat.id)
        print(f"✅ Forwarded media to {chat.title}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    web.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Pyrogram client (blocking)
    app.run()