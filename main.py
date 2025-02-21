import pytesseract
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator
from langdetect import detect
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
import os
import re

# Налаштування перекладача
translator = GoogleTranslator(source='auto', target='uk')

# Функція для визначення мови
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return None

# Функція для перевірки наявності тексту (ігноруємо смайлики та порожні повідомлення)
def is_valid_text(text):
    # Видаляємо смайлики та пробіли
    cleaned_text = re.sub(r'[^\w\s.,!?]', '', text).strip()
    return bool(cleaned_text)

# Обробка зображень
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    img_bytes = await photo_file.download_as_bytearray()

    # Розпізнаємо текст
    img = Image.open(BytesIO(img_bytes))
    extracted_text = pytesseract.image_to_string(img, lang='eng+ukr+rus')  # Англ, укр, рос

    # Якщо тексту немає, або він не містить корисної інформації — ігноруємо
    if not extracted_text.strip() or not is_valid_text(extracted_text):
        return

    lang = detect_language(extracted_text)
    if lang in ["uk", "ru"]:
        return  # Ігноруємо, якщо текст українською чи російською

    # Перекладаємо текст і відправляємо тільки переклад
    translated_text = translator.translate(extracted_text)
    await update.message.reply_text(f"{translated_text}")

# Обробка текстових повідомлень
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text

    # Ігноруємо, якщо в тексті немає корисної інформації
    if not is_valid_text(user_text):
        return

    lang = detect_language(user_text)
    if lang in ["uk", "ru"]:
        return  # Ігноруємо, якщо текст українською чи російською

    # Перекладаємо
    translated_text = translator.translate(user_text)
    await update.message.reply_text(f"🌍 Переклад:\n{translated_text}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привіт! Надсилай мені текст іншими мовами – я перекладу на українську!")

# Запуск бота
def main():
    bot_token = os.getenv("BOT_TOKEN")  # Токен беремо з середовища змінних
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    print("Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()
