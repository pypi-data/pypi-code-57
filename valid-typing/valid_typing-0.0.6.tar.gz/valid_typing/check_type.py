import typing

TYPING_MAP = {
    list: typing.List,
    set: typing.Set,
    dict: typing.Dict,
}


def check_type(actual, definition):
    try:
        actual = TYPING_MAP[actual]
    except KeyError:
        pass
    try:
        definition = TYPING_MAP[definition]
    except KeyError:
        pass

    if type(definition) == typing.TypeVar:
        # Currently any type variable will be considered generic
        return True

    if hasattr(definition, "__origin__") and definition.__origin__ == list:
        # The only valid case is that they're both lists, and
        # if that's the case we want to check their types
        return (
            hasattr(actual, "__origin__")
            and actual.__origin__ == list
            and check_type(actual.__args__[0], definition.__args__[0])
        )

    if hasattr(definition, "__origin__") and definition.__origin__ == set:
        # The only valid case is that they're both sets, and
        # if that's the case we want to check their types
        return (
            hasattr(actual, "__origin__")
            and actual.__origin__ == set
            and check_type(actual.__args__[0], definition.__args__[0])
        )

    if hasattr(definition, "__origin__") and definition.__origin__ == dict:
        # The only valid case is that they're both dicts, and
        # if that's the case we want to check their types
        return (
            hasattr(actual, "__origin__")
            and actual.__origin__ == dict
            and check_type(actual.__args__[0], definition.__args__[0])
            and check_type(actual.__args__[1], definition.__args__[1])
        )

    if hasattr(definition, "__origin__") and definition.__origin__ == typing.Union:
        if hasattr(actual, "__origin__") and actual.__origin__ == typing.Union:
            return all(check_type(arg, definition) for arg in actual.__args__)
        return any(check_type(actual, arg) for arg in definition.__args__)

    return actual == definition
