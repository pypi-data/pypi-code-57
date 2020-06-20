import typing
import hashlib
import time

DEFAULT_BASE = (2 ** 30 - 123) * 0.91
DEFAULT_A = (2 ** 29 - 456) * 0.93
DEFAULT_B = (2 ** 28 - 789) * 0.95

class Random(object):

    def __init__(self, seed=None, a=DEFAULT_A, b=DEFAULT_B, base=DEFAULT_BASE):
        self.seed = self.get_seed(seed)
        self.a = a
        self.b = b
        self.base = base

    @classmethod
    def get_seed(cls, seed: typing.Union[str, bytes, int, float]) -> typing.Union[int, float]:
        if seed is None:
            return time.time()
        if isinstance(seed, str):
            seed = seed.encode("utf-8")
        if isinstance(seed, bytes):
            seed = int.from_bytes(hashlib.sha512(seed).digest(), "big")
        if isinstance(seed, (int, float)):
            return seed
        else:
            raise RuntimeError("Random seed type must be in (str, bytes, int, float), but {} got.".format(type(seed)))

    def random(self) -> float:
        """return a float number in [0, 1).
        """
        r = (self.a * self.seed + self.b) % self.base
        p = r / self.base
        self.seed = r
        return p

    def randint(self, max, min=0) -> int:
        """return int number in [min, max)
        """
        return int(self.random() * (max - min) + min)

    def get_bytes(self, length: int = 1) -> bytes:
        return bytes([self.randint(256) for _ in range(length)])

    def choice(self, seq: typing.List) -> typing.Any:
        index = self.randint(len(seq))
        return seq[index]

    def choices(self, population: typing.List, weights=None, *, cum_weights=None, k: int = 1) -> typing.List:
        result = []
        for _ in range(k):
            result.append(self.choice(population))
        return result
