from unittest.mock import Mock

from django.test import TestCase
from jsm_user_services.middleware import JsmJwtService
from jsm_user_services.support.local_threading_utils import get_from_local_threading
from jsm_user_services.support.string_utils import get_first_value_from_comma_separated_string


def _build_mocked_request(user_ip: str) -> Mock:
    request = Mock()
    request.META = {
        "REQUEST_METHOD": "POST",
        "HTTP_X_ORIGINAL_FORWARDED_FOR": user_ip,
    }
    request.path = "/fake/url/"
    request.session = {}
    return request


class TestMiddleware(TestCase):
    def setUp(self):
        self.user_ip = "8.8.8.8"
        self.user_ip_comma_separated = "7.7.7.7, 8.8.8.8, 9.9.9.9"

        self.middleware = JsmJwtService()

        self.request = _build_mocked_request(self.user_ip)
        self.request_comma_separated_user_ip = _build_mocked_request(self.user_ip_comma_separated)

    def test_should_get_user_ip_from_request(self):
        response = self.middleware.process_request(self.request)
        self.assertIsNone(response)

        self.assertEqual(get_from_local_threading("user_ip"), self.user_ip)

    def test_should_get_user_ip_from_request(self):
        expected_user_ip = get_first_value_from_comma_separated_string(self.user_ip_comma_separated)
        self.assertEqual(expected_user_ip, "7.7.7.7")

        response = self.middleware.process_request(self.request_comma_separated_user_ip)
        self.assertIsNone(response)
        self.assertEqual(get_from_local_threading("user_ip"), expected_user_ip)
