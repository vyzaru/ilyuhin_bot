from pathlib import Path
from os import getenv
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = getenv("TELEGRAM_BOT_KEY", "")