"""message parsing methods used in a number of applications"""

import logging
from typing import List
from functools import wraps
from .bots import BOT_LIST


logger = logging.getLogger(__name__)


def is_bot_message(**payload) -> bool:
    """
    Returns whether the message is a bot message

    :param payload: RTM slack payload
    """
    message_info = payload['data']
    if any([
        message_info.get('subtype') == 'bot_message',
        message_info.get('bot_id') is not None,
        message_info.get('user') in BOT_LIST,
    ]):
        logger.debug('message is from a bot')
        return True
    return False


def is_event(**payload) -> bool:
    """
    Returns whether the message is an event

    :param payload: RTM payload
    """
    message_info = payload['data']
    if message_info.get('subtype') is not None:
        logger.debug('message is an event')
        return True
    return False


def ignore_bot_users(f):
    """
    Decorator which ignores posts from bot users in RTM messages

    :param f: function to be executed
    """
    @wraps(f)
    def wrapped(**payload):
        if is_bot_message(**payload) is True:
            logger.debug(f'bypassing {f}')
            return
        return f(**payload)
    return wrapped


def ignore_events(f):
    """
    Decorator which ignores messages with a subtype (event subtypes)

    :param f: function to be executed
    """
    @wraps(f)
    def wrapped(**payload):
        if is_event(**payload) is True:
            logger.debug(f'bypassing {f}')
            return
        return f(**payload)
    return wrapped


def check_authorized(authorized_users: List[str]):
    """
    Decorator which will execute the function if the message poster is in a list of authorized users

    Implementation:

    ::

        @check_authorized(authorized_users=['userid1', 'userid2', ...])
        def run_on_message(**payload):
            ...


    :param f: function to be decorated
    :param authorized_users: list of authorized users
    """
    # todo generalize this method
    def authorize(f):
        @wraps(f)
        def wrapped(**payload):
            message_info = payload['data']
            user_id = message_info.get('user')
            if user_id is None or user_id not in authorized_users:
                logger.debug(f'user {user_id} is not authorized to access this functionality')
                return
            logger.debug(f'user @{user_id} is authorized, executing callback')
            return f(**payload)
        return wrapped
    return authorize


def standard_parsing(f):
    """
    Applies standard parsing (non-bot users and event-only messages) to the function.

    :param f: function to be decorated
    """
    return ignore_events(
        ignore_bot_users(
            f
        )
    )


