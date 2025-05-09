import logging
from telegram import Bot
from config import BOT_TOKEN  # config.py faylından BOT_TOKEN alınır

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram Bot obyektini yaradın
bot = Bot(token=BOT_TOKEN)

# Komanda cavabları
COMMAND_RESPONSES = {
    "canli_oyunlar": "📺 Canlı oyunlar siyahısı:\nCanlı oyunların siyahısı burada göstəriləcək.",
    "bugunku_oyunlar": "📅 Bugünkü oyunlar:\nBugünkü oyunların siyahısı burada göstəriləcək.",
    "komanda_axtar": "🔍 Komanda axtar:\nKomanda axtarışı üçün uyğun cavab burada olacaq.",
    "abune_ol": "✅ Abunəliyiniz aktivləşdirildi!",
    "ayarlar": "⚙️ Ayarlar:\nBurada ayarlar menyusu göstəriləcək."
}

# Telegram Botuna bağlanmaq üçün asinxron funksiya
async def handle_command(user_id, command):
    """
    Verilən komandaya əsasən istifadəçiyə cavab göndərir.
    
    :param user_id: Komandanı göndərən istifadəçinin ID-si
    :param command: İcra ediləcək komanda (məsələn, "canli_oyunlar", "bugunku_oyunlar")
    """
    try:
        # Komanda üçün cavabı seç
        response = COMMAND_RESPONSES.get(command, "⚠️ Bu komanda mövcud deyil.")
        
        # Cavabı istifadəçiyə göndər
        logging.info(f"Komanda icra olunur: {command} - İstifadəçi ID: {user_id}")
        await bot.send_message(chat_id=user_id, text=response)
        logging.info(f"Cavab göndərildi: {response} - İstifadəçi ID: {user_id}")
    except Exception as e:
        logging.error(f"Komanda icra edilərkən xəta baş verdi: {e}")

# Bildiriş göndərən funksiya
async def send_notification(user_id, message):
    """
    İstifadəçiyə bildiriş göndərir.
    
    :param user_id: Bildirişi alacaq istifadəçinin ID-si
    :param message: Göndəriləcək mesaj
    """
    try:
        # Bildirişi göndər
        logging.info(f"Bildiriş göndərilir: {message} - İstifadəçi ID: {user_id}")
        await bot.send_message(chat_id=user_id, text=message)
        logging.info(f"Bildiriş uğurla göndərildi: {message} - İstifadəçi ID: {user_id}")
    except Exception as e:
        logging.error(f"Bildiriş göndərilərkən xəta baş verdi: {e}")