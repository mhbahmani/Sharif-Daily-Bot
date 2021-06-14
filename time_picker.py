import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import utils
from datetime import datetime


def create_time_picker(year=None, month=None):

    now = datetime.now()

    if year == None:
        year = now.hour
        month = now.minute

    data_ignore = utils.create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    day = 1
    row.append(
        InlineKeyboardButton(
            "↑",
            callback_data=utils.create_callback_data("NEXT-HOUR", year, month, day)
        )
    )
    row.append(
        InlineKeyboardButton(
            "↑",
            callback_data=utils.create_callback_data("NEXT-MIN", year, month, day)
        )
    )
    keyboard.append(row)

    row=[]
    row.append(InlineKeyboardButton(year, callback_data=data_ignore))
    row.append(InlineKeyboardButton(month, callback_data=data_ignore))
    keyboard.append(row)

    row=[]
    day = 1
    row.append(
        InlineKeyboardButton(
            "↓",
            callback_data=utils.create_callback_data("PREV-HOUR", year, month, day)
        )
    )
    row.append(
        InlineKeyboardButton(
            "↓",
            callback_data=utils.create_callback_data("PREV-MIN", year, month, day)
        )
    )
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_time_selection(bot, update):
    ret_data = (False, None)
    query = update.callback_query
    (action, year, month, day) = utils.separate_callback_data(query.data)
    import datetime
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        bot.edit_message_text(
            text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        ret_data = True,datetime.datetime(int(year), int(month), int(day))
    elif action == "NEXT-HOUR":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(year + 1, month))
    elif action == "NEXT-MIN":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(year, month + 1))
    elif action == "PREV-HOUR":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(year - 1, month))
    elif action == "PREV-MIN":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(year - 1, month - 1))
    else:
        bot.answer_callback_query(callback_query_id= query.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data