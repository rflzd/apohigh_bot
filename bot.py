# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from services.notification_service import send_notification
from services.subscription_service import check_subscription_status
from handlers.ai_coupon_analysis_handler import handle_ai_coupon_analysis  # Handler faylından import

# /start komandasını idarə edən funksiya
def start(update: Update, context: CallbackContext):
    """
    İstifadəçi /start komandasını göndərdikdə baş verən hadisə.
    
    :param update: Telegram mesaj məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    user_id = update.message.from_user.id
    
    # Abunəlik statusunu yoxlayırıq
    if check_subscription_status(user_id):
        menu_text = "⚽️ Canlı Oyunlar\n📅 Bugünkü Oyunlar\n🔍 Komanda Axtar\n📝 Sevimlilərim\n🤖 AI Analiz\n📊 Kupon Analizi\n⚙️ Ayarlar"
        buttons = [
            [InlineKeyboardButton("📺 Canlı Oyunlar", callback_data='live_games')],
            [InlineKeyboardButton("📅 Bugünkü Oyunlar", callback_data='today_games')],
            [InlineKeyboardButton("🔍 Komanda Axtar", callback_data='search_team')],
            [InlineKeyboardButton("📝 Sevimlilərim", callback_data='favorites')],
            [InlineKeyboardButton("🤖 AI Analiz", callback_data='ai_analysis')],
            [InlineKeyboardButton("📊 Kupon Analizi", callback_data='coupon_analysis')],
            [InlineKeyboardButton("⚙️ Ayarlar", callback_data='settings')]
        ]
    else:
        menu_text = "⚽️ Canlı Oyunlar\n📅 Bugünkü Oyunlar\n🔍 Komanda Axtar\n🔒 Abunəlik olmadan bu xidmətləri görə bilməzsiniz!"
        buttons = [
            [InlineKeyboardButton("📺 Canlı Oyunlar", callback_data='live_games')],
            [InlineKeyboardButton("📅 Bugünkü Oyunlar", callback_data='today_games')],
            [InlineKeyboardButton("🔍 Komanda Axtar", callback_data='search_team')],
            [InlineKeyboardButton("🔒 Abunə ol", callback_data='subscribe')],
            [InlineKeyboardButton("⚙️ Ayarlar", callback_data='settings')]
        ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(menu_text, reply_markup=reply_markup)

# Callback query-lərini idarə edən funksiya
def handle_callback(update: Update, context: CallbackContext):
    """
    İstifadəçidən gələn callback məlumatlarını idarə edir.
    
    :param update: Telegram mesaj məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'live_games':
        send_notification(user_id, "📺 Canlı oyunlar siyahısı:")
        live_games = "Canlı oyunların siyahısı burada göstəriləcək."
        send_notification(user_id, live_games)
    elif query.data == 'today_games':
        send_notification(user_id, "📅 Bugünkü oyunlar:")
        today_games = "Bugünkü oyunların siyahısı burada göstəriləcək."
        send_notification(user_id, today_games)
    elif query.data == 'search_team':
        send_notification(user_id, "🔍 Komanda Axtar: Komanda adını yazın.")
    elif query.data == 'favorites':
        send_notification(user_id, "📝 Sevimlilərim:")
    elif query.data == 'ai_analysis':
        # AI analizi üçün handler-i çağırırıq
        handle_ai_coupon_analysis(update, context)
    elif query.data == 'coupon_analysis':
        # Kupon analizi üçün handler-i çağırırıq
        handle_ai_coupon_analysis(update, context)
    elif query.data == 'subscribe':
        send_notification(user_id, "✅ Abunəliyiniz aktivləşdirildi!")
    elif query.data == 'settings':
        send_notification(user_id, "⚙️ Ayarlar: Burada parametrlərinizi dəyişə bilərsiniz.")

# Botu başladan funksiya
def main():
    """
    Telegram botunu başladan əsas funksiya.
    """
    updater = Updater(token="YOUR_BOT_API_KEY", use_context=True)
    dispatcher = updater.dispatcher

    # Əsas handlerləri əlavə edirik
    dispatcher.add_handler(CommandHandler('start', start))  # /start komandasını idarə edir
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))  # Callback query-ləri idarə edir

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
