import copy
from typing import Type

import requests
from pydantic import BaseModel

from tktl.core import utils, loggers as sdk_logger
from tktl.core.exceptions.exceptions import APIClientException
from tktl.core.managers.auth import AuthConfigManager


class API(object):
    DEFAULT_HEADERS = {
        "Accept": "application/json",
    }

    def __init__(self, api_url, headers=None, logger=sdk_logger.MuteLogger()):
        """

        :param str api_url: url you want to connect
        :param dict headers: headers
        :param str api_key: your API key
        :param str ps_client_name: Client name
        :param sdk_logger.Logger logger:
        """
        self.api_url = api_url
        headers = headers or self.DEFAULT_HEADERS
        self.headers = headers.copy()
        self.logger = logger
        self.api_key = AuthConfigManager.get_api_key()
        self.DEFAULT_HEADERS.update({"X-Api-Key": self.api_key})

    def get_path(self, url=None):
        if not url:
            return self.api_url
        full_path = utils.concatenate_urls(self.api_url, url)
        return full_path

    def post(self, url=None, json=None, params=None, files=None, data=None):
        path = self.get_path(url)
        headers = copy.deepcopy(self.DEFAULT_HEADERS)
        if data:
            headers["Content-Type"] = data.content_type

        self.logger.debug(
            "POST request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}\n\tfiles: {}\n\tdata: {}".format(
                path, headers, json, params, files, data
            )
        )
        response = requests.post(
            path, json=json, params=params, headers=headers, files=files, data=data
        )
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def put(self, url=None, json=None, params=None, data=None):
        path = self.get_path(url)
        self.logger.debug(
            "PUT request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}".format(
                path, self.headers, json, params
            )
        )
        response = requests.put(
            path, json=json, params=params, headers=self.DEFAULT_HEADERS, data=data
        )
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def patch(self, url=None, json=None, params=None, data=None):
        path = self.get_path(url)
        self.logger.debug(
            "PATCH request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}".format(
                path, self.headers, json, params
            )
        )
        response = requests.patch(
            path, json=json, params=params, headers=self.DEFAULT_HEADERS, data=data
        )
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def get(self, url=None, json=None, params=None):
        path = self.get_path(url)

        self.logger.debug(
            "GET request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}".format(
                path, self.headers, json, params
            )
        )
        response = requests.get(
            path, params=params, headers=self.DEFAULT_HEADERS, json=json
        )
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def delete(self, url=None, json=None, params=None):
        path = self.get_path(url)
        response = requests.delete(path, params=params, headers=self.headers, json=json)
        self.logger.debug(
            "DELETE request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}".format(
                response.url, self.headers, json, params
            )
        )
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response


class TaktileResponse(object):
    def __init__(self, body, code, headers, data):
        self.body = body
        self.code = code
        self.headers = headers
        self.data = data

    @property
    def ok(self):
        return 200 <= self.code < 400

    @classmethod
    def interpret_response(cls, response: requests.Response, model: Type[BaseModel]):
        """
        Parameters
        ----------
        response

        model
        """

        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise APIClientException(status_code=e.response.status_code, detail=repr(e))
        return model(**response.json())
