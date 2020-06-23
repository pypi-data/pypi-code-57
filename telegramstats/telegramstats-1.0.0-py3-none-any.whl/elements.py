from typing import *


def render_element(element: Union[Dict[str, str], str]) -> str:
    """Convert a Telegram element to a string, if possible."""
    if isinstance(element, str):
        return element
    elif isinstance(element, dict):
        return element.get("text", "")
    else:
        raise TypeError("Unknown element type")


def merge_message(message: Union[List[str], str]) -> str:
    """Create a string from all elements contained inside of a message."""
    if isinstance(message, str):
        return message
    elif isinstance(message, list):
        return "".join([render_element(element) for element in message])
    raise TypeError("Unknown message type")
