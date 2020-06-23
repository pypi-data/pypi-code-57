# -*- coding: utf-8 -*-
import sys
import unittest

from yandex_checkout import Webhook
from yandex_checkout.domain.request.webhook_request import WebhookRequest
from yandex_checkout.domain.response.webhook_response import WebhookList, WebhookResponse

if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch

from yandex_checkout.configuration import Configuration


class TestWebhook(unittest.TestCase):

    def setUp(self):
        Configuration.configure(account_id='test_account_id', secret_key='test_secret_key')

    def test_list(self):
        self.maxDiff = None
        with patch('yandex_checkout.client.ApiClient.request') as request_mock:
            request_mock.return_value = {
                "type": "list",
                "items": [
                    {
                        "id": "wh-e44e8088-bd73-43b1-959a-954f3a7d0c54",
                        "event": "payment.canceled",
                        "url": "https://www.merchant-website.com/notification_url"
                    },
                    {
                        "id": "wh-22d6d597-000f-5000-9000-145f6df21d6f",
                        "event": "payment.succeeded",
                        "url": "https://www.merchant-website.com/notification_url"
                    }
                ]
            }
            wh_list = Webhook.list()

            self.assertIsInstance(wh_list, WebhookList)
            self.assertEqual(wh_list.type, "list")
            self.assertIsInstance(wh_list.items[0], WebhookResponse)

    def test_add(self):
        self.maxDiff = None
        with patch('yandex_checkout.client.ApiClient.request') as request_mock:
            request_mock.return_value = {
                "id": "wh-22d6d597-000f-5000-9000-145f6df21d6f",
                "event": "payment.succeeded",
                "url": "https://www.merchant-website.com/notification_url"
            }

            params = WebhookRequest({
                "event": "payment.succeeded",
                "url": "https://www.merchant-website.com/notification_url",
            })
            wh = Webhook.add(params)

            self.assertIsInstance(wh, WebhookResponse)
            self.assertEqual(wh.event, "payment.succeeded")

            params = {
                "event": "payment.succeeded",
                "url": "https://www.merchant-website.com/notification_url",
            }
            wh = Webhook.add(params)

            self.assertIsInstance(wh, WebhookResponse)
            self.assertEqual(wh.event, "payment.succeeded")

        with self.assertRaises(TypeError):
            Webhook.add('invalid data')

    def test_remove(self):
        self.maxDiff = None
        with patch('yandex_checkout.client.ApiClient.request') as request_mock:
            request_mock.return_value = {}

            response = Webhook.remove("wh-22d6d597-000f-5000-9000-145f6df21d6f")

            self.assertIsInstance(response, WebhookResponse)
