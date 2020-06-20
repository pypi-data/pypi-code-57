from os import environ
from collections import namedtuple
from urllib3.exceptions import InsecureRequestWarning
import asyncio

import requests
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

Result = namedtuple('Result', ('json'))

class CountOnce:
    DEFAULT_SCHEMA = "https"
    DEFAULT_DOMAIN = "countapi.com"
    
    def __init__(self, account_id: str, auth_token: str):
        self.account_id = account_id
        self.auth_token = auth_token
        
        schema = environ.get("_API_PROTOCOL") or self.DEFAULT_SCHEMA
        domain = environ.get("_API_DOMAIN") or self.DEFAULT_DOMAIN
        self.url = "{}://{}.{}".format(schema, self.account_id, domain)

    async def ping(self, ping_options: dict) -> Result:
        url_params = {}

        for (key, value) in ping_options.items():
            if key == "attributes":
                for attribute in ping_options[key].items():
                    url_params["{}[{}]".format(key, attribute[0])] = attribute[1]
            else:
                url_params[key] = value

        url_params["key"] = url_params.get("key") or ""
        url_params["unique_value"] = url_params.get("unique_value") or ""

        headers = {}
        if self.auth_token != "":
            headers["Authorization"] = "Bearer {}".format(self.auth_token)

        response = requests.post(
            self.url + "/ping",
            data = url_params,
            headers = headers,
            verify = False
        )

        return Result(response.json()) 
    
    async def query(self, key_name: str, query_type: str, query_options: dict = {}, iterator: int = None) -> Result:
        url_params = {}
        
        for (key, value) in query_options.items():
            if key == "filter":
                for fil in query_options[key].items():
                    url_params["{}[{}]".format(key, fil[0])] = fil[1]
            elif key == "include":
                if type(query_options[key]) is list:
                    query_options[key] = ",".join(query_options[key])
                url_params[key] = query_options[key]
            elif key == "metric":
                next
            else:
                url_params[key] = value

        headers = {}
        if self.auth_token != "":
            headers["Authorization"] = "Bearer {}".format(self.auth_token)

        metric = query_options.get("metric") or "daily"
        query_url = "{}/{}/{}/{}".format(self.url, query_type, key_name, metric)

        response = requests.get(
            query_url,
            params = url_params,
            headers = headers,
            verify = False
        )

        return Result(response.json())

    async def getUniques(self, key_name: str, query_options: dict = {}, iterator: int = None):
        return await self.query(key_name, "uniques", query_options, iterator)

    async def getIncrements(self, key_name: str, query_options: dict = {}, iterator: int = None):
        return await self.query(key_name, "increments", query_options, iterator)

    async def getRevenue(self, key_name: str, query_options: dict = {}, iterator: int = None):
        return await self.query(key_name, "revenue", query_options, iterator)

    async def getCombined(self, key_name: str, query_options: dict = {}, iterator: int = None):
        return await self.query(key_name, "combined", query_options, iterator)
