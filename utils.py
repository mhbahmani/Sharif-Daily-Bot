from typing import Dict
from jdatetime import set_locale, datetime
from convert_numbers import english_to_hindi
    
from messages import choices_to_fa, suggestion_message_header, CALENDAR_CALLBACK, TIME_PICKER_CALLBACK
from time_picker import process_time_selection
from tcalendar import process_calendar_selection


def event_data_to_str(event_data: Dict[str, str]) -> str:
    """
    Helper function for formatting the gathered event info.
    """

    data = [f'{choices_to_fa[key]}: {value}' for key, value in event_data.items()]
    return "\n".join(data).join(['\n', '\n'])


def reformat_username(username: str) -> str:
    return '@{}'.format(username.replace("_", "\\_"))


def seprate_admins(admins: str) -> list:
    return [int(admin_id) for admin_id in admins.split('\\n')]


def get_suggestion_message_header() -> str:
    set_locale('fa_IR')
    return datetime.now().strftime(
        suggestion_message_header.format(
            english_to_hindi(
                datetime.now().day)
            )
        )
        

def inline_keyboard_handler(self, bot, update):
    query = update.callback_query
    (kind, _, _, _, _) = separate_callback_data(query.data)
    if kind == TIME_PICKER_CALLBACK: return process_time_selection(bot, update)
    if kind == CALENDAR_CALLBACK: return process_calendar_selection(bot, update)


def separate_callback_data(data):
    return data.split(";")