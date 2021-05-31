from telegram.ext import Updater

import logging


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

    def setup_handlers(self):
        pass
        

    def run(self):
        self.setup_handlers()
        self.updater.start_polling()