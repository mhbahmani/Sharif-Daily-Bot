from typing import Dict
from allnumbers import Numbers
from jdatetime import set_locale, datetime, timedelta
from convert_numbers import english_to_hindi
    
from messages import choices_to_fa, suggestion_message_header, events_message, event_emojis, info

import re


mandatory_fields = ['Title', 'Date', 'Time']


def event_data_to_str(event_data: Dict[str, str]) -> str:
    """
    Helper function for formatting the gathered event info.
    """

    data = [f'{choices_to_fa[key]}: {value}' for key, value in event_data.items()]
    return "\n".join(data).join(['\n', '\n'])


def check_mandatory_fields(event_data: Dict[str, str]) -> tuple:
    """
    Check mandatory fields
    Returns empty fields
    """
    empty_fields = []
    for field in mandatory_fields:
        if not event_data.get(field, None): empty_fields.append(choices_to_fa[field])

    return len(empty_fields) == 0, '، '.join(empty_fields)


def reformat_username(username: str) -> str:
    return '@{}'.format(username.replace("_", "\\_"))


def seprate_admins(admins: str) -> list:
    return [int(admin_id) for admin_id in admins.split('\\n')]


def create_events_message(events):
    all_events = []
    for event in events:
        events_info = []
        for key in info:
            if not event.get(key): continue
            data = event[key].split('\n')
            for d in data: events_info.append(f'{event_emojis[key]}{d}')
        all_events.append('\n'.join(
            list(filter(lambda x: x != '', events_info))
            ))

    return '\n\n'.join(all_events)


def create_tomorrow_events_message(db):
    header = get_suggestion_message_header()
    date = re.sub(':', '', header.split('، ')[1])
    events = get_events_by_date(date)
    return events_message.format(header, events)


def create_events_message_by_date(db, date):
    header = get_suggestion_message_header(date)
    events = get_events_by_date(date)
    return events_message.format(header, events)


def get_events_by_date(db, date):
    return create_events_message(db.get_events(date))


def get_suggestion_message_header(date: None) -> str:
    set_locale('fa_IR')
    if date: return suggestion_message_header.format(date)
    tomorrow = datetime.today() + timedelta(days=1)
    return tomorrow.strftime(
        suggestion_message_header.format(
            english_to_hindi(
                tomorrow.day)
            )
        )


def separate_callback_data(data):
    return data.split(";")


def translate_date_to_fa(date: str):
    date = date\
        .replace('یکشنبه', 'یک‌شنبه')\
        .replace('سه شنبه', 'سه‌شنبه')\
        .replace('پنجشنبه', 'پنج‌شنبه')
    splitted = date.split()
    return f'{splitted[0]} {english_to_hindi(splitted[1])} {splitted[2]}'


def translate_time_to_fa(date: str):
    splitted = date.split(':')
    return f'{english_to_hindi(splitted[0])}:{english_to_hindi(splitted[1])}'