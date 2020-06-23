# -*- coding: utf-8 -*-
import unittest

from yandex_checkout.domain.models.currency import Currency
from yandex_checkout.domain.request.refund_request_builder import RefundRequestBuilder


class TestRefundRequestBuilder(unittest.TestCase):
    def test_build_request(self):
        self.maxDiff = None
        builder = RefundRequestBuilder()
        request = builder.set_amount({'value': 0.1, 'currency': Currency.RUB}) \
            .set_description('test comment') \
            .set_payment_id('21a632d2-000f-5061-a000-01e90bc2de12') \
            .set_receipt({
                'phone': '79990000000',
                'email': 'test@email.com',
                'tax_system_code': 1,
                'items': [
                    {
                        "description": "Product 1",
                        "quantity": 2.0,
                        "amount": {
                            "value": 250.0,
                            "currency": Currency.RUB
                        },
                        "vat_code": 2
                    },
                    {
                        "description": "Product 2",
                        "quantity": 1.0,
                        "amount": {
                            "value": 100.0,
                            "currency": Currency.RUB
                        },
                        "vat_code": 2
                    }
                ]}) \
            .build()

        self.assertEqual({
            'payment_id': '21a632d2-000f-5061-a000-01e90bc2de12',
            'description': 'test comment',
            'receipt': {
                'customer': {'email': 'test@email.com', 'phone': '79990000000'},
                'phone': '79990000000',
                'email': 'test@email.com',
                'tax_system_code': 1,
                'items': [
                    {
                        "description": "Product 1",
                        "quantity": 2.0,
                        "amount": {
                            "value": 250.0,
                            "currency": Currency.RUB
                        },
                        "vat_code": 2
                    },
                    {
                        "description": "Product 2",
                        "quantity": 1.0,
                        "amount": {
                            "value": 100.0,
                            "currency": Currency.RUB
                        },
                        "vat_code": 2
                    }
                ]},
            'amount': {'value': 0.1, 'currency': Currency.RUB}
        }, dict(request))
