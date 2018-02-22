updater = Updater("token here")

def get_messages(bot, update):
    pass

def add_messages(bot, update, text):
    pass

# Bot commands
updater.dispatcher.add_handler(CommandHandler(
    "viestit", get_messages))

# User message handling
updater.dispatcher.add_handler(MessageHandler(
    Filters.text, add_message))

updater.start_polling()
