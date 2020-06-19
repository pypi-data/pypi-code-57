import requests
import json


class AuthException(Exception):
    """Custom exception for authentication errors"""

    def __init__(self, message):
        self.message = message


class Client:
    """Client exposes the public api for sethealth"""

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def getToken(self):
        """getToken returns a new short-living token
        to be used by client side"""

        try:
            response = requests.post(
                url="https://api.set.health/token",
                headers={"Content-Type": "application/json; charset=utf-8"},
                data=json.dumps({"key": self.key, "secret": self.secret}),
            )
            if response.status_code != 200:
                raise AuthException("Bad auth")

            jsonContent = response.json()
            if "token" not in jsonContent:
                raise AuthException("Bad response")

            return jsonContent["token"]
        except requests.exceptions.RequestException:
            raise AuthException("Bad request")
