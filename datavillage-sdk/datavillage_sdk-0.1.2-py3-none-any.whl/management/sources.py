import requests


class Sources:
    """
    This class provides you all authentication based services.

    Initiate the class

    ``from datavillage_sdk.management.sources import Sources``

    ``sources = Sources()``

    This provides an ``auth`` object
    which can then be used to call methods in this class

    """

    def __init__(self):
        super().__init__()
        self.url = "https://api.datavillage.me/sources/"

    def get_data_sources(self, app_token):
        """Use your client id and client secret,
        generated at https://developer.datavillage.me

        :param clientid: clientid from developer portal
        :type clientid: string
        :param clientsecret: your application secret
        :type clientsecret: string
        :return: access token object
        :rtype: object
        """
        token = "Bearer" + app_token
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)
        return response
