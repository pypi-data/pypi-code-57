import hashlib, hmac, datetime
import requests
import json

class AuthRequests:

    def __init__(self, domain="", key_id=None, secret=None):
        self.domain = domain
        self.key_id = key_id
        self.secret = secret

    def auth(self, method, path, query=None, data=None):
        authreq = {'query':''}

        if method not in ['GET', 'POST']:
            raise Exception('Wrong HTTP method')

        if query is not None:
            authreq['query'] = '&'.join([q+'='+query[q] for q in query.keys()])

        time = int(datetime.datetime.now().timestamp())
        authreq['headers'] = {'Host': self.domain.split('/')[0],
                              'X-Mlfork-Time': str(time)}

        headers = '\n'.join([h.lower()+':'+authreq['headers'][h] for h in authreq['headers'].keys()])
        signed_headers = ';'.join([h.lower() for h in authreq['headers'].keys()])

        if data is None:
            payload = ''
        else:
            payload = json.dumps(data)
        data_hash = hashlib.sha256((payload).encode('utf-8')).hexdigest()

        canonReq = '\n'.join([method, path, authreq['query'], headers, signed_headers, data_hash])
        toSign = '\n'.join(['HMAC-SHA256', str(time), hashlib.sha256((canonReq).encode('utf-8')).hexdigest()])

        kTime = hmac.new(('MLFORK'+self.secret).encode('utf-8'), str(time).encode('utf-8'), hashlib.sha256).digest()
        kSigning = hmac.new(kTime, 'api_request'.encode('utf-8'), hashlib.sha256).digest()
        signature = hmac.new(kSigning, (toSign).encode('utf-8'), hashlib.sha256).hexdigest()

        authreq['headers']['Authorization'] = ','.join(['HMAC-SHA256', self.key_id, signed_headers, signature])
        authreq['headers']['Content-Type']='application/json'
        return authreq


    def post(self, path, query=None, data=None):
        authreq = self.auth('POST', path, query, data)
        url = "https://" + self.domain + path
        if query is not None:
            url += '?' + authreq['query']
        return requests.post(url, headers=authreq['headers'], data=json.dumps(data))


    def get(self, path, query=None):
        authreq = self.auth('GET', path, query)
        url = "https://" + self.domain + path
        if query is not None:
            url += '?' + authreq['query']
        return requests.get(url, headers=authreq['headers'])
