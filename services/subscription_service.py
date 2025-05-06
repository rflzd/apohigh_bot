from highlightly_db import get_subscription_status, update_subscription_status, activate_subscription  # Verilənlər bazasından abunəlik statusunu alırıq
from services.notification_service import send_notification
from datetime import datetime, timedelta


# Abunəlik statusunu yoxlamaq
def check_subscription_status(user_id):
    """
    İstifadəçinin abunəlik statusunu yoxlayır.
    
    :param user_id: İstifadəçi ID-si
    :return: True - əgər abunədirsə, False - əgər abunə deyil
    """
    is_subscribed = get_subscription_status(user_id)
    
    if is_subscribed:
        return True
    else:
        return False

def confirm_payment(user_id, payment_receipt):
    """
    Ödəniş təsdiqləndikdən sonra istifadəçinin abunəliyini aktivləşdirir.
    
    :param user_id: İstifadəçinin ID-si
    :param payment_receipt: Ödənişə dair təsdiq məlumatı
    """
    # Admin təsdiqindən sonra verilənlər bazasında abunəlik statusu yenilənir
    update_subscription_status(user_id, True, payment_receipt)  # True - abunəlik aktivdir
    send_subscription_notification(user_id)  # İstifadəçiyə abunəliyin aktivləşdiyi barədə bildiriş göndəririk

# Abunəlik aktivləşdirmək
def activate_user_subscription(user_id):
    """
    İstifadəçinin abunəliyini aktivləşdirir.
    
    :param user_id: İstifadəçi ID-si
    :return: Heç bir şey qaytarmır
    """
    activate_subscription(user_id)  # Verilənlər bazasında abunəlik aktivləşdiririk
    send_notification(user_id, "✅ Abunəliyiniz aktivləşdirildi!")

def notify_subscription_expiration(user_id, expiration_date):
    """
    İstifadəçiyə abunəlik müddətinin bitməsinə yaxınlaşdığını bildirir.
    
    :param user_id: İstifadəçinin ID-si
    :param expiration_date: Abunəlik bitmə tarixi
    """
    current_time = datetime.now()
    if expiration_date - current_time <= timedelta(days=1):  # 1 gün qalmış xəbərdarlıq
        message = f"⚠️ Sizin abunəliyinizin bitməsinə 1 gün qalıb! Xahiş edirik yeniləyin."
        send_notification(user_id, message)
