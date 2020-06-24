# -*- coding: utf-8 -*-

from decimal import (
    Decimal,
    ROUND_HALF_UP
)


class ForexRate(object):

    def __init__(self, base_currency, target_currency, rate):

        self.weight = Decimal('1')
        self.accuracy = Decimal('0.00000001')

        self.rate = (Decimal(rate) * self.weight).quantize(
            self.accuracy,
            rounding=ROUND_HALF_UP
        )
        self.base_currency = base_currency
        self.target_currency = target_currency

    def __str__(self):

        return f'1 {self.base_currency} = {self.rate} / {self.weight} {self.target_currency}'

    def __repr__(self):

        return self.__str__()

    def reverse(self):

        rate_value_reversed = (
            Decimal('1') * self.weight / self.rate
        ) * self.weight

        rate_reversed = rate_value_reversed.quantize(
            self.accuracy,
            rounding=ROUND_HALF_UP,
        ) / self.weight

        return ForexRate(
            self.target_currency,
            self.base_currency,
            rate_reversed
        )
