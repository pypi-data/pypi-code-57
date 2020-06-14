from .database import Base
from datetime import date, timedelta, datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, DATETIME, LargeBinary, event
from sqlalchemy.ext.hybrid import hybrid_property
from hashlib import sha1


class Purchase(Base):
    __tablename__ = "purchase"
    hash_id = Column(LargeBinary, primary_key=True)
    name = Column(String(255))
    id = Column(Integer)
    price = Column(Integer)
    level = Column(Integer)
    _purchase_date = Column(DATETIME)

    @hybrid_property
    def purchase_date(self):
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, purchase_date):
        # Friday 06/03, 20:39
        # Today at 11:30
        if isinstance(purchase_date, datetime):
            self._purchase_date = purchase_date
            return
        if ":" not in purchase_date:
            # If purchased at midnight GMT, timestamp is omitted
            # Ex  	Wednesday 05/06/2019
            purchase_date += ", 00:00"
        split_date = str(purchase_date).split()
        try:
            purch_date = datetime.combine(datetime.now(), datetime.strptime(split_date[2], "%H:%M").time())
        except BaseException:
            raise ValueError(f"Failed to convert {purchase_date}: Ended up with {split_date}")
        if split_date[0] == "Yesterday":
            purch_date -= timedelta(days=1)
        elif split_date[1] != "at":
            if len(split_date[1].split("/")) == 2:
                purch_date = datetime.strptime(purchase_date, "%A %d/%m, %H:%M")
                purch_date = purch_date.replace(year=datetime.now().year)
            else:
                purch_date = datetime.strptime(purchase_date, "%A %d/%m/%Y, %H:%M")

        self._purchase_date = purch_date

    def __init__(self,
                 name: Optional[str] = "",
                 id: Optional[int] = 0,
                 price: Optional[int] = 0,
                 level: Optional[int] = 0,
                 purchase_date: Optional[str] = datetime.now()):
        self.name = str(name)
        self.id = int(id)
        self.price = int(price)
        self.level = int(level)
        self.purchase_date = purchase_date
        self.hash_id = create_hash(self)

    def __repr__(self):
        return 'id: ' + repr(self.id)

    def __str__(self):
        return ",".join(f"{item[0]}: {item[1]}" for item in vars(self).items())

    def __eq__(self, other):
        if not isinstance(other, Purchase):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.hash_id == other.hash_id


@event.listens_for(Purchase, 'before_insert')
@event.listens_for(Purchase, 'before_update')
def receive_before_insert(mapper, connection, target):
    """Update hash before insert"""
    target.hash_id = create_hash(target)


def create_hash(target):
    hash_columns = [target.id, target.price, target.level, target.purchase_date]
    bytes_hash_target = "".join([str(item) for item in hash_columns]).encode()
    return sha1(bytes_hash_target).digest()
