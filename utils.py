from typing import Dict


def facts_to_str(event_data: Dict[str, str]) -> str:
    """
    Helper function for formatting the gathered event info.
    """

    facts = [f'{key}: {value}' for key, value in event_data.items()]
    return "\n".join(facts).join(['\n', '\n'])
