from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from ..types import BrawlhallaRank, BrawlhallaTier, BrawlhallaMetal


class BrawlhallaDuo:
    __tablename__ = "brawlhalladuos"

    @declared_attr
    def id_one(self):
        return Column(Integer, ForeignKey("brawlhalla.brawlhalla_id"), primary_key=True)

    @declared_attr
    def id_two(self):
        return Column(Integer, ForeignKey("brawlhalla.brawlhalla_id"), primary_key=True)

    @declared_attr
    def one(self):
        return relationship("Brawlhalla", foreign_keys=self.id_one, backref=backref("_duos_one"))

    @declared_attr
    def two(self):
        return relationship("Brawlhalla", foreign_keys=self.id_two, backref=backref("_duos_two"))

    @declared_attr
    def rating_2v2(self):
        return Column(Integer)

    @declared_attr
    def tier_2v2(self):
        return Column(Enum(BrawlhallaTier))

    @declared_attr
    def metal_2v2(self):
        return Column(Enum(BrawlhallaMetal))

    @property
    def rank_2v2(self):
        return BrawlhallaRank(metal=self.metal_2v2, tier=self.tier_2v2)

    @rank_2v2.setter
    def rank_2v2(self, value):
        if not isinstance(value, BrawlhallaRank):
            raise TypeError("rank_1v1 can only be set to BrawlhallaRank values.")
        self.metal_2v2 = value.metal
        self.tier_2v2 = value.tier

    def other(self, bh):
        if bh == self.one:
            return self.two
        elif bh == self.two:
            return self.one
        else:
            raise ValueError("Argument is unrelated to this duo.")

    def __repr__(self):
        return f"<BrawlhallaDuo {self.id_one} & {self.id_two}>"
