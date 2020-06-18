from __future__ import annotations
from typing import Any, Optional, Union

import collections
import copy
import numpy as np


__all__ = ["Dimension", "Quantity"]


class Dimension(collections.abc.MutableMapping):
    def __init__(
        self,
        L: Optional[int] = 0,
        T: Optional[int] = 0,
        M: Optional[int] = 0,
        I: Optional[int] = 0,
        K: Optional[int] = 0,
        N: Optional[int] = 0,
        J: Optional[int] = 0,
    ) -> None:

        self._d = {
            "L": L,
            "T": T,
            "M": M,
            "I": I,
            "K": K,
            "N": N,
            "J": J,
        }

    def __iter__(self):
        # FIXME: how to type annotate this?
        return iter(self._d)

    def __getitem__(self, k: str) -> int:
        return self._d.__getitem__(k)

    def __setitem__(self, k: str, v: int) -> None:
        self._d.__setitem__(k, v)

    def __delitem__(self, k: str) -> None:
        del self[k]

    def __len__(self) -> int:
        return 7

    # MULTIPLICATION

    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(**{k: self._d[k] + other._d[k] for k in self._d})

    def __rmul__(self, other: Dimension) -> Dimension:
        return Dimension(**{k: self._d[k] + other._d[k] for k in self._d})

    def __imul__(self, other: Dimension) -> Dimension:
        for k, v in other._d.items():
            self._d[k] += v

        return self

    # DIVISION

    def __truediv__(self, other: Dimension) -> Dimension:
        return Dimension(**{k: self._d[k] - other._d[k] for k in self._d})

    def __rtruediv__(self, other: Dimension) -> Dimension:
        return Dimension(**{k: other._d[k] - self._d[k] for k in self._d})

    def __itruediv__(self, other: Dimension) -> Dimension:
        for k, v in other._d.items():
            self._d[k] -= v

        return self

    # EXPONENTIATION

    def __pow__(self, other: Dimension) -> Dimension:
        return Dimension(**{k: v * other for k, v in self._d.items()})

    def __ipow__(self, other: Dimension) -> Dimension:
        for k in self._d:
            self._d[k] *= other

        return self

    # COMPARISON

    def __eq__(self, other: Dimension) -> bool:
        return self._d == other._d

    def __hash__(self) -> int:
        return hash(tuple(sorted(self._d.items())))

    def __str__(self) -> str:
        positive_power_strings = (
            dim.replace("K", "\u03B8") + "^" + str(pow)
            for dim, pow in self._d.items()
            if pow > 0
        )
        negative_power_strings = (
            dim.replace("K", "\u03B8") + "^" + str(-pow)
            for dim, pow in self._d.items()
            if pow < 0
        )

        numerator_string = "*".join(sorted(positive_power_strings))
        denominator_string = "*".join(sorted(negative_power_strings))

        if numerator_string == "" and denominator_string == "":
            s = ""
        elif numerator_string != "" and denominator_string == "":
            s = numerator_string
        elif numerator_string == "" and denominator_string == "":
            s = f"1/({denominator_string})"
        else:
            s = f"({numerator_string})/({denominator_string})"

        return s.replace("^1", "")

    def __repr__(self) -> str:
        kwargs_str = ",".join(f"{k}={v}" for k, v in self._d.items())
        return f"Dimension({kwargs_str})"


def _preconvert(func):
    def dec(self, other):
        return func(self, other.convert(self.unit))

    return dec


def _precast(func):
    def dec(self, other):
        try:
            return func(self, other)
        except AttributeError:
            return func(self, Quantity(other))

    return dec


