"""Implements a number of useful probability distributions."""

import itertools
import math
from typing import Sequence, Tuple, Optional, Any, List, Dict

from .algorithms import sample_discrete_roulette

__all__ = [
    'Constant',
    'Uniform',
    'DiscreteUniform',
    'Geometric',
    'FiniteGeometric',
    'ZipfMandelbrot',
    'Gamma',
    'Triangular',
    'LogNormal',
    'Exponential',
    'VonMises',
    'Beta',
    'Pareto',
    'Weibull',
    'Gaussian',
    'Bernoulli',
    'WeightedCategorical',
    'UniformCategorical',
    'FiniteGeometricCategorical',
    'ZipfMandelbrotCategorical',
    'distribution_from_dict',
    'distribution_from_list'
]


class Distribution(object):

    def sample(self, rand):
        """Sample from the distribution.

        Args:
            rand: The random generator used to generate the sample.
        """
        raise NotImplementedError

    def as_list(self) -> List:
        """Return a representation of the distribution as a list.

        The first element if the list is the name of the distribution,
        and the subsequent elements are ordered parameters.
        """
        raise NotImplementedError

    def as_dict(self) -> Dict:
        """Return a representation of the distribution as a dict.

        The 'distribution' key is the name of the distribution, and
        the remaining keys are the distribution's kwargs."""
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __str__(self):
        return '<{}Distribution>'.format(self.__class__.__name__)

    def __repr__(self):
        return 'Distribution.from_list({})'.format(self.as_list())

    @classmethod
    def from_dict(cls, dist_as_dict):
        return distribution_from_dict(dist_as_dict)

    @classmethod
    def from_list(cls, dist_as_list):
        return distribution_from_list(dist_as_list)


class Constant(Distribution):
    """Represents a distribution that always returns a constant value."""

    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def value(self):
        """Read-only property for the distribution's constant value."""
        return self._value

    def sample(self, rand):
        # N.B. A random value is still generated and discarded in case
        # the generator is an indexed sequence that should advance
        # regardless of distribution type.
        rand.random()
        return self._value

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._value]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'value': self._value
        }


class Uniform(Distribution):
    r"""Represents a continuous uniform distribution with support
    [`min_val`, `max_val`).

    The uniform distribution is defined as

    .. math::

        \text{P}(x) =
        \begin{cases}
        \frac{1}{b - a} & \text{for } x \in [a, b) \\
        0 & \text{otherwise}
        \end{cases}
    """

    def __init__(self, min_val: float = 0.0, max_val: float = 1.0):
        super().__init__()
        self._min: float = min(min_val, max_val)
        self._max: float = max(min_val, max_val)

    @property
    def min_val(self) -> float:
        """Read-only property for the distribution's lower limit."""
        return self._min

    @property
    def max_val(self) -> float:
        """Read-only property for the distribution's upper limit."""
        return self._max

    def sample(self, rand) -> float:
        return rand.uniform(self._min, self._max)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._min, self._max]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'min_val': self._min,
            'max_val': self._max
        }


class DiscreteUniform(Distribution):
    """Represents a discrete uniform distribution of integers
    in [`min_value`, `max_value`)."""

    def __init__(self, min_val: int, max_val: int):
        super().__init__()
        self._min: int = min(min_val, max_val)
        self._max: int = max(min_val, max_val)

    @property
    def min_val(self) -> int:
        """Read-only property for the distribution's lower limit."""
        return self._min

    @property
    def max_val(self) -> int:
        """Read-only property for the distribution's upper limit."""
        return self._max

    def sample(self, rand) -> int:
        return rand.randrange(self._min, self._max)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._min, self._max]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'min_val': self._min,
            'max_val': self._max
        }


