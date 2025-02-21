import pytesseract
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator
from langdetect import detect
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import os
import re

# Вказуємо шлях до Tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Налаштування перекладача
translator = GoogleTranslator(source='auto', target='uk')

# Функція для визначення мови
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return None

# Функція для перевірки наявності тексту (ігноруємо смайлики, цифри та порожні повідомлення)
def is_valid_text(text):
    cleaned_text = re.sub(r'[^\w\s.,!?]', '', text)
    cleaned_text = re.sub(r'\d', '', cleaned_text).strip()
    return bool(cleaned_text)

# Обробка зображень
async def handle_photo(update: Update, context) -> None:
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    img_bytes = await photo_file.download_as_bytearray()

    # Розпізнаємо текст
    img = Image.open(BytesIO(img_bytes))
    img = img.convert('L')  # Перетворення на чорно-біле
    img = img.point(lambda x: 0 if x < 140 else 255)  # Збільшення контрасту
    extracted_text = pytesseract.image_to_string(img, lang='eng+ukr+rus')

    # Логи для відладки
    print(f"Розпізнаний текст: {extracted_text}")

    if not extracted_text.strip() or not is_valid_text(extracted_text):
        await update.message.reply_text("Не вдалося розпізнати текст 😔")
        return

    lang = detect_language(extracted_text)
    if lang in ["uk", "ru"]:
        return  # Ігноруємо, якщо текст українською чи російською

    translated_text = translator.translate(extracted_text)
    await update.message.reply_text(f"🌍 Переклад:\n{translated_text}")

# Обробка текстових повідомлень
async def handle_text(update: Update, context) -> None:
    user_text = update.message.text

    if not is_valid_text(user_text):
        return

    lang = detect_language(user_text)
    if lang in ["uk", "ru"]:
        return

    translated_text = translator.translate(user_text)
    await update.message.reply_text(f"🌍 Переклад:\n{translated_text}")

# Команда /start
async def start(update: Update, context) -> None:
    await update.message.reply_text("Привіт! Надсилай мені текст іншими мовами – я перекладу на українську!")

# Запуск бота
def main():
    bot_token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    print("Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()
