# -*- coding: utf-8 -*-

from decimal import (
    Decimal,
    ROUND_DOWN
)


class Amount(object):

    def __init__(self, value):

        self._value = Decimal(value)

    @property
    def value(self):
        # hipopay采取货币最小单位分为基本计价单位，
        # 所以这里直接舍掉小数位
        return self._value.quantize(
            Decimal('0'),
            ROUND_DOWN
        )

    def __str__(self):
        return f'{self._value}'

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return self.__class__(
            abs(self._value)
        )

    def __neg__(self):
        return self.__class__(
            -self._value
        )

    def __add__(self, other):
        if isinstance(other, Amount):
            other_value = other.value
        else:
            other_value = Decimal(other)
        return self.__class__(
            self._value + other_value
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Amount):
            other_value = other.value
        else:
            other_value = Decimal(other)
        return self.__add__(-other_value)

    def __rsub__(self, other):
        return other - self

    def __eq__(self, other):
        if isinstance(other, Amount):
            return self._value == other.value
        else:
            return self._value == Decimal(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, Amount):
            return self._value > other.value
        else:
            return self._value > Decimal(other)

    def __lt__(self, other):
        if isinstance(other, Amount):
            return self._value < other.value
        else:
            return self._value < Decimal(other)

    def __ge__(self, other):
        return (self == other) or (self > other)

    def __le__(self, other):
        return (self == other) or (self < other)

    def exchange(self, forex_rate):

        return Amount(self.value * forex_rate.rate / forex_rate.weight).value
