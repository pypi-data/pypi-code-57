from __future__ import annotations
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_microservice_library.integrations.fact import get_fact_endpoint

from ehelply_bootstrapper.utils.state import State


class User(Integration):
    """
    Note integration is used to talk to the ehelply-notes microservice
    """

    def __init__(self) -> None:
        super().__init__("user")

        self.m2m = State.integrations.get("m2m")

    def init(self):
        super().init()

    def load(self):
        super().load()

    def get_base_url(self) -> str:
        return get_fact_endpoint('ehelply-users')
