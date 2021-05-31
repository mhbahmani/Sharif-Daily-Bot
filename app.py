from telegram.ext import (
    Updater, CommandHandler
)

import messages
import logging


# Stages:
TITLE, MONTH, DAY, TIME, INVITED, LOCATION, LINK, CHANNEL, CALENDAR = range(9)


class SharifDailyBot:

    def __init__(self, token, admin_id, log_level='INFO'):
        self.admin_id = admin_id
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level={
                'INFO': logging.INFO,
                'DEBUG': logging.DEBUG,
                'ERROR': logging.ERROR,
                }[log_level])

    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.start_message)


    def setup_handlers(self):
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        

    def run(self):
        self.setup_handlers()
        self.updater.start_polling()

        self.updater.idle()