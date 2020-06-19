from collections import UserDict


class NeverNoneDict(UserDict):
    """
    Dictionary with no None entries.
    Deletes keys that get updated to None and works recursively.

    >>> nndict_ = NeverNoneDict({"a": 2, "b": None, "c": {"d": None}})
    >>> nndict_ == {'a': 2, 'c': {}}
    True
    >>> nndict_ = NeverNoneDict({"a": 2})
    >>> nndict_ == {'a': 2}
    True
    >>> nndict_["a"] = None
    >>> nndict_
    {}
    """
    def __setitem__(self, key, value):
        if value is not None:
            if isinstance(value, dict):
                value = NeverNoneDict(value)
            return super().__setitem__(key, value)
        elif super().__contains__(key):
            return super().__delitem__(key)
