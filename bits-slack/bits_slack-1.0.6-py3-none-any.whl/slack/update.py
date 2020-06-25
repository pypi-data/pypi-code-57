# -*- coding: utf-8 -*-
"""Slack Update class file."""

import re


class Update:
    """Slack Update class."""

    def __init__(self, slack, args, auth):
        """Initialize a class instance."""
        self.slack = slack
        self.args = args
        self.auth = auth

        self.email = False
        if "email" in args:
            self.email = True

        self.verbose = False
        if "verbose" in args or auth.verbose:
            self.verbose = True

        self.google_users = None
        self.other_accounts = None
        self.people = None
        self.slack_emails = None
        self.slack_users = None
        self.team_profile = None

    def _check_user(self, user):
        """Check a single user."""
        user_id = user["id"]
        profile = user["profile"]

        # get profile fields
        email = profile.get("email", "").lower()
        first_name = profile.get("first_name")
        last_name = profile.get("last_name")
        real_name = profile.get("real_name")
        phone = profile.get("phone")
        title = profile.get("title")

        # skip users with no email
        if not email:
            print(f"ERROR: User with no email: {real_name}")
            return

        # check for an existing other account
        if email in self.other_accounts:
            return

        # check for an existing person
        if email not in self.people:
            print(f"ERROR: Unknown user: {real_name} <{email}>")
            return

        # get person
        person = self.people[email]
        person_first_name = person["first_name"]
        person_last_name = person["last_name"]
        person_phone = person.get("primary_work_phone")
        person_title = person["title"]

        suffix = self._get_pronouns_suffix(last_name)
        if suffix:
            person_last_name = f"{person_last_name} {suffix}"

        changes = []

        # check first name
        if person_first_name != first_name:
            changes.append(f"  first_name: {first_name} -> {person_first_name}")
            profile["first_name"] = person_first_name

        # check last name
        if person_last_name != last_name:
            changes.append(f"  last_name: {last_name} -> {person_last_name}")
            profile["last_name"] = person_last_name

        # check phone
        if person_phone and person_phone != phone:
            changes.append(f"  phone: {phone} -> {person_phone}")
            profile["phone"] = person_phone

        # check title
        if person_title != title:
            changes.append(f"  title: {title} -> {person_title}")
            profile["title"] = person_title

        # display changes
        if changes:
            print(f"\n{email}:")
            print("\n".join(changes))
            try:
                self.slack.set_user_profile(user_id, profile)
            except Exception as e:
                print(f"ERROR: Failed to update profile for user: {email} [{e}")

        # check activate
        if not person['terminated'] and user['deleted']:
            return "activate"

        # check terminated
        if person['terminated'] and not user['deleted']:
            return "deactivate"

        return None

    def _get_github_profile_field(self):
        """Return the ID of the field that represents the GitHub Profile."""
        label = "GitHub Profile"
        for field in self.team_profile.get("fields", {}):
            if field["label"] == label:
                return field["id"]
        return None

    def _get_google_group_users(self, email):
        """Return the list of Slack users in a Google group."""
        g = self.auth.google()
        g.auth_service_account(g.scopes, g.subject)
        members = g.directory().get_derived_members(email)
        users = []
        for member in members:
            if member["type"] != "USER":
                continue
            member_id = member["id"]
            if member_id in self.google_users:
                email = self.google_users[member_id]["primaryEmail"]
            else:
                email = member["email"].lower()
            if email not in self.slack_emails:
                continue
            user = self.slack_emails[email]
            user_id = user["id"]
            if not user["deleted"] and user_id not in users:
                users.append(user_id)
        return users

    def _get_google_users(self):
        """Return a dict of Google users."""
        g = self.auth.google()
        g.auth_service_account(g.scopes, g.subject)
        fields = 'nextPageToken,users(id,primaryEmail,name/fullName,suspended)'
        return g.directory().get_users_dict(fields=fields)

    def _get_other_accounts(self):
        """Return a dict of other accounts from BITSdb."""
        mongo = self.auth.mongo()
        other_accounts = {}
        for account in mongo.get_collection("other_accounts"):
            key = account.get("slack_username")
            if not key:
                continue
            key = key.lower()
            if key in other_accounts:
                print(f"ERROR: Duplicate email in other accounts: {key}")
                continue
            other_accounts[key] = account
        return other_accounts

    def _get_slack_user_emails(self):
        """Return a dict of Slack users by email address."""
        if not self.slack_users:
            if self.verbose:
                print("Getting Slack users...")
            self.slack_users = self.slack.get_users_dict()
        if self.verbose:
            print(f"Found {len(self.slack_users)} Slack users.")
        emails = {}
        for user_id in self.slack_users:
            user = self.slack_users[user_id]
            email = user["profile"].get("email")
            if not email:
                continue
            if email in emails:
                print(f"ERROR: Duplicate email: {email}")
                continue
            emails[email.lower()] = user
        self.slack_emails = emails
        return self.slack_emails

    def _get_slack_usergroup_syncs(self):
        """Return a list of Slack Usergroup syncs from BITSdb."""
        emails = []
        usergroup_ids = []
        syncs = []
        for sync in self.auth.mongo().get_collection("slack_usergroup_sync"):
            email = sync["google_group"]
            usergroup_id = sync["slack_usergroup"]
            usergroup_name = sync["slack_usergroup_name"]
            if email in emails:
                print(f"WARNING: Duplicate sync email: {email}")
                continue
            emails.append(email)
            if usergroup_id in usergroup_ids:
                print(f"WARNING: Duplicate sync usergroup: {usergroup_name} [{usergroup_id}]")
                continue
            usergroup_ids.append(usergroup_id)
            syncs.append(sync)
        return syncs

    def _get_people(self):
        """Return a dict of people from BITSdb."""
        collection = "people_people"
        project = "broad-bitsdb-firestore"
        g = self.auth.google()
        firestore = g.firestore(project)
        people = {}
        for person in firestore.get_collection(collection):
            key = person["email_username"]
            if not key:
                continue
            key = key.lower()
            if key in people:
                print(f"ERROR: Duplicate email in people: {key}")
                continue
            people[key] = person
        return people

    def _get_pronouns_suffix(self, last_name):
        """Return the pronouns suffix for the given last name."""
        suffix = ""
        if last_name and re.search(r'\(.*/.*\)$', last_name):
            suffix = re.sub(r'.* (\(.*/.*\))$', r'\1', last_name).replace(" ", "")
        return suffix

    def profiles(self):
        """Update user profiles in Slack."""
        if not self.team_profile:
            self.team_profile = self.slack.get_team_profile().get("profile")
        self.github_profile_id = self._get_github_profile_field()

        if not self.people:
            if self.verbose:
                print("Getting people...")
            self.people = self._get_people()
        if self.verbose:
            print(f"Found {len(self.people)} people.\n")

        if not self.slack_users:
            if self.verbose:
                print("Getting Slack users...")
            self.slack_users = self.slack.get_users_dict()
        if self.verbose:
            print(f"Found {len(self.slack_users)} Slack users.")

        for user_id in sorted(self.slack_users, key=lambda x: self.slack_users[x]["profile"].get("email", "")):
            user = self.slack_users[user_id]

            # skip deleted users
            if user["deleted"] or user["is_bot"] or user["id"] == "USLACKBOT":
                continue

            email = user["profile"].get("email")

            # skip people with no email address
            if email not in self.people:
                continue

            # get person and their github login
            person = self.people[email]
            github_login = person.get("github_login")

            # check github profile field
            if github_login and self.github_profile_id:

                # get the user profile with profile fields
                profile = self.slack.get_user_profile(user_id).get("profile")
                fields = profile.get("fields")
                if not fields:
                    fields = {}

                # create the profile value from the github_login
                github_url = f"https://github.com/{github_login}"
                body = {
                    "value": github_url,
                    "alt": github_login,
                }

                if self.github_profile_id not in fields:
                    fields[self.github_profile_id] = body
                elif fields[self.github_profile_id] != body:
                    fields[self.github_profile_id] = body

                if fields != profile.get("fields"):
                    print(f"Updating GitHub Profile for: {email}...")
                    profile["fields"] = fields
                    self.slack.set_user_profile(user_id, profile)

    def usergroups(self):
        """Update usergroups in Slack."""
        self._get_slack_user_emails()

        if self.verbose:
            print("Getting syncs...")
        syncs = self._get_slack_usergroup_syncs()
        if self.verbose:
            print(f"Usergroup Sync Rules: {len(syncs)}")

        if self.verbose:
            print("Getting Usergroups...")
        usergroups = self.slack.get_usergroups_dict(include_disabled=True, include_users=True)
        if self.verbose:
            print(f"Usergroups: {len(usergroups)}")

        self.google_users = self._get_google_users()

        for sync in sorted(syncs, key=lambda x: x.get("google_group", "")):
            google_group = sync.get("google_group")
            usergroup_id = sync.get("slack_usergroup")
            usergroup_name = sync.get("slack_usergroup_name")

            if usergroup_id not in usergroups:
                print(f"ERROR: Usergroup not found: {usergroup_name} [{usergroup_id}] ({google_group})")
                continue

            usergroup = usergroups[usergroup_id]

            # skip deleted usergroups
            if usergroup.get("date_delete"):
                continue

            # get current slack usergroup users
            users = sorted(usergroup.get("users", []))

            # get google group members as slack users
            group_users = sorted(self._get_google_group_users(google_group))

            if users != group_users:
                print(f"\n{google_group} -> {usergroup_name} [{usergroup_id}]")
                add = list(set(group_users) - set(users))
                delete = list(set(users) - set(group_users))
                if add:
                    print(f"  Adding {len(add)} users:")
                    for user_id in sorted(add, key=lambda x: self.slack_users[x]["profile"]["email"].lower()):
                        user = self.slack_users[user_id]
                        email = user["profile"]["email"].lower()
                        print(f"   + {email}")
                if delete:
                    print(f"  Deleting {len(delete)} users:")
                    for user_id in sorted(delete, key=lambda x: self.slack_users[x]["profile"]["email"].lower()):
                        user = self.slack_users[user_id]
                        email = user["profile"]["email"].lower()
                        print(f"   - {email}")
                if add or delete:
                    try:
                        self.slack.update_usergroup_users(usergroup_id, group_users)
                    except Exception as e:
                        print(f"ERROR: Failed to update Usergroup: {usergroup_name} [{usergroup_id}]: {e}")

    def users(self):
        """Update users in Slack."""
        if not self.other_accounts:
            if self.verbose:
                print("Getting other accounts...")
            self.other_accounts = self._get_other_accounts()
        if self.verbose:
            print(f"Found {len(self.other_accounts)} other accounts.\n")

        if not self.people:
            if self.verbose:
                print("Getting people...")
            self.people = self._get_people()
        if self.verbose:
            print(f"Found {len(self.people)} people.\n")

        if not self.slack_users:
            if self.verbose:
                print("Getting Slack users...")
            self.slack_users = self.slack.get_users_dict()
        if self.verbose:
            print(f"Found {len(self.slack_users)} Slack users.")

        bots = []
        restricted = []
        ultra_restricted = []

        activate = []
        deactivate = []

        # check each user
        for user_id in sorted(self.slack_users, key=lambda x: self.slack_users[x]["profile"].get("email", "")):
            user = self.slack_users[user_id]

            # skip deleted users
            if user["deleted"]:
                continue

            # count and skip bot users
            if user["is_bot"] or user["id"] == "USLACKBOT":
                bots.append(user)
                continue

            # count single-channel and multi-channel guests
            if user["is_ultra_restricted"]:
                ultra_restricted.append(user)
            elif user["is_restricted"]:
                restricted.append(user)

            # check for users to activate or deactivate
            action = self._check_user(user)
            if action == "activate":
                activate.append(user)
            elif action == "deactivate":
                deactivate.append(user)

        # output activations/decativations
        if activate:
            print(f"\nUsers to activate: {len(activate)}")
            for user in activate:
                print(f"  + {user['profile']['email']}")
        if deactivate:
            print(f"\nUsers to deactivate: {len(deactivate)}")
            for user in deactivate:
                print(f"  - {user['profile']['email']}")

        # output stats about bots/guests
        if self.verbose:
            print(f"\nBot Users: {len(bots)}")
            print(f"Single-Channel Guests: {len(ultra_restricted)}")
            print(f"Multi-Channel Guests: {len(restricted)}")
