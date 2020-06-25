from typing import Tuple

import requests
from flask import jsonify
from flask.wrappers import Response


def safe_get(json, key):
    if key in json:
        return json[key]
    else:
        return None


class RequestTool:
    def post(self, url, data=dict()):
        headers = {'Content-type': 'application/json'}
        return requests.post(url, json=data, headers=headers)

    # TODO every service should register self in registry service
    def register_me(self, service_name, port=5000):
        return self.post('http://registry/register', dict(service_name=service_name, port=port))


class ResponseTool:

    def __init__(self, default_headers=dict()):
        self.default_headers = default_headers

    def create(self, data: dict = None, status: int = 200, message: str = "", headers=dict()) -> \
            Tuple[Response, int]:
        """Wraps response in a consistent format throughout the API.

        Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
        Modifications included:
        - make success a boolean since there's only 2 values
        - make message a single string since we will only use one message per response

        IMPORTANT: data must be a dictionary where:
        - the key is the name of the type of data
        - the value is the data itself

        :param headers <dict> Dictionary of headers
        :param data <str> optional data
        :param status <int> optional status code, defaults to 200
        :param message <str> optional message
        :returns tuple of Flask Response and int
        """

        if type(data) is not dict and data is not None:
            raise TypeError("Data should be a dictionary 😞")

        # merge default headers with current
        headers = {**self.default_headers, **headers}
        res = {"success": 200 <= status < 300, "message": message, "result": data,
               "headers": headers}
        response = jsonify(res)
        response.status_code = status
        return response, status

    def copy(self, response, message=None):
        if response is not None:
            return self.create(data=response.json()["result"], status=response.status_code,
                               message=message if message else response.json()["message"])
        else:
            raise TypeError("Response should not be None")


req = RequestTool()
post = req.post
register_me = req.register_me

resp = ResponseTool()
create_response = resp.create
copy_response = resp.copy
