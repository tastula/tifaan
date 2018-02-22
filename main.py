from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import path, mkdir, remove, rename
import logging


# Enable error messages
logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)


def create_path(directory):
    if not path.exists(directory):
        mkdir(directory)


def create_file(file_name, directory = ""):
    if not path.exists(directory + "/" + file_name):
        open(directory + "/" + file_name, "w+").close()


def get_message_stats(bot, update):
    chat = update.message.chat.title

    # Make sure the file exists
    create_path("chats")
    create_path("chats/" + chat)
    create_file("statistics", "chats/" + chat)

    # Read statistics
    stats = []
    total_messages = 0
    with open("chats/" + chat + "/statistics", "r+") as file_stats:
        for line in file_stats:
            data = line.split()
            total_messages += int(data[0])
            stats.append((data[0], data[1]))
    file_stats.close()
    stats.sort(key = lambda data: data[0], reverse = True)

    # Form the message
    message = ""
    for data in stats:
        percent = round((100*int(data[0]))/total_messages)
        message = message + str(data[0] + " (" + str(percent) + "%) - " + \
                                data[1] + "\n")
    message = message + "\nViestejä yhteensä " + str(total_messages)

    # Print statistics
    bot.send_message(
        chat_id = update.message.chat_id,
        text = message
    )


def set_message_stats(bot, update):
    chat = update.message.chat.title
    user = update.message.from_user
    name = user.first_name
    
    # Make sure the file exists
    create_path("chats")
    create_path("chats/" + chat)
    create_file("statistics", "chats/" + chat)

    # Write statistics
    new_user = True
    with open("chats/" + chat + "/statistics_new", "a+") as file_stats_new:
        with open("chats/" + chat + "/statistics", "r") as file_stats:
            for line in file_stats:
                data = line.split()
                if data and name == data[1]:
                    messages = int(data[0]) + 1
                    file_stats_new.write(str(messages) + " " + name)
                    new_user = False
                else:
                    file_stats_new.write(line)
        file_stats.close()
    file_stats_new.close()
    if new_user:
        with open("chats/" + chat + "/statistics", "a") as file_stats:
            file_stats.write("1 " + name)
        file_stats.close()
    remove("chats/" + chat + "/statistics")
    rename("chats/" + chat + "/statistics_new",
           "chats/" + chat + "/statistics")


updater = Updater("token")

# Bot commands
updater.dispatcher.add_handler(CommandHandler("viestit",
    lambda bot, update: get_message_stats(bot, update)))

# User message handling
updater.dispatcher.add_handler(MessageHandler(Filters.text, 
    lambda bot, update: set_message_stats(bot, update)))

updater.start_polling()
