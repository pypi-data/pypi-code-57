#  © Copyright IBM Corporation 2020.

import requests as r
from ai_lifecycle_cli.lib.utils.AuthHandler import AuthHandler


class RESTClient():

    def __init__(self, host, auth):
        self.client = r.Session()
        self.host = host
        self.auth = AuthHandler(host, auth)
        self._setup_client()

    def _setup_client(self):
        self.client.verify = False

    def set_authorization(self):
        self.client.headers.update(self.auth.get_authorization_header())

    def make_request(self, method_name, path="", body={}, files=None, data=None, *args, **kwargs):
        self.set_authorization()
        full_url = "{}".format(self.host) + path

        methods = {
            'GET': self.client.get,
            'POST': self.client.post,
            'PUT': self.client.put,
            'DELETE': self.client.delete,
            'PATCH': self.client.patch,
            'HEAD': self.client.head
        }
        req = methods[method_name.upper()]

        if files is not None:
            res = req(
                url=full_url,
                files=files
            )
            return res

        elif data is not None:
            self.client.headers.update({
                "Content-Type": "application/zip"
            })
            res = req(
                url=full_url,
                data=data
            )
            self.client.headers.update({
                "Content-Type": "application/json"
            })
            return res
        else:
            if len(body) == 0:
                res = req(
                    url=full_url
                )
                return res
            else:
                res = req(
                    url=full_url,
                    json=body
                )
            return res
