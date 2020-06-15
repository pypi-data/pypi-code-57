import json
import requests

class Client:
    def __init__(self, base_url, username, password):
        self.session = requests.Session()
        if base_url.endswith("/"):
            self.base_url = base_url[:-1]
        else:
            self.base_url = base_url
        self.username = username
        self.password = password
        self.session.auth = (username, password)
    
    def url(self, resource_path):
        if not resource_path.startswith("/"):
            resource_path = "/" + resource_path
        return self.base_url + resource_path

    def get(self, resource_path, **kwargs):
        return self.session.get(self.url(resource_path), **kwargs)
    
    def post(self, resource_path, data=None, **kwargs):
        return self.session.post(self.url(resource_path), data, **kwargs)
    
    def getCrumb(self):
        data = json.loads(self.get("/crumbIssuer/api/json").text)
        crumb = data['crumb']
        return crumb