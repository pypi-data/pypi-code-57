import typing


def check_type(actual, definition):
    if hasattr(definition, "__origin__") and definition.__origin__ == list:
        # The only valid case now is that the actual type is also a list, therefore test both types of list
        if not hasattr(actual, "__origin__") or actual.__origin__ != list:
            return False

        # The definition accepts any type
        if not len(definition.__args__):
            return True

        # Both have list element definitions, so check their equality
        return len(definition.__args__) and check_type(
            actual.__args__[0], definition.__args__[0]
        )

    if hasattr(definition, "__origin__") and definition.__origin__ == typing.Union:
        if hasattr(actual, "__origin__") and actual.__origin__ == typing.Union:
            return all(check_type(arg, definition) for arg in actual.__args__)
        return any(check_type(actual, arg) for arg in definition.__args__)

    return actual == definition
