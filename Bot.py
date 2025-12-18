import telebot
from webserver import keep_alive
import os

# =========================
# Настройки бота
# =========================
TOKEN = "7083901949:AAFBtRVRGVX_4OFMHgdIoI_L9IY4UHQucDE"
ADMIN_ID = 2057965337
# =========================

bot = telebot.TeleBot(TOKEN)

# message_id администратора -> user_id
reply_map = {}

# ====== Запускаем веб-сервер ======
keep_alive()
# =================================

# Пытаемся вывести URL
repl_id = os.environ.get("REPL_SLUG")
username = os.environ.get("REPL_OWNER")
if repl_id and username:
    print(f"✅ Публичный URL: https://{repl_id}.{username}.repl.co")
else:
    print("⚠️ URL не найден автоматически (это нормально на Replit)")

# =========================
# /start
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "✉️ Напиши сообщение — админ сможет ответить анонимно"
    )

# =========================
# ТЕКСТ
# =========================
@bot.message_handler(content_types=['text'])
def handle_text(message):

    # Ответ админа
    if (
        message.from_user.id == ADMIN_ID
        and message.reply_to_message
        and message.reply_to_message.message_id in reply_map
    ):
        user_id = reply_map[message.reply_to_message.message_id]
        bot.send_message(user_id, f"📨 Ответ администратора:\n\n{message.text}")
        bot.send_message(ADMIN_ID, "✅ Ответ отправлен")
        return

    sent = bot.send_message(
        ADMIN_ID,
        f"📩 Анонимное сообщение:\n\n{message.text}"
    )
    reply_map[sent.message_id] = message.from_user.id

    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "✅ Сообщение отправлено")

# =========================
# ФОТО
# =========================
@bot.message_handler(content_types=['photo'])
def handle_photo(message):

    caption = message.caption or ""
    file_id = message.photo[-1].file_id

    sent = bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=f"📷 Анонимное фото\n\n{caption}"
    )
    reply_map[sent.message_id] = message.from_user.id

    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "✅ Фото отправлено")

# =========================
# ВИДЕО
# =========================
@bot.message_handler(content_types=['video'])
def handle_video(message):

    caption = message.caption or ""
    file_id = message.video.file_id

    sent = bot.send_video(
        ADMIN_ID,
        file_id,
        caption=f"🎥 Анонимное видео\n\n{caption}"
    )
    reply_map[sent.message_id] = message.from_user.id

    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "✅ Видео отправлено")

# =========================
# СТИКЕРЫ
# =========================
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):

    sent = bot.send_sticker(
        ADMIN_ID,
        message.sticker.file_id
    )
    reply_map[sent.message_id] = message.from_user.id

    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "✅ Стикер отправлен")

print("🤖 Бот запущен и работает")
bot.polling(non_stop=True)
