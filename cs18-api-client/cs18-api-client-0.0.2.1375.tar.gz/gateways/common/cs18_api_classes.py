"""
Container for object classes used in cs18-api-client
"""
from datetime import datetime
from typing import Optional

import dateutil.parser


class AccessLink:
    def __init__(self, protocol: str, link: str):
        self.link = link
        self.protocol = protocol


class CloudAccountCostResponse:
    def __init__(self, last_update: Optional[datetime]):
        self.last_update = last_update


class CloudComputeService:
    def __init__(
            self,
            name: str,
            service_type: str,
            created_date: datetime,
            created_by: str,
            user_defined: bool,
    ):
        self.name = name
        self.type = service_type
        self.created_date = created_date
        self.created_by = created_by
        self.user_defined = user_defined


class Commit:
    def __init__(self, data: dict):
        self.sha = data["sha"]
        self.author = data["commit"]["author"]["name"]
        self.date = dateutil.parser.parse(data["commit"]["author"]["date"])
        self.comment = data["commit"]["message"]

    def __str__(self):
        return "{0}: [{1}] {2}".format(self.date, self.sha[:7], self.comment)


class ColonyAccount:
    def __init__(
            self, account: str, email: str, password: str, first_name: str, last_name: str
    ):
        self.account = account
        self.default_space = "Trial"
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class BlueprintRepositoryDetails:
    def __init__(self, repository_url: str, access_token: str, repository_type: str):
        self.repository_url = repository_url
        self.repository_type = repository_type
        self.access_token = access_token
