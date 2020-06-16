from __future__ import annotations

# https://github.com/alleycat-at-git/monad/blob/master/python/src/monad.py
from typing import TypeVar, Generic, Callable

T = TypeVar("T")
T2 = TypeVar("T2")


class Monad(Generic[T]):
    # pure :: a -> M a
    @staticmethod
    def pure(x):
        raise Exception("pure method needs to be implemented")

    # flat_map :: # M a -> (a -> M b) -> M b
    def flat_map(self, f: Callable[[T], T2]):
        raise Exception("flat_map method needs to be implemented")

    # map :: # M a -> (a -> b) -> M b
    def map(self, f: Callable[[T], T2]) -> Monad[T2]:
        return self.flat_map(lambda x: self.pure(f(x)))
