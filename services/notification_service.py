import logging
from telegram import Bot
from config import BOT_TOKEN  # config.py faylından BOT_TOKEN-i alırıq

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram Botuna bağlanmaq üçün funksiyalar
def send_notification(user_id, message):
    """
    İstifadəçiyə bildiriş göndərir.
    
    :param user_id: Bildirişi alacaq istifadəçinin ID-si
    :param message: Göndəriləcək mesaj
    """
    # Bildiriş göndərilərkən log yazırıq
    logging.info(f"Bildiriş göndərildi: {message} - İstifadəçi ID: {user_id}")
    
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=user_id, text=message)

