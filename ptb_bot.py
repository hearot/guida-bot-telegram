from telegram.ext import MessageHandler, Updater
from telegram.ext.filters import Filters

from conf_primo_bot import bot_token

bot = Updater(token=bot_token, use_context=True)


def handler(update, *_):
    update.message.reply_text("Ciao mondo!")


def main():
    bot.dispatcher.add_handler(MessageHandler(Filters.all, handler))
    bot.start_polling()
    bot.idle()


main()
