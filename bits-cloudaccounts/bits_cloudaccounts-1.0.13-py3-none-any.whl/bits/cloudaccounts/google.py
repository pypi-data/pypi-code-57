# -*- coding: utf-8 -*-
"""Cloud Accounts Google Class file."""


class Google:
    """Cloud Accounts Google Class."""

    def __init__(self):
        """Initialize a class instance."""

    # Billing Accounts
    def get_billing_account(self, billing_account_name):
        """Return a Billing Account from Google."""

    def get_billing_accounts(self):
        """Return a list of Billing Accounts from Google."""

    # Budgets
    def get_budget(self, billing_account_name, budget_name):
        """Return a Billing Account Budget from Google."""

    def get_budgets(self, billing_account_name):
        """Return a list of Billing Account Budgets from Google."""

    # Invoices
    def get_invoice(self, invoice_name):
        """Return an Invoice from a GCS Bucket."""

    def get_invoices(self):
        """Return a list of Invoice from a GCS Bucket."""