class Geometric(Distribution):
    r"""Represents a geometric distribution.

    If `include_zero` is ``False``, returns integers from
    1 to infinity according to
    :math:`\text{Pr}(x = k) = p {(1 - p)}^{k - 1}` where
    :math:`p = \frac{1}{\mathit{mean}}`.

    If `include_zero` is ``True``, returns integers from
    0 to infinity according to
    :math:`\text{Pr}(x = k) = p {(1 - p)}^{k}` where
    :math:`p = \frac{1}{\mathit{mean} + 1}`.
    """

    def __init__(self, mean: float, include_zero: bool = False):
        super().__init__()
        self._mean: float = mean
        self._include_zero: bool = include_zero

    @property
    def mean(self) -> float:
        """Read-only property for the distribution's mean."""
        return self._mean

    @property
    def include_zero(self) -> bool:
        """Read-only property for whether or not the distribution's
        support includes zero."""
        return self._include_zero

    def sample(self, rand) -> int:
        func = getattr(rand,
                       'geometric',
                       lambda *args: self._impl(rand, *args))
        return func(self._mean, self._include_zero)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._mean, self._include_zero]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'mean': self._mean,
            'include_zero': self._include_zero
        }

    @staticmethod
    def _impl(rand, mean, include_zero):
        if include_zero:
            if mean < 0.0:
                raise ValueError('Mean must be at least 0.')
            p = 1.0 / (mean + 1.0)
        else:
            if mean < 1.0:
                raise ValueError('Mean must be at least 1.')
            p = 1.0 / mean

        if p == 1.0:
            # N.B. A random value is still generated and discarded in case
            # the generator is an indexed sequence that should advance
            # regardless of distribution type.
            rand.random()
            return 0 if include_zero else 1

        # Sample from inverse CDF
        result = int(math.ceil(math.log(1.0 - rand.random(), 1.0 - p)))
        if include_zero:
            result -= 1
        return result


class FiniteGeometric(Distribution):
    r"""Represents a geometric-like distribution with exponent `s`
    and finite support {1, ..., `n`}.

    The finite geometric distribution is defined by the equation

    .. math::

        \text{Pr}(x=k) = \frac{s^{k}}{\sum_{i=1}^{N} s^{i}}

    The distribution is defined such that each result is `s` times
    as likely to occur as the previous; i.e.
    :math:`\text{Pr}(x=k) = s \text{Pr}(x=k-1)` over the support.
    """

    def __init__(self, s: float, n: int):
        super().__init__()
        assert n >= 1, 'n must be at least 1.'
        self._s: float = s
        self._n: int = n
        self._cum_weights = list(itertools.accumulate(
            math.pow(s, i) for i in range(n)))

    @property
    def s(self) -> float:
        """Read-only property for the distribution's `s` exponent."""
        return self._s

    @property
    def n(self) -> int:
        """Read-only property for the number of values in the
        distribution's support."""
        return self._n

    def sample(self, rand) -> int:
        return sample_discrete_roulette(
            rand.random, self._cum_weights) + 1

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._s, self._n]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            's': self._s,
            'n': self._n
        }


class ZipfMandelbrot(Distribution):
    r"""Represents a Zipf-Mandelbrot distribution with exponent `s`,
    offset `q`, and support {1, ..., `n`}.

    The Zipf-Mandelbrot distribution is defined by the equation

    .. math::

        \text{Pr}(x=k) = \frac{(k+q)^{-s}}{\sum_{i=1}^{N} (i+q)^{-s}}

    When ``q == 0``, the distribution becomes the Zipf distribution, and
    as `n` increases, it approaches the Zeta distribution.
    """

    def __init__(self, s: float, q: float, n: int):
        super().__init__()
        assert n >= 1, 'n must be at least 1.'
        self._s: float = s
        self._q: float = q
        self._n: int = n
        self._cum_weights = list(itertools.accumulate(
            math.pow(i + q, -s) for i in range(1, n + 1)))

    @property
    def s(self) -> float:
        """Read-only property for the distribution's `s` exponent."""
        return self._s

    @property
    def q(self) -> float:
        """Read-only property for the distribution's `q` offset."""
        return self._q

    @property
    def n(self) -> int:
        """Read-only property for the number of values in the
        distribution's support."""
        return self._n

    def sample(self, rand) -> int:
        return sample_discrete_roulette(
            rand.random, self._cum_weights) + 1

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._s, self._q, self._n]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            's': self._s,
            'q': self._q,
            'n': self._n
        }


