import os
from django.test import TestCase
from django.contrib.staticfiles import finders

from lionclaw import settings
from lionclaw.core.templatetags import lionclawcore_tags

class TagTests(TestCase):

    def _test_static_file(self, pth):
        result = finders.find(pth)
        print(result)
        self.assertTrue(result)

    def test_vendors_bundle(self):
        ctx = lionclawcore_tags.lionclaw_vendors_bundle()
        print(ctx)
        self._test_static_file(ctx['path'])

    def test_client_bundle(self):
        ctx = lionclawcore_tags.lionclaw_client_bundle()
        self._test_static_file(ctx['path'])

    def test_api_url_prefix(self):
        self.assertEqual(
            settings.API_URL_PREFIX,
            lionclawcore_tags.lionclaw_api_url_prefix()
        )
