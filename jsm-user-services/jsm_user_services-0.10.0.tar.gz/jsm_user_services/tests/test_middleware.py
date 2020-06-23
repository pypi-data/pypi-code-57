from unittest.mock import Mock

from django.test import TestCase

from jsm_user_services.middleware import JsmJwtService
from jsm_user_services.support.local_threading_utils import get_from_local_threading


class TestMiddleware(TestCase):
    def setUp(self):
        self.user_ip = "8.8.8.8"
        self.middleware = JsmJwtService()
        self.request = Mock()
        self.request.META = {
            "REQUEST_METHOD": "POST",
            "HTTP_X_ORIGINAL_FORWARDED_FOR": self.user_ip,
        }
        self.request.path = '/fake/url/'
        self.request.session = {}

    def test_should_get_user_ip_from_request(self):
        response = self.middleware.process_request(self.request)
        self.assertIsNone(response)

        self.assertEqual(get_from_local_threading("user_ip"), self.user_ip)
