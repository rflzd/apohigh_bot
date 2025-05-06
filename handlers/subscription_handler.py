# handlers/subscription_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from services.notification_service import send_notification
from services.payment_service import get_payment_account

def handle_payment_method(update, context):
    """
    İstifadəçi ödəniş metodunu seçdikdən sonra, ödəniş hesabatı verilir.
    
    :param update: Telegram update məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    query = update.callback_query
    user_id = query.from_user.id
    payment_method = query.data.split('_')[0]  # M10 və ya Card2Card
    selected_plan = query.data.split('_')[1]  # Abunəlik planı

    if payment_method == "M10":
        payment_message = f"Ödəniş üçün M10 hesabı: {get_payment_account(selected_plan, 'M10')}"
    elif payment_method == "Card2Card":
        payment_message = f"Ödəniş üçün Card2Card hesabı: {get_payment_account(selected_plan, 'Card2Card')}"
    
    # Kopyalama funksiyası əlavə edirik
    buttons = [
        [InlineKeyboardButton("Kopyala", callback_data=f"copy_{payment_method}_{selected_plan}")],
        [InlineKeyboardButton("🔙 Geri", callback_data="back_to_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    send_notification(user_id, payment_message)
    send_notification(ADMIN_USER_ID, f"Yeni ödəniş tələb olunur: {payment_message}")
    send_notification(user_id, "Ödənişi tamamladıqdan sonra çeki göndərin.")
    update.callback_query.message.edit_text(payment_message, reply_markup=reply_markup)

def handle_copy_payment_info(update, context):
    """
    İstifadəçi ödəniş hesabı məlumatını kopyaladıqda, onlara məlumat verir.
    
    :param update: Telegram update məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    query = update.callback_query
    user_id = query.from_user.id
    payment_method = query.data.split('_')[1]  # M10 və ya Card2Card
    selected_plan = query.data.split('_')[2]  # Abunəlik planı
    
    # Kopyalanan hesab məlumatı
    payment_account = get_payment_account(selected_plan, payment_method)
    
    # Kopyalanan məlumatı istifadəçiyə bildiririk
    send_notification(user_id, f"Ödəniş hesabı kopyalandı: {payment_account}")
