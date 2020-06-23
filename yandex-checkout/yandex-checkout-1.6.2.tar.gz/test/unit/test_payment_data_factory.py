# -*- coding: utf-8 -*-
import unittest

from yandex_checkout.domain.common.data_context import DataContext
from yandex_checkout.domain.common.payment_method_type import PaymentMethodType
from yandex_checkout.domain.models.payment_data.payment_data_factory import PaymentDataFactory
from yandex_checkout.domain.models.payment_data.request.payment_data_yandex_wallet import PaymentDataYandexWallet
from yandex_checkout.domain.models.payment_data.response.payment_data_webmoney import PaymentDataWebmoney


class TestPaymentDataFactory(unittest.TestCase):
    def test_factory_method(self):
        factory = PaymentDataFactory()
        request_payment_data = factory.create({'type': PaymentMethodType.YANDEX_MONEY}, DataContext.REQUEST)
        self.assertIsInstance(request_payment_data, PaymentDataYandexWallet)

        response_payment_data = factory.create({'type': PaymentMethodType.WEBMONEY}, DataContext.RESPONSE)
        self.assertIsInstance(response_payment_data, PaymentDataWebmoney)
