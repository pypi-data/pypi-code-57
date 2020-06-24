# -*- coding: utf-8 -*-

from hp_money.fee_rate import FeeRate
from decimal import Decimal


def test_fee_rate():

    fee_rate_1 = FeeRate('0.01')
    fee_rate_2 = FeeRate('0.1')
    fee_rate_3 = FeeRate('0.1')

    assert fee_rate_1.rate == Decimal('0.01'), 'Fee Rate Error'
    assert fee_rate_1 != fee_rate_2, 'Fee Rate Error'
    assert fee_rate_2 == fee_rate_3, 'Fee Rate Error'
    assert fee_rate_3 >= fee_rate_1, 'Fee Rate Error'
    assert fee_rate_3 > fee_rate_1, 'Fee Rate Error'
    assert fee_rate_1 <= fee_rate_2, 'Fee Rate Error'
    assert fee_rate_1 < fee_rate_2, 'Fee Rate Error'
