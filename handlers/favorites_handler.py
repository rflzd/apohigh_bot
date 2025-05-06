# handlers/favorites_handler.py
from services.highlightly_db import add_to_favorites, get_user_favorites
from services.notification_service import send_notification
from services.subscription_service import check_subscription_status  # Abunəlik yoxlama funksiyası import edilir

def add_favorite(user_id, team_or_match):
    """
    İstifadəçi seçilən komanda və ya matçı sevimlilər siyahısına əlavə edir.
    Əgər istifadəçi abunə deyilsə, ona abunəlik təklif edilir.
    
    :param user_id: İstifadəçi ID-si
    :param team_or_match: Komanda və ya matç
    """
    # Abunəlik yoxlanır
    if not check_subscription_status(user_id):
        send_notification(user_id, "🔒 Bu funksiyadan istifadə etmək üçün abunə olun!")
        return
    
    # Komanda və ya matç verilənlər bazasına əlavə olunur
    add_to_favorites(user_id, team_or_match)
    send_notification(user_id, f"✅ {team_or_match} sevimlilərinizə əlavə olundu!")

def show_favorites(user_id):
    """
    İstifadəçinin sevimli komandalarını və ya matçlarını göstərir.
    
    :param user_id: İstifadəçi ID-si
    :return: Sevimlilərin siyahısı
    """
    # Abunəlik yoxlanır
    if not check_subscription_status(user_id):
        send_notification(user_id, "🔒 Sevimlilərimi görmək üçün abunə olmalısınız!")
        return
    
    favorites = get_user_favorites(user_id)
    if favorites:
        favorites_text = "📝 Sevimlilərim:\n" + "\n".join(favorites)
    else:
        favorites_text = "📝 Hələlik heç bir sevimli əlavə etməmisiniz."
    return favorites_text
