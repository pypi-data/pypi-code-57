import logging

from roboself.types import ROBOSELF_TYPE_ATTR, ROBOSELF_ACTION_VALUE

log = logging.getLogger(__name__)


def register(intent, handles_multiple=False, timeout=30):
    """Registers an action to the runtime.

    The registration is done either by intent name, or through the combination of `verb`:`entity`.
    When an action is registered for "some_name:*" it will match any "some_name:bla".
    """
    def decorator(func):
        intent_name = intent
        if intent_name is None:
            intent_name = func.__name__

        log.debug(f"Registering {intent_name}")

        setattr(func, ROBOSELF_TYPE_ATTR, ROBOSELF_ACTION_VALUE)

        func.handles_multiple = handles_multiple
        func.timeout = timeout

        action_keys = getattr(func, 'action_keys') if hasattr(func, 'action_keys') else []
        action_keys.append(intent_name)
        func.action_keys = action_keys

        return func

    return decorator
