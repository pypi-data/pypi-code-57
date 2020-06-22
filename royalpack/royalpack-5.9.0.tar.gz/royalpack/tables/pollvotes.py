from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from ..types import PollMood
from sqlalchemy.dialects.postgresql import UUID


class PollVote:
    __tablename__ = "pollvotes"

    @declared_attr
    def caster_id(self):
        return Column(Integer, ForeignKey("users.uid"), primary_key=True)

    @declared_attr
    def caster(self):
        return relationship("User", backref=backref("poll_votes_cast"))

    @declared_attr
    def poll_id(self):
        return Column(UUID(as_uuid=True), ForeignKey("polls.id"), primary_key=True)

    @declared_attr
    def poll(self):
        return relationship("Poll", backref=backref("votes"))

    @declared_attr
    def posted(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def vote(self):
        return Column(Enum(PollMood), nullable=False, default=PollMood.NEUTRAL)
