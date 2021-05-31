from typing import Dict


def event_data_to_str(event_data: Dict[str, str]) -> str:
    """
    Helper function for formatting the gathered event info.
    """

    facts = [f'{key}: {value}' for key, value in event_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def reformat_username(username: str) -> str:
    return '@{}'.format(username.replace("_", "\\_"))