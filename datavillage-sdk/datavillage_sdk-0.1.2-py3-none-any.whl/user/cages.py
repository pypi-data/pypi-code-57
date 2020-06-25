import requests


class Cages:
    """
    This class provides you all services around cages.
    A secure, privacy enabled container environment to execute your algorithm


    Initiate the class

    ``from datavillage_sdk.user.cages import Cages``

    ``cage = Cages()``

    This provides an ``cage`` object
    which can then be used to call methods in this class

    """

    def __init__(self):
        super().__init__()

    def load_digital_profile(
        self, start_date, end_date, consent_receipt, user_access_token
    ):
        """Load a digital profile

        :param start_date: start date from to load data of a user in the cage
        :type start_date: date
        :param end_date: end date upto which to load data of a user in the cage
        :type end_date: date
        :param consent_receipt: consent_receipt ID
        :type consent_receipt: string
        :return: [description]
        :rtype: [type]
        """
        token = "Bearer" + user_access_token
        url = (
            "https://api.datavillage.me/cages/"
            + consent_receipt
            + "/importData?startDate="
            + start_date
            + "&endDate="
            + end_date
        )
        payload = {}
        headers = {"Content-Type": "application/json", "Authorization": token}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def query_digital_profile(self, query, user_access_token):
        """[summary]

        :param query: graphQL query to execute on the schema.
        :type query: string
        :param user_token: user_access_token
        :type user_token: string
        :return: [description]
        :rtype: [type]
        """
        token = "Bearer " + user_access_token
        url = "https://api.datavillage.me/query/graphql"
        payload = query
        headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
