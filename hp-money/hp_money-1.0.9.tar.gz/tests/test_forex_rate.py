# -*- coding: utf-8 -*-

from hp_money import Money
from hp_money.currency import Currency
from hp_money.forex_rate import ForexRate
from decimal import Decimal


def test_forex_rate():

    base_currency = Currency(
        iso_code='HKD',
        numric_code='999',
        accuracy=100
    )
    target_currency = Currency(
        iso_code='CNY',
        numric_code='998',
        accuracy=100
    )
    f1 = ForexRate(
        base_currency,
        target_currency,
        '0.912'
    )

    f2 = f1.reverse()

    assert f1.rate == Decimal('91200000'), 'Error'
    assert f2.rate == Decimal('109649123'), 'Error'

    f3 = ForexRate(
        base_currency,
        target_currency,
        '912',
        True
    )

    assert f3.rate == Decimal('912'), 'Error'

    m1 = Money(
        amount=320,
        currency=base_currency
    )

    m2 = m1.exchange(f1)

    m3 = m2.exchange(f2)

    assert m2.amount == '291', 'Error'
    assert m3.amount == '319', 'Error'
