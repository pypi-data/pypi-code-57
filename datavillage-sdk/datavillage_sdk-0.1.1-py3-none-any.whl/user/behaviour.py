import requests


class Behaviour:
    """
    This class offers methods to manage a behaviours

    ``from datavillage_sdk.user.behaviour import Behaviour``

    ``behaviour = Behaviour()``

    """

    def __init__(self):
        super().__init__()

    def create_behaviour(
        self, user, consent_receipt_processing, behaviour, user_access_token
    ):
        """Create a new behaviour

        :param user: unique user identifier
        :type user: string
        :param consent_receipt_processing: consent receipt ID
        :type consent_receipt_processing: string
        :param behaviour: base64 encoded JSON-LD
        :type behaviour: base64
        :param user_access_token: user access token
        :type user_access_token: string
        :return: behaviour instance
        :rtype: object
        """
        token = "Bearer" + user_access_token
        url = (
            "https://api.datavillage.me/behaviors/"
            + user
            + "/"
            + consent_receipt_processing
        )
        payload = behaviour
        headers = {"Content-Type": "application/json", "Authorization": token}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def get_behaviour(self, user_id, consent_receipt, behaviour_id):
        """Get Behaviour

        :param user_id: unique user identifier
        :type user_id: string
        :param consent_receipt: consent receipt ID
        :type consent_receipt: string
        :param behaviour_id: behavior_id
        :type behaviour_id: string
        :return: behaviour instance
        :rtype: object
        """
        url = "https://api.datavillage.me/behaviors/{{user_id}}/{{consent_receipt}}/{{behavior_id}}"
        payload = {}
        headers = {"Content-Type": "application/json"}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def get_all_behaviour(self, user_id, consent_receipt_processing):
        """Get Behaviour

        :param user_id: unique user identifier
        :type user_id: string
        :param consent_receipt_processing: consent receipt
        :type consent_receipt: string
        :return: behaviour instance
        :rtype: object
        """
        url = "https://api.datavillage.me/behaviors/{{user_id}}/{{consent_receipt_processing}}"
        payload = {}
        headers = {"Content-Type": "application/json"}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response
