from typing import Dict

from messages import choices_to_fa


def event_data_to_str(event_data: Dict[str, str]) -> str:
    """
    Helper function for formatting the gathered event info.
    """

    data = [f'{choices_to_fa[key]}: {value}' for key, value in event_data.items()]
    return "\n".join(data).join(['\n', '\n'])


def reformat_username(username: str) -> str:
    return '@{}'.format(username.replace("_", "\\_"))