import json

import requests


FORMATTERS = {
    'json': lambda content: json.loads(content),
}


class ReadOnlyClient(object):

    def __init__(self, domain, namespace=None, value_format='json'):
        self.domain = domain
        self.namespace = namespace
        self.value_format = value_format

    def __getitem__(self, item):
        return self.get_formatter()(self.read(self.get_item_path(item)))

    def get_item_path(self, item):

        item_path = f'{self.namespace}/{item}' if self.namespace is not None else item
        item_path = f'{item_path}.{self.value_format}' if self.value_format else item_path

        return f'https://{self.domain}/{item_path}'

    def get_formatter(self):
        return FORMATTERS[self.value_format]

    @staticmethod
    def read(url):

        response = requests.get(url)

        if 400 <= response.status_code < 500:
            raise KeyError(f'No matching key found in key-value store at: {url}.')
        if response.status_code >= 500:
            raise ValueError(f'Error fetching from key-value store: {response.reason}')

        return response.content.decode(response.encoding)

    def get(self, key, default=None):
        try:
            self[key]
        except KeyError:
            return default
