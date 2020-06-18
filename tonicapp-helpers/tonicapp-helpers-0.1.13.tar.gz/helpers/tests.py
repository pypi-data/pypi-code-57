from rest_framework import status
from rest_framework.test import APITestCase

from .requests import get_sort_in_django_format


class HelpersTests(APITestCase):
    def test_get_sort_in_django_format_with_descent(self):
        """
        Test function get_sort_in_django_format for descendent case
        """
        sort = get_sort_in_django_format('desc[last_modified]')
        self.assertEqual(sort, '-last_modified')

    def test_get_sort_in_django_format_with_ascendant(self):
        """
        Test function get_sort_in_django_format for ascendant case
        """
        sort = get_sort_in_django_format('asc[last_modified]')
        self.assertEqual(sort, 'last_modified')
