from dotenv import load_dotenv
import os
import requests

load_dotenv()

#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# app variables
BOT_TOKEN=os.environ.get('BOT_TOKEN', os.getenv('BOT_TOKEN'))
HEROKU_PORT=int(os.environ.get('HEROKU_PORT', os.getenv('HEROKU_PORT')))
HEROKU_APP_URL=os.environ.get('HEROKU_APP_URL', os.getenv('HEROKU_APP_URL'))
JOKESBAPACK2_API_URL=os.environ.get('JOKESBAPACK2_API_URL', os.getenv('JOKESBAPACK2_API_URL'))


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Halo, {update.message.chat.first_name} {update.message.chat.last_name}!')
    update.message.reply_text('Kirim pesan apa saja, dan saya akan membalasnya dengan jokes bapack2.')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Kirim pesan apa saja, dan saya akan membalasnya dengan jokes bapack2.')


def joke(update: Update, context: CallbackContext) -> None:
    """Send user a random joke."""
    joke = requests.get(JOKESBAPACK2_API_URL).json()['data']
    update.message.reply_text(joke)


def error(update, context) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - send a random joke on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, joke))

    # log all error
    dispatcher.add_error_handler(error)

    # Start the Bot using webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=HEROKU_PORT,
                          url_path=BOT_TOKEN,
                          webhook_url=HEROKU_APP_URL + BOT_TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
