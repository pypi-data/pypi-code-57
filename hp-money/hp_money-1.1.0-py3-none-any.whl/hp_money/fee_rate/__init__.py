# -*- coding: utf-8 -*-

from decimal import (
    Decimal,
    ROUND_HALF_UP
)


class FeeRate(object):

    def __init__(self, rate):

        self.weight = Decimal('1')
        self.accuracy = Decimal('0.00000001')

        self.rate = (Decimal(rate) * self.weight).quantize(
            self.accuracy,
            rounding=ROUND_HALF_UP
        )

    def __str__(self):

        return f'FeeRate: {self.rate}'

    def __repr__(self):

        return self.__str__()

    def __eq__(self, other):

        if not isinstance(other, FeeRate):
            return False

        return (self.weight == other.weight) and \
               (self.accuracy == other.accuracy) and \
               (self.rate == other.rate)

    def __ne__(self, other):

        return not self.__eq__(other)

    def __gt__(self, other):

        if not isinstance(other, FeeRate):
            return False

        if self.weight != other.weight:
            return False

        if self.accuracy != other.accuracy:
            return False

        return self.rate > other.rate

    def __ge__(self, other):

        return self > other or self == other

    def __lt__(self, other):

        if not isinstance(other, FeeRate):
            return False

        if self.weight != other.weight:
            return False

        if self.accuracy != other.accuracy:
            return False

        return self.rate < other.rate

    def __le__(self, other):

        return self < other or self == other
