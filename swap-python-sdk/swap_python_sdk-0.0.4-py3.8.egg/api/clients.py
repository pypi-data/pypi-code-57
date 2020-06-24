import os
import requests
from urllib.parse import urljoin
from swap.common.config import Settings


class UBLClient:
    def __init__(self):
        self.base_url = Settings.UBL_URL
        self.id_token = os.getenv('SWAP_API_TOKEN')

    def url(self, path):
        return urljoin(self.base_url, path)

    def get(self, path=''):
        joined_url = self.url(path)
        response = requests.get(joined_url, headers={'id_token': self.id_token})

        return response.text

    def post(self, path='', data={}):
        response = requests.post(self.url(path), json=data, headers={'id_token': self.id_token})

        if response.status_code != requests.codes.ok:
            raise Exception(f'UBL API call response not OK: {response.status_code}')

        return response.text

    def get_input_datasets(self):
        return self.get('/inputdata')


class ServiceDiscoveryClient:
    def __init__(self):
        self.base_url = Settings.SERVICE_DISCOVERY_URL

    def url(self, path):
        return urljoin(self.base_url, path)

    def get(self, path=''):
        joined_url = self.url(path)
        response = requests.get(joined_url)
        return response.text

    def get_services(self):
        return self.get('/servicediscovery')


class IngestionClient:
    def __init__(self):
        self.base_url = Settings.INGESTION_URL
        self.id_token = os.getenv('SWAP_API_TOKEN')

    def url(self, path):
        return urljoin(self.base_url, path)

    def get(self, path=''):
        joined_url = self.url(path)
        response = requests.get(joined_url, headers={'id_token': self.id_token})

        return response.text

    def post(self, path='', data={}):
        response = requests.post(self.url(path), json=data, headers={'id_token': self.id_token})

        return response.text

    def post_ingestion(self, data):
        return self.post('/ingestions', data=data)

    def get_ingestion_progress(self, id):
        return self.get(f'/ingestions/{id}')
