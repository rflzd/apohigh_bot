from datetime import datetime, timedelta
from services.notification_service import send_notification

def notify_live_game(user_id, match):
    match_start_time = match['start_time']
    current_time = datetime.now()
    time_left = match_start_time - current_time

    if time_left <= timedelta(hours=4):
        message = f"🔔 {match['team1']} vs {match['team2']} oyununa 4 saat qaldı! Başlama vaxtı: {match['start_time']}"
        send_notification(user_id, message)

def notify_goal(user_id, match, scorer):
    message = f"⚽️ {match['team1']} vs {match['team2']} - Qol vuruldu! Qol vuran: {scorer}"
    send_notification(user_id, message)

def notify_card(user_id, match, card_type, player):
    card_emoji = "🟨" if card_type == 'yellow' else "🟥"
    message = f"{card_emoji} {player} {card_type} kart aldı! Oyun: {match['team1']} vs {match['team2']}"
    send_notification(user_id, message)

def notify_match_end(user_id, match):
    message = f"🔚 {match['team1']} vs {match['team2']} oyunu bitdi! Son skor: {match['score']}"
    send_notification(user_id, message)

def notify_lineup(user_id, match, lineup):
    message = f"📝 {match['team1']} vs {match['team2']} - Start heyətləri:\n"
    for player in lineup:
        message += f"{player}\n"
    send_notification(user_id, message)