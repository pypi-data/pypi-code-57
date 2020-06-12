"""Mock for provider."""

from django.http.request import HttpRequest


class ProviderMock:
    """Mock to provider."""

    def __init__(self, request: HttpRequest):
        """Initialize the mock."""
        self.request = request

    def get(self):
        """Mock the get method."""
        return {
            'country': 'AU',
            'ip': self.request.META.get('REMOTE_ADDR')
        }
