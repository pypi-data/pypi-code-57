import typing

TYPING_MAP = {
    list: typing.List,
    set: typing.Set,
    dict: typing.Dict,
}


def check_type(actual, definition):
    # For comparisons to work out the box, first convert from builtin to typing equivilant
    try:
        actual = TYPING_MAP[actual]
    except KeyError:
        pass
    try:
        definition = TYPING_MAP[definition]
    except KeyError:
        pass

    # Currently any type variable will be considered generic
    if type(definition) == typing.TypeVar:
        return True

    # Any allows any.
    if definition == typing.Any:
        return True

    # Currently support list, set, dict and union
    if hasattr(definition, "__origin__"):
        if hasattr(actual, "__origin__"):
            return actual.__origin__ == definition.__origin__ and all(
                check_type(actual.__args__[i], definition.__args__[i])
                for i in range(len(actual.__args__))
            )
        return any(check_type(actual, arg) for arg in definition.__args__)

    try:
        return issubclass(actual, definition)
    except TypeError:
        return actual == definition
