from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from ..types import PollMood


class PollComment:
    __tablename__ = "pollcomments"

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def author_id(self):
        return Column(Integer, ForeignKey("users.uid"), nullable=False)

    @declared_attr
    def author(self):
        return relationship("User", backref=backref("poll_comments_created"))

    @declared_attr
    def poll_id(self):
        return Column(UUID(as_uuid=True), ForeignKey("polls.id"))

    @declared_attr
    def poll(self):
        return relationship("Poll", backref=backref("comments"))

    @declared_attr
    def posted(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def mood(self):
        return Column(Enum(PollMood), nullable=False, default=PollMood.NEUTRAL)

    @declared_attr
    def comment(self):
        return Column(Text)
