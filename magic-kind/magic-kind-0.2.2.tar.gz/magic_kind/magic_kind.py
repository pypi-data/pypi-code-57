

def is_magic_choice(attr_name: str) -> bool:
    """Determine iff attr_name meets magic choice formatting requirements.

    This is a helper for MagicKind metaclass that determines if an attribute
    name should be treated as a user defined magic-value choice

    Args:
        attr_name: name of an attribute
    Returns:
        True iff all the following are true about attr_name:
           * Is a valid python identifier.
           * Is upper case.
           * Does not begin with an underscore.
    """
    return (
        attr_name.isupper()
        and attr_name.isidentifier()
        and not attr_name.startswith("_")
    )


class MetaMagicKind(type):
    """Meta class to MagicKind class."""

    def __new__(cls, name, bases, dct):
        meta = super().__new__(cls, name, bases, dct)
        meta._choice_dict = {}
        meta._choice_set = set()
        for attr_name, value in dct.items():
            if is_magic_choice(attr_name):
                meta._choice_set.add(value)
                meta._choice_dict[attr_name] = value
        return meta

    def __iter__(cls):
        for choice in cls._choice_set:
            yield choice

    def __contains__(cls, value):
        return bool(value in cls._choice_set)

    def __len__(cls):
        return len(cls._choice_set)

    def __getitem__(cls, attr_name):
        return cls._choice_dict[attr_name]

    def get_dict(cls):
        """Get dictionary of choice names to their values."""
        return dict(cls._choice_dict)

    def get_names(cls):
        """Get set of choice names."""
        return set(cls._choice_dict)


class MagicKind(metaclass=MetaMagicKind):
    """Simple alternative to Enum for common "Magic Value" cases."""

    @classmethod
    def _pydantic_validate(cls, v):
        """To support use of MagicKind types in Pydantic models."""
        if not v in cls:
            raise ValueError(f"The value {v} of type {type(v)} not valid for {cls}")
        return v

    @classmethod
    def __get_validators__(cls):
        """To support use of MagicKind types in Pydantic models."""
        yield cls._pydantic_validate
