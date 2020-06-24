# -*- coding: utf-8 -*-

from decimal import (
    Decimal,
    ROUND_DOWN
)


class Amount(object):

    def __init__(self, value, accuracy=100):

        """
            采用币种最小单位整数作为持久化单位，并直接切除非整数位。
                原本以分为最小单位的货币，比如HKD，CNY等，
                    持久化金额 = 原金额 * accuracy，如 1.23 * 100 = 123.00 = 123
                原本以元为最小单位的货币，比如JPY，KRW等，
                    持久化金额 = 原金额 * accuracy，如 1.23 * 1 = 1.23 = 1
        """

        self.accuracy = Decimal(accuracy)
        self._value = (Decimal(value) * self.accuracy).quantize(
            Decimal('1'),
            rounding=ROUND_DOWN
        )

    @property
    def value(self):
        # hipopay采取货币最小单位分为基本计价单位，
        # 所以这里直接舍掉小数位
        return self._value.quantize(
            Decimal('1'),
            ROUND_DOWN
        )

    @property
    def standard_value(self):

        return (self._value / self.accuracy).quantize(
            Decimal(1) / self.accuracy,
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

        return self.__class__(
            (self.value / forex_rate.base_currency.accuracy) * forex_rate.rate / forex_rate.weight,
            forex_rate.target_currency.accuracy
        ).value
