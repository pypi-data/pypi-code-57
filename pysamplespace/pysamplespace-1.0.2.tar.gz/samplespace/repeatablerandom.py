"""Allows for generating generate repeatable, deterministic
random sequences."""

from base64 import standard_b64encode, standard_b64decode
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from itertools import accumulate
from math import ceil, log, sqrt, exp, cos, sin, acos, pi as PI, e as E
from typing import Optional, Sequence, Tuple, Any

import xxhash

from .algorithms import sample_discrete_roulette

__all__ = [
    'RepeatableRandomSequence',
    'RepeatableRandomSequenceState'
]

TWO_PI = 6.283185307179586  # 2 * pi
LOG_4 = 1.3862943611198906  # log(4)
GAMMA_MAGIC = 2.504077396776274  # 1.0 + log(4.5)
CONV_53BIT_TO_FLOAT = 1.1102230246251565e-16  # 2^-53


def _no_cascade(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        if self._cascading:
            raise RuntimeError('Operation forbidden while cascading.')
        return method(self, *method_args, **method_kwargs)

    return _impl


@dataclass
class RepeatableRandomSequenceState:
    """An object representing a :class:`RepeatableRandomSequence`'s
    internal state."""
    _seed: Any
    _hash_input: bytes
    _index: int

    def as_dict(self):
        """Return the sequence state as a dictionary for serialization."""
        return {
            'seed': self._seed,
            'hash_input': standard_b64encode(self._hash_input).decode('ascii'),
            'index': self._index
        }

    @classmethod
    def from_dict(cls, as_dict):
        """Construct a new sequence state from a dictionary, as
        returned by :meth:`as_dict`.

        Examples:

            >>> rrs = RepeatableRandomSequence()
            >>>
            >>> state_as_dict = rrs.getstate().as_dict()
            >>> state_as_dict
            {'seed': 0, 'hash_input': 'NMlqzcrbG7s=', 'index': 0}
            >>>
            >>> new_state = RepeatableRandomSequenceState.from_dict(state_as_dict)
            >>> rrs.setstate(new_state)

        """
        return cls(
            _seed=as_dict['seed'],
            _hash_input=standard_b64decode(as_dict['hash_input']),
            _index=as_dict['index'])

    def __repr__(self):
        return f'<{self.__class__.__name__}: ' \
            f'{repr(self._seed)}, {repr(self._index)}>'


class RepeatableRandomSequence(object):
    """A deterministic and repeatable random number generator compatible
    with Python's builtin :mod:`random` module.

    Args:
        seed (int, str, bytes, bytearray): The sequence's initial seed.
            See the :meth:`seed()` method below for more details.
    """

    BLOCK_SIZE_BITS: int = 64
    """The number of bits generated for each unique index."""

    BLOCK_MASK: int = 0xFFFFFFFFFFFFFFFF
    """A bitmask corresponding to ``(1 << BLOCK_SIZE_BITS) - 1``"""

    _MAX_ITERATIONS: int = 1024

    __slots__ = ('_seed', '_hash_input', '_index', '_cascading')

    def __init__(self, seed=None):
        self._seed = None
        self._hash_input: bytes = None
        self._index: int = 0
        self._cascading: int = 0
        self.seed(seed)

    @_no_cascade
    def seed(self, value=None) -> None:
        """Re-initialize the random generator with a new seed. Resets
        the sequence to its first value.

        Caution:
            This method cannot be called from within :meth:`cascade`,
            and will raise a :class:`RuntimeError` if attempted.

        Args:
            value (int, str, bytes, bytearray): The value to seed with.
                If this is a sequence type, the sequence is first hashed
                with seed 0.

        Raises:
            ValueError: If the seed value is not a supported type.
        """
        if value is None:
            value = 0

        self._seed = value
        if isinstance(value, int):
            # Convert int to at least 8 bytes, then hash them with
            # seed 0 to find the sequence's hash input.
            num_bytes = max(8, (value.bit_length() + 7) // 8)
            self._hash_input = xxhash.xxh64_digest(
                value.to_bytes(num_bytes, 'big'), seed=0)
        elif isinstance(value, (str, bytes, bytearray)):
            if isinstance(value, str):
                value = value.encode()
            # Hash the input with seed 0.
            self._hash_input = xxhash.xxh64_digest(value, seed=0)
        else:
            raise ValueError('Seed must be an int, str, bytes, or bytearray.')

        self.reset()

    def getseed(self):
        """Returns: the original value passed to
         :meth:`RepeatableRandomSequence` or :meth:`seed`."""
        return self._seed

    @property
    @_no_cascade
    def index(self) -> int:
        """int: The sequence's current index. Generating random values
        will always increase the index.

        Tip:
            Prefer :meth:`getstate()` and :meth:`setstate()` over index
            manipulation when saving and restoring state.

        Caution:
            The index cannot be read or written within :meth:`cascade`,
            and will raise a :class:`RuntimeError` if attempted."""
        return self._index

    @index.setter
    @_no_cascade
    def index(self, value: int):
        self._index = value

    @_no_cascade
    def reset(self) -> None:
        """Reset the sequence to the beginning, setting
        :attr:`index` to 0.

        Caution:
            This method cannot be called from within :meth:`cascade`,
            and will raise a :class:`RuntimeError` if attempted."""
        self._index = 0

    @contextmanager
    def cascade(self):
        """Returns a context manager that defines a generation cascade.

        Cascades are not required for most applications, but may be
        useful for certain advanced procedural generation techniques.

        A cascade allows multiple random samples to be treated as part
        the same logical unit.

        For example, generating a random position in space can be
        treated as a single "transaction" by grouping the fields into
        a single cascade::

            >>> print(rrs.index)
            10
            >>> with rrs.cascade():
            ...     x = rrs.random()  # index is 10
            ...     y = rrs.random()  # index is the previously-generated random block
            ...     z = rrs.random()  # index is the previously generated random block
            ...
            >>> print(rrs.index)
            11

        The use of cascades ensure that random values are repeatable and
        based only on the number of previously-generated values, not the
        type of the values themselves. This is often useful when
        creating procedurally-generated content using pre-defined seeds.

        While cascading, subsequent calls to
        random generation functions use the result of the most recently
        generated random data rather than incrementing the index.
        When a cascade completes, the index is set to one more than the
        index when the cascade began.
        """
        start_index = self._index
        self._cascading += 1
        try:
            yield self
        except Exception:
            self._index = start_index
            raise
        finally:
            self._cascading -= 1

        if not self._cascading:
            self._index = start_index + 1

    @_no_cascade
    def getstate(self) -> RepeatableRandomSequenceState:
        """Returns an opaque object representing the sequence's current
        state, used for saving, restoring, and serializing
        the sequence. This object can be passed to :meth:`setstate()`
        to restore the sequence's state."""
        return RepeatableRandomSequenceState(
            _seed=self._seed,
            _hash_input=self._hash_input,
            _index=self._index
        )

    # noinspection PyProtectedMember
    @_no_cascade
    def setstate(self, state: RepeatableRandomSequenceState) -> None:
        """Restore the sequence's state from previous call to
        :meth:`getstate()`."""
        self._seed = state._seed
        self._hash_input = state._hash_input
        self._index = state._index

    # ---- Integer Methods ----

    def getnextblock(self) -> int:
        """Get a block of random bits from the random generator.

        Tip:
            Calling this method will advance the sequence exactly one
            time. The resulting index depends on whether or not the
            call occurs within a cascade.

        Returns:
            A block of :attr:`BLOCK_SIZE_BITS` random bits as an int
        """
        # Note that the current index is used as the hash seed, and
        # the hash input (generated by hashing the sequence's seed)
        # remains constant over the run of the sequence. This greatly
        # simplifies index generation across platforms, and, based on
        # testing, has no adverse effects on value distribution.
        result = xxhash.xxh64_intdigest(self._hash_input, self._index)
        if self._cascading:
            # Normally, the index is incremented after each block.
            # When cascading, generated blocks are fed forward to use
            # in subsequent blocks; hence, single indices cascade across
            # multiple calls to getnextblock().
            self._index = result
        else:
            self._index += 1
        return result

    def getrandbits(self, k: int) -> int:
        """Generate an int with `k` random bits.

        This method may call :meth:`getnextblock()` multiple times if
        `k` is greater than :attr:`BLOCK_SIZE_BITS`; regardless of
        the number of calls, the index will only advance once.

        Tip:
            Note that ``k == 0`` is a valid input, which will advance
            the sequence even though no elements are chosen.

        Args:
            k (int): The number of random bits to generate.

        Returns:
            A random integer in [0, ``max(2^k, 1)``)
        """
        if k <= 0:
            self._index += 1
            return 0

        # Only one block is needed
        if k <= self.BLOCK_SIZE_BITS:
            block = self.getnextblock()
            if k == self.BLOCK_SIZE_BITS:
                return block
            return block >> (self.BLOCK_SIZE_BITS - k)

        # Multiple blocks required to produce enough bits
        result: int = 0
        with self.cascade():
            while k > 0:
                block = self.getnextblock()
                if k >= self.BLOCK_SIZE_BITS:
                    result = (result << self.BLOCK_SIZE_BITS) | block
                    k -= self.BLOCK_SIZE_BITS
                else:
                    result = \
                        (result << k) | \
                        block >> (self.BLOCK_SIZE_BITS - k)
                    k = 0

        return result

    def randrange(self,
                  start: int,
                  stop: Optional[int] = None,
                  step: int = 1) -> int:
        """Generate a random integer from
        ``range(start[, stop][, step]).``

        If only one argument is provided, samples from ``range(start)``.

        Args:
            start (int): The starting point for the range, inclusive.
                If `stop` is ``None``, this becomes the endpoint for
                the range, exclusive. None `None`
            stop (int, optional): The end point for the range, exclusive.
            step (int, default 1): Steps between possible values.
                May not be 0.

        Raises:
            TypeError: if any arguments are not integral.
            ValueError: if step is 0
        """
        if start != int(start):
            raise TypeError('Arguments to randrange() must be integers.')

        # randrange(N) case
        if stop is None:
            if start > 0:
                return self._randbelow(start)
            else:
                self._index += 1
                return 0

        # randrange(N, M) case
        if stop != int(stop):
            raise TypeError('Arguments to randrange() must be integers.')
        _range = stop - start
        if step == 1:
            return start + self._randbelow(_range)

        # randrange(N, M, S) case
        if step != int(step):
            raise TypeError('Arguments to randrange() must be integers.')

        if step > 0:
            _range = (_range + step - 1) // step
        elif step < 0:
            _range = (_range + step + 1) // step
        else:
            raise ValueError('Step argument to randrange() may not be 0.')

        return start + step * self._randbelow(_range)

    def randint(self, a: int, b: int) -> int:
        """Generate a random integer in the range [`a`, `b`].

        This is an alias for ``randrange(a, b + 1)``, included for
        compatibility with the builtin :mod:`random` module."""
        return self.randrange(a, b + 1)

    def randbytes(self, num_bytes) -> bytes:
        """Generate a sequence of random bytes.

        The index will only increment once, regardless of the number of
        bytes in the sequence.

        This method produces similar results to ::

            with rrs.cascade():
                result = bytes([rrs.randrange(256) for _ in range(num_bytes])

        but offers significantly-improved performance and does not
        discard excess random bits.

        Returns:
            A :class:`bytes` object with `num_bytes` random
            integers in [0, 255].
        """
        random = 0
        available_bits = 0
        result = [0] * num_bytes
        with self.cascade():
            for i in range(num_bytes):
                if available_bits < 8:
                    random = \
                        (random << self.BLOCK_SIZE_BITS) | \
                        self.getnextblock()
                    available_bits += self.BLOCK_SIZE_BITS
                result[i] = random & 0xFF
                random >>= 8
                available_bits -= 8
        return bytes(result)

    def geometric(self, mean: float, include_zero: bool = False) -> int:
        r"""Generate integers according to a geometric distribution.

        If `include_zero` is ``False``, returns integers from
        1 to infinity according to
        :math:`\text{Pr}(x = k) = p {(1 - p)}^{k - 1}` where
        :math:`p = \frac{1}{\mathit{mean}}`.

        If `include_zero` is ``True``, returns integers from
        0 to infinity according to
        :math:`\text{Pr}(x = k) = p {(1 - p)}^{k}` where
        :math:`p = \frac{1}{\mathit{mean} + 1}`.

        Args:
            mean (float): The desired mean value.
            include_zero (bool): Whether or not the distribution's
                support includes zero.

        Raises:
            ValueError: if `mean` is less than 1 if `include_zero`
                is ``False``, or less than 0 if `include_zero`
                is ``True``.
        """
        if include_zero:
            if mean < 0.0:
                raise ValueError('Mean must be at least 0.')
            p = 1.0 / (mean + 1.0)
        else:
            if mean < 1.0:
                raise ValueError('Mean must be at least 1.')
            p = 1.0 / mean

        if p == 1.0:
            self._index += 1
            return 0 if include_zero else 1

        # Sample from inverse CDF
        result = int(ceil(log(1.0 - self.random(), 1.0 - p)))
        if include_zero:
            result -= 1
        return result

    def finitegeometric(self, s: float, n: int):
        r"""Generate a random integer according to a geometric-like
        distribution with exponent `s` and finite
        support {1, ..., `n`}.

        The finite geometric distribution is defined by the equation

        .. math::

            \text{Pr}(x=k) = \frac{s^{k}}{\sum_{i=1}^{N} s^{i}}

        Raises:
            ValueError: if n is not at least 1
        """

        if n < 1:
            raise ValueError('n must be at least 1')

        cum_weights = list(accumulate(s ** i for i in range(n)))
        return sample_discrete_roulette(self.random, cum_weights) + 1

    def zipfmandelbrot(self, s: float, q: float, n: int):
        r"""Generate a random integer according to a Zipf-Mandelbrot
        distribution with exponent `s`, offset `q`, and
        support {1, ..., `n`}.

        The Zipf-Mandelbrot distribution is defined by the equation

        .. math::

            \text{Pr}(x=k) = \frac{(k + q)^{-s}}{\sum_{i=1}^{N} (i+q)^{-s}}

        Raises:
            ValueError: if n is not at least 1

        """

        if n < 1:
            raise ValueError('n must be at least 1')

        cum_weights = list(accumulate((i + q) ** (-s) for i in range(1, n + 1)))
        return sample_discrete_roulette(self.random, cum_weights) + 1

    # ---- Categorical Methods ----

    def choice(self, sequence: Sequence):
        """Choose a single random element from within a sequence.

        Raises:
            IndexError: if the sequence is empty.
        """
        length = len(sequence)
        if length == 0:
            raise IndexError('Sequence must have at least one element.')

        return sequence[self._randbelow(length)]

    def shuffle(self, sequence: Sequence) -> None:
        """Shuffle a sequence in place.

        The index is only incremented once."""
        # Fisher–Yates shuffle
        with self.cascade():
            for i in reversed(range(1, len(sequence))):
                j = self._randbelow(i + 1)
                sequence[i], sequence[j] = sequence[j], sequence[i]

    def sample(self, population, k: int) -> Sequence:
        """Choose `k` unique random elements from a population,
        **without** replacement.

        Elements are returned in selection order, so all subsets of the
        returned list are valid samples.

        If the population includes duplicate values, each occurrence is
        as distinct possible selection in the result.

        Tip:
            Note that ``k == 0`` is a valid input, which returns an empty
            list an advances the sequence once even though no
            elements are chosen.

        Args:
            population (list, tuple, set, range): The source population.
            k (int): The number of samples to choose, no more than the
                total number of elements in population.

        Raises:
            IndexError: if population is empty.
            ValueError: if `k` is greater than the population size.
        """
        # Implementation adapted from Python's standard library
        if k <= 0:
            self._index += 1
            return []

        if isinstance(population, set):
            population = tuple(population)

        length = len(population)
        if length == 0:
            raise IndexError('Sequence must have at least one element')

        if k > length:
            raise ValueError('k must be at least 0 and '
                             'at most the population size.')

        result = [None] * k

        # Size of a small set, less the size of an empty list
        setsize = 21
        if k > 5:
            # Table size for big sets
            setsize += 4 ** ceil(log(k * 3, 4))

        if length <= setsize:
            # Track potential selections in a list
            pool = list(population)
            with self.cascade():
                for i in range(k):
                    j = self._randbelow(length - i)
                    result[i] = pool[j]
                    pool[j] = pool[length - i - 1]
        else:
            # Track prior selections in a set
            selected = set()
            with self.cascade():
                for i in range(k):
                    j = self._randbelow(length)
                    for _ in range(self._MAX_ITERATIONS):
                        if j not in selected:
                            break
                        j = self._randbelow(length)
                    else:
                        raise RuntimeError('Could not make a random '
                                           'selection within limit.')
                    selected.add(j)
                    result[i] = population[j]

        return result

    def choices(self,
                population: Sequence,
                weights: Optional[Sequence[float]] = None, *,
                cum_weights: Optional[Sequence[float]] = None,
                k: int = 1) -> Sequence:
        """Choose `k` elements from a population, **with** replacement.

        Either relative (via `weights`) or cumulative (via
        `cum_weights`) weights may be specified. If no weights are
        specified, selections are made uniformly with equal probability.

        Tip:
            Note that ``k == 0`` is a valid input, which returns an
            empty list an advances the sequence once even though no
            elements are chosen.

        Args:
            population (sequence): The population to sample from, which
                may include duplicate elements.
            weights (sequence[float], optional): Relative weights for
                each element in the population. Need not sum to 1.
            cum_weights (sequence[float], optional): Cumulative weights
                for each element in the population, as calculated by
                something like ``list(accumulate(weights))``.
            k (int): The number of elements to choose.

        Raises:
            IndexError: The population is empty.
            ValueError: The length of `weights` or `cum_weights` does
                not match the population size.
            TypeError: Both `weights` and `cum_weights` are specified.
        """
        if k <= 0:
            self._index += 1
            return []

        pop_size = len(population)
        if pop_size == 0:
            raise IndexError('Population must have at least one element.')

        if cum_weights is None:
            if weights is None:
                # Use uniform distribution if no weights are given
                with self.cascade():
                    result = [population[self._randbelow(pop_size)]
                              for _ in range(k)]
                return result

            cum_weights = list(accumulate(weights))
        elif weights is not None:
            raise TypeError('Cannot specify both weights and '
                            'cumulative weights.')

        if len(cum_weights) != pop_size:
            raise ValueError('The number of weights must match '
                             'the population size.')

        if pop_size == 1:
            self._index += 1
            return [population[0]] * k

        # Sample from a PMF using a roulette wheel binary search.
        # N.B. Alias tables were tested as well, but table generation
        # time greatly sampling speedup.
        with self.cascade():
            result = [population[
                          sample_discrete_roulette(self.random, cum_weights)]
                      for _ in range(k)]
        return result

    # ---- Float Methods ----

    def random(self) -> float:
        """Return a random float in [0.0, 1.0)."""
        # N.B. This explicitly depends on the block size being 64.
        # No assertions are included since this is performance-critical.
        return self._64bits_to_float(self.getnextblock())

    def uniform(self, a: float, b: float) -> float:
        """Return a random float uniformly distributed in [`a`, `b`)."""
        return a + (b - a) * self.random()

    def triangular(self,
                   low: float = 0.0,
                   high: float = 1.0,
                   mode: Optional[float] = None) -> float:
        r"""Sample from a triangular distribution with lower limit `low`,
        upper limit `low`, and mode `mode`.

        The triangular distribution is defined by

        .. math::

            \text{P}(x) =
            \begin{cases}
            0 & \text{for } x \lt l, \\
            \frac{2(x-l)}{(h-l)(m-l)} &
            \text{for }l\le x \lt h, \\
            \frac{2}{h-l} &
            \text{for } x = m, \\
            \frac{2(h-x)}{(h-l)(h-m)} &
            \text{for } m \lt x \le h, \\
            0 & \text{for } h \lt x
            \end{cases}

        Raises:
            ValueError: if the mode is not in [`low`, `high`].
        """
        if mode is None:
            if not low <= high:
                raise ValueError('Mode must be between low and high ranges.')

            c = 0.5
        else:
            if not low <= mode <= high:
                raise ValueError('Mode must be between low and high ranges.')

            try:
                c = 0.5 if mode is None else (mode - low) / (high - low)
            except ZeroDivisionError:
                self._index += 1
                return low

        # Implementation adapted from Python's standard library
        u = self.random()
        if u > c:
            u = 1.0 - u
            c = 1.0 - c
            low, high = high, low
        return low + (high - low) * sqrt(u * c)

    def chance(self, p: float) -> bool:
        """Returns ``True`` with probability `p`, else ``False``.

        Alias for ``random() < p``."""
        return self.random() < p

    def normalvariate(self, mu: float, sigma: float) -> float:
        """Sample from a normal distribution with mean `mu` and
        standard variation `sigma`.

        Note:
            Unlike :func:`random.normalvariate`, this is an alias for
            `gauss(mu, sigma)`. It is included for compatibility with
            the built-in :mod:`random` module."""
        return self.gauss(mu, sigma)

    def lognormvariate(self, mu: float, sigma: float) -> float:
        r"""Sample from a log-normal distribution with parameters
        `mu` and `sigma`.

        The logarithms of values sampled from a log-normal
        distribution are normally distributed with mean `mu` and
        standard deviation `sigma`. The distribution is defined by

        .. math::

            \text{P}(x) = \frac{1}{x \sigma \sqrt{2 \pi}}
            \exp{\left(- \frac{(\ln{x} - \mu)^2}{2 \sigma ^2}\right)}
        """
        return exp(self.normalvariate(mu, sigma))

    def expovariate(self, lambd: float) -> float:
        r"""Sample from an exponential distribution with rate `lambd`.

        The probability density function for the exponential
        distribution is defined by
        :math:`\text{P}(x)= \lambda e^{-\lambda x}` where :math:`x\ge 0`"""
        # 1.0 - random() is here used to prevent taking the log of 0.0
        return -log(1.0 - self.random()) / lambd

    def vonmisesvariate(self, mu: float, kappa: float) -> float:
        r"""Sample from a von Mises distribution with
        parameters `mu` and `kappa`.

        Samples from a von Mises distribution represent randomly-chosen
        angles clustered around a mean angle. This distribution is an
        approximation to the wrapped normal distribution and is
        defined by

        .. math::

            \text{P}(x) = \frac{e^{\kappa \cos{(x - \mu)}}}{2 \pi I_0(\kappa)}

        where :math:`I_0(\kappa)` is the modified Bessel function
        of order 0.

        Args:
            mu (float): The mean angle, in radians, around which to
                cluster.
            kappa (float): The concentration parameter, which must be
                at least 0.

        Returns:
            An angle in radians within [0, `2 pi`)
        """
        # Implementation adapted from Python's standard library
        if kappa <= 1e-6:
            return TWO_PI * self.random()

        s = 0.5 / kappa
        r = s + sqrt(1.0 + s * s)
        with self.cascade():
            b = self.getnextblock() < (self.BLOCK_MASK >> 1)
            for _ in range(self._MAX_ITERATIONS):
                u1 = self.random()
                u2 = self.random()

                candidate_z = cos(PI * u1)
                d = candidate_z / (r + candidate_z)
                if (u2 < 1.0 - d * d) or (u2 <= (1.0 - d) * exp(d)):
                    z = candidate_z
                    break
            else:
                raise RuntimeError('Could not make a random '
                                   'selection within limit.')

        q = 1.0 / r
        f = (q + z) / (1.0 + q * z)
        theta = mu + acos(f) * (-1.0 if b else 1.0)
        return theta % TWO_PI

    def gammavariate(self, alpha: float, beta: float) -> float:
        r"""Sample from a gamma distribution with parameters `alpha`
        and `beta`. Not to be confused with :func:`math.gamma`!

        The gamma distribution is defined as

        .. math::

            \text{P}(x) = \frac{x^{\alpha - 1} e^{-\frac{x}{\beta}}}
            {\Gamma(\alpha) \beta^{\alpha}}

        Caution:
            This implementation defines its parameters to match
            :func:`random.gammavariate`. The parametrization differs
            from most common definitions of the gamma distribution,
            as defined on Wikipedia, et al. Take care when setting
            `alpha` and `beta`!

        Raises:
            ValueError: if either `alpha` or `beta` is not greater than 0.
        """
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError('alpha and beta must be greater than 0.')

        if alpha > 1.0:
            ainv = sqrt(2.0 * alpha - 1.0)
            b = alpha - LOG_4
            c = alpha + ainv

            with self.cascade():
                for _ in range(self._MAX_ITERATIONS):
                    u1 = self.random()
                    if (u1 < 1e-7) or (u1 > 0.9999999):
                        continue
                    u2 = 1.0 - self.random()

                    v = log(u1 / (1.0 - u1)) / ainv
                    x = alpha * exp(v)
                    z = u1 * u1 * u2
                    r = b + c * v - x
                    if (r + GAMMA_MAGIC - 4.5 * z >= 0.0) or \
                            (r >= log(z)):
                        result = x * beta
                        break
                else:
                    raise RuntimeError('Could not make a random '
                                       'selection within limit.')
        elif alpha == 1.0:
            result = -log(1.0 - self.random()) * beta
        else:
            # Alpha in (0.0, 1.0)
            with self.cascade():
                for _ in range(self._MAX_ITERATIONS):
                    u1 = self.random()
                    u2 = self.random()

                    b = (E + alpha) / E
                    p = b * u1
                    if p <= 1.0:
                        x = p ** (1.0 / alpha)
                        if u2 <= exp(-x):
                            result = x * beta
                            break
                    else:
                        x = -log((b - p) / alpha)
                        if u2 <= x ** (alpha - 1.0):
                            result = x * beta
                            break
                else:
                    raise RuntimeError('Could not make a random '
                                       'selection within limit.')

        return result

    def gauss(self, mu: float, sigma: float) -> float:
        r"""Sample from a Gaussian distribution with parameters
        `mu` and `sigma`.

        The Gaussian, or Normal distribution is defined by

        .. math::

            \text{P}(x) = \frac{1}{\sigma \sqrt{2 \pi}}
            e^{-\frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^2}

        Tip:
            If multiple normally-distributed values are required,
            consider using :meth:`gausspair` for improved performance.
        """
        a, b = self._gauss_impl()
        return mu + cos(a) * b * sigma

    def gausspair(self, mu: float, sigma: float) -> Tuple[float, float]:
        """Return a pair of *independent* samples from a Gaussian
        distribution with parameters `mu` and `sigma`.

        This method produces similar results to ::

            with rrs.cascade():
                result = rrs.gauss(mu, sigma), rrs.gauss(mu, sigma)

        but offers improved performance."""
        a, b = self._gauss_impl()
        return (mu + cos(a) * b * sigma,
                mu + sin(a) * b * sigma)

    def betavariate(self, alpha: float, beta: float) -> float:
        r"""Sample from a beta distribution with parameters `alpha`
        and `beta`.

        The beta distribution is defined by

        .. math::

            \text{P}(x) = x^{\alpha - 1} (1 - x)^{\beta - 1}
            \frac{\Gamma(\alpha + \beta)}{\Gamma(\alpha)\Gamma(\beta)}

        Returns:
            A random, beta-distributed value in [0.0, 1.0]

        Raises:
            ValueError: if either alpha or beta is not greater than 0.
        """
        #  N.B. This isn't affected by random.gammavariate's uncommon
        # parametrization, because beta=1 produces the same result as
        # the standard definition.
        with self.cascade():
            y = self.gammavariate(alpha, 1.0)
            if y == 0.0:
                return 0.0
            else:
                return y / (y + self.gammavariate(beta, 1.0))

    def paretovariate(self, alpha: float) -> float:
        r"""Sample from a Pareto distribution with shape
        parameter `alpha` and minimum value 1.

        The Pareto distribution has PDF

        .. math::

            \text{P}(x) = \frac{\alpha}{x^{\alpha + 1}}

        Raises:
            ValueError: if `alpha` is zero.
        """

        if alpha == 0.0:
            raise ValueError('Alpha must not be 0.')

        u = 1.0 - self.random()
        return u ** (-1.0 / alpha)

    def weibullvariate(self, alpha: float, beta: float) -> float:
        r"""Sample from a Weibull distribution with scale
        parameter `alpha` and shape parameter `beta`.

        The distribution is defined by

        .. math::

            \text{P}(x) = \frac{\beta}{\alpha}
            \left(\frac{x}{\alpha}\right)^{k-1}
            e^{-(x/\alpha)^k}

        where :math:`x \ge 0`.

        Raises:
            ValueError: if `alpha` is zero.
        """
        if beta == 0.0:
            raise ValueError('Beta must not be 0.')

        u = 1.0 - self.random()
        return alpha * (-log(u)) ** (1.0 / beta)

    # ---- Internal ----

    def _randbelow(self, limit: int) -> int:
        """Return an int in the range [0, `limit`).

         Raises:
             ValueError: if `limit` is not greater than 0.
             TypeError: if `limit` is not an integer.
         """
        if limit <= 0:
            raise ValueError('Limit must be greater than 0.')

        if limit != int(limit):
            raise TypeError('Limit must be an integer.')
        limit = int(limit)

        # Implementation based on MSVC standard library.
        # Supports limits greater than _BLOCK_SIZE_BITS bits long
        with self.cascade():
            for i in range(self._MAX_ITERATIONS):
                result = 0
                mask = 0
                while mask < limit - 1:
                    result = \
                        (result << self.BLOCK_SIZE_BITS) | \
                        self.getnextblock()
                    mask = \
                        (mask << self.BLOCK_SIZE_BITS) | \
                        self.BLOCK_MASK

                if (result // limit < mask // limit) or \
                        (mask % limit == limit - 1):
                    return result % limit
            else:
                raise RuntimeError('Could not make a random '
                                   'selection within limit.')

    def _gauss_impl(self) -> Tuple[float, float]:
        with self.cascade():
            a = self.random() * TWO_PI
            b = sqrt(-2.0 * log(1.0 - self.random()))
        return a, b

    @staticmethod
    def _64bits_to_float(value: int) -> float:
        # A double-precision float has 53 significant bits,
        # so chop off 11 from a 64 bit hash then rescale
        return (value >> 11) * CONV_53BIT_TO_FLOAT

    def __getstate__(self):
        return self.getstate()

    def __setstate__(self, state):
        self.setstate(state)

    def __reduce__(self):
        return self.__class__, (), self.getstate()
