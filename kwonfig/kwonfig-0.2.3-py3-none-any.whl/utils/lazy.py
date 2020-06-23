import typing as T

Ty = T.TypeVar('Ty')  # Any type


class LazyInit(T.Generic[Ty]):
    def __init__(self, cls: T.Type[Ty], *args: T.Any, **kwargs: T.Any):
        self.__cls__ = cls
        self.__args__ = args
        self.__kwargs__ = kwargs

        self.__instance__ = None

    def __init_singleton__(self):
        cls = self.__cls__
        args = self.__args__
        kwargs = self.__kwargs__

        self.__instance__ = cls(*args, **kwargs)

    def __getattr__(self, name: str) -> T.Any:
        if self.__instance__ is None:
            self.__init_singleton__()
        return getattr(self.__instance__, name)


def lazy(cls: T.Type[Ty], *args, **kwargs) -> Ty:
    return LazyInit(cls, *args, **kwargs)
