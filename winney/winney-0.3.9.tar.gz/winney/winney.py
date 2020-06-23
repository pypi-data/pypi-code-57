#coding:utf-8
import json
import chardet
import requests
import urllib.parse
from requests.utils import guess_json_utf


class Result(object):
    def __init__(self, resp=None, url=None, method=None):
        if resp and not isinstance(resp, requests.Response):
            raise Exception("resp should be object of requests.Response, but {} found.".format(type(resp)))
        self.status   = resp.ok
        self.reason   = resp.reason
        self.content  = resp.content
        self.headers  = resp.headers.__repr__()
        self.encoding = resp.encoding
        self.status_code = resp.status_code
        self.request_url = url
        self.request_method = method
        self.encoding = None
        # if not self.encoding:
        #     self.encoding = chardet.detect(self.content)["encoding"]


    def ok(self):
        return self.status
    
    def get_bytes(self):
        return self.content
    
    def get_text(self):
        """
        Quoted from: requests.models.text()
        """
        text = None
        if not self.encoding:
            self.encoding = chardet.detect(self.content)["encoding"]
        try:
            text = str(self.content, self.encoding, errors='replace')
        except (LookupError, TypeError):
            text = str(self.content, errors='replace')
        return text

    def get_json(self, **kwargs):
        """
        Quoted from: requests.models.json()
        """
        if not self.encoding:
            self.encoding = chardet.detect(self.content)["encoding"]
        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using chardet to make
            # a best guess).
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return json.loads(
                        self.content.decode(encoding), **kwargs
                    )
                except UnicodeDecodeError:
                    pass
        return json.loads(self.get_text(), **kwargs)
    
    def json(self, **kwargs):
        return self.get_json(**kwargs)
        


class Winney(object):

    def __init__(self, host, port=80, protocol="http", headers=None, base_path=""):
        self.host = host
        self.port = port
        self.headers = headers
        self.protocol = protocol
        self.base_path = base_path
        self.domain = ""
        self.build_domain()
        # self.domain = "{}://{}".format(protocol, host)
        # if port and port != 80:
        #     self.domain = self.domain+":"+str(port)
        self.RESULT_FORMATS = ["json", "unicode", "bytes"]
        self.result = {}
        self.apis = []

    def build_domain(self):
        self.domain = "{}://{}:{}".format(self.protocol, self.host, self.port)
    
    def _bind_func_url(self, url, method):
        def req(data=None, json=None, files=None, headers=None, **kwargs):
            if data and json:
                raise Exception("data 和 json 不可以同时存在")
            url2 = url.format(**kwargs)
            r = self.request(method, url2, data, json, files, headers)
            return Result(r, url2, method)
        return req
    
    def add_url(self, method, uri, function_name):
        method = method.upper()
        function_name = function_name.lower()
        if function_name in self.apis:
            raise Exception("Duplicate function_name, {}".format(function_name))
        # url = urllib.parse.urljoin(self.domain, uri)
        setattr(self, function_name, self._bind_func_url(uri, method))
        self.apis.append(function_name)
        return getattr(self, function_name)
    
    def register(self, method, name, uri):
        self.add_url(method, uri, name)
    
    def request(self, method, url, data=None, json=None, files=None, headers=None):
        url = "/".join([self.base_path, url]).replace("//", "/").replace("//", "/") \
                if self.base_path else url
        url = urllib.parse.urljoin(self.domain, url)
        if headers and isinstance(headers, dict):
            if self.headers:
                for key, value in self.headers.items():
                    if key in headers:
                        continue
                    headers[key] = value
        else:
            headers = self.headers
        if method.upper() == "GET":
            return self.get(url, data, headers=headers)
        if method.upper() == "POST":
            return self.post(url, data=data, json=json, files=files, headers=headers)
        if method.upper() == "PUT":
            return self.put(url, data=data, json=json, files=files, headers=headers)
        if method.upper() == "DELETE":
            return self.delete(url, data=data, headers=headers)

    def get(self, url, data=None, headers=None):
        assert url
        assert (not data or isinstance(data, dict))
        return requests.get(url, params=data, headers=headers)
    
    def post(self, url, data=None, json=None, files=None, headers=None):
        assert url
        assert (not data or isinstance(data, dict))
        assert (not json or isinstance(json, dict))
        return requests.post(url, data=data, json=json, files=files, headers=headers)
    
    def put(self, url, data=None, json=None, files=None, headers=None):
        assert url
        assert (not data or isinstance(data, dict))
        return requests.put(url, data, json=json, files=files, headers=headers)
    
    def delete(self, url, data=None, headers=None):
        assert url
        assert (not data or isinstance(data, dict))
        return requests.delete(url, data=data, headers=headers)
    
    def options(self, url, headers=None):
        assert url
        return requests.options(url, headers=headers)



if __name__ == "__main__":
    wy = Winney(host="www.baidu.com")
    wy.add_url(method="get", uri="/", function_name="download")
    r = wy.download()
    t = r.get_bytes()
    print(t)
