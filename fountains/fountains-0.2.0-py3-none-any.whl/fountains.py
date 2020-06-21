"""Library for generating and embedding test data.

Python library for generating and embedding in a compact way
random but reproducible data for unit testing.
"""

import doctest
import string
from math import log2
from hashlib import sha256
from bitlist import bitlist

class fountains():
    """
    Class for test data enumeration objects.

    >>> [int.from_bytes(bs, 'little') for (_, bs) in zip(range(3), fountains(2))]
    [45283, 7118, 54574]
    >>> [int.from_bytes(bs, 'little') for bs in fountains(1, 3)]
    [227, 206, 46]
    >>> fun = lambda bs: bytes(reversed(bs))
    >>> bitlist(list(fountains(4, 4*8, function=fun))).hex()
    '733a5900'
    >>> list(fountains(4, 4, function=fun, bits=[0,1,0,1]))
    [True, True, False, True]
    >>> fun = lambda bs: bitlist([1])
    >>> list(fountains(4, 4, function=fun, bits=[0,1,0,1]))
    [False, True, False, True]
    >>> fun = lambda bs: ['this is a list']
    >>> list(fountains(1, 1, function=fun, bits=[1]))
    Traceback (most recent call last):
      ...
    ValueError: test output must be a bytes-like object or bitlist
    """

    def __init__(
            self,
            length=1,
            limit=None,
            seed=bytes(0),
            bits=None,
            function=None
        ):
        self.length = length
        self.limit = limit
        self.count = 0
        self.bit_ = 0

        if isinstance(seed, int):
            if seed < 0:
                raise ValueError("integer seed must be non-negative")
            self.state = seed.to_bytes(int(log2(seed+1)) // 8, 'little')
        elif isinstance(seed, str):
            self.state = str.encode(seed)
        elif isinstance(seed, (bytes, bytearray)):
            self.state = seed
        else:
            raise ValueError("seed must be of type int, str, bytes, or bytearray")

        if bits is None:
            self.bits = None
        elif isinstance(bits, (bytes, bytearray)):
            self.bits = bitlist(bits)
            self.limit = len(self.bits) # Only enough data for target bits.
        elif isinstance(bits, list) and all(isinstance(n, int) for n in bits):
            self.bits = bitlist(bits)
            self.limit = len(self.bits) # Only enough data for target bits.
        elif isinstance(bits, str) and all(c in string.hexdigits for c in bits):
            self.bits = bitlist.fromhex(bits)
            self.limit = len(self.bits) # Only enough data for target bits.
        else:
            raise ValueError(
                "target bits must be of type int, str of hexdigits, bytes, " +
                "bytearray, or list of integers in the range [0, 1]"
            )

        self.function = function

    def bit(self, bs):
        """Obtain the next bit from the output."""
        if isinstance(bs, (bytes, bytearray)):
            bs = bitlist(bs)
        if not isinstance(bs, bitlist):
            raise ValueError("test output must be a bytes-like object or bitlist")

        # Reset the bit counter if the output is too short.
        self.bit_ = self.bit_ if self.bit_ < len(bs) else 0

        return bs[self.bit_]

    def __iter__(self):
        while self.limit is None or self.count < self.limit:
            bs = bytearray()
            while len(bs) < self.length:
                bs_ = sha256(self.state).digest()
                bs.extend(bs_[:16])
                self.state = bs_[16:]

            if self.function is not None and self.bits is None:
                # Return the output bits of the function on the
                # generated test inputs, one at a time.
                yield self.bit(self.function(bs[:self.length]))
            elif self.function is not None and self.bits is not None:
                # Return whether the function has the correct bit
                # in its output for this generated input.
                yield\
                    self.bits[self.count] ==\
                        self.bit(self.function(bs[:self.length]))
            elif self.function is None and self.bits is not None:
                # If a target bit sequence has been supplied
                # but no function has been supplied, return a
                # function that checks an output for that bit.
                yield (
                    bs[:self.length],
                    lambda bs:\
                        self.bit(bs) == self.bits[self.count]
                )
            else:
                # Return the generated test input.
                yield bs[:self.length]

            self.count += 1
            self.bit_ += 1

if __name__ == "__main__":
    doctest.testmod()
