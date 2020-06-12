"""Ip2c provider."""

import requests
from django.http.request import HttpRequest


class Ip2C:
    """Implementation of the provider based on the ip2c.org service."""

    URI = 'https://ip2c.org/{}'

    def __init__(self, request: HttpRequest):
        """Initialize class."""
        self.request = request

    def get(self):
        """Must return the country and the IP address that made the request in the application."""
        ip = self.request.META.get('REMOTE_ADDR')
        response = requests.get(self.URI.format(ip))
        if response.status_code != 200:
            raise Exception(
                'Ip2c.org error: {}\n{}'.format(
                    response.status_code,
                    response.content
                )
            )
        country = response.content.decode().split(';')[1]
        return {'country': country, 'ip': ip}
