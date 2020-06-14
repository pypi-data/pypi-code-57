from typing import Optional, Dict, Any
from jamboree.utils import omit

class AllocationContainer(object):
    def __init__(self, pct: float, fill: float):
        assert isinstance(pct, float), "Percentage is not a float."
        assert isinstance(fill, float), "The percentage filled is not a float. Please provide one."
        self._percentage:float = pct
        self._filling:float = fill
    


    @property
    def percentage(self) -> float:
        """Get the latest bar.

        Returns:
            float: The percentage cap of the 
        """
        return self._percentage

    @property
    def filling(self) -> float:
        """The percentage of the allocation filled.

        Returns:
            float: The percentage of the allocation filled. Should be greater than 0, yet less than 1.2. Symbolizing 120%.
        """
        return self._filling

    def __str__(self):
        return f"<AllocationContainer percentage={self.percentage} filling={self.filling}>"
    