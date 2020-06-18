import requests
from datavillage_sdk.management.sources import Sources


class Consent:
    """
    This class provides the services around consent.
    - Create a new consent consent receipt
    - Manage privacy center
    - Check consent status

    Initiate the class

    ``from datavillage_sdk.management.consent import Consent``

    ``consent = Consent()``

    This provides an ``consent`` object
    which can then be used to call methods in this class
    """

    def __init__(self):
        super().__init__()

    def create_consent_receipt(
        self,
        app_token,
        name,
        description,
        purpose,
        duration,
        data_categories,
        data_sources,
        creator_name,
        creator_uri,
        creator_logo,
        behaviour_extracted_frequency,
    ):
        """Use this method to create consent receipt.
        
        :param app_token: application access token
        :type app_token: string
        :param name: name Name of the consent receipt
        :type name: string 
        :param description: description
        :type description: string
        :param purpose: purpose of the consent
        :type purpose: string
        :param duration: duration
        :type duration: string
        :param data_categories: data_categories
        :type data_categories: string
        :param data_sources: data_sources
        :type data_sources: array
        :param creator_name: creator_name
        :type creator_name: string
        :param creator_uri: creator_uri
        :type creator_uri: string
        :param creator_logo: creator_logo
        :type creator_logo: string
        :param behavior_extracted_frequency: behavior_extracted_frequency
        :type behavior_extracted_frequency: string
        :return: consent_receipt_processing
        :rtype: string
        """

        token = "Bearer" + app_token
        url = "https://api.datavillage.me/consentReceipts"
        sources = Sources().get_data_sources(app_token)
        source_id = []
        if data_sources in sources:
            source_id = sources["ID"]
        payload = {
            "name": name,
            "description": description,
            "purpose": purpose,
            "duration": duration,
            "data-categories": data_categories,
            "data-sources": source_id,
            "creator-name": creator_name,
            "creator-uri": creator_uri,
            "creator-logo": creator_logo,
            "behavior-extracted-frequency": behaviour_extracted_frequency,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def get_consent_receipt(self, consent_receipt_processing, app_token):
        """Use this to get consent receipt

        :param consent_receipt_processing: consent ID
        :type consent_receipt_processing: string
        :param app_token: application token
        :type app_token: string
        :return: consent receipt details
        :rtype: object
        """ """
        Use this end-point to get consent receipt.
        """
        token = "Bearer" + app_token
        url = (
            "https://api.datavillage.me/consentReceipts/"
            + consent_receipt_processing
            + "?consentReceiptChain=true"
        )
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def list_consent_receipts(self, app_token):
        """Get list of consent receipts created for your App

        :param app_token: application token
        :type app_token: string

        :return: [description]
        :rtype: [type]
        """
        token = "Bearer" + app_token

        url = "https://api.datavillage.me/consentReceipts/"
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def get_consent(self, consent_receipt_processing, user_access_token):
        """Create Consent based on the consent receipt

        :param consent_receipt_processing: consent ID
        :type consent_receipt_processing: string
        :param user_access_token: user access token
        :type user_access_token: string
        :return: [description]
        :rtype: [type]
        """
        user_token = "Bearer" + user_access_token
        url = (
            "https://api.datavillage.me/consents/"
            + consent_receipt_processing
            + "?consentChain=true"
        )
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": user_token,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def get_consent_history(self, userid, user_access_token):
        """Create Consent based on the consent receipt

        :param userid: unique user id
        :type userid: string
        :param user_access_token: user access token
        :type user_access_token: string
        :return: consent_history
        :rtype: object
        """
        token = "Bearer" + user_access_token
        url = "https://api.datavillage.me/consents/" + userid
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": token,
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
