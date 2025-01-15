#7361029236:AAGs7qp56N0J5lr9Irk60VvO3c5dxXYRGGc

import logging
from PIL import Image, ImageEnhance
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, ConversationHandler
from googletrans import Translator
import torch
import torch.backends
import easyocr
import numpy as np
import cv2 as cv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
available_languages = {
    'English': 'en',
    'French': 'fr',
    'Spanish': 'es',
    'German': 'de',
    'Russian': 'ru',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Arabic': 'ar',
    'Japanese': 'jp'
}
LANGUAGE, = range(1)
user_languages = {}

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    photo_bytes = await file.download_as_bytearray()
    #image = Image.open(BytesIO(photo_bytes))

    nparr = np.frombuffer(photo_bytes, np.uint8)
    image = cv.imdecode(nparr, cv.IMREAD_COLOR)

    processed_image = image
    reader = easyocr.Reader(['ru','en'])
    easyocr_data = reader.readtext(processed_image)
    easyocr_text = []

    for (_, text, _) in easyocr_data:
        easyocr_text.append(text)

    final_text = ' '.join(easyocr_text)
    
    for_translation_text = ''.join(easyocr_text)
    translator = Translator()
    if update.message.from_user.id in user_languages:
        user_language = user_languages[update.message.from_user.id]
    else:
        await update.message.reply_text("Вы не установили язык перевода. Язык по умолчанию: английский.")
        user_language = 'en'  # Или любой другой язык по умолчанию

    translated_text = await translator.translate(for_translation_text,dest= user_language)

    await update.message.reply_text(
    f" Распознанный текст: \n {final_text}\n\n Перевод:\n {translated_text.text if translated_text else 'Я ничего не смог распознать на этой картинке.'}"
)
    
async def list_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language_list = '\n'.join([f"{lang}: {code}" for lang, code in available_languages.items()])
    await update.message.reply_text(f"Доступные языки:\n{language_list}")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Команда не распознана.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот, который умеет распознавать русский и английский текст с фотографий и затем переводить в выбранный язык. Используйте команду /translateto чтобы изменить язык перевода. По умолчанию перевод производится на английский. Команда /languages показывает все доступные для перевода языки.")

async def set_translation_language(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Пожалуйста, выберите язык для перевода.\nДля отмены используйте команду /cancel.\nЧтобы увидеть доступные языки используйте команду /languages")
    return LANGUAGE

async def receive_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = update.message.text.strip().lower()
    if language in available_languages.values():
        user_languages[update.message.from_user.id] = language
        await update.message.reply_text(f"Язык перевода установлен на: {language}")
        return ConversationHandler.END 
    else:
        await update.message.reply_text("Неверный язык. Пожалуйста, введите один из доступных языков: en, ru, sp.")
        return LANGUAGE  # Повторяем этот этап для получения корректного ответа

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Отмена команды.")
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token('7361029236:AAGs7qp56N0J5lr9Irk60VvO3c5dxXYRGGc').build()
    
    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    image_handler = MessageHandler(filters.PHOTO, handle_photo)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("translateto", set_translation_language)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_language)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    languages_handler = CommandHandler('languages', list_languages)
    application.add_handler(start_handler)
    application.add_handler(image_handler)
    application.add_handler(conv_handler)
    application.add_handler(languages_handler)

    application.add_handler(unknown_handler)
    application.run_polling()