from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Treasure:
    __tablename__ = "treasures"

    @declared_attr
    def code(self):
        return Column(String, primary_key=True)

    @declared_attr
    def redeemed_by_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def redeemed_by(self):
        return relationship("User")

    @declared_attr
    def value(self):
        return Column(Integer, nullable=False)
