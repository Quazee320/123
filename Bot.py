import telebot
from webserver import keep_alive
import uuid
import json
import os

# =========================
# НАСТРОЙКИ
# =========================
TOKEN = "7083901949:AAHjnpfUiDeg8SlSJBhfNkz7NRtv8MBUJCk"
ADMIN_ID = 2057965337
DB_FILE = "messages.json"
# =========================

bot = telebot.TeleBot(TOKEN)

# =========================
# БАЗА СООБЩЕНИЙ
# =========================
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        msg_db = json.load(f)
else:
    msg_db = {}

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(msg_db, f, ensure_ascii=False, indent=2)

# =========================
# WEB SERVER
# =========================
keep_alive()

# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "✉️ Напиши сообщение — админ сможет ответить анонимно"
    )

# =========================
# /reply ID текст
# =========================
@bot.message_handler(commands=["reply"])
def manual_reply(message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(
            ADMIN_ID,
            "❌ Формат:\n/reply ID текст ответа"
        )
        return

    uid = parts[1]
    reply_text = parts[2]

    if uid not in msg_db:
        bot.send_message(
            ADMIN_ID,
            "❌ Пользователь для этого ID не найден"
        )
        return

    user_id = msg_db[uid]

    bot.send_message(
        user_id,
        f"📨 Ответ администратора:\n\n{reply_text}"
    )
    bot.send_message(ADMIN_ID, "✅ Ответ отправлен")

# =========================
# ОБЩАЯ ФУНКЦИЯ СОХРАНЕНИЯ
# =========================
def register_message(user_id):
    uid = str(uuid.uuid4())[:8]
    msg_db[uid] = user_id
    save_db()
    return uid

# =========================
# ТЕКСТ
# =========================
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.from_user.id == ADMIN_ID:
        return

    uid = register_message(message.from_user.id)

    bot.send_message(
        ADMIN_ID,
        f"📩 Анонимное сообщение:\n\n{message.text}\n\n[ID:{uid}]"
    )

    bot.send_message(message.chat.id, "✅ Сообщение отправлено")

# =========================
# ФОТО
# =========================
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    uid = register_message(message.from_user.id)
    caption = message.caption or ""

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"📷 Анонимное фото\n\n{caption}\n\n[ID:{uid}]"
    )

    bot.send_message(message.chat.id, "✅ Фото отправлено")

# =========================
# ВИДЕО
# =========================
@bot.message_handler(content_types=["video"])
def handle_video(message):
    uid = register_message(message.from_user.id)
    caption = message.caption or ""

    bot.send_video(
        ADMIN_ID,
        message.video.file_id,
        caption=f"🎥 Анонимное видео\n\n{caption}\n\n[ID:{uid}]"
    )

    bot.send_message(message.chat.id, "✅ Видео отправлено")

# =========================
# ГИФКИ
# =========================
@bot.message_handler(content_types=["animation"])
def handle_gif(message):
    uid = register_message(message.from_user.id)
    caption = message.caption or ""

    bot.send_animation(
        ADMIN_ID,
        message.animation.file_id,
        caption=f"🎞 Анонимная гифка\n\n{caption}\n\n[ID:{uid}]"
    )

    bot.send_message(message.chat.id, "✅ Гифка отправлена")

# =========================
# СТИКЕРЫ
# =========================
@bot.message_handler(content_types=["sticker"])
def handle_sticker(message):
    uid = register_message(message.from_user.id)

    bot.send_sticker(ADMIN_ID, message.sticker.file_id)
    bot.send_message(ADMIN_ID, f"[ID:{uid}]")

    bot.send_message(message.chat.id, "✅ Стикер отправлен")

# =========================
# АУДИО
# =========================
@bot.message_handler(content_types=["audio"])
def handle_audio(message):
    uid = register_message(message.from_user.id)
    caption = message.caption or ""

    bot.send_audio(
        ADMIN_ID,
        message.audio.file_id,
        caption=f"🎵 Анонимное аудио\n\n{caption}\n\n[ID:{uid}]"
    )

    bot.send_message(message.chat.id, "✅ Аудио отправлено")

# =========================
# ГОЛОСОВЫЕ
# =========================
@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    uid = register_message(message.from_user.id)

    bot.send_voice(
        ADMIN_ID,
        message.voice.file_id,
        caption=f"🎤 Анонимное голосовое\n\n[ID:{uid}]"
    )

    bot.send_message(message.chat.id, "✅ Голосовое отправлено")

print("🤖 Бот запущен и работает")
bot.polling(non_stop=True)

    bot.send_message(message.chat.id, "✅ Голосовое отправлено")

print("🤖 Бот запущен и работает")
bot.polling(non_stop=True)
