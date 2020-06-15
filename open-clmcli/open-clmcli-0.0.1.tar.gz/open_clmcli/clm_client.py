# Copyright 2020 Maxime Terras <mterras@bouyguestelecom.fr>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import json
import base64


class CLMConnection(object):
    def _encode_b64(self, s):
        # Convert into byte type
        s_byte = s.encode("utf-8")
        # encode into base64 (in byte type)
        s_b64 = base64.urlsafe_b64encode(s_byte)
        # return into str type
        return s_b64.decode('utf-8')

    def _remove_final_slash(self, url):
        if url.endswith('/'):
            return url[:-1]
        else:
            return url

    def __init__(self, username, password,
                 api_nsp, api_clm, api_version, disable_proxy=False, proxy={},
                 debug=False, force_auth=False):
        
        self.base_nsp_url = '%s/rest-gateway/rest/api/v%s/' % (self._remove_final_slash(api_nsp), api_version)
        self.base_clm_url = '%s/license-manager/rest/api/v%s/' % (self._remove_final_slash(api_clm), api_version)
        self.username = username
        #  in byte
        auth_base64 = self._encode_b64(username + ":" + password)
        self.headers = {
            'Authorization': "Basic %s" % auth_base64,
            'Content-Type': "application/json",
        }
        self.debug = debug
        self.force_auth = force_auth
        if disable_proxy:
            self.proxies = {
                    "http": None,
                    "https": None
                    }
        else:
            if proxy:
                self.proxies = proxy
            else:
                self.proxies = None

    def _do_request(self, method, url, headers=None, params=None):
        import requests
        requests.packages.urllib3.disable_warnings()
        try:
            data = json.dumps(params) if params is not None else None
            if self.debug:
                print_headers = "# Headers:"
                for line in json.dumps(headers, indent=4).split('\n'):
                    print_headers += '\n#    %s' % line
                print('#####################################################')
                print('# Request')
                print('# Method: %s' % method)
                print('# URL: %s' % url)
                print(print_headers)
                print("# Parameters: %s" % data)
                print('#####################################################')
            response = requests.request(method, url, headers=headers,
                                        verify=False, timeout=10, data=data,
                                        proxies=self.proxies)
        except requests.exceptions.RequestException as error:
            print('Error: Unable to connect.')
            print('Detail: %s' % error)
            raise SystemExit(1)
        if self.debug:
            print_headers = "# Headers:"
            for line in json.dumps(dict(response.headers),
                                   indent=4).split('\n'):
                print_headers += '\n#    %s' % line
            print('# Response')
            print('# Status code: %s' % response)
            print(print_headers)
            print('# Body: %s' % response.text)
            print('#####################################################')
            print('')
        return response

    def _response(self, resp):
        if resp.status_code == 401:
            print('Error: Athentication failed. '
                  'Please verify your credentials.')
            raise SystemExit(1)
        if resp.status_code < 200 or resp.status_code >= 300:
            try:
                print('Error: %s' % resp.json()['errors'][0]
                      ['descriptions'][0]['description'])
                raise SystemExit(1)
            except ValueError:
                print('Unknown Error: CLM returns\n%s' % resp.text)
                raise SystemExit(1)
        if resp.text == '':
            return []
        return resp.json()

    def remove_extra_slash_url(func):
        def wrapper(self, url, *args, **kwargs):
            if url.startswith('/'):
                return func(self, url[1:], *args, **kwargs)
            else:
                return func(self, url, *args, **kwargs)
        return wrapper

    @remove_extra_slash_url
    def get(self, url, filter=None, headers={}):
        self.authenticate()
        h = self.headers.copy()
        h.update(headers)

        r = self._do_request('GET', self.base_clm_url + url,
                                 headers=h)
        return self._response(r)

    @remove_extra_slash_url
    def post(self, url, params, headers={}):
        self.authenticate()
        h = self.headers.copy()
        h.update(headers)
        r = self._do_request('POST', self.base_clm_url + url,
                             headers=h, params=params)
        return self._response(r)

    @remove_extra_slash_url
    def put(self, url, params, headers={}):
        self.authenticate()
        h = self.headers.copy()
        h.update(headers)
        r = self._do_request('PUT', self.base_clm_url + url,
                             headers=h, params=params)
        return self._response(r)

    @remove_extra_slash_url
    def delete(self, url):
        self.authenticate()
        r = self._do_request('DELETE', self.base_clm_url + url,
                             headers=self.headers)
        return self._response(r)

    def authenticate(self):
        import os
        import time

        data_dir = '%s/.clm' % os.path.expanduser("~")
        Token_file = data_dir + '/NSPToken'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        do_auth = False
        if os.path.exists(Token_file) and not self.force_auth:
            with open(Token_file) as data_file:
                token_session = json.load(data_file)
            # replay auth if expire
            if int(token_session['token_creation']) + token_session['expires_in'] < int(time.time()):
                do_auth = True

        else:
            do_auth = True

        if do_auth:
            body = { "grant_type": "client_credentials"}
            r = self._do_request('POST', self.base_nsp_url + 'auth/token',
                                 headers=self.headers, params=body)
            rjson = self._response(r)
            self.headers['Authorization'] = "Bearer %s" % rjson['access_token']
            token_session = {'access_token': rjson['access_token'],
                             'refresh_token': rjson['refresh_token'],
                             'expires_in': rjson['expires_in'],
                             'token_creation': time.time()}
            with open(Token_file, 'w') as data_file:
                json.dump(token_session, data_file)
        else:
            self.headers['Authorization'] = "Bearer %s" % token_session['access_token']

