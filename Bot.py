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
