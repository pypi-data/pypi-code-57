import typing as T

Ty = T.TypeVar('Ty')  # Any type

Many = T.Union[Ty, T.Sequence[Ty]]
