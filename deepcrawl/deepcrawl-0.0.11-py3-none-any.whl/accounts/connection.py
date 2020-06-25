"""
Accounts Connection
===================
"""

from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .account import DeepCrawlAccount


class AccountConnection(ApiConnection):
    """
    ACCOUNT

        * endpoint: /accounts
        * http methods: GET, POST
        * methods: get_accounts, create_account

        - endpoint: /accounts/{account_id}
        - http methods: GET, PATCH, DELETE
        - methods: get_account, update_account, delete_account
    """

    def create_account(self, account_data):
        """Create account

        .. code-block::

            account_data = {
                "address_city": str,
                "address_street": str,
                "country": str,
                "custom_color_header": str,
                "limit_levels_max": int,
                "limit_pages_max": int,
                "custom_color_menu": str,
                "name": str,
                "phone": str,
                "address_zip": str,
                "pref_email_support": bool,
                "custom_domain": str,
                "address_state": str,
                "custom_support_email": str,
                "custom_support_phone": str,
                "timezone": str,
                "finance_vat": str,
                "splunk_enabled": bool,
                "active": bool
            }

        >>> connection.create_account(account_data)
        [0] DeepCrawlAccount

        :param account_data: account configuration
        :type account_data: dict
        :return: Account instance
        :rtype: DeepCrawlAccount
        """
        endpoint_url = get_api_endpoint(endpoint='accounts')
        response = self.dc_request(url=endpoint_url, method='post', json=account_data)
        return DeepCrawlAccount(account_data=response.json())

    def get_account(self, account_id):
        """Get account

        >>> connection.get_account(0)
        [0] DeepCrawlAccount

        :param account_id: account id
        :type account_id: int
        :return: requested instance
        :rtype: DeepCrawlAccount
        """
        endpoint_url = get_api_endpoint(endpoint='account', account_id=account_id)
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlAccount(account_data=response.json())

    def update_account(self, account_id, account_data):
        """Update account

        >>> connection.update_account("0", account_data)
        [0] DeepCrawlAccount

        :param account_id: account id
        :type account_id: int
        :param account_data: account configuration
        :type account_data: dict
        :return: Account instance
        :rtype: DeepCrawlAccount
        """
        endpoint_url = get_api_endpoint(endpoint='account', account_id=account_id)
        response = self.dc_request(url=endpoint_url, method='patch', json=account_data)
        return DeepCrawlAccount(account_data=response.json())

    def get_accounts(self, filters=None, **kwargs):
        """Get all accounts associated with the credentials used to generate the connection

        >>> connection.get_accounts()
        [[0] DeepCrawlAccount,
        [1] DeepCrawlAccount]

        :param filters: filters
        :type filters: dict
        :param kwargs: extra arguments, like pagination ones
        :type kwargs: dict
        :return: List of accounts
        :rtype: list
        """
        endpoint_url = get_api_endpoint(endpoint='accounts')
        accounts = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)

        list_of_accounts = []
        for account in accounts:
            list_of_accounts.append(
                DeepCrawlAccount(account_data=account)
            )
        return list_of_accounts
