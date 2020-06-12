# -*- coding: utf-8 -*-
"""Cloud Accounts Firestore Class file."""

import datetime
import os

from bits.google.services.firestore import Firestore as FirestoreBase
from google.cloud import firestore


class Firestore(FirestoreBase):
    """Cloud Accounts Firestore Class."""

    def __init__(self, project=None, credentials=None):
        """Initialize a class instance."""
        if not project:
            project = os.environ.get("GCP_PROJECT")
        if not project:
            project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.db = firestore.Client(project=project)
        self.firestore = firestore

    #
    # accounts
    #
    def get_account(self, name):
        """Return a single account."""
        return self.db.collection("accounts").document(name).get().to_dict()

    def get_accounts(self):
        """Return a list of Accounts from Firestore."""
        return self.get_collection("accounts")

    def get_accounts_by_id(self, account_ids):
        """Return a list of accounts by id."""
        references = []
        for account_id in account_ids:
            ref = self.db.collection("accounts").document(account_id)
            references.append(ref)
        accounts = []
        for doc in self.db.get_all(references):
            if doc.exists:
                accounts.append(doc.to_dict())
        return accounts

    def get_accounts_dict(self):
        """Return a dict of Accounts from Firestore."""
        return self.get_collection_dict("accounts")

    #
    # actions
    #
    def delete_action(self, name):
        """Save a single action."""
        return self.db.collection("actions").document(name).delete()

    def get_action(self, name):
        """Return a single action."""
        return self.db.collection("actions").document(name).get().to_dict()

    def get_actions(self):
        """Return a list of actions."""
        return self.get_collection("actions")

    def save_action(self, name, action):
        """Save a single action."""
        return self.db.collection("actions").document(name).set(action)

    #
    # amazon accounts
    #
    def get_amazon_account(self, name):
        """Return a list of Amazon Accounts from Firestore."""
        return self.db.collection("amazon_accounts").document(name).get().to_dict()

    def get_amazon_accounts(self):
        """Return a list of Amazon Accounts from Firestore."""
        return self.get_collection("amazon_accounts")

    #
    # azure accounts
    #
    def get_azure_accounts(self):
        """Return a list of Azure Accounts."""
        return self.get_collection("azure_accounts")

    #
    # cost objects
    #
    def get_active_cost_objects(self):
        """Return a dict of active cost objects."""
        cost_objects = self.get_cost_objects_dict()
        active = {}
        for a in self.get_accounts():
            # skip accounts that are not active
            if a["status"] not in ["open", "ACTIVE"]:
                continue
            # get a list of cost objects for this account
            cos = []
            if "split" in a:
                for co in a["split"]:
                    cos.append(co)
            if "cost_object" in a and a["cost_object"]:
                co = a["cost_object"]
                cos.append(co)
            # add cos to active dict
            for co in set(cos):
                if co not in active:
                    if co not in cost_objects:
                        print("ERROR: No such Cost Object: %s" % (co))
                        continue
                    active[co] = cost_objects[co]
                    active[co]["accounts"] = []
                active[co]["accounts"].append(a)
        return active

    def get_available_google_cost_objects(self, cost_object=None):
        """Return a list of cost objects available for Google accounts."""
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # get all cost objects
        all_cost_objects = self.get_cost_objects()

        # get cost objects used for google accounts
        google_cost_objects = self.get_google_cost_objects()

        # create a list of available cost objects
        cost_objects = []
        for co in all_cost_objects:
            # if cost object is specified, include it in the list
            if cost_object and co["costobject"] == cost_object:
                cost_objects.append(co)
                continue

            # skip expired cost objects as they should not be used
            if co["end_date"] and co["end_date"] < today:
                continue

            # skip cost objects that are already used
            if co["costobject"] in google_cost_objects:
                continue

            cost_objects.append(co)

        return cost_objects

    def get_cost_object(self, cost_object):
        """Return a list of cost objects."""
        return self.db.collection("cost_objects").document(cost_object).get().to_dict()

    def get_cost_objects(self):
        """Return a list of Cost Objects from Firestore."""
        return self.get_collection("cost_objects")

    def get_cost_objects_dict(self):
        """Return a list of Cost Objects from Firestore."""
        return self.get_collection_dict("cost_objects")

    def get_google_cost_objects(self):
        """Return a dict of cost objects linked to Google accounts."""
        accounts = self.get_accounts()
        cost_objects = {}
        for a in accounts:
            if a.get("type") != "google":
                continue
            cost_object = a.get("cost_object")
            if cost_object:
                if cost_object not in cost_objects:
                    cost_objects[cost_object] = []
                cost_objects[cost_object].append(a)
            elif "Disabled Broad Institute - " in a["display_name"]:
                num = a["display_name"].replace("Disabled Broad Institute - ", "").split(" ")[0]
                if num not in cost_objects:
                    cost_objects[num] = []
                cost_objects[num].append(a)
        return cost_objects

    #
    # google billing accounts
    #
    def get_google_billing_account(self, billing_account_name, full=True):
        """Return a Google Billing Account from Firestore."""
        ref = self.db.collection("google_billing_accounts").document(billing_account_name)

        # get account
        account = ref.get().to_dict()

        # return the base account info if we don't want the subrecords
        if not full:
            return account

        # add budgets
        account["budgets"] = []
        for doc in ref.collection("budgets").stream():
            account["budgets"].append(doc.to_dict())

        # add iam policy bindings
        account["iam_policy_bindings"] = []
        for doc in ref.collection("iam_policy_bindings").stream():
            account["iam_policy_bindings"].append(doc.to_dict())

        # add projects
        account["projects"] = []
        for doc in ref.collection("projects").stream():
            account["projects"].append(doc.to_dict())

        return account

    def get_google_billing_accounts(self):
        """Return a list of Google Billing Accounts from Firestore."""
        return self.get_collection("google_billing_accounts")

    def get_google_billing_accounts_dict(self):
        """Return a dict of Google Billing Accounts from Firestore."""
        return self.get_collection_dict("google_billing_accounts")

    def get_unused_google_billing_accounts(self):
        """Return a list of unused google billing accounts."""
        accounts = self.get_collection("google_billing_accounts")
        unused = []
        for a in sorted(accounts, key=lambda x: x["displayName"]):
            displayName = a["displayName"]
            if "Disabled Broad Institute - 0" in displayName:
                unused.append(a)
        return unused

    #
    # google budget notifications
    #
    def get_google_budget_notifications(self):
        """Return a list of Google Budget Notifiations from Firestore."""
        return self.get_collection("google_budget_notifications")

    def get_google_budget_notifications_by_budget_id(self, notifications=None):
        """Return a dict of google budget notifications by billing account."""
        if not notifications:
            notifications = self.get_google_budget_notifications()
        accounts = {}
        for budget in notifications:
            budget_id = budget["budget_id"]
            accounts[budget_id] = budget
        return accounts

    #
    # google budgets (under google_billing_accounts)
    #
    def delete_google_budget(self, billing_account_name, budget_name):
        """Return a Google Billing Budget from Firestore."""
        ref = self.db.collection("google_billing_accounts").document(billing_account_name)
        return ref.collection("budgets").document(budget_name).delete()

    def get_google_budget(self, billing_account_name, budget_name):
        """Return a Google Billing Budget from Firestore."""
        ref = self.db.collection("google_billing_accounts").document(billing_account_name)
        return ref.collection("budgets").document(budget_name).get().to_dict()

    def get_google_budgets(self, billing_account_name=None):
        """Return a list of Google Billing Account Budgets from Firestore."""
        if billing_account_name:
            collection = f"google_billing_accounts/{billing_account_name}/budgets"
            budgets = self.get_collection(collection)
        else:
            budgets = self.get_collection_group("budgets")
        # assemble budgets with billing_account_id and budget_id
        google_budgets = []
        for budget in budgets:
            _, billing_account_id, _, budget_id = budget["name"].split("/")
            budget["billing_account_id"] = billing_account_id
            budget["budget_id"] = budget_id
            google_budgets.append(budget)
        return google_budgets

    def get_google_budgets_by_account(self, budgets=None):
        """Return a dict of google budgets by billing account."""
        if not budgets:
            budgets = self.get_google_budgets()
        accounts = {}
        for budget in budgets:
            billing_account_id = budget["billing_account_id"]
            if billing_account_id not in accounts:
                accounts[billing_account_id] = []
            accounts[billing_account_id].append(budget)
        return accounts

    #
    # google invoices
    #
    def get_google_invoice(self, date):
        """Return a single google invoice."""
        return self.db.collection("google_invoices").document(date).get().to_dict()

    def get_google_invoices(self):
        """Return a list of Google Invoices from Firestore."""
        return self.get_collection("google_invoices")

    #
    # iam_policy_bindings (under google_billing_accounts)
    #
    def get_iam_policy_bindings(self, billing_account_name):
        """Return a list of Google Billing Account IAM Policy Bindings from Firestore."""
        collection = f"google_billing_accounts/{billing_account_name}/iam_policy_bindings"
        return self.get_collection(collection)

    #
    # projects (under google_billing_accounts)
    #
    def get_projects(self, billing_account_name):
        """Return a list of Google Billing Account Projects from Firestore."""
        collection = f"google_billing_accounts/{billing_account_name}/projects"
        return self.get_collection(collection)

    #
    # triggers
    #
    def delete_trigger(self, name):
        """Save a single trigger."""
        return self.db.collection("triggers").document(name).delete()

    def get_trigger(self, name):
        """Return a single trigger."""
        return self.db.collection("triggers").document(name).get().to_dict()

    def get_triggers(self):
        """Return a list of triggers."""
        # return get_collection("triggers")
        triggers = []
        for doc in self.db.collection("triggers").stream():
            trigger = doc.to_dict()
            trigger["id"] = doc.id
            triggers.append(trigger)
        return triggers

    def save_trigger(self, trigger):
        """Save a single trigger."""
        return self.db.collection("triggers").add(trigger)

    #
    # user accounts
    #
    def get_user_amazon_accounts(self, email):
        """Return a list of Google Billing Accounts associated with the user."""
        username = email.replace("@broadinstitute.org", "")
        query = self.db.collection("accounts").where("admins", "array_contains", username)
        accounts = []
        for doc in query.stream():
            a = doc.to_dict()
            a["role"] = "admin"
            accounts.append(a)
            # print(a)
        return accounts

    def get_user_google_billing_accounts(self, email):
        """Return a list of Google Billing Accounts associated with the user."""
        user = "user:{}".format(email)
        query = self.db.collection_group("iam_policy_bindings").where("members", "array_contains", user)

        # get account_ids associated with the given email address
        account_ids = {}
        for doc in query.stream():
            path = doc.reference.path
            billing_account_id = path.split("/")[1]
            account_ids[billing_account_id] = doc.to_dict()

        # assemble accounts with bindings
        accounts = []
        for a in self.get_accounts_by_id(account_ids):
            name = a["name"]
            a["role"] = None
            a["admins"] = []
            a["users"] = []
            if name in account_ids:
                b = account_ids[name]

                # check for admin role
                if b["role"] == "roles/billing.admin":
                    for m in b["members"]:
                        m = m.replace("user:", "")
                        if m == email:
                            a["role"] = "admin"
                        if "@broadinstitute.org" in m:
                            a["admins"].append(m.replace("@broadinstitute.org", ""))

                # check for user role
                elif b["role"] == "roles/billing.user":
                    for m in b["members"]:
                        m = m.replace("user:", "")
                        if m == email:
                            a["role"] = "user"
                        if "@broadinstitute.org" in m:
                            a["admins"].append(m.replace("@broadinstitute.org", ""))

            accounts.append(a)
        return accounts

    #
    # webhooks
    #
    def delete_webhook(self, name):
        """Save a single webhook."""
        return self.db.collection("webhooks").document(name).delete()

    def get_webhook(self, name):
        """Return a single webhook."""
        return self.db.collection("webhooks").document(name).get().to_dict()

    def get_webhooks(self):
        """Return a list of Webhooks from Firestore."""
        return self.get_collection("webhooks")

    def save_webhook(self, name, webhook):
        """Save a single webhook."""
        return self.db.collection("webhooks").document(name).set(webhook)
