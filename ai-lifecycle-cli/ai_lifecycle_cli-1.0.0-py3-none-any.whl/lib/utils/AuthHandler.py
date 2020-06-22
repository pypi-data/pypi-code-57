#  © Copyright IBM Corporation 2020.

import requests
import jwt
from datetime import datetime as dt


class AuthHandler:

    def __init__(self, url, auth):
        self.url = url
        self.token = None
        self.token_expire_at = 0
        self.token_refresh = True
        self.apikey = None
        self.user = None
        self.password = None

        if "token" in auth:
            self.token = auth['token']
            self.token_refresh = False
        elif "iam_apikey" in auth:
            self.apikey = auth['iam_apikey']
        else:
            self.user = auth[0]
            self.password = auth[1]

    def get_token(self):
        """
        Retrieves authorization token and refreshes if needed/possible.

        :return: Bearer token
        """
        if self.token_refresh:
            if dt.utcfromtimestamp(self.token_expire_at) < dt.utcnow() or self.token is None:
                if self.apikey is not None:
                    iam_token_url = "https://iam.cloud.ibm.com/identity/token"
                    iam_token_params = {
                        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                        "apikey": self.apikey
                    }
                    token_res = requests.post(
                        iam_token_url,
                        params=iam_token_params
                    )
                else:
                    token_res = requests.get(
                        self.url + "/v1/preauth/validateAuth",
                        auth=(self.user, self.password),
                        verify=False
                    )
                if token_res.ok:
                    self.token = token_res.json().get('accessToken')
                    self.token_expire_at = jwt.decode(self.token, verify=False).get('exp', '0')
                else:
                    raise Exception("Cannot generate token!\n Reason:\n{}".format(token_res.text))
        return self.token

    def get_authorization_header(self):
        """
        Returns authorization header with valid token

        :return: HTTP Authorization Header
        """
        return {
            "Authorization": "Bearer " + self.get_token()
        }
