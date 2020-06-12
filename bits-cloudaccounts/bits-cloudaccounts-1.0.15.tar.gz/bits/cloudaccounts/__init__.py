# -*- coding: utf-8 -*-
"""CloudAccounts class file."""

import requests

# from .amazon import Amazon
# from .api import API
# from .bitsdb import BITSdb
from .firestore import Firestore
# from .google import Google


class CloudAccounts(object):
    """CloudAccounts class."""

    def __init__(
        self,
        google,
        host='cloudaccounts.broadapis.org',
    ):
        """Initialize an CloudAccounts class instance."""
        self.host = host
        self.google = google
        self.verbose = google.verbose

        # set API base url
        self.base_url = 'https://%s' % (host)

        # get id token
        self.google.auth_service_account()
        self.token = self.get_id_token()

        # set requests params
        self.params = {
            'key': self.google.api_key,
        }

        # set request headers
        self.headers = {
            'Authorization': 'Bearer %s' % (self.token),
            'Content-type': 'application/json',
        }

    # def amazon(self):
    #     """Return an Amazon instance."""
    #     return Amazon()

    # def api(self):
    #     """Return an API instance."""
    #     return API()

    # def bitsdb(self):
    #     """Return an BITSdb instance."""
    #     return BITSdb()

    def firestore(self):
        """Return an Firestore instance."""
        return Firestore()

    # def google(self):
    #     """Return an Google instance."""
    #     return Google()

    def get(self, path):
        """Return a response to a get request."""
        url = '%s/%s' % (self.base_url, path)
        return requests.get(
            url,
            headers=self.headers,
            params=self.params
        )

    def get_id_token(self):
        """Return a Google ID token."""
        return self.google.iamcredentials().generate_id_token(
            serviceAccount=self.google.service_account_email,
            audience=self.host,
            delegates=[self.google.service_account_email],
            include_email=True,
        )

    def post(self, path, body):
        """Return a response to a post request."""
        url = '%s/%s' % (self.base_url, path)
        return requests.post(
            url,
            headers=self.headers,
            params=self.params,
            json=body,
        )

    # Accounts
    def update_accounts(self):
        """Update Accounts."""
        return self.get('/accounts/update').text

    def remove_google_cost_object(self, body):
        """Remove the cost object from a google billing account."""
        return self.post('/accounts/update_google_cost_object', body).text

    # Amazon Accounts
    def get_amazon_accounts(self):
        """Return a list of Amazon Accounts."""
        return self.get('/amazon/accounts').json()

    def update_amazon_accounts(self):
        """Update Amazon Accounts."""
        return self.get('/amazon/accounts/update').text

    # Cost Objects
    # def get_cost_object(self, co):
    #     """Return a cost object with details."""

    def get_cost_objects(self):
        """Return a list of Cost Objects."""
        return self.get('/costObjects').json()

    def update_cost_objects(self):
        """Update Cost Objects."""
        return self.get('/costObjects/update').text

    # Google Billing Accounts
    def check_google_billing_accounts(self):
        """Check Google Billing Accounts."""
        return self.get('/google/billingAccounts/check').text

    def update_google_billing_accounts(self):
        """Update Google Billing Accounts."""
        return self.get('/google/billingAccounts/update').text

    def update_google_billing_accounts_iam_policy(self):
        """Update Google Billing Accounts IAM Policy."""
        return self.get('/google/billingAccounts/update:iamPolicy').text

    def update_google_billing_accounts_projects(self):
        """Update Google Billing Accounts Projects."""
        return self.get('/google/billingAccounts/update:projects').text

    # Google Budgets
    def check_google_budgets(self):
        """Check Google Budgets."""
        return self.get('/google/budgets/check').text

    def get_google_budget(self, body):
        """Return a budget from Google."""
        return self.post('/google/budgets/get', body).text

    def update_google_budgets(self):
        """Update Google Budgets."""
        return self.get('/google/budgets/update').text

    # Google Budget Notifications
    def update_google_budget_notifications(self):
        """Update Google Budget Notifications."""
        return self.get('/google/budgets/notifications/update').text

    # Google Invoices
    def update_google_invoices(self):
        """Update Google Invoices."""
        return self.get('/google/invoices/update').text

    # Sheets
    def update_amazon_sheet(self):
        """Update Amazon Sheet."""
        return self.get('/amazon/accounts/update:sheet').text

    def update_costobjects_sheet(self):
        """Update Splits Sheet."""
        return self.get('/costObjects/update:sheet').text

    def update_google_sheet(self):
        """Update Google Sheet."""
        return self.get('/google/billingAccounts/update:sheet').text

    def update_splits_sheet(self):
        """Update Splits Sheet."""
        return self.get('/splits/update:sheet').text
