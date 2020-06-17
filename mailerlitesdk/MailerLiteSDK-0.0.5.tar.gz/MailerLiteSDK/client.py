import requests
import json
from .exceptions import MailerLiteApiError
DEFAULT_TIMEOUT = 3


class MailerClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_endpoint = "https://api.mailerlite.com/api/v2"
        self.headers = {
            'content-type': "application/json",
            'x-mailerlite-apikey': self.api_key
        }

    def get_group_id(self, group_name):
        response = requests.get(self.api_endpoint + "/groups", headers=self.headers, timeout=DEFAULT_TIMEOUT)
        # print(r.text)
        self.__check_error(response)
        results = json.loads(response.text)
        for result in results:
            if result.get('name') == group_name:
                print(result.get('id'))
                group_id = result.get('id')
                return group_id

        return None

    # status:
    def change_user_status(self, email, status='active'):
        """
        :param email: user's email
        :param status: (optional) active or unsubscribed
        :return: dict
        """
        url = self.api_endpoint + '/subscribers/' + str(email)
        data = {"type": status}
        payload = json.dumps(data)
        response = requests.request("PUT", url, data=payload, headers=self.headers, timeout=DEFAULT_TIMEOUT)
        print(response.text)
        self.__check_error(response)
        return {"status_code": response.status_code, "body": response.json()}


    def subscribe(self, email, name=None, other_fields={}):
        """
        :param email: user's email
        :param name: user's name
        :param other_fields: "company", "country", "city", "phone", "state", "zip", "industry"
        :return:
        """
        url = self.api_endpoint + '/subscribers'

        data = {
            'name': name,
            'email': email,
            'fields': other_fields
        }

        payload = json.dumps(data)

        response = requests.request("POST", url, data=payload, headers=self.headers, timeout=DEFAULT_TIMEOUT)

        result = response.json()
        if 'error' in result:
            if result['error'].get('code') == 400:
                self.change_user_status(email, status='active')
                response = requests.request("POST", url, data=payload, headers=self.headers, timeout=DEFAULT_TIMEOUT)

        return {"status_code": response.status_code, "body": response.json()}

    def join_group(self, email, group_id=None, group_name=None):
        if group_id is None:
            group_id = self.get_group_id(group_name=group_name)

        url = self.api_endpoint + f'''/groups/{group_id}/subscribers'''

        data = {
            'email': email,
        }

        payload = json.dumps(data)

        response = requests.request("POST", url, data=payload, headers=self.headers, timeout=DEFAULT_TIMEOUT)

        self.__check_error(response)
        print(response.text)
        return {"status_code": response.status_code, "body": response.json()}

    @staticmethod
    def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            raise MailerLiteApiError(status_code=response.status_code,
                                     headers=dict(response.headers.items()),
                                     error=response.json())
