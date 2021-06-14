import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import utils
from datetime import datetime
from messages import TIME_PICKER_CALLBACK


def create_callback_data(action, hour=0, minute=0, day=0):
    return TIME_PICKER_CALLBACK + ";" + ";".join([action, str(hour), str(minute), str(day)])


def create_time_picker(hour=None, minute=None):

    now = datetime.now()
    if not hour: hour = now.hour
    if not minute: minute = now.minute

    keyboard = []

    # First row - Upward pointing arrows
    row=[]
    day = 1
    row.append(
        InlineKeyboardButton(
            "↑",
            callback_data=create_callback_data("NEXT-HOUR", hour, minute, day)
        )
    )
    row.append(
        InlineKeyboardButton(
            "↑",
            callback_data=create_callback_data("NEXT-MIN", hour, minute, day)
        )
    )
    keyboard.append(row)

    # Second row - Time
    row=[]
    row.append(InlineKeyboardButton(hour, callback_data=create_callback_data("IGNORE")))
    row.append(InlineKeyboardButton(minute, callback_data=create_callback_data("IGNORE")))
    keyboard.append(row)

    # Third row - Downward pointing arrows
    row=[]
    day = 1
    row.append(
        InlineKeyboardButton(
            "↓",
            callback_data=create_callback_data("PREV-HOUR", hour, minute, day)
        )
    )
    row.append(
        InlineKeyboardButton(
            "↓",
            callback_data=create_callback_data("PREV-MIN", hour, minute, day)
        )
    )
    keyboard.append(row)

    # Last row - Select button
    row = []
    row.append(
        InlineKeyboardButton(
            "Select",
            callback_data=create_callback_data("SELECT", hour, minute, day)
        )
    )
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_time_selection(bot, update):
    ret_data = (False, None)
    query = update.callback_query
    (_, action, year, month, day) = utils.separate_callback_data(query.data)
    import datetime
    curr = datetime.datetime(2021, 4, 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == "SELECT":
        bot.edit_message_text(
            text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        ret_data = True, f'{year} {month}'
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
            reply_markup=create_time_picker(year, month - 1))
    else:
        bot.answer_callback_query(callback_query_id= query.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data