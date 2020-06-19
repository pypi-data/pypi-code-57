import typing


def check_type(actual, definition):
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

    if hasattr(definition, "__origin__") and definition.__origin__ == typing.Union:
        if hasattr(actual, "__origin__") and actual.__origin__ == typing.Union:
            return all(check_type(arg, definition) for arg in actual.__args__)
        return any(check_type(actual, arg) for arg in definition.__args__)

    return actual == definition
