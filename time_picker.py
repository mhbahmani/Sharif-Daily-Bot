from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from datetime import datetime
from utils import separate_callback_data, translate_numbers_to_fa
from messages import TIME_PICKER_CALLBACK, CALLBACK_ERROR


def create_callback_data(action, hour=0, minute=0, day=0):
    return TIME_PICKER_CALLBACK + ";" + ";".join([action, str(hour), str(minute), str(day)])


def create_time_picker(hour=None, minute=None):

    now = datetime.now()
    if hour == None: hour = now.hour
    if minute == None: minute = now.minute + 5 - (now.minute % 5 if now.minute % 5 else 5)

    hour %= 24
    minute %= 60 
    
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
    out = (False, None)
    query = update.callback_query
    (_, action, hour, minute, day) = separate_callback_data(query.data)
    hour = int(hour)
    minute = int(minute)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == "SELECT":
        bot.edit_message_text(
            text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        hour = translate_numbers_to_fa(hour)
        minute = translate_numbers_to_fa(minute)
        out = True, f'{hour}:{minute}'
    elif action == "NEXT-HOUR":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(hour + 1, minute))
    elif action == "NEXT-MIN":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(hour, minute + 5))
    elif action == "PREV-HOUR":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(hour - 1, minute))
    elif action == "PREV-MIN":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(hour, minute - 5))
    else:
        bot.answer_callback_query(callback_query_id= query.id, text=CALLBACK_ERROR)

    return out