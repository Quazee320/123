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
reply_map = {}

# ====== Запускаем веб-сервер ======
keep_alive()
# =================================

# Получаем публичный URL Replit и выводим в консоль
repl_id = os.environ.get("REPL_SLUG")  # имя проекта
username = os.environ.get("REPL_OWNER")  # никнейм
if repl_id and username:
    url = f"https://{repl_id}.{username}.repl.co"
    print(f"✅ Публичный URL для UptimeRobot: {url}")
else:
    print("⚠️ Не удалось определить URL автоматически. Используй Open in a new tab")

# ==
# Словарь: message_id администратора -> id пользователя
reply_map = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "✉️ Привет! Напиши сообщение — админ сможет ответить анонимно"
    )

# Обработка всех сообщений
@bot.message_handler(func=lambda m: True)
def handle_message(message):

    # =================================
    # Если сообщение от админа и это ответ на чужое сообщение
    # =================================
    if (
        message.from_user.id == ADMIN_ID
        and message.reply_to_message
        and message.reply_to_message.message_id in reply_map
    ):
        user_id = reply_map[message.reply_to_message.message_id]

        bot.send_message(
            user_id,
            f"📨 Ответ администратора:\n\n{message.text}"
        )

        bot.send_message(
            ADMIN_ID,
            "✅ Ответ отправлен"
        )
        return

    # =================================
    # Любое другое сообщение (от анонима или админа)
    # =================================
    sent = bot.send_message(
        ADMIN_ID,
        f"📩 Анонимное сообщение:\n\n{message.text}"
    )

    # Сохраняем соответствие, чтобы ответить позже
    reply_map[sent.message_id] = message.from_user.id

    # Подтверждение отправителю (кроме админа, чтобы не спамить самому себе)
    if message.from_user.id != ADMIN_ID:
        bot.send_message(
            message.chat.id,
            "✅ Сообщение отправлено"
        )

print("Бот запущен и ждёт сообщения...")
bot.polling(non_stop=True)
