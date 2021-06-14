import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import utils
from datetime import datetime
from messages import TIME_PICKER_CALLBACK


def create_callback_data(action, year, month, day):
    return TIME_PICKER_CALLBACK + ";" + ";".join([ action, str(year), str(month), str(day)])


def create_time_picker(year=None, month=None):

    now = datetime.now()

    if year == None:
        year = now.hour
        month = now.minute

    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    day = 1
    row.append(
        InlineKeyboardButton(
            "↑",
            callback_data=create_callback_data("NEXT-HOUR", year, month, day)
        )
    )
    row.append(
        InlineKeyboardButton(
            "↑",
            callback_data=create_callback_data("NEXT-MIN", year, month, day)
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
            callback_data=create_callback_data("PREV-HOUR", year, month, day)
        )
    )
    row.append(
        InlineKeyboardButton(
            "↓",
            callback_data=create_callback_data("PREV-MIN", year, month, day)
        )
    )
    keyboard.append(row)

    keyboard.append(
        [InlineKeyboardButton(
            "Select",
            callback_data=create_callback_data("SELECT", year, month, day)
        )]
    )

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