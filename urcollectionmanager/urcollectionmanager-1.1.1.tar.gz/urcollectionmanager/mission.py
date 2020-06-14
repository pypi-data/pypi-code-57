from .database import Base
from typing import Optional
from sqlalchemy import Column, String, Integer, Boolean, LargeBinary, event
from hashlib import sha1


class Mission(Base):
    __tablename__ = "mission"
    hash_id = Column(LargeBinary, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    progress = Column(Integer)
    goal = Column(Integer)
    completed = Column(Boolean)

    def __init__(self,
                 name: Optional[str] = "",
                 description: Optional[str] = "",
                 progress: Optional[int] = 0,
                 goal: Optional[int] = 0,
                 completed: Optional[bool] = False):
        self.name = str(name)
        self.description = str(description)
        self.progress = int(progress)
        self.goal = int(goal)
        self.completed = bool(completed)
        self.hash_id = create_hash(self)

    def __repr__(self):
        return 'name: ' + repr(self.name)

    def __str__(self):
        return ",".join(f"{item[0]}: {item[1]}" for item in vars(self).items())

    def __eq__(self, other):
        if not isinstance(other, Mission):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.hash_id == other.hash_id


@event.listens_for(Mission, 'before_insert')
@event.listens_for(Mission, 'before_update')
def receive_before_insert(mapper, connection, target):
    """Update hash before insert"""
    target.hash_id = create_hash(target)


def create_hash(target):
    hash_columns = [target.name, target.description]
    bytes_hash_target = "".join([str(item) for item in hash_columns]).encode()
    return sha1(bytes_hash_target).digest()
