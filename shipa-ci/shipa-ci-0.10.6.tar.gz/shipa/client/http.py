import requests


class HttpClient(object):

    def post(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)

    def get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def put(self, url, **kwargs):
        return requests.put(url, **kwargs)


class MockClient(object):

    def __init__(self, response=None):
        self.response = response

    def post(self, url, **kwargs):
        return self.response

    def delete(self, url, **kwargs):
        return self.response

    def get(self, url, **kwargs):
        return self.response

    def put(self, url, **kwargs):
        return self.response


class MockResponse(object):

    def __init__(self, code=200, text=None):
        self.status_code = code
        self.text = text
