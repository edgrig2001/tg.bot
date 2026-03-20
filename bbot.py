import os

print("TELEGRAM_TOKEN =", os.environ.get("TELEGRAM_TOKEN"))
print("OPENAI_API_KEY =", os.environ.get("OPENAI_API_KEY"))

print("Бот запускается")
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Бот запускается...")
    app.run_polling()
