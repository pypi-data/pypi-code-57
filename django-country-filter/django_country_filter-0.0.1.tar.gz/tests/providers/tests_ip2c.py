"""Test case for ip2c provider."""

from django_country_filter.providers.ip2c import Ip2C


def test_initialize(get_request_mock):
    """Initialize should be define a attribute request."""
    provider = Ip2C(get_request_mock)
    assert provider.request is get_request_mock


def test_get(requests_mock, get_request_mock):
    """Return a dict with country and ip."""
    requests_mock.get('https://ip2c.org/1.1.1.1', text='1;AU;AUS;Australia')

    provider = Ip2C(get_request_mock)
    response = provider.get()

    assert response['country'] == 'AU'
    assert response['ip'] == '1.1.1.1'
