from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Cvstats:
    __tablename__ = "cvstats"

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def timestamp(self):
        return Column(DateTime)

    @declared_attr
    def members_connected(self):
        return Column(Integer)

    @declared_attr
    def users_connected(self):
        return Column(Integer)

    @declared_attr
    def members_online(self):
        return Column(Integer)

    @declared_attr
    def users_online(self):
        return Column(Integer)

    @declared_attr
    def members_playing(self):
        return Column(Integer)

    @declared_attr
    def users_playing(self):
        return Column(Integer)

    @declared_attr
    def members_total(self):
        return Column(Integer)

    @declared_attr
    def users_total(self):
        return Column(Integer)

    def json(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "users_total": self.users_total,
            "members_total": self.members_total,
            "users_online": self.users_online,
            "members_online": self.members_online,
            "users_connected": self.users_connected,
            "members_connected": self.members_connected,
            "users_playing": self.users_playing,
            "members_playing": self.members_playing,
        }