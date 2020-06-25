from cms import api
from django.http import SimpleCookie
from django.test import TestCase


class CookieTest(TestCase):
    def setUp(self) -> None:
        self.client.cookies = SimpleCookie({
            'cookies_confirmed': True,
            'analysis_confirmed': True,
        })
        self.page = api.create_page(
            'Test',
            'home.html',
            'en-us',
            slug='home',
        )
        self.page.publish('en-us')

    def test_set_cookies(self):
        self.assertTrue(self.page.is_published('en-us'), "Could not publish page")
        response = self.client.get('/home', follow=True)
        html = response.content.decode('utf-8')
        self.assertTrue('id="cookie-alert"' not in html, "Cookie alert still showed after confirmation")
