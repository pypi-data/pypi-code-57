import unittest
from unittest import mock

from django.conf import settings
from django import http
from django import test
from django import views
from django.test import client

from querystringer import middleware

settings.configure()


class MiddlewareTest(unittest.TestCase):

    class SampleView(views.View):

        def get(self, request):
            return http.HttpResponse()

    def setUp(self):
        self.view = MiddlewareTest.SampleView()
        self.middleware = middleware.ProfilerMiddleware()
        self.request = client.RequestFactory().get('/sample/?test=true')
        self.default_response = http.HttpResponse('Hello World')
        self.override_settings = {
            'DEBUG': True,
        }
        self.profile_content = '<pre>'.encode('utf-8')

    def test_url(self):
        with test.override_settings(**self.override_settings):
            self.middleware.process_view(
                self.request, self.view.get, (self.request,), {})
            response = self.middleware.process_response(
                self.request, self.default_response)
                
        self.assertIn('Hello World', response.content)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_debug_required(self):
        self.override_settings['DEBUG'] = False
        with test.override_settings(**self.override_settings):
            self.middleware.process_view(
                self.request, self.view.get, (self.request,), {})
            response = self.middleware.process_response(
                self.request, self.default_response)
        self.assertEqual(response.content, self.default_response.content)
