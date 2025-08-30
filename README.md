# Telegram Media Forwarder Bot

A Python bot that automatically forwards media files from multiple Telegram bots to a target channel. Built with Pyrogram and Flask.

## Features

- Monitors multiple Telegram bots for media messages
- Automatically forwards media to a specified target channel
- Handles channel membership automatically
- Web server endpoint for health checks and monitoring
- Environment-based configuration

## Prerequisites

- Python 3.7+
- Telegram API credentials (API_ID and API_HASH)
- Telegram session string
- Target channel invite link
- Bot usernames to monitor

## Installation

1. Clone this repository or create a new directory for the project
2. Install the required dependencies:
```bash
pip install pyrogram flask python-dotenv

```

## Create a .env file with your configuration
```bash
API_ID=your_api_id_here
API_HASH=your_api_hash_here
SESSION_STRING=your_session_string_here
BOT_USERNAMES=bot1_username,bot2_username,bot3_username
TARGET_CHANNEL_INVITE=your_channel_invite_link_here
```

## Configuration
- API_ID: Your Telegram API ID (get from https://my.telegram.org)
- API_HASH: Your Telegram API hash
- SESSION_STRING: Your Telegram session string (use session_generator.py to create one)
- BOT_USERNAMES: Comma-separated list of bot usernames to monitor (without @)
- TARGET_CHANNEL_INVITE: Invite link to the target channel

### Run
```bash
python main.py
```