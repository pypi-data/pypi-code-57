# -*- coding: utf-8 -*-
"""Tests for Firestore class."""

import unittest
from unittest.mock import patch

from bits.cloudaccounts import firestore


class TestFirestore(unittest.TestCase):
    """Test Firestore class."""

    def setUp(self):
        """Set up the tests."""
        self.action_name = "notify-slack-channel-cloudaccounts"
        self.amazon_account_name = "374741154730"
        self.billing_account_name = "00A539-93294F-AC9B6F"
        self.budget_name = "XHCVHIQYECSFQJI2QSVXVGKEJ4000000"
        self.cost_object = "1550167"
        self.email = "karlsson@broadinstitute.org"
        self.trigger_name = "BjLsyldJsKWpcMYGwuBT"
        self.webhook_name = "notify-slack-webhook"

    @patch.dict("os.environ", {"GCP_PROJECT": "broad-cloudaccounts-app-dev"}, clear=True)
    def test_gcp_project(self):
        """Test __init__() with GCP_PROJECT."""
        fs = firestore.Firestore()
        self.assertTrue(fs)

    @patch.dict("os.environ", {"GOOGLE_CLOUD_PROJECT": "broad-cloudaccounts-app-dev"}, clear=True)
    def test_google_cloud_project(self):
        """Test __init__() with GOOGLE_CLOUD_PROJECT."""
        fs = firestore.Firestore()
        self.assertTrue(fs)

    def test_get_account(self):
        """Test get_account()."""
        fs = firestore.Firestore()
        account = fs.get_account(self.amazon_account_name)
        self.assertIsInstance(account, dict)
        print(account)

    def test_get_accounts(self):
        """Test get_accounts()."""
        fs = firestore.Firestore()
        accounts = fs.get_accounts()
        self.assertIsInstance(accounts, list)
        print(f"Found {len(accounts)} accounts in Firestore.")

    def test_get_accounts_by_id(self):
        """Test get_accounts_by_id()."""
        fs = firestore.Firestore()
        accounts = fs.get_accounts_by_id([self.billing_account_name])
        self.assertIsInstance(accounts, list)
        print(f"Found {len(accounts)} accounts in Firestore.")

    def test_get_accounts_dict(self):
        """Test get_accounts_dict()."""
        fs = firestore.Firestore()
        accounts = fs.get_accounts_dict()
        self.assertIsInstance(accounts, dict)
        print(f"Found {len(accounts)} accounts in Firestore.")

    def test_get_action(self):
        """Test get_action()."""
        fs = firestore.Firestore()
        action = fs.get_action(self.action_name)
        self.assertIsInstance(action, dict)
        print(action)

    def test_get_actions(self):
        """Test get_actions()."""
        fs = firestore.Firestore()
        actions = fs.get_actions()
        self.assertIsInstance(actions, list)
        print(f"Found {len(actions)} actions in Firestore.")

    def test_get_amazon_account(self):
        """Test get_amazon_account()."""
        fs = firestore.Firestore()
        amazon_account = fs.get_amazon_account(self.amazon_account_name)
        self.assertIsInstance(amazon_account, dict)
        print(amazon_account)

    def test_get_amazon_accounts(self):
        """Test get_amazon_accounts()."""
        fs = firestore.Firestore()
        amazon_accounts = fs.get_amazon_accounts()
        self.assertIsInstance(amazon_accounts, list)
        print(f"Found {len(amazon_accounts)} Amazon accounts in Firestore.")

    def test_save_action(self):
        """Test save_action()."""
        fs = firestore.Firestore()
        action_name = "fake-action"
        action = {"name": action_name}
        print(fs.save_action(action_name, action))
        print(fs.delete_action(action_name))

    def test_get_azure_accounts(self):
        """Test get_azure_accounts()."""
        fs = firestore.Firestore()
        azure_accounts = fs.get_azure_accounts()
        self.assertIsInstance(azure_accounts, list)
        print(f"Found {len(azure_accounts)} Azure accounts in Firestore.")

    def test_get_active_cost_objects(self):
        """Test get_active_cost_objects()."""
        fs = firestore.Firestore()
        cost_objects = fs.get_active_cost_objects()
        self.assertIsInstance(cost_objects, dict)
        print(f"Found {len(cost_objects)} active cost objects in Firestore.")

    def test_get_available_google_cost_objects(self):
        """Test get_available_google_cost_objects()."""
        fs = firestore.Firestore()
        cost_objects = fs.get_available_google_cost_objects()
        self.assertIsInstance(cost_objects, list)
        print(f"Found {len(cost_objects)} available cost objects in Firestore.")

    def test_get_cost_object(self):
        """Test get_cost_object()."""
        fs = firestore.Firestore()
        cost_object = fs.get_cost_object(self.cost_object)
        self.assertIsInstance(cost_object, dict)
        print(cost_object)

    def test_get_cost_objects(self):
        """Test get_cost_objects()."""
        fs = firestore.Firestore()
        cost_objects = fs.get_cost_objects()
        self.assertIsInstance(cost_objects, list)
        print(f"Found {len(cost_objects)} cost objects in Firestore.")

    def test_get_cost_objects_dict(self):
        """Test get_cost_objects_dict()."""
        fs = firestore.Firestore()
        cost_objects = fs.get_cost_objects_dict()
        self.assertIsInstance(cost_objects, dict)
        print(f"Found {len(cost_objects)} cost objects in Firestore.")

    def test_get_google_billing_account(self):
        """Test get_google_billing_account()."""
        fs = firestore.Firestore()
        account = fs.get_google_billing_account(self.billing_account_name)
        self.assertIsInstance(account, dict)
        print(account)

    def test_get_google_billing_accounts(self):
        """Test get_google_billing_accounts()."""
        fs = firestore.Firestore()
        google_billing_accounts = fs.get_google_billing_accounts()
        self.assertIsInstance(google_billing_accounts, list)
        print(f"Found {len(google_billing_accounts)} Google billing accounts in Firestore.")

    def test_get_google_billing_accounts_dict(self):
        """Test get_google_billing_accounts_dict()."""
        fs = firestore.Firestore()
        google_billing_accounts = fs.get_google_billing_accounts_dict()
        self.assertIsInstance(google_billing_accounts, dict)
        print(f"Found {len(google_billing_accounts)} Google billing accounts in Firestore.")

    def test_get_unused_google_billing_accounts(self):
        """Test get_unused_google_billing_accounts()."""
        fs = firestore.Firestore()
        google_billing_accounts = fs.get_unused_google_billing_accounts()
        self.assertIsInstance(google_billing_accounts, list)
        print(f"Found {len(google_billing_accounts)} Google billing accounts in Firestore.")

    def test_get_google_budget(self):
        """Test get_google_budget()."""
        fs = firestore.Firestore()
        budget = fs.get_google_budget(self.billing_account_name, self.budget_name)
        self.assertIsInstance(budget, dict)
        print(budget)

    def test_get_google_budget_notifications(self):
        """Test get_google_budget_notifications()."""
        fs = firestore.Firestore()
        google_budget_notifications = fs.get_google_budget_notifications()
        self.assertIsInstance(google_budget_notifications, list)
        print(f"Found {len(google_budget_notifications)} Google budget notifications in Firestore.")

    def test_get_google_budget_notifications_by_budget_id(self):
        """Test get_google_budget_notifications_by_budget_id()."""
        fs = firestore.Firestore()
        google_budget_notifications = fs.get_google_budget_notifications_by_budget_id()
        self.assertIsInstance(google_budget_notifications, dict)
        print(f"Found {len(google_budget_notifications)} Google budget notifications in Firestore.")

    def test_get_google_budgets_by_account(self):
        """Test get_google_budgets_by_account()."""
        fs = firestore.Firestore()
        accounts = fs.get_google_budgets_by_account()
        self.assertIsInstance(accounts, dict)
        print(f"Found {len(accounts)} accounts with budgets in Firestore.")

    def test_get_google_budgets_group(self):
        """Test get_google_budgets()."""
        fs = firestore.Firestore()
        budgets = fs.get_google_budgets()
        self.assertIsInstance(budgets, list)
        print(f"Found {len(budgets)} budgets in Firestore.")

    def test_get_google_budgets(self):
        """Test get_google_budgets()."""
        fs = firestore.Firestore()
        budgets = fs.get_google_budgets(self.billing_account_name)
        self.assertIsInstance(budgets, list)
        print(f"Found {len(budgets)} budgets for {self.billing_account_name} in Firestore.")

    def test_get_google_invoice(self):
        """Test get_google_invoice()."""
        fs = firestore.Firestore()
        invoice = fs.get_google_invoice("2020-01-31")
        self.assertIsInstance(invoice, dict)
        print(invoice)

    def test_get_google_invoices(self):
        """Test get_google_invoices()."""
        fs = firestore.Firestore()
        invoices = fs.get_google_invoices()
        self.assertIsInstance(invoices, list)
        print(f"Found {len(invoices)} Google invoices in Firestore.")

    def test_get_iam_policy_bindings(self):
        """Test get_iam_policy_bindings()."""
        fs = firestore.Firestore()
        iam_policy_bindings = fs.get_iam_policy_bindings(self.billing_account_name)
        self.assertIsInstance(iam_policy_bindings, list)
        print(f"Found {len(iam_policy_bindings)} IAM policy bindings for {self.billing_account_name} in Firestore.")

    def test_get_projects(self):
        """Test get_projects()."""
        fs = firestore.Firestore()
        projects = fs.get_projects(self.billing_account_name)
        self.assertIsInstance(projects, list)
        print(f"Found {len(projects)} projects for {self.billing_account_name} in Firestore.")

    def test_get_trigger(self):
        """Test get_google_trigger()."""
        fs = firestore.Firestore()
        trigger = fs.get_trigger(self.trigger_name)
        self.assertIsInstance(trigger, dict)
        print(trigger)

    def test_get_triggers(self):
        """Test get_triggers()."""
        fs = firestore.Firestore()
        triggers = fs.get_triggers()
        self.assertIsInstance(triggers, list)
        print(f"Found {len(triggers)} triggers in Firestore.")

    def test_save_trigger(self):
        """Test save_trigger()."""
        fs = firestore.Firestore()
        trigger = {"name": "my-trigger"}
        _, doc = fs.save_trigger(trigger)
        print(fs.delete_trigger(doc.id))

    def test_get_user_amazon_accounts(self):
        """Test get_user_amazon_accounts()."""
        fs = firestore.Firestore()
        accounts = fs.get_user_amazon_accounts(self.email)
        self.assertIsInstance(accounts, list)
        print(f"Found {len(accounts)} user Amazon accounts in Firestore.")

    def test_get_user_google_billing_accounts(self):
        """Test get_user_google_billing_accounts()."""
        fs = firestore.Firestore()
        accounts = fs.get_user_google_billing_accounts(self.email)
        self.assertIsInstance(accounts, list)
        print(f"Found {len(accounts)} Google billing accounts in Firestore.")

    def test_get_webhook(self):
        """Test get_google_webhook()."""
        fs = firestore.Firestore()
        webhook = fs.get_webhook(self.webhook_name)
        self.assertIsInstance(webhook, dict)
        print(webhook)

    def test_get_webhooks(self):
        """Test get_google_webhooks()."""
        fs = firestore.Firestore()
        webhooks = fs.get_webhooks()
        self.assertIsInstance(webhooks, list)
        print(f"Found {len(webhooks)} webhooks in Firestore.")

    def test_save_webhook(self):
        """Test save_webhook()."""
        fs = firestore.Firestore()
        webhook_name = "fake-webhook"
        webhook = {"name": webhook_name}
        print(fs.save_webhook(webhook_name, webhook))
        print(fs.delete_webhook(webhook_name))
