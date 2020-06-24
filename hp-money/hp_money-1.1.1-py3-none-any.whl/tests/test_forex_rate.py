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
    jpy_currency = Currency(
        iso_code='JPY',
        numric_code='997',
        accuracy=1
    )
    f1 = ForexRate(
        base_currency,
        target_currency,
        '0.912'
    )

    f2 = f1.reverse()

    f4 = ForexRate(
        target_currency,
        jpy_currency,
        '15.0932'
    )

    f5 = f4.reverse()

    assert f1.rate == Decimal('0.912'), 'Error'
    assert f2.rate == Decimal('1.09649123'), 'Error'

    f3 = ForexRate(
        base_currency,
        target_currency,
        '0.912',
    )

    assert f3.rate == Decimal('0.912'), 'Error'

    m1 = Money(
        amount=3.20,
        currency=base_currency
    )

    m2 = m1.exchange(f1)

    m3 = m2.exchange(f2)

    assert m2.amount == '291', 'Error'
    assert m3.amount == '319', 'Error'

    m_jpy = Money(
        amount=100,
        currency=jpy_currency
    )

    m_cny = m_jpy.exchange(f5)

    m_jpy_2 = m_cny.exchange(f4)

    assert m_cny.amount == '662', 'Error'
    assert m_jpy_2.amount == '99', 'Error'
