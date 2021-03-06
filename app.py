from typing import Text
from db import DB
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
import time_picker


# Stages:
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


class SharifDailyBot:

    def __init__(self, token, admin_ids=None, log_level='INFO'):
        if not admin_ids: admin_ids = []
        self.admin_ids = admin_ids
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.markup = ReplyKeyboardMarkup(messages.choices_keyboard, one_time_keyboard=True)

        self.db = DB()

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level={
                'INFO': logging.INFO,
                'DEBUG': logging.DEBUG,
                'ERROR': logging.ERROR,
                }[log_level])


    def check_admin(func):
        def wrapper(self, *args, **kwargs):
            update, context = args[0], args[1]
            user_id = update.message.chat.id
            if user_id not in self.admin_ids:
                msg = messages.you_are_not_admin_message
                update.message.reply_text(text=msg)
                return
            return func(self, *args, **kwargs)
        return wrapper


    def is_admin(self, update):
        return update.message.chat.id in self.admin_ids


    def send_msg_to_admins(self, context, message):
        for admin_id in self.admin_ids:
            context.bot.send_message(
                admin_id, message
            )


    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.start_message)


    def help(self, update, context):
        if self.is_admin(update):
            msg = messages.admin_help_message
        else: 
            msg = messages.help_message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg)


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
        elif text == "Time":
            update.message.reply_text(
                text=messages.choices_message[text],
                reply_markup=time_picker.create_time_picker()
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
        Save and display the gathered info and end.
        """

        event_data = context.user_data
        if 'choice' in event_data:
            del event_data['choice']

        success, empty_fields = utils.check_mandatory_fields(event_data)
        if not success:
            update.message.reply_text(
                text=messages.fill_mandatory_fields_message.format(empty_fields),
                reply_markup=self.markup,
            )
            return CHOOSING

        try:
            self.db.add_event(event_data.copy())

            update.message.reply_text(
                text=messages.choices_message['Done'].format(utils.event_data_to_str(event_data)),
                reply_markup=ReplyKeyboardRemove(),
            )
            
            self.send_msg_to_admins(
                context,
                messages.new_event_admin_message.format(
                    utils.reformat_username(update.effective_user.username)
                    )
            )
        except:
            update.message.reply_text(
                text=messages.add_event_failed_message,
                reply_markup=ReplyKeyboardRemove(),
            )

            self.send_msg_to_admins(
                context,
                messages.new_event_admin_message.format(
                    utils.reformat_username(update.effective_user.username),
                    utils.event_data_to_str(event_data))
            )

        event_data.clear()
        return ConversationHandler.END

    def cancel(self, update: Update, context: CallbackContext) -> int:
        """
        End the conversation
        """
        
        update.message.reply_text(
            text=messages.cancel_message,
            reply_markup=self.markup,
        )

        if context.user_data: context.user_data.clear()
        return ConversationHandler.END


    def inline_keyboard_handler(self, update: Update, context: CallbackContext):
        query = update.callback_query
        (kind, _, _, _, _) = utils.separate_callback_data(query.data)
        if kind == messages.TIME_PICKER_CALLBACK:
            self.inline_time_handler(update, context)
        elif kind == messages.CALENDAR_CALLBACK:
            self.inline_calendar_handler(update, context)

        return CHOOSING


    def inline_calendar_handler(self, update: Update, context: CallbackContext):
        selected, date = tcalendar.process_calendar_selection(context.bot, update)
        if not selected: return

        event_data = context.user_data
        category = event_data['choice']
        event_data[category] = date
        del event_data['choice']

        # delete date message
        context.bot.delete_message(
            update.callback_query.message.chat_id,
            update.callback_query.message.message_id,
        )

        if category.startswith('admin'):
            if category == 'admin_Date':
                date = event_data['admin_Date']
                update.callback_query.message.reply_text(
                    text=utils.create_events_message_by_date(self.db, date),
                    parse_mode='html',
                    reply_markup=self.markup,
                )
            event_data.clear()
        else:
            update.callback_query.message.reply_text(
                text=messages.received_info_message.format(utils.event_data_to_str(event_data)),
                reply_markup=self.markup,
            )


    def inline_time_handler(self, update: Update, context: CallbackContext):
        selected, time = time_picker.process_time_selection(context.bot, update)
        if not selected: return

        event_data = context.user_data
        category = event_data['choice']
        event_data[category] = utils.translate_time_to_fa(time)
        del event_data['choice']

        # delete date message
        context.bot.delete_message(
            update.callback_query.message.chat_id,
            update.callback_query.message.message_id,
        )

        update.callback_query.message.reply_text(
            text=messages.received_info_message.format(utils.event_data_to_str(event_data)),
            reply_markup=self.markup,
        )


    @check_admin
    def get_tomorrow_events(self, update, context):
        events_message = utils.create_tomorrow_events_message(self.db)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode='html',
            text=events_message
        )


    @check_admin
    def get_events(self, update, context):
        choice = 'admin_Date'
        context.user_data['choice'] = choice
        update.message.reply_text(
            text=messages.choices_message[choice],
            reply_markup=tcalendar.create_calendar()
        )


    def setup_handlers(self):
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help)
        self.dispatcher.add_handler(help_handler)

        get_tomorrow_events_handler = CommandHandler('get', self.get_tomorrow_events)
        self.dispatcher.add_handler(get_tomorrow_events_handler)

        get_events_handler = CommandHandler('getall', self.get_events)
        self.dispatcher.add_handler(get_events_handler)

        inline_handler = CallbackQueryHandler(self.inline_keyboard_handler)
        self.dispatcher.add_handler(inline_handler)

        add_handler = ConversationHandler(
            entry_points=[CommandHandler('add', self.add)],
            states={
                CHOOSING: [
                    MessageHandler(
                        Filters.regex('^(Title|Date|Time|Location|Link|Telegram Channel|Invited|Calendar)$'),
                        self.regular_choice
                    )
                ],
                TYPING_CHOICE: [
                    MessageHandler(
                        Filters.text & ~(Filters.command | Filters.regex('^Done$') | Filters.regex('^Cancel$')),
                        self.regular_choice
                    )
                ],
                TYPING_REPLY: [
                    MessageHandler(
                        Filters.text & ~(Filters.command | Filters.regex('^Done$') | Filters.regex('^Cancel$')),
                        self.received_information,
                    )
                ],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), self.done), MessageHandler(Filters.regex('^Cancel$'), self.cancel)],
        )   
        self.dispatcher.add_handler(add_handler)


    def run(self):
        self.setup_handlers()
        self.updater.start_polling()

        self.updater.idle()