from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID


class Poll:
    __tablename__ = "polls"

    @declared_attr
    def id(self):
        return Column(UUID(as_uuid=True), primary_key=True)

    @declared_attr
    def question(self):
        return Column(String, nullable=False)

    @declared_attr
    def description(self):
        return Column(Text, nullable=False, server_default="")

    @declared_attr
    def creator_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def creator(self):
        return relationship("User", backref=backref("polls_created"))

    @declared_attr
    def expires(self):
        return Column(DateTime)

    @declared_attr
    def created(self):
        return Column(DateTime, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "question": self.question,
            "description": self.description,
            "creator": self.creator.json(),
            "expires": self.expires.isoformat(),
            "created": self.created.isoformat(),
            "votes": map(
                lambda v: {
                    "caster": v.caster.json(),
                    "posted": v.posted.isoformat(),
                    "vote": v.vote.name
                },
                sorted(self.votes, key=lambda v: v.posted)
            ),
            "comments": map(
                lambda c: {
                    "id": c.id,
                    "comment": c.comment,
                    "creator": c.creator.json(),
                    "posted": c.posted.isoformat(),
                    "mood": c.mood.name,
                },
                sorted(self.comments, key=lambda c: c.posted)
            )
        }
