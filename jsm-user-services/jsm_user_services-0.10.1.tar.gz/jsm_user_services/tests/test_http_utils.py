from unittest import TestCase

from jsm_user_services.support.http_utils import convert_header_to_meta_key
from jsm_user_services.support.http_utils import request
from requests.exceptions import ConnectTimeout


class TestContracts(TestCase):
    def test_should_raise_timeout(self):
        with request() as r:
            # check https://stackoverflow.com/a/100859 for the reason of "http://www.google.com:81/"
            self.assertRaises(ConnectTimeout, r.get, "http://www.google.com:81/")

    def test_should_convert_header_to_meta_key(self):
        header1 = "x-original-forwarded-for"
        header2 = "authentication"
        header3 = "x-forwarded-for"

        self.assertEqual(convert_header_to_meta_key(header1), "HTTP_X_ORIGINAL_FORWARDED_FOR")
        self.assertEqual(convert_header_to_meta_key(header2), "HTTP_AUTHENTICATION")
        self.assertEqual(convert_header_to_meta_key(header3), "HTTP_X_FORWARDED_FOR")
