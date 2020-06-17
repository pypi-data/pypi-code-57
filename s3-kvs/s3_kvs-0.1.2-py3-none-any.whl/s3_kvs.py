import json

import requests


FORMATTERS = {
    'text': lambda content: content,
    'json': lambda content: json.loads(content),
}

FILE_EXTENSIONS = {
    'text': 'txt',
    'json': 'json',
}


class ReadOnlyClient(object):

    def __init__(self, domain, namespace=None, value_format='text'):
        self.domain = domain
        self.namespace = namespace
        self.value_format = value_format

    def __getitem__(self, item):
        return self.get_formatter()(self.read(self.get_item_path(item)))

    def get_item_path(self, item):
        item_path = f'{self.namespace}/{item}' if self.namespace is not None else item
        return f'https://{self.domain}/{item_path}.{self.get_extension()}'

    def get_formatter(self):
        return FORMATTERS[self.value_format]

    def get_extension(self):
        return FILE_EXTENSIONS[self.value_format]

    @staticmethod
    def read(url):

        response = requests.get(url)

        if 400 <= response.status_code < 500:
            raise KeyError(f'No matching key found in key-value store at: {url}.')
        if response.status_code >= 500:
            raise ValueError(f'Error fetching from key-value store: {response.reason}')

        return response.content.decode()

    def get(self, key, default=None):
        try:
            self[key]
        except KeyError:
            return default
