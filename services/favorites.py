from highlightly_db import add_favorite_to_db, get_favorite_teams  # Verilənlər bazasına əlaqə

def add_favorite(user_id, team_name):
    """
    İstifadəçinin sevimli komandasını əlavə edir.
    
    :param user_id: İstifadəçinin ID-si
    :param team_name: Komanda adı
    """
    add_favorite_to_db(user_id, team_name)  # Komandayı verilənlər bazasına əlavə edirik

def get_favorite_teams(user_id):
    """
    İstifadəçinin sevimli komandalarını gətirir.
    
    :param user_id: İstifadəçinin ID-si
    :return: Sevimli komandalar
    """
    return get_favorite_teams(user_id)  # Verilənlər bazasından sevimli komandaları alırıq

def notify_favorite(user_id, match, event):
    """
    İstifadəçinin sevimli komandası ilə bağlı hadisə baş verdikdə bildiriş göndərir.
    
    :param user_id: İstifadəçinin ID-si
    :param match: Matç məlumatları
    :param event: Hadisə (qol, kart, və s.)
    """
    favorite_teams = get_favorite_teams(user_id)
    
    if match['team1'] in favorite_teams or match['team2'] in favorite_teams:
        if event == "goal":
            notify_goal(user_id, match, event['scorer'])
        elif event == "card":
            notify_card(user_id, match, event['card_type'], event['player'])
