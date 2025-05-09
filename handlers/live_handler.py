from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.highlightly import get_live_matches  # Canlı oyunları gətirən funksiyanı idxal edirik

# /live komandasını idarə edən funksiya
async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Canlı oyunları idarə edən funksiya.
    """
    await update.message.reply_text("⚽ Canlı oyunlar yüklənir, zəhmət olmasa gözləyin...")

    # Canlı oyunları məlumat bazasından və ya API-dən alırıq
    matches = get_live_matches()

    # Məlumat yoxlaması
    if not matches:
        await update.message.reply_text("❌ Hazırda heç bir canlı oyun yoxdur.")
        return

    # Oyunları formatlaşdırırıq və inline düymələr əlavə edirik
    message = "⚽ Hazırda davam edən canlı oyunlar:\n\n"
    keyboard = []

    for match in matches:
        league_name = match.get("league_name", "Naməlum Liqa")
        home_team = match.get("home_team", "Naməlum Komanda")
        away_team = match.get("away_team", "Naməlum Komanda")
        score = match.get("score", "Naməlum")
        status = match.get("status", "Bilinmir")
        match_id = match.get("id", "0")  # Hər oyun üçün unikal ID

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