from collections import MutableMapping


class DocumentDict(MutableMapping):
    """Almost copy-paste of collections.UserDict but without locked .data attribute
    it was moved to dunder data (__data__) for allowing usage of data.
    All dunder attributes are not passed to internal mapping.

    Init does not create a new dict but links passed mapping.

    """

    # Start by filling-out the abstract methods
    def __init__(*args, **kwargs):
        if not args:
            raise TypeError("descriptor '__init__' of 'UserDict' object "
                            "needs an argument")
        self, *args = args
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        if args:
            dict = args[0]
        elif 'dict' in kwargs:
            dict = kwargs.pop('dict')
            import warnings
            warnings.warn("Passing 'dict' as keyword argument is deprecated",
                          DeprecationWarning, stacklevel=2)
        else:
            dict = None
        self.__data__ = dict
    __init__.__text_signature__ = '($self, dict=None, /, **kwargs)'

    def __len__(self): return len(self.__data__)

    def __getitem__(self, key):
        if key in self.__data__:
            return self.__data__[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item): self.__data__[key] = item

    def __delitem__(self, key): del self.__data__[key]

    def __iter__(self):
        return iter(self.__data__)

    # Modify __contains__ to work correctly when __missing__ is present
    def __contains__(self, key):
        return key in self.__data__

    # Now, add the methods in dicts but not in MutableMapping
    def __repr__(self): return repr(self.__data__)

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["__data__"] = self.__dict__["__data__"].copy()
        return inst

    def copy(self):
        if self.__class__ is DocumentDict:
            return DocumentDict(self.__data__.copy())
        import copy
        data = self.__data__
        try:
            self.__data__ = {}
            c = copy.copy(self)
        finally:
            self.__data__ = data
        c.update(self)
        return c

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __getattr__(self, item):
        try:
            if isinstance(self.__data__[item], dict):
                return DocumentDict(self.__data__[item])
            else:
                return self.__data__[item]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key: str, value):
        if key.startswith("__") and key.endswith("__"):
            super().__setattr__(key, value)
        else:
            self.__data__[key] = value

    def __delattr__(self, item):
        try:
            del self.__data__[item]
        except KeyError as e:
            raise AttributeError(e)