class Quantity(collections.abc.Sequence):
    def __init__(
        self,
        value: Optional[Union[int, float, Iterable[int], Iterable[float]]] = 1.0,
        prefactor: Optional[Union[int, float]] = 1.0,
        L: Optional[int] = 0,
        M: Optional[int] = 0,
        T: Optional[int] = 0,
        I: Optional[int] = 0,
        K: Optional[int] = 0,
        N: Optional[int] = 0,
        J: Optional[int] = 0,
    ) -> None:

        self.value = np.array(value)
        self.prefactor = prefactor
        self.dimension = Dimension(L=L, M=M, T=T, I=I, K=K, N=N, J=J)

    @property
    def magnitude(self):
        return self.value * self.prefactor

    @property
    def unit(self) -> Quantity:
        return Quantity(prefactor=self.prefactor, **self.dimension)

    def to_unit(self) -> Quantity:
        # FIXME: how to preserve value dtype?
        return Quantity(prefactor=self.prefactor * self.value, **self.dimension)

    def convert(self, convert_to: Quantity) -> Quantity:
        if self.dimension != convert_to.dimension:
            raise ValueError("Cannot convert quantities with different dimensions.")
        if self.unit != convert_to.unit:
            # NOTE: can't write this as 'self.value *= ...' without causing numpy unsafe casting error in some cases
            return Quantity(
                value=self.magnitude / convert_to.prefactor,
                prefactor=convert_to.prefactor,
                **convert_to.dimension,
            )
        return Quantity(self.value, self.prefactor, **self.dimension)

    @property
    def T(self):
        return self.value.T * self.unit

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError
        # if not hasattr(self,name):
        return getattr(self.value, name)

    __array_priority__ = 1000

    # ADDITION

    @_precast
    @_preconvert
    def __add__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(self.value + other.value, self.prefactor, **self.dimension)

    @_precast
    @_preconvert
    def __radd__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(other.value + self.value, self.prefactor, **self.dimension)

    @_precast
    @_preconvert
    def __iadd__(self, other: Union[Quantity, int, float]) -> Quantity:
        self.value += other.value
        return self

    # SUBTRACTION

    @_precast
    @_preconvert
    def __sub__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(self.value - other.value, self.prefactor, **self.dimension)

    @_precast
    @_preconvert
    def __rsub__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(other.value - self.value, self.prefactor, **self.dimension)

    @_precast
    @_preconvert
    def __isub__(self, other: Union[Quantity, int, float]) -> Quantity:
        self.value -= other.convert(self.unit).value
        return self

    # MULTIPLICATION

    @_precast
    def __mul__(self, other: Union[Quantity, float]) -> Quantity:
        return Quantity(
            self.value * other.value,
            self.prefactor * other.prefactor,
            **(self.dimension * other.dimension),
        )

    @_precast
    def __rmul__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(
            other.value * self.value,
            other.prefactor * self.prefactor,
            **(self.dimension * other.dimension),
        )

    @_precast
    def __imul__(self, other: Union[Quantity, int, float]) -> Quantity:
        self.value *= other.value
        self.prefactor *= other.prefactor
        self.dimension *= other.dimension

        return self

    # MATRIX MULTIPLICATION

    @_precast
    def __matmul__(self, other: Union[Quantity, float]) -> Quantity:
        return Quantity(
            self.value @ other.value,
            self.prefactor * other.prefactor,
            **(self.dimension * other.dimension),
        )

    @_precast
    def __rmatmul__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(
            other.value @ self.value,
            other.prefactor * self.prefactor,
            **(self.dimension * other.dimension),
        )

    @_precast
    def __imatmul__(self, other: Union[Quantity, int, float]) -> Quantity:
        self.value @= other.value
        self.prefactor *= other.prefactor
        self.dimension *= other.dimension

        return self

    # DIVISION

    @_precast
    def __truediv__(self, other: Union[Quantity, int, float]) -> Quantity:
        return Quantity(
            self.value / other.value,
            self.prefactor / other.prefactor,
            **(self.dimension / other.dimension),
        )

    @_precast
    def __rtruediv__(self, other: Union[Unit, int, float]) -> Quantity:
        return Quantity(
            other.value / self.value,
            other.prefactor / self.prefactor,
            **(other.dimension / self.dimension),
        )

    @_precast
    def __itruediv__(self, other: Union[Unit, int, float]) -> Quantity:
        self.value /= other.value
        self.prefactor /= other.prefactor
        self.dimension /= other.dimension

        return self

    # EXPONENTIATION

    def __pow__(self, other: Union[int, float]) -> Quantity:
        return Quantity(
            self.value ** other, self.prefactor ** other, **(self.dimension ** other)
        )

    def __ipow__(self, other: Union[int, float]) -> Quantity:
        self.value **= other
        self.prefactor **= other
        self.dimension **= other

    # COMPARISON

    @_precast
    def __eq__(
        self, other: Union[Quantity, int, float, Iterable[int], Iterable[float]]
    ) -> bool:
        # np.array_equal works on any array_like and also single values, which should cover all reasonable types for self.value
        return (
            np.array_equal(self.value, other.value)
            and self.prefactor == other.prefactor
            and self.dimension == other.dimension
        )

    @_precast
    @_preconvert
    def __lt__(self, other: Union[Quantity, int, float]) -> bool:
        return self.magnitude < other.magnitude

    @_precast
    @_preconvert
    def __le__(self, other: Union[Quantity, int, float]) -> bool:
        return self.magnitude <= other.magnitude

    @_precast
    @_preconvert
    def __gt__(self, other: Union[Quantity, int, float]) -> bool:
        return self.magnitude > other.magnitude

    @_precast
    @_preconvert
    def __ge__(self, other: Union[Quantity, int, float]) -> bool:
        return self.magnitude >= other.magnitude

    # UNARY

    def __neg__(self) -> Quantity:
        return Quantity(-self.value, self.prefactor, **self.dimension)

    def __pos__(self) -> Quantity:
        return Quantity(+self.value, self.prefactor, **self.dimension)

    def __abs__(self) -> Quantity:
        # FIXME: should abs apply to the prefactor too?
        return Quantity(abs(self.value), self.prefactor, **self.dimension)

    def __invert__(self) -> Quantity:
        # FIXME: should ~ apply to the prefactor too?
        return Quantity(~self.value, self.prefactor, **self.dimension)

    # OTHER

    def __getitem__(self, index):
        return Quantity(self.value[index], self.prefactor, **self.dimension)

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        # FIXME: check this is a good hash method, esp. wrt performance
        return hash((self.value.data.tobytes(), self.dimension))

    def __str__(self) -> str:
        dimension_string = (
            str(self.dimension)
            .replace("L", "m")
            .replace("M", "kg")
            .replace("T", "s")
            .replace("I", "A")
            .replace("\u03B8", "K")
            .replace("N", "mol")
            .replace("J", "cd")
        )

        return f"{self.value*self.prefactor} {dimension_string}"

    def __repr__(self) -> str:
        dim_str = ",".join(f"{k}={v}" for k, v in self.dimension.items())

        return f"Quantity(value={self.value},prefactor={self.prefactor},{dim_str})"
