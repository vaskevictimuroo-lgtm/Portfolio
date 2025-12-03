#config.py

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MODERATOR_CHAT_ID = os.getenv("MODERATOR_CHAT_ID")
