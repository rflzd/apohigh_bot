import logging
from telegram import Bot
from config import BOT_TOKEN  # config.py faylından BOT_TOKEN alınır

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram Bot obyektini yaradın
bot = Bot(token=BOT_TOKEN)

# Telegram Botuna bağlanmaq üçün asinxron funksiya
async def send_notification(user_id, message):
    """
    İstifadəçiyə bildiriş göndərir.
    
    :param user_id: Bildirişi alacaq istifadəçinin ID-si
    :param message: Göndəriləcək mesaj
    """
    try:
        # Bildiriş göndərilərkən log yazırıq
        logging.info(f"Bildiriş göndərilir: {message} - İstifadəçi ID: {user_id}")
        
        # Mesajı göndər
        await bot.send_message(chat_id=user_id, text=message)
        
        # Uğurlu bildiriş göndərildikdən sonra log yazırıq
        logging.info(f"Bildiriş uğurla göndərildi: {message} - İstifadəçi ID: {user_id}")
    except Exception as e:
        # Xətalar üçün log yazırıq
        logging.error(f"Bildiriş göndərilərkən xəta baş verdi: {e}")