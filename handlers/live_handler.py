from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from api_requests import get_matches  # API ilə məlumatları gətirən funksiya

# /live komandasını idarə edən funksiya
async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Canlı oyunlar yüklənir, zəhmət olmasa gözləyin...")

    # API-dən canlı oyun məlumatlarını alırıq
    matches = get_matches()

    # Məlumat yoxlaması
    if not matches:
        await update.message.reply_text("❌ Hazırda heç bir canlı oyun yoxdur.")
        return

    # Oyunları formatlaşdırırıq və inline düymələr əlavə edirik
    message = "⚽ Hazırda davam edən canlı oyunlar:\n\n"
    keyboard = []
    for match in matches:
        league_name = match["league"]["name"]
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        score = match["state"]["score"]["current"]
        status = match["state"]["description"]
        match_id = match["id"]  # Hər oyun üçün unikal ID

        # Mesaj formatı
        message += f"🏆 Liqa: {league_name}\n"
        message += f"🏟️ {home_team} vs {away_team}\n"
        message += f"🔢 Nəticə: {score} | Status: {status}\n\n"

        # Hər oyun üçün düymələr
        keyboard.append([
            InlineKeyboardButton("ℹ️ Detallar", callback_data=f"details_{match_id}"),
            InlineKeyboardButton("🎥 Xülasə", callback_data=f"summary_{match_id}"),
            InlineKeyboardButton("🔢 Əmsallar", callback_data=f"odds_{match_id}")
        ])

    # Geri düyməsi
    keyboard.append([InlineKeyboardButton("🔙 Geri", callback_data="back_main_menu")])

    # Inline klaviatura yarat
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Mesajı və düymələri göndər
    await update.message.reply_text(message, reply_markup=reply_markup)