from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import path
from .views import bad_request_view, page_not_found_view, permission_denied_view, error_view

urlpatterns = [
    path('400/', bad_request_view),
    path('403/', permission_denied_view),
    path('404/', page_not_found_view),
    path('500/', error_view),
]

handler400 = bad_request_view
handler403 = permission_denied_view
handler404 = page_not_found_view
handler500 = error_view


# ROOT_URLCONF must specify the module that contains handler403 = ...
@override_settings(ROOT_URLCONF=__name__)
class CustomErrorHandlerTests(TestCase):

    def test_handler_renders_template_response_for_400(self):
        response = self.client.get('/400/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Bad request', status_code=400)

    def test_handler_renders_template_response_for_403(self):
        response = self.client.get('/403/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Permission denied', status_code=403)

    def test_handler_renders_template_response_for_404(self):
        response = self.client.get('/404/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Page not found', status_code=404)


    def test_handler_renders_template_response_for_500(self):
        response = self.client.get('/500/')
        # Make assertions on the response here. For example:
        self.assertContains(response, 'Internal server error', status_code=500)