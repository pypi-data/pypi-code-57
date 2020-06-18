# -*- coding: utf-8 -*-

from decimal import (
    Decimal,
    ROUND_HALF_UP
)


class ForexRate(object):

    def __init__(self, base_currency, target_currency, rate, origin=False):

        # 汇率 = 原汇率 * 10的8次方
        self.weight = Decimal('1') if origin else Decimal(pow(10, 8))
        # 精度，保持小数点后0位
        self.accuracy = Decimal('1')

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
