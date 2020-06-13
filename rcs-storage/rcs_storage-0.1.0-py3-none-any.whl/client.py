from __future__ import unicode_literals

from datetime import date
import json
import re
try:
    from urlparse import urljoin # py2
except ImportError:
    from urllib.parse import urljoin # py3

import requests


def request(method):
    def function_decorator(func):
        def function_wrapper(self, *args, **kwargs):
            uri, data = func(self, *args, **kwargs)
            request_kwargs = {'url': urljoin(self._host, uri),
                'headers': self._headers, 'data': json.dumps(data)}
            response = getattr(requests, method.lower())(**request_kwargs)
            if response.status_code in [200, 201]:
                return json.loads(response.content)
            elif response.status_code == 404:
                raise DoesNotExist
            else:
                # TODO(elyas): Do something with response.text
                raise Exception('{} {}'.format(
                    response.status_code, response.reason))
        return function_wrapper
    return function_decorator


class DoesNotExist(Exception):
    pass


class Client(object):

    def __init__(self, host, token):
        self.collections = CollectionManager(host, token)
        self.ingests = IngestManager(host, token)
        self.reports = ReportManager(host, token)


class Manager(object):

    def __init__(self, host, token):
        self._host = host
        self._headers = {'Authorization': 'Token {}'.format(token),
                         'Content-Type': 'application/json'}

    def get_headers(self):
        return self._headers


class CollectionManager(Manager):

    @request('POST')
    def create(self, **data):
        return ('/api/collections/', data)

    @request('GET')
    def get(self, code):
        return ('/api/collections/{}/'.format(code), {})

    @request('GET')
    def list(self):
        return ('/api/collections/', {})

    @request('PUT')
    def update(self, collection):
        return (collection['url'], collection)

    @request('OPTIONS')
    def options(self):
        return ('/api/collections/', {})

    @property
    @request('GET')
    def storage_products(self):
        return ('/api/storage_products/', {})

    def get_request_sources_map(self):
        return_dict = {}
        for c in self.list():
            for r_s in re.findall(r'((?:TASK|RITM)\d{7})',
                                  c['request_source']):
                if r_s not in return_dict:
                    return_dict[r_s] = []
                return_dict[r_s].append(c['code'])
        return return_dict


class IngestManager(Manager):

    @request('GET')
    def list(self):
        return ('/ingest/upload/', {})

    def upload_storage_report(self, path_to_file):
        url = urljoin(self._host, '/ingest/upload/')
        files = {'data': open(path_to_file, 'rb')}
        headers = self._headers
        if 'Content-Type' in headers:
            headers.pop('Content-Type')
        resp = requests.post(url, files=files, headers=headers, verify=False)
        return json.loads(resp.content)


class ReportManager(Manager):

    @request('GET')
    def usage_by_department(self, date=None):
        query_string =  ('?date={}'.format(date) if date else '')
        return ('/api/reports/usage-by-department/' + query_string, {})
