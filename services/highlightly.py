import aiohttp
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime
import requests
from timezonefinder import TimezoneFinder
from telegram import Update
from telegram.ext import CallbackContext
from highlightly_db import init_db, SessionLocal

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')
API_BASE_URL = os.getenv('API_BASE_URL')
BASE_URL = API_BASE_URL

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

BAKU_TIMEZONE = pytz.timezone('Asia/Baku')


def get_baku_time(date_str):
    utc_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return utc_time.replace(tzinfo=pytz.utc).astimezone(BAKU_TIMEZONE)


# Yeni: xam matç məlumatlarını qaytaran funksiya
def get_matches(date=None, limit=10, timezone="Asia/Baku"):
    # Əgər tarix verilməyibsə, bu zaman günün tarixi alınır
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")  # Bugünkü tarixi alırıq (yyyy-mm-dd formatında)

    url = f"{BASE_URL}/matches"
    params = {
        'date': date,
        'limit': limit,
        'timezone': timezone
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("API Xətası:", response.status_code)
            return []
        return response.json().get("data", [])
    except Exception as e:
        print("Xəta baş verdi:", e)
        return []


# Əvvəlki funksiyanı sadəcə string cavab formatı üçün saxlayırıq
async def get_raw_matches_sync(date=None, limit=10, timezone="Asia/Baku"):
    url = f"{BASE_URL}/matches"
    params = {
        'date': date,
        'limit': limit,
        'timezone': timezone
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return "Xəta baş verdi!"
                data = await resp.json()
                games_info = "Canlı Oyunlar:\n"
                for match in data.get("data", []):
                    home_team = match.get("homeTeam", {}).get("name", "Unknown")
                    away_team = match.get("awayTeam", {}).get("name", "Unknown")
                    match_time = match.get("date", "N/A")
                    games_info += f"{home_team} vs {away_team} at {match_time}\n"
                return games_info
    except Exception as e:
        return f"Xəta baş verdi: {e}"


# Canlı və planlaşdırılan matçları ayırmaq üçün funksiya
def categorize_matches_by_status(matches):
    started = []
    not_started = []
    for m in matches:
        if isinstance(m, dict):
            if m.get("status") == "started":
                started.append(m)
            else:
                not_started.append(m)
        else:
            print(f"Invalid match data: {m}")
    return started, not_started


# Canlı matç seçildikdə matç detallarını göstərmək üçün funksiya
async def handle_match_detail(update: Update, context: CallbackContext):
    query = update.callback_query
    match_id = query.data.split("_")[1]  # Matç ID-sini alırıq

    # Matç detallarını API-dən alırıq
    match_details = get_match_details_by_id(match_id)

    if match_details:
        message = f"*Matç Detalları:*\n\n"
        message += f"🏟️ {match_details['home_team']} vs {match_details['away_team']}\n"
        message += f"🔢 Nəticə: {match_details['score']}\n"
        message += f"🕒 Başlama Vaxtı: {match_details['time']}\n"
        message += f"⚽ Qollar: {', '.join(match_details['goals'])}"

        await query.answer()  # Callback cavablandırılır
        await query.message.edit_text(message, parse_mode="Markdown")
    else:
        await query.answer("Matç məlumatları tapılmadı.")


def get_match_details_by_id(match_id):
    # API və ya fayldan matç detallarını alırıq
    # Bu funksiyanı istədiyiniz API-dən və ya yerli verilənlər bazasından məlumatları çəkə bilərsiniz.
    # Aşağıda sadə bir nümunə göstərilmişdir:
    match_data = {
        "home_team": "Real Betis",
        "away_team": "Valladolid",
        "score": "5 - 1",
        "time": "90'",
        "goals": ["Home Team Goal Scorer 1", "Away Team Goal Scorer 1"]
    }
    return match_data