from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from services.notification_service import send_notification
from highlightly_db import get_favorite_matches  # Sevimli matçları verilənlər bazasından alırıq

scheduler = BackgroundScheduler()

def schedule_notifications():
    """
    Bildirişləri zamanında göndərmək üçün planlaşdırma funksiyası.
    """
    # Verilənlər bazasında sevimli matçları yoxlayaq
    favorite_matches = get_favorite_matches()

    for match in favorite_matches:
        match_start_time = match['start_time']
        notification_time = match_start_time - timedelta(hours=4)  # Oyun başlamazdan 4 saat əvvəl bildiriş

        if datetime.now() <= notification_time:
            scheduler.add_job(
                send_notification, 
                'date', 
                run_date=notification_time, 
                args=[match['user_id'], f"🔔 {match['team1']} vs {match['team2']} oyununa 4 saat qaldı! Başlama vaxtı: {match['start_time']}"]
            )

# Planlaşdırıcıyı işə salırıq
scheduler.start()