class Gamma(Distribution):
    r"""Represents a gamma distribution with parameters `alpha`
    and `beta`.

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
    """

    def __init__(self, alpha: float, beta: float):
        super().__init__()
        self._alpha: float = alpha
        self._beta: float = beta

    @property
    def alpha(self) -> float:
        """Read-only property for the distribution's `alpha` parameter."""
        return self._alpha

    @property
    def beta(self) -> float:
        """Read-only property for the distribution's `beta` parameter."""
        return self._beta

    def sample(self, rand) -> float:
        return rand.gammavariate(self._alpha, self._beta)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._alpha, self._beta]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'alpha': self._alpha,
            'beta': self._beta
        }


class Triangular(Distribution):
    r"""Represents a triangular distribution with lower limit `low`,
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
    """

    def __init__(self,
                 low: float = 0.0,
                 high: float = 1.0,
                 mode: Optional[float] = None):
        self._low = low
        self._high = high
        self._mode = mode

    @property
    def low(self) -> float:
        """Read-only property for the distribution's lower bound."""
        return self._low

    @property
    def high(self) -> float:
        """Read-only property for the distribution's upper bound."""
        return self._high

    @property
    def mode(self) -> Optional[float]:
        """Read-only property for the distribution's mode, if specified,
        otherwise ``None``."""
        return self._mode

    def sample(self, rand) -> float:
        return rand.triangular(self._low, self._high, self._mode)

    def as_list(self) -> List:
        if self._mode is None:
            return [self.__class__.__name__.casefold(),
                    self._low, self._high]
        else:
            return [self.__class__.__name__.casefold(),
                    self._low, self._high, self._mode]

    def as_dict(self) -> Dict:
        result = {
            'distribution': self.__class__.__name__.casefold(),
            'low': self._low,
            'high': self._high
        }
        if self._mode is not None:
            result['mode'] = self._mode
        return result


class LogNormal(Distribution):
    r"""Represents a log-normal distribution with parameters
    `mu` and `sigma`.

    The logarithms of values sampled from a log-normal
    distribution are normally distributed with mean `mu` and
    standard deviation `sigma`. The distribution is defined by

    .. math::

        \text{P}(x) = \frac{1}{x \sigma \sqrt{2 \pi}}
        \exp{\left(- \frac{(\ln{x} - \mu)^2}{2 \sigma ^2}\right)}
    """

    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        self._mu = mu
        self._sigma = sigma

    @property
    def mu(self) -> float:
        """Read-only property for the distribution's `mu` parameter."""
        return self._mu

    @property
    def sigma(self) -> float:
        """Read-only property for the distribution's `sigma` parameter."""
        return self._sigma

    def sample(self, rand) -> float:
        return rand.lognormvariate(self._mu, self._sigma)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._mu, self._sigma]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'mu': self._mu,
            'sigma': self._sigma
        }


class Exponential(Distribution):
    r"""Represents an exponential distribution with rate `lambd`.

    The probability density function for the exponential
    distribution is defined by
    :math:`\text{P}(x)= \lambda e^{-\lambda x}` where :math:`x\ge 0`"""

    def __init__(self, lambd: float):
        self._lambda = lambd

    @property
    def lambd(self):
        """Read-only property for the distribution's rate parameter."""
        return self._lambda

    def sample(self, rand) -> float:
        return rand.expovariate(self._lambda)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._lambda]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'lambd': self._lambda
        }


