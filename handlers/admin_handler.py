from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from services.admin_checker import is_user_admin
from services.highlightly_db import session, Admin
from services.notification_service import send_notification

def admin_panel(update, context):
    """
    Admin panelini göstərir. Admin istifadəçi ID-si yoxlanır.
    
    :param update: Telegram mesaj məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    user_id = update.message.from_user.id

    if not is_user_admin(user_id):
        send_notification(user_id, "🔒 Bu funksiyanı yalnız adminlər istifadə edə bilər.")
        return

    # Admin funksiyaları təqdim edilir
    panel_message = (
        "🛠 Admin Paneli:\n\n"
        "1️⃣ Yeni admin əlavə et\n"
        "2️⃣ İstifadəçiyə abunəlik ver\n"
        "3️⃣ Admin statusunu dəyişdir\n"
        "4️⃣ Ödəniş hesabını əlavə et\n"
        "Seçim edin!"
    )

    buttons = [
        [InlineKeyboardButton("Yeni admin əlavə et", callback_data="add_admin")],
        [InlineKeyboardButton("İstifadəçiyə abunəlik ver", callback_data="give_subscription")],
        [InlineKeyboardButton("Admin statusunu dəyişdir", callback_data="change_admin_status")],
        [InlineKeyboardButton("Ödəniş hesabını əlavə et", callback_data="add_payment_account")],
        [InlineKeyboardButton("🔙 Geri", callback_data="back_to_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(panel_message, reply_markup=reply_markup)

def handle_admin_action(update, context):
    """
    Admin tərəfindən seçilən funksiyaları idarə edir.
    
    :param update: Telegram update məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    query = update.callback_query
    user_id = query.from_user.id

    if not is_user_admin(user_id):
        send_notification(user_id, "🔒 Bu funksiyanı yalnız adminlər istifadə edə bilər.")
        return

    action = query.data

    if action == "add_admin":
        # Yeni admin əlavə et funksiyasını işə sal
        send_notification(user_id, "💡 Yeni adminin Telegram ID-sini göndərin:")
    elif action == "give_subscription":
        # İstifadəçiyə abunəlik vermək funksiyası
        send_notification(user_id, "📅 İstifadəçiyə abunəlik vermək üçün istifadəçi ID-si təqdim edin.")
    elif action == "change_admin_status":
        # Admin statusunu dəyişmək funksiyası
        send_notification(user_id, "🔐 Admin statusunu dəyişmək üçün istifadəçi ID-si təqdim edin.")
    elif action == "add_payment_account":
        # Ödəniş hesabı əlavə etmək funksiyası
        send_notification(user_id, "💳 Ödəniş hesabını əlavə etmək üçün məlumatları təqdim edin.")
    else:
        send_notification(user_id, "🔒 Tanınmayan əməliyyat!")


def add_admin(user_id, db):
    """
    Yeni admin əlavə etmək üçün istifadə olunur.
    :param user_id: Adminin Telegram istifadəçi ID-si
    :param db: Verilənlər bazası
    """
    db_admin = Admin(user_id=user_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def change_admin_status(user_id, status, db):
    """
    Adminin statusunu dəyişmək üçün istifadə olunur.
    :param user_id: Adminin Telegram istifadəçi ID-si
    :param status: Yeni status (True - aktiv, False - deaktiv)
    :param db: Verilənlər bazası
    """
    db_admin = db.query(Admin).filter(Admin.user_id == user_id).first()
    if db_admin:
        db_admin.admin_status = status
        db.commit()
        db.refresh(db_admin)
        return db_admin
    return None

def give_subscription(user_id, db):
    """
    İstifadəçiyə abunəlik vermək üçün istifadə olunur.
    :param user_id: İstifadəçi ID-si
    :param db: Verilənlər bazası
    """
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db_user.is_subscribed = True
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def cancel_subscription(user_id, db):
    """
    İstifadəçinin abunəliyini ləğv etmək üçün istifadə olunur.
    :param user_id: İstifadəçi ID-si
    :param db: Verilənlər bazası
    """
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db_user.is_subscribed = False
        db.commit()
        db.refresh(db_user)
        return db_user
    return None
