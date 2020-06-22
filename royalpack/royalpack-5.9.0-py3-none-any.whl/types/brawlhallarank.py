from .brawlhallametal import BrawlhallaMetal
from .brawlhallatier import BrawlhallaTier


class BrawlhallaRank:
    __slots__ = "metal", "tier"

    def __init__(self, metal: BrawlhallaMetal, tier: BrawlhallaTier):
        self.metal: BrawlhallaMetal = metal
        self.tier: BrawlhallaTier = tier

    def __gt__(self, other):
        if other is None:
            return True
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can't compare {self.__class__.__qualname__} with {other.__class__.__qualname__}")
        if self.metal > other.metal:
            return True
        elif self.metal < other.metal:
            return False
        elif self.tier > other.tier:
            return True
        return False

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can't compare {self.__class__.__qualname__} with {other.__class__.__qualname__}")
        return self.metal == other.metal and self.tier == other.tier

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {self.metal} {self.tier}>"

    def __str__(self):
        return f"{self.metal} {self.tier}"
