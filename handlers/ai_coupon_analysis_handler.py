# handlers/ai_coupon_analysis_handler.py
from services.ai_coupon_analysis import ai_analysis, fuzzy_coupon_analysis
from services.notification_service import send_notification

def handle_ai_coupon_analysis(update, context):
    """
    Callback query-lərini idarə edir. AI analizi və kupon analizi seçimləri.
    
    :param update: Telegram update məlumatları
    :param context: Telegram konteksti
    :return: Heç bir şey qaytarmır
    """
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'ai_analysis':
        send_notification(user_id, "🤖 AI Analiz: İstədiyiniz matçı seçərək süni intellekt analizi əldə edin.")
        # Burada AI analizi üçün məlumat göndərmək olar
        match_data = {"team1": "Arsenal", "team2": "Chelsea", "goal_probability": 60}
        ai_result = ai_analysis(user_id, match_data)
        send_notification(user_id, ai_result)
    elif query.data == 'coupon_analysis':
        send_notification(user_id, "📊 Kupon Analizi: Mərc kuponu göndərərək analizinizi əldə edin.")
        # Burada kupon analizi üçün məlumat göndərə bilərik
        coupon_data = [
            {"team1": "Arsenal", "team2": "Chelsea", "over_under": "Üst 2.5", "odds": 1.85, "risk": "Orta"}
        ]
        coupon_result = fuzzy_coupon_analysis(80, 70)  # Komanda formalarını da alırıq
        send_notification(user_id, coupon_result)
