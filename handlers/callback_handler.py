from telegram import Update
from telegram.ext import ContextTypes

# Callback düymələrini idarə edən funksiya
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("details_"):
        match_id = data.split("_")[1]
        await query.answer("ℹ️ Matç Detalları göstərilir...")
        # Detallar funksiyasını çağırın
        await query.message.reply_text(f"📝 Matç ID: {match_id} üzrə detalları göstəririk... (Funksiya əlavə ediləcək)")

    elif data.startswith("summary_"):
        match_id = data.split("_")[1]
        await query.answer("🎥 Video xülasə göstərilir...")
        # Xülasə funksiyasını çağırın
        await query.message.reply_text(f"🎥 Matç ID: {match_id} üzrə video xülasə... (Funksiya əlavə ediləcək)")

    elif data.startswith("odds_"):
        match_id = data.split("_")[1]
        await query.answer("🔢 Əmsallar göstərilir...")
        # Əmsallar funksiyasını çağırın
        await query.message.reply_text(f"🔢 Matç ID: {match_id} üzrə əmsallar... (Funksiya əlavə ediləcək)")

    elif data == "back_main_menu":
        # Əsas menyuya qayıt
        await query.message.edit_text(
            "⚽️ Futbol Botuna xoş gəlmisiniz! Aşağıdakılardan birini seçin:\n\n"
            "📺 Canlı Oyunlar\n"
            "📅 Bugünkü Oyunlar\n"
            "🏆 Liqalar\n"
            "🔍 Komanda Axtar\n"
            "⚙️ Ayarlar"
        )