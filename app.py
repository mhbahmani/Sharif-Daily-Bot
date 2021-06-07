from typing import Text
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
)

import tcalendar
import messages
import utils
import logging


# Stages:
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


class SharifDailyBot:

    def __init__(self, token, admin_id, log_level='INFO'):
        self.admin_id = admin_id
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.markup = ReplyKeyboardMarkup(messages.choices_keyboard, one_time_keyboard=True)

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level={
                'INFO': logging.INFO,
                'DEBUG': logging.DEBUG,
                'ERROR': logging.ERROR,
                }[log_level])


    def send_msg_to_admin(self, context, message):
        context.bot.send_message(
            self.admin_id, 
            message
        )


    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.start_message)


    def add(self, update: Update, _: CallbackContext) -> int:
        """
        Add a new program
        """

        update.message.reply_text(
            text=messages.add_message,
            reply_markup=self.markup,
        )

        return CHOOSING


    def regular_choice(self, update: Update, context: CallbackContext) -> int:
        """
        Ask the user for info about the selected predefined choice
        """

        text = update.message.text
        context.user_data['choice'] = text
        
        if text == "Date":
            update.message.reply_text(
                text=messages.choices_message[text],
                reply_markup=tcalendar.create_calendar()
            )
            return CHOOSING
    
        update.message.reply_text(
            text=messages.choices_message[text]
        )
        return TYPING_REPLY


    def received_information(self, update: Update, context: CallbackContext) -> int:
        """
        Store info provided by user and ask for the next category.
        """

        event_data = context.user_data
        text = update.message.text
        category = event_data['choice']
        event_data[category] = text
        del event_data['choice']

        update.message.reply_text(
            text=messages.received_info_message.format(utils.event_data_to_str(event_data)),
            reply_markup=self.markup,
        )

        return CHOOSING


    def done(self, update: Update, context: CallbackContext) -> int:
        """
        Display the gathered info and end.
        """

        event_data = context.user_data
        if 'choice' in event_data:
            del event_data['choice']

        update.message.reply_text(
            text=messages.choices_message['Done'].format(utils.event_data_to_str(event_data)),
            reply_markup=ReplyKeyboardRemove(),
        )

        self.send_msg_to_admin(
            context,
            messages.new_event_admin_message.format(
                utils.reformat_username(update.effective_user.username)
                )
        )

        event_data.clear()
        return ConversationHandler.END


    def inline_handler(self, update: Update, context: CallbackContext):
        selected, date = tcalendar.process_calendar_selection(context.bot, update)
        if selected:
            context.bot.send_message(chat_id=update.callback_query.from_user.id,
                            text="You selected %s" % (date.strftime("%d/%m/%Y")),
                            reply_markup=ReplyKeyboardRemove())

        event_data = context.user_data
        category = event_data['choice']
        event_data[category] = date.strftime('%A %d %B')
        del event_data['choice']

        update.message.reply_text(
            text=messages.received_info_message.format(utils.event_data_to_str(event_data)),
            reply_markup=self.markup,
        )
        return CHOOSING


    def setup_handlers(self):
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        calendar_handler = CallbackQueryHandler(self.inline_handler)
        self.dispatcher.add_handler(calendar_handler)
        
        add_handler = ConversationHandler(
            entry_points=[CommandHandler('add', self.add)],
            states={
                CHOOSING: [
                    MessageHandler(
                        Filters.regex('^(Title|Date|Hour|Location|Link|Telegram Channel|Invited)$'), self.regular_choice
                    )
                ],
                TYPING_CHOICE: [
                    MessageHandler(
                        Filters.text & ~(Filters.command | Filters.regex('^Done$')), self.regular_choice
                    )
                ],
                TYPING_REPLY: [
                    MessageHandler(
                        Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                        self.received_information,
                    )
                ],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), self.done)],
        )   
        self.dispatcher.add_handler(add_handler)


    def run(self):
        self.setup_handlers()
        self.updater.start_polling()

        self.updater.idle()