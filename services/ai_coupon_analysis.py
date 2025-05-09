import numpy as np
import skfuzzy as fuzz
from random import randint
from services.notification_service import send_notification
from services.highlightly import get_matches, get_odds, get_match_statistics  # Düzəliş: get_odds əlavə edildi
from highlightly_db import get_subscription_status  # Abunəlik statusunu yoxlamaq

# Fuzzy logic ilə kupon analizi
def fuzzy_coupon_analysis(team1_form, team2_form):
    """
    Komanda formalarına əsaslanan qeyri-səlis analiz.
    
    :param team1_form: Komanda 1-in forması (0-100)
    :param team2_form: Komanda 2-in forması (0-100)
    :return: Hər komandanın qalib gəlmə ehtimalı
    """
    x = np.arange(0, 101, 1)  # Formanın gücü 0-100 arasında
    team1_fuzzy = fuzz.trimf(x, [0, 50, 100])  # Komanda 1-in qeyri-səlis funksiyası
    team2_fuzzy = fuzz.trimf(x, [0, 50, 100])  # Komanda 2-in qeyri-səlis funksiyası
    
    # Komanda 1-in qalib gəlmə ehtimalı
    team1_prob = fuzz.interp_membership(x, team1_fuzzy, team1_form)
    team2_prob = fuzz.interp_membership(x, team2_fuzzy, team2_form)
    
    # Qalib gəlmə ehtimalları
    team1_win_prob = team1_prob / (team1_prob + team2_prob) * 100
    team2_win_prob = team2_prob / (team1_prob + team2_prob) * 100
    
    return team1_win_prob, team2_win_prob


# AI analizi funksiyası
async def ai_analysis(user_id, match_id):
    """
    AI analizi, komandaların gücünü və oyundakı üstünlük ehtimallarını qiymətləndirir.
    
    :param user_id: İstifadəçinin ID-si
    :param match_id: Matçın ID-si
    :return: Təhlil nəticəsi
    """
    if not check_subscription(user_id):
        send_notification(user_id, "🔒 Bu funksiya yalnız premium abunəçilər üçün mövcuddur.")
        return

    # API-dən matç məlumatlarını alırıq
    match_data = get_matches()  # Bu günün matçlarını çəkirik
    odds_data = await get_odds(match_id)  # Düzəliş: Əmsalları almaq üçün get_odds funksiyası istifadə edilir

    # Komanda 1 və Komanda 2-nin hücum gücü
    team1_attack = match_data['homeTeam']['attack']
    team2_attack = match_data['awayTeam']['attack']
    
    # AI proqnozu: Hər komanda üçün real-time hücum gücü
    team1_score_prob = randint(1, 100) * team1_attack
    team2_score_prob = randint(1, 100) * team2_attack
    
    if team1_score_prob > team2_score_prob:
        result = f"AI proqnozu: {match_data['homeTeam']['name']} qalib gələcək"
    elif team1_score_prob < team2_score_prob:
        result = f"AI proqnozu: {match_data['awayTeam']['name']} qalib gələcək"
    else:
        result = "AI proqnozu: Bərabərlik"
    
    send_notification(user_id, result)


# Əmsalları manipulyasiya etmək üçün funksiya
def manipulate_odds(odds_data, team1_form, team2_form):
    """
    Əmsalları qeyri-səlis məntiqə əsaslanaraq manipulyasiya edir.
    
    :param odds_data: Əmsalların orijinal məlumatları
    :param team1_form: Komanda 1-in forması
    :param team2_form: Komanda 2-in forması
    :return: Manipulyasiya edilmiş əmsallar
    """
    # Fuzzy logic tətbiq edirik
    manipulated_odds = {
        'team1_win': odds_data['team1_win'] * 1.05,  # 5% artım
        'draw': odds_data['draw'] * 1.02,            # 2% artım
        'team2_win': odds_data['team2_win'] * 0.95   # 5% azalma
    }
    
    # Komandanın forması əsasında əmsalları dəyişirik
    if team1_form > team2_form:
        manipulated_odds['team1_win'] *= 1.10  # Komanda 1-in üstünlüyü 10% artırır
    elif team2_form > team1_form:
        manipulated_odds['team2_win'] *= 1.10  # Komanda 2-in üstünlüyü 10% artırır
    
    return manipulated_odds


# Real-time əmsalları almaq və manipulyasiya etmək
async def get_odds_for_match(match_id):
    """
    Match üçün real-time əmsalları alır.
    
    :param match_id: Matç ID
    :return: Əmsallar (qələbə, heç-heçə və s.)
    """
    odds_data = await get_odds(match_id)  # Düzəliş: Əmsalları almaq üçün get_odds funksiyası istifadə edilir
    return odds_data


# Qeyri-səlis məntiq ilə əmsalların manipulyasiyası
def fuzzy_manipulate_odds(odds_data, team1_form, team2_form):
    """
    Əmsalları fuzzy məntiqi ilə manipulyasiya edir.
    
    :param odds_data: Əmsalların orijinal məlumatları
    :param team1_form: Komanda 1-in forması
    :param team2_form: Komanda 2-in forması
    :return: Manipulyasiya edilmiş əmsallar
    """
    manipulated_odds = manipulate_odds(odds_data, team1_form, team2_form)
    return manipulated_odds


# Abunəlik statusu yoxlamaq (bu funksiya daha əvvəlki məsələlərdə təqdim edilib)
def check_subscription(user_id):
    """
    İstifadəçinin abunəlik statusunu yoxlayır.
    
    :param user_id: İstifadəçinin ID-si
    :return: True - əgər abunədirsə, False - əgər abunə deyil
    """
    return get_subscription_status(user_id)  # Verilənlər bazasında abunəlik statusunu alırıq