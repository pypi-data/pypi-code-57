import requests


class Authentication:
    """
    This class provides you all authentication based services.

    Initiate the class

    ``from datavillage_sdk.management.auth import Authentication``

    ``auth = Authentication()``

    This provides an ``auth`` object
    which can then be used to call methods in this class

    """

    def __init__(self):
        super().__init__()
        self.url = "https://api.datavillage.me/oauth/token"

    def get_application_token(self, clientid, clientsecret):
        """Use your client id and client secret,
        generated at https://developer.datavillage.me

        :param clientid: clientid from developer portal
        :type clientid: string
        :param clientsecret: your application secret
        :type clientsecret: string
        :return: access token object
        :rtype: object
        """
        payload = "client_id=" + clientid + "&client_secret=" + clientsecret
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        return response
