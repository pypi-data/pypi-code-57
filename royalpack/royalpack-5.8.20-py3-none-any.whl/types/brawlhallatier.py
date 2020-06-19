import enum


class BrawlhallaTier(enum.Enum):
    ZERO = 0
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self.name}"

    def __gt__(self, other):
        if other is None:
            return True
        if not isinstance(other, self.__class__):
            raise TypeError(f"Can't compare {self.__class__.__qualname__} with {other.__class__.__qualname__}")
        return self.value > other.value