class VonMises(Distribution):
    r"""Represents a von Mises distribution with
    parameters `mu` and `kappa`.

    Samples from a von Mises distribution represent randomly-chosen
    angles clustered around a mean angle. This distribution is an
    approximation to the wrapped normal distribution and is
    defined by

    .. math::

        \text{P}(x) = \frac{e^{\kappa \cos{(x - \mu)}}}{2 \pi I_0(\kappa)}

    where :math:`I_0(\kappa)` is the modified Bessel function
    of order 0.
    """

    def __init__(self, mu: float, kappa: float):
        self._mu = mu
        self._kappa = kappa

    @property
    def mu(self) -> float:
        """Read-only property for the distribution's `mu` parameter."""
        return self._mu

    @property
    def kappa(self) -> float:
        """Read-only property for the distribution's `kappa` parameter."""
        return self._kappa

    def sample(self, rand) -> float:
        return rand.vonmisesvariate(self._mu, self._kappa)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._mu, self._kappa]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'mu': self._mu,
            'kappa': self._kappa
        }


class Beta(Distribution):
    r"""Represents a beta distribution with parameters `alpha`
    and `beta`.

    The beta distribution is defined by

    .. math::

        \text{P}(x) = x^{\alpha - 1} (1 - x)^{\beta - 1}
        \frac{\Gamma(\alpha + \beta)}{\Gamma(\alpha)\Gamma(\beta)}
    """

    def __init__(self, alpha: float, beta: float):
        self._alpha = alpha
        self._beta = beta

    @property
    def alpha(self) -> float:
        """Read-only property for the distribution's `alpha` parameter."""
        return self._alpha

    @property
    def beta(self) -> float:
        """Read-only property for the distribution's `beta` parameter."""
        return self._beta

    def sample(self, rand) -> float:
        return rand.betavariate(self._alpha, self._beta)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._alpha, self._beta]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'alpha': self._alpha,
            'beta': self._beta
        }


class Pareto(Distribution):
    r"""Represents a Pareto distribution with shape
    parameter `alpha` and minimum value 1.

    The Pareto distribution has PDF

    .. math::

        \text{P}(x) = \frac{\alpha}{x^{\alpha + 1}}
    """

    def __init__(self, alpha: float):
        self._alpha = alpha

    @property
    def alpha(self) -> float:
        """Read-only property for the distribution's `alpha` parameter."""
        return self._alpha

    def sample(self, rand) -> float:
        return rand.paretovariate(self._alpha)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._alpha]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'alpha': self._alpha
        }


class Weibull(Distribution):
    r"""Represents a Weibull distribution with scale
    parameter `alpha` and shape parameter `beta`.

    The distribution is defined by

    .. math::

        \text{P}(x) = \frac{\beta}{\alpha}
        \left(\frac{x}{\alpha}\right)^{k-1}
        e^{-(x/\alpha)^k}

    where :math:`x \ge 0`.
    """

    def __init__(self, alpha: float, beta: float):
        self._alpha = alpha
        self._beta = beta

    @property
    def alpha(self) -> float:
        """Read-only property for the distribution's `alpha` parameter."""
        return self._alpha

    @property
    def beta(self) -> float:
        """Read-only property for the distribution's `beta` parameter."""
        return self._beta

    def sample(self, rand) -> float:
        return rand.weibullvariate(self._alpha, self._beta)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._alpha, self._beta]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'alpha': self._alpha,
            'beta': self._beta
        }


class Gaussian(Distribution):
    r"""Represents a Gaussian distribution with parameters
    `mu` and `sigma`.

    The Gaussian, or Normal distribution is defined by

    .. math::

        \text{P}(x) = \frac{1}{\sigma \sqrt{2 \pi}}
        e^{-\frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^2}
    """

    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        super().__init__()
        self._mu: float = mu
        self._sigma: float = sigma

    @property
    def mu(self) -> float:
        """Read-only property for the distribution's `mu` parameter."""
        return self._mu

    @property
    def sigma(self) -> float:
        """Read-only property for the distribution's `sigma` parameter."""
        return self._sigma

    def sample(self, rand):
        return rand.gauss(self._mu, self._sigma)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._mu, self._sigma]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'mu': self._mu,
            'sigma': self._sigma
        }


