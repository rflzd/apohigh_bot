from dotenv import load_dotenv
import os

# .env faylını yükləmək
load_dotenv()

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Highlightly API
API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
BASE_URL = os.getenv("BASE_URL")
API_HOST = os.getenv("API_HOST")

# MySQL database bağlantısı
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Subscription price
SUBSCRIPTION_PRICE = os.getenv("SUBSCRIPTION_PRICE")

# Admin IDs
ADMIN_IDS = os.getenv("ADMIN_IDS")

# Payment details
M10_ACCOUNT = os.getenv("M10_ACCOUNT")
CARD2CARD_ACCOUNT = os.getenv("CARD2CARD_ACCOUNT")

# MySQL database URL (for SQLAlchemy)
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
