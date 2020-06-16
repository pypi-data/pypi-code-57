from abc import ABCMeta, abstractmethod
import json
import urllib3,certifi

_default_options = {
    'headers':{
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    },
    'fields': {},
    'urlopen_kw': {},
}

def _get_content_type(headers):
    ct_type = headers['Content-Type']
    if 'application/json' in ct_type:
        return 'application/json'
    if 'text/html' in ct_type:
        return 'text/html'

def httpResponseFactory(response):
    ct_type = _get_content_type(dict(response.headers))
    if ct_type == 'application/json':
        return JsonResponse(response)
    if ct_type == 'text/html':
        return HtmlResponse(response)

class IHttpResponse(metaclass=ABCMeta):
    _raw_response = None
    _data = None
    _headers_dict = None
    _status_code = None

    def __init__(self, response):
        self._raw_response = response

    @property
    def raw_response(self):
        return self._raw_response

    @property
    def headers(self):
        return dict(self._raw_response.headers)

    @property
    def status_code(self):
        return self._raw_response.status

    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError('no need to implement here')
    
class JsonResponse(IHttpResponse):
    @property
    def data(self):
        '''
        return json dict
        '''
        data = json.loads(self._raw_response.data.decode('utf-8'))
        return data

class HtmlResponse(IHttpResponse):
    @property
    def data(self):
        '''
        return html str
        '''
        data = self._raw_response.data.decode('utf-8')
        return data

class SimpleHttpClient:
    def __init__(self, addr, *, options_kwargs=None):
        self._addr = addr
        self._headers = _default_options['headers']
        if options_kwargs and 'headers' in options_kwargs:
            self.set_headers(headers=options_kwargs['headers'])

        self._pool_manager = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),
            timeout=urllib3.Timeout(connect=1.0, read=10),
            retries=urllib3.Retry(3, redirect=3)
        )

    def set_headers(self, *, headers=None):
        if headers:
            self._headers.update(headers)
    
    def _do_request(self, http_method, uri, data=None):
        url = '{}{}'.format(self._addr, uri)
        content_type = _get_content_type(self._headers)
        pool_mgr = self._pool_manager
        request_body = None
        if data is not None:
            # tbd request_body can be wraped by http request body data factory in future
            if content_type == 'application/json':
                request_body = json.dumps(data).encode('utf-8')
            else:
                NotImplemented('NotImplemented')

        resp = pool_mgr.request(http_method, url, body=request_body, headers=self._headers, timeout=urllib3.Timeout(10))
        return httpResponseFactory(resp)

            
    def GET(self, uri='', data=None):
        r = self._do_request("GET", uri, data)
        return r
    
    def POST(self, uri, data=None):
        r = self._do_request("POST", uri, data)
        return r

if __name__ == "__main__":
    addr = 'http://127.0.0.1:8000'
    options_kwargs = {
        'headers': {
            'Your_header': 'aloha',
        }
    }
    client = SimpleHttpClient(addr,options_kwargs=options_kwargs)
    r = client.GET()
    print(r.data)