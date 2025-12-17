import telebot

TOKEN = "7083901949:AAFBtRVRGVX_4OFMHgdIoI_L9IY4UHQucDE"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 2057965337  # твой Telegram ID
import telebot

# =========================
# Настройки бота
# =========================
TOKEN = "7083901949:AAFBtRVRGVX_4OFMHgdIoI_L9IY4UHQucDE"
ADMIN_ID = 2057965337  # твой Telegram ID
# =========================

bot = telebot.TeleBot(TOKEN)

# Словарь: message_id администратора -> id пользователя
reply_map = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "✉️ Привет! Напиши сообщение — я буду рад его прочитать"
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
            f"📨 Ответ от Кваса:\n\n{message.text}"
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
