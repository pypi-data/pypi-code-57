# -*- coding: utf-8 -*-

from hp_money import Money
from hp_money.currency import Currency
import pytest


HKD = Currency('HKD', '344', 100)
JPY = Currency('JPY', '392', 1)

amount1 = 888
amount2 = '888'
amount3 = '888.00'
amount4 = 999


def test_currency_stringify():
    """ 测试币种字符串输出 """

    assert str(HKD) == 'HKD', 'Currency stringify test error'
    assert str(HKD) != 'JPY', 'Currency stringify test error'
    assert str(JPY) == 'JPY', 'Currency stringify test error'


def test_currency_equality():
    """ 测试币种相等性 """

    assert HKD == HKD, 'Currency equivalent test error'
    assert HKD == Currency('HKD', '344', 100), 'Currency equality test error'
    assert HKD != Currency('HKD', '355', 100), 'Currency equality test error'
    assert HKD != Currency('HKD', '355', 1), 'Currency equality test error'
    assert HKD != JPY, 'Currency equivalent test error'


def test_money_equality():

    money1 = Money(
        amount=amount1,
        currency=HKD
    )
    money2 = Money(
        amount=amount3,
        currency=HKD
    )
    money3 = Money(
        amount=amount1,
        currency=JPY
    )
    money4 = Money(
        amount=amount4,
        currency=HKD
    )

    assert str(money2.amount.value) == '888', 'Money equality test error'
    assert money1 == money2, 'Money equality test error'
    assert money1 != money3, 'Money equality test error'
    assert money4 != money1, 'Money equality test error'


def test_money_calculation():

    money1 = Money(
        amount=amount1,
        currency=HKD
    )
    money2 = Money(
        amount=amount4,
        currency=HKD
    )
    money3 = Money(
        amount=amount4,
        currency=JPY
    )

    sum1 = money1 + money2
    diff1 = money1 - money2
    diff2 = money2 - money1

    assert sum1 == Money(currency=HKD, amount='1887')
    assert diff1 == -Money(currency=HKD, amount='111')
    assert diff2 == Money(currency=HKD, amount='111')
    assert abs(diff1) == Money(currency=HKD, amount='111')
    assert abs(diff1) == abs(diff2)

    with pytest.raises(TypeError) as exc_info:
        sum2 = money1 + money3

    with pytest.raises(TypeError) as exc_info:
        sum2 = money1 + '2'