class Bernoulli(Distribution):
    """Represents a Bernoulli distribution with parameter `p`.

    Returns ``True`` with probability `p`, and ``False`` otherwise.
    """

    def __init__(self, p: float):
        super().__init__()
        self._p: float = p

    @property
    def p(self) -> float:
        """Read-only property for the distribution's `p` parameter."""
        return self._p

    def sample(self, rand) -> bool:
        return rand.random() < self._p

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._p]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'p': self._p,
        }


class WeightedCategorical(Distribution):
    """Represents a categorical distribution defined by a
    population and a list of relative weights.

    Either `items`, `population` and `weights`, or `population` and
    `cum_weights` should be provided, not all three.

    Args:
        items (Sequence[Tuple[Any]]): A sequence of tuples in
            the format (weight, relative value).
        population (Sequence): A sequence of possible values.
        weights (Sequence[float], optional): A sequence of
            relative weights corresponding to each item in the
            population. Must be the same length as the population list.
        cum_weights (Sequence[float], optional): A sequence of
            cumulative weights corresponding to each item in the
            population. Must be the same length as the population list.
            Only one of `weights` and `cum_weights` should be provided.
    """

    def __init__(self,
                 items: Optional[Sequence[Tuple[float, Any]]] = None,
                 population: Optional[Sequence] = None,
                 weights: Optional[Sequence[float]] = None, *,
                 cum_weights: Optional[Sequence[float]] = None):
        super().__init__()

        if items is not None:
            assert population is None \
                   and weights is None \
                   and cum_weights is None, \
                'Specify either items or population and weight.'
            population, weights = zip(*items)
        else:
            assert population is not None, 'Must specify population.'

        self._population: Sequence = list(population)

        if cum_weights is None:
            if weights is None:
                # Use uniform distribution if no weights are given
                self._cum_weights = \
                    [i + 1.0 for i in range(len(self._population))]
            else:
                self._cum_weights: Sequence[float] = \
                    list(itertools.accumulate(weights))
        else:
            assert weights is None, \
                'Cannot specify both  weights and cumulative weights.'
            self._cum_weights = list(cum_weights)

        assert len(self._cum_weights) == len(self._population), \
            'Population and weights must have the same number of elements.'

    @property
    def population(self) -> Sequence:
        """A read-only property for the distribution's population."""
        return self._population

    @property
    def cum_weights(self) -> Sequence[float]:
        """A read-only property for the distribution's cumulative
        weights."""
        return self._cum_weights

    @property
    def items(self) -> Sequence[Tuple]:
        """A read-only property returning a sequence of tuples in
        the format (weight, relative value)."""
        weights = [self._cum_weights[i] -
                   (self._cum_weights[i - 1] if i > 0 else 0.0)
                   for i in range(len(self._cum_weights))]
        return [(item, weight)
                for item, weight in zip(self._population, weights)]

    def sample(self, rand):
        return self.samples(rand, 1)[0]

    def samples(self, rand, k: int) -> Sequence:
        return rand.choices(self._population,
                            cum_weights=self._cum_weights,
                            k=k)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(), self.items]

    def as_dict(self) -> Dict:
        items = [list(x) for x in self.items]
        return {
            'distribution': self.__class__.__name__.casefold(),
            'items': items
        }


class UniformCategorical(Distribution):
    """Represents a uniform categorical distribution over a
    given population."""

    def __init__(self, population: Sequence):
        super().__init__()
        self._population = list(population)

    @property
    def population(self) -> Sequence:
        """A read-only property for the distribution's population."""
        return self._population

    def sample(self, rand):
        return rand.choice(self._population)

    def samples(self, rand, k: int) -> Sequence:
        return rand.choices(self._population, k=k)

    def samples_unique(self, rand, k: int) -> List[Any]:
        return rand.sample(self._population, k=k)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._population]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'population': self._population
        }


