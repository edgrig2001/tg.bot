import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f)

users = load_users()

keyboard = ReplyKeyboardMarkup(
    [["▶️ Старт", "❓ Помощь"], ["🧹 Очистить историю"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши мне 🙂", reply_markup=keyboard)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Просто пиши текст")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    users[user_id] = []
    save_users(users)
    await update.message.reply_text("История очищена")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text

    if text == "▶️ Старт":
        return await start(update, context)
    if text == "❓ Помощь":
        return await help_cmd(update, context)
    if text == "🧹 Очистить историю":
        return await clear(update, context)

    if user_id not in users:
        users[user_id] = []

    users[user_id].append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=users[user_id]
    )

    answer = response.choices[0].message.content

    users[user_id].append({"role": "assistant", "content": answer})
    save_users(users)

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()