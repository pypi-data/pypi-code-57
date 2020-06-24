from json import dumps

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from .client_libs.data_wrappers import ZuoraResponse
from .client_libs.zuora_client_exceptions import (ZuoraErrorResponseException,
                                                  ZuoraErrorEmptyPostBody,
                                                  ZuoraErrorHeaderWrongDataType)


class ZuoraBasicClient:
    def __init__(self, base_url=None, client_id=None,
                 client_secret=None, entity=None, headers=None,
                 query_retry_timeout=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_uri = f'{self.base_url}/oauth/token'

        if entity is not None:
            self.headers = {'zuora-entity-ids': entity}
        elif headers is not None and isinstance(headers, dict):
            # Compatibility with 0.1
            self.headers = headers
        else:
            self.headers = dict()

        if query_retry_timeout is not None and query_retry_timeout > 0:
            self.query_retry_timeout = query_retry_timeout
        else:
            self.query_retry_timeout = 1

    def __enter__(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        self.client = BackendApplicationClient(client_id=self.client_id)
        # Get oauth2 token
        with OAuth2Session(client=self.client) as oauth:
            self.token = oauth.fetch_token(token_url=self.token_uri, auth=auth)
        # Start session
        self.session = OAuth2Session(self.client, token=self.token, auto_refresh_url=self.token_uri,
                                     auto_refresh_kwargs={
                                         'client_id': self.client_id,
                                         'client_secret': self.client_secret,
                                     },
                                     token_updater=self.__save_token)
        return self

    def __save_token(self, token):
        self.token = token

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def set_default_content_type(self):
        self.headers['content-type'] = 'application/json;charset=UTF-8'

    def set_content_type(self, new_type):
        self.headers['content-type'] = new_type

    def update_headers(self, headers):
        try:
            self.headers.update(headers)
        except TypeError as e:
            raise ZuoraErrorHeaderWrongDataType()

    def get(self, url):
        resp = self.session.get(f'{self.base_url}{url}', headers=self.headers)
        if not resp.status_code == 200:
            raise ZuoraErrorResponseException(resp)
        return ZuoraResponse(resp)

    def post(self, url, data=None):
        try:
            assert data is not None
            resp = self.session.post(f'{self.base_url}{url}', data=dumps(data), headers=self.headers)
            if resp.status_code != 200:
                raise ZuoraErrorResponseException(resp)
            return ZuoraResponse(resp)
        except AssertionError:
            raise ZuoraErrorEmptyPostBody()

    def put(self, url, data=None):
        resp = self.session.put(f'{self.base_url}{url}', headers=self.headers, data=dumps(data))
        if resp.status_code != 200:
            raise ZuoraErrorResponseException(resp)
        return ZuoraResponse(resp)

    def delete(self, url):
        resp = self.session.delete(f'{self.base_url}{url}', headers=self.headers)
        if resp.status_code != 200:
            raise ZuoraErrorResponseException(resp)
        return ZuoraResponse(resp)
