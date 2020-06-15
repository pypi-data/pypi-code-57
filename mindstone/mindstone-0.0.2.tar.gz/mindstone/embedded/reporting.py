""" reporting module.

"""

_verbose = True
_reported_errors = []
_reported_messages = []


def set_verbosity(verbose: bool):
    """ sets the verbosity of the driver system. """
    global _verbose
    _verbose = verbose


def display(*args, **kwargs):
    if _verbose:
        print(*args, **kwargs)


def report_error(message: str):
    _reported_errors.append(message)


def report_message(message: str):
    _reported_messages.append(message)


def get_reported_errors():
    return _reported_errors


def get_reported_messages():
    return _reported_messages


def clear_reported_errors():
    global _reported_errors
    _reported_errors = []


def clear_reported_messages():
    global _reported_messages
    _reported_messages = []