class FiniteGeometricCategorical(WeightedCategorical):
    r"""Represents a categorical distribution with weights
    corresponding to a finite geometric-like distribution with
    exponent `s`.

    The finite geometric distribution is defined by the equation

    .. math::

        \text{Pr}(x=k) = \frac{s^{k}}{\sum_{i=1}^{N} s^{i}}

    The distribution is defined such that each result is `s` times
    as likely to occur as the previous; i.e.
    :math:`\text{Pr}(x=k) = s \text{Pr}(x=k-1)` over the support.
    """

    def __init__(self, population: Sequence, s: float):
        self._s: float = s
        weights = [math.pow(s, i) for i in range(len(population))]
        super().__init__(population=population, weights=weights)

    @property
    def s(self) -> float:
        """Read-only property for the distribution's `s` exponent."""
        return self._s

    @property
    def n(self) -> int:
        """Read-only property for the number of values in the
        distribution's support."""
        return len(self._population)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._population, self._s]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'population': self._population,
            's': self._s,
        }


class ZipfMandelbrotCategorical(WeightedCategorical):
    r"""Represents a categorical distribution with weights
    corresponding to a Zipf-Mandelbrot distribution with exponent `s`
    and offset `q`.

    The Zipf-Mandelbrot distribution is defined by the equation

    .. math::

        \text{Pr}(x=k) = \frac{(k+q)^{-s}}{\sum_{i=1}^{N} (i+q)^{-s}}

    When ``q == 0``, the distribution becomes the Zipf distribution, and
    as `n` increases, it approaches the Zeta distribution.
    """

    def __init__(self, population: Sequence, s: float, q: float):
        self._s: float = s
        self._q: float = q
        weights = [math.pow(i + q, -s) for i in range(len(population))]
        super().__init__(population=population, weights=weights)

    @property
    def s(self) -> float:
        """Read-only property for the distribution's `s` exponent."""
        return self._s

    @property
    def q(self) -> float:
        """Read-only property for the distribution's `q` offset."""
        return self._q

    @property
    def n(self) -> int:
        """Read-only property for the number of values in the
        distribution's support."""
        return len(self._population)

    def as_list(self) -> List:
        return [self.__class__.__name__.casefold(),
                self._population, self._s, self._q]

    def as_dict(self) -> Dict:
        return {
            'distribution': self.__class__.__name__.casefold(),
            'population': self._population,
            's': self._s,
            'q': self._q
        }


_distribution_lookup = {
    dist.casefold(): globals()[dist]
    for dist in __all__
    if dist not in ('distribution_from_list', 'distribution_from_dict')
}


def distribution_from_list(as_list):
    """Build a distribution using a list of parameters.

    Expects a list of values in the same form return by a call to
    ``Distribution.as_list()``; i.e. ``['name', arg0, arg1, ...]``.

    Examples:
        >>> tri = Triangular(2.0, 5.0)
        >>> tri_as_list = tri.as_list()
        >>> tri_as_list
        ['triangular', 2.0, 5.0]
        >>> new_tri = distribution_from_list(tri_as_list)
        >>> assert tri == new_tri

    Raises:
        KeyError: if the distribution name is not recognized.
        TypeError: if the wrong number of arguments is given.
    """
    dist_name, *args = as_list
    dist = _distribution_lookup[dist_name.casefold()]
    return dist(*args)


def distribution_from_dict(as_dict):
    """Build a distribution using a dictionary of keyword arguments.

    Expects a dict in the same form as returned by a call to
    ``Distribution.as_dict()``; i.e.
    ``{'distribution':'name', 'arg0':'value', 'arg1':'value', ...}``.

    Examples:
        >>> gauss = Gaussian(0.8, 5.0)
        >>> gauss_as_dict = gauss.as_dict()
        >>> gauss_as_dict
        {'distribution': 'gaussian', 'mu': 0.8, 'sigma': 5.0}
        >>> new_gauss = distribution_from_dict(gauss_as_dict)
        >>> assert gauss == new_gauss

    Raises:
        KeyError: if the distribution name is not recognized or provided.
        TypeError: if the wrong keyword arguments are provided.
    """
    dist_name = as_dict['distribution'].casefold()
    kwargs = dict(as_dict)
    del kwargs['distribution']
    dist = _distribution_lookup[dist_name.casefold()]
    return dist(**kwargs)
