from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import utils


def create_time_picker(year=None, month=None):

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
    #Second row - Week Days
    # row=[]
    # for day in days:
    #     row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    # keyboard.append(row)

    # month_weeks = monthcalendar(year, month)
    # for week in month_weeks:
    #     row = []
    #     for day in week:
    #         if day == 0:
    #             row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    #         else:
    #             row.append(
    #                 InlineKeyboardButton(
    #                     str(day),
    #                     callback_data=create_callback_data("DAY", year, month, day)
    #                 )
    #             )
    #     keyboard.append(row)
    # #Last row - Buttons
    # row = []
    # if month != now.month:
    #     row.append(
    #         InlineKeyboardButton(
    #             "<",
    #             callback_data=create_callback_data("PREV-MONTH", year, month, day)
    #         )
    #     )
    # else:
    #     row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    # row.append(
    #     InlineKeyboardButton(
    #         ">",
    #         callback_data=create_callback_data("NEXT-MONTH", year, month, day)
    #     )
    # )
    # keyboard.append(row)

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
            reply_markup=create_time_picker(int(pre.year), int(pre.month)))
    elif action == "NEXT-MIN":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_time_picker(int(ne.year), int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id= query.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data