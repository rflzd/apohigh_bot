# services/payment_service.py
from config import M10_ACCOUNT, CARD2CARD_ACCOUNT

def get_payment_account(selected_plan, payment_method):
    """
    Sabit ödəniş hesabları təqdim edir, aylara görə dəyişmir.
    
    :param selected_plan: Seçilən abunəlik planı (bu parametr artıq yalnız **ödəniş metodu** üçün istifadə olunur)
    :param payment_method: Ödəniş metodu (M10 və ya Card2Card)
    :return: Hesab məlumatı
    """
    # Sabit M10 və Card2Card hesabları
    if payment_method == "M10":
        return M10_ACCOUNT
    elif payment_method == "Card2Card":
        return CARD2CARD_ACCOUNT
    else:
        return "Ödəniş hesabı tapılmadı"
