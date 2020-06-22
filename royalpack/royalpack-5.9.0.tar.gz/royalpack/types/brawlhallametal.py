import enum


class BrawlhallaMetal(enum.Enum):
    TIN = 0
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    DIAMOND = 5

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self.name}"

    def __gt__(self, other):
        if other is None:
            return True
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can't compare {self.__class__.__qualname__} with {other.__class__.__qualname__}")
        return self.value > other.value
