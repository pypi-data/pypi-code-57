from __future__ import annotations

# https://github.com/alleycat-at-git/monad/blob/master/python/src/option.py
from common_py.monad import Monad
from typing import TypeVar, Generic, Callable, Optional

S = TypeVar("S")
S2 = TypeVar("S2")


class Option(Monad, Generic[S]):
    def __init__(self, value: Optional[S]):
        self.value: Optional[S] = value

    # pure :: a -> Option a
    @staticmethod
    def pure(x: S) -> Option[S]:
        return Some(x)

    # flat_map :: # Option a -> (a -> Option b) -> Option b
    def flat_map(self, f: Callable[[S], Option[S2]]) -> Option[S2]:
        if self.value is None:
            return f(self.value)
        else:
            return nil


class Some(Option):
    def __init__(self, value: S):
        super(Some, self).__init__(value)


class Nil(Option):
    def __init__(self):
        self.value = None


nil = Nil()
