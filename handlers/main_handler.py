from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from services.notification_service import send_notification
from services.subscription_service import check_subscription_status, activate_user_subscription
from services.highlightly import get_matches, get_odds_data

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
        menu_text = "⚽️ Canlı Oyunlar\n📅 Bugünkü Oyunlar\n🔍 Komanda Axtar\n📝 Abunəlik Aktivdir\n⚙️ Ayarlar"
    else:
        menu_text = "⚽️ Canlı Oyunlar\n📅 Bugünkü Oyunlar\n🔍 Komanda Axtar\n🔒 Abunəlik olmadan bu xidmətləri görə bilməzsiniz!\n⚙️ Ayarlar"
    
    # İstifadəçiyə əsas menyu göndəririk
    send_notification(user_id, menu_text)

# /subscribe komandasını idarə edən funksiya
def subscribe(update: Update, context: CallbackContext):
    """
    İstifadəçiyə abunəlik seçimindən faydalanmağa imkan verən funksiya.
    
    :param update: Telegram mesaj məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    user_id = update.message.from_user.id
    
    # Abunəlik sistemini aktivləşdiririk
    activate_user_subscription(user_id)
    
    # İstifadəçiyə abunəlik məlumatı göndəririk
    send_notification(user_id, "✅ Abunəliyiniz aktivləşdirildi! İndi AI analizi və daha çox xidmətlərdən istifadə edə bilərsiniz.")

# Məsləhət üçün callback handler
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
        # Burada live oyunlar məlumatlarını göstərmək üçün əlavə funksiya yazmaq olar
    elif query.data == 'today_games':
        send_notification(user_id, "📅 Bugünkü oyunlar:")
        # Bugünkü oyunlar üçün əlavə məlumat verə bilərik
    elif query.data == 'search_team':
        send_notification(user_id, "🔍 Komanda Axtar: Komanda adını yazın.")
    elif query.data == 'subscribe':
        subscribe(update, context)  # Abunəlik funksiyasını çağırırıq
    elif query.data == 'settings':
        send_notification(user_id, "⚙️ Ayarlar: Burada parametrlərinizi dəyişə bilərsiniz.")

# Telegram Handlers
def main_handlers(dispatcher):
    """
    Telegram botu üçün əsas handlerlər.
    
    :param dispatcher: Telegram botunun dispatcher obyektini alırıq
    """
    dispatcher.add_handler(CommandHandler('start', start))  # /start komandasını idarə edir
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))  # Callback query-ləri idarə edir
