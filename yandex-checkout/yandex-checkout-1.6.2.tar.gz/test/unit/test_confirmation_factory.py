# -*- coding: utf-8 -*-
import unittest

from yandex_checkout.domain.common.confirmation_type import ConfirmationType
from yandex_checkout.domain.common.data_context import DataContext
from yandex_checkout.domain.models.confirmation.confirmation_factory import ConfirmationFactory
from yandex_checkout.domain.models.confirmation.request.confirmation_embedded import \
    ConfirmationEmbedded as RequestConfirmationEmbedded
from yandex_checkout.domain.models.confirmation.request.confirmation_external import \
    ConfirmationExternal as RequestConfirmationExternal
from yandex_checkout.domain.models.confirmation.request.confirmation_qr import \
    ConfirmationQr as RequestConfirmationQr
from yandex_checkout.domain.models.confirmation.request.confirmation_redirect import \
    ConfirmationRedirect as RequestConfirmationRedirect
from yandex_checkout.domain.models.confirmation.response.confirmation_embedded import \
    ConfirmationEmbedded as ResponseConfirmationEmbedded
from yandex_checkout.domain.models.confirmation.response.confirmation_external import \
    ConfirmationExternal as ResponseConfirmationExternal
from yandex_checkout.domain.models.confirmation.response.confirmation_qr import \
    ConfirmationQr as ResponseConfirmationQr
from yandex_checkout.domain.models.confirmation.response.confirmation_redirect import \
    ConfirmationRedirect as ResponseConfirmationRedirect


class TestConfirmationFactory(unittest.TestCase):
    def test_factory_method(self):
        req_redirect_instance = ConfirmationFactory().create({'type': ConfirmationType.REDIRECT}, DataContext.REQUEST)
        self.assertIsInstance(req_redirect_instance, RequestConfirmationRedirect)

        res_redirect_instance = ConfirmationFactory().create({'type': ConfirmationType.REDIRECT}, DataContext.RESPONSE)
        self.assertIsInstance(res_redirect_instance, ResponseConfirmationRedirect)

        req_external_instance = ConfirmationFactory().create({'type': ConfirmationType.EXTERNAL}, DataContext.REQUEST)
        self.assertIsInstance(req_external_instance, RequestConfirmationExternal)

        res_external_instance = ConfirmationFactory().create({'type': ConfirmationType.EXTERNAL}, DataContext.RESPONSE)
        self.assertIsInstance(res_external_instance, ResponseConfirmationExternal)

        res_redirect_instance = ConfirmationFactory().create({'type': ConfirmationType.EMBEDDED}, DataContext.REQUEST)
        self.assertIsInstance(res_redirect_instance, RequestConfirmationEmbedded)

        res_external_instance = ConfirmationFactory().create({'type': ConfirmationType.EMBEDDED}, DataContext.RESPONSE)
        self.assertIsInstance(res_external_instance, ResponseConfirmationEmbedded)

        res_redirect_instance = ConfirmationFactory().create({'type': ConfirmationType.QR}, DataContext.REQUEST)
        self.assertIsInstance(res_redirect_instance, RequestConfirmationQr)

        res_external_instance = ConfirmationFactory().create({'type': ConfirmationType.QR}, DataContext.RESPONSE)
        self.assertIsInstance(res_external_instance, ResponseConfirmationQr)
