import pytesseract
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator
from langdetect import detect
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
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

# Функція для перевірки наявності тексту (ігноруємо смайлики, цифри та порожні повідомлення)
def is_valid_text(text):
    # Видаляємо смайлики, цифри та пробіли
    cleaned_text = re.sub(r'[^\w\s.,!?]', '', text)
    cleaned_text = re.sub(r'\d', '', cleaned_text).strip()
    return bool(cleaned_text)

# Обробка зображень
def handle_photo(update: Update, context) -> None:
    photo = update.message.photo[-1]
    photo_file = photo.get_file()
    img_bytes = photo_file.download_as_bytearray()

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
    update.message.reply_text(f"{translated_text}")

# Обробка текстових повідомлень
def handle_text(update: Update, context) -> None:
    user_text = update.message.text

    # Ігноруємо, якщо в тексті немає корисної інформації
    if not is_valid_text(user_text):
        return

    lang = detect_language(user_text)
    if lang in ["uk", "ru"]:
        return  # Ігноруємо, якщо текст українською чи російською

    # Перекладаємо
    translated_text = translator.translate(user_text)
    update.message.reply_text(f"🌍 Переклад:\n{translated_text}")

# Команда /start
def start(update: Update, context) -> None:
    update.message.reply_text("Привіт! Надсилай мені текст іншими мовами – я перекладу на українську!")

# Запуск бота
def main():
    bot_token = os.getenv("BOT_TOKEN")  # Токен беремо з середовища змінних
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text))

    print("Бот запущено!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
