from typing import Optional, Dict, Any
from loguru import logger

class PriceContainer(object):
    def __init__(self, current_bar: Dict[str, Any], previous_bar: Optional[Dict[str, Any]] = None):
        self.is_bar(current_bar)
        self._current = current_bar
        self._previous = previous_bar

        self._cprice = current_bar.get("close", 0.0)

        if bool(previous_bar):
            self.is_bar(previous_bar)
            self._previous = previous_bar
            self._pprice = previous_bar.get("close", 0.0)

    @property
    def current(self) -> Dict[str, Any]:
        """Get the latest bar.

        Returns:
            Dict[str, Any]: The latest bar.
        """
        return self._current

    @property
    def previous(self) -> Dict[str, Any]:
        """The previous price bar.

        Returns:
            Dict[str, Any]: The previous price bar.
        """
        return self._previous

    @property
    def is_none(self) -> bool:
        """Checks if both variables are empty.

        Returns:
            bool: Are both variables there.
        """
        is_current = bool(self.current)
        is_previous = bool(self.current)
        return bool(self.current) == False and bool(self.previous) == False

    @property
    def is_current(self) -> bool:
        """Determines if the event has only the current bar.

        Returns:
            bool: if this is the current bar.
        """
        return bool(self.current)
    
    @property
    def is_previous(self) -> bool:
        """Determines if the event has only the current bar.

        Returns:
            bool: if this is the current bar.
        """
        return bool(self.previous)

    @property
    def is_both(self) -> bool:
        """Determines if the event has only the current bar.

        Returns:
            bool: if this is the current bar.
        """
        return bool(self.current) and bool(self.previous)

    def verify(self, is_both: bool = False, is_prev: bool = False) -> None:
        """Run through a series of verifications.

        1. Check if at least one of the variables have been set.
        2. If we're checking for both, yet both variables aren't there, we should exit.
        3. We're checking if the latest price information is there.

        

        Args:
            is_both (bool, optional): Determines if we're checking for both variables. Defaults to False.
            is_prev (bool, optional): Determines if we're checking for the previous bar. Defaults to False.

        Raises:
            AttributeError: None of the variables have been set.
            AttributeError: One of the two expected values isn't there.
            AttributeError: The current price isn't there.
        """
        # If none of the variables have been set. We raise an attribute error.
        if self.is_none:
            raise AttributeError("None of the variables have been set.")

        # If we're looking for both variables, and one isn't set, we raise a value error
        if (is_both or is_prev) and not self.is_both:
            raise AttributeError("One of the two expected values isn't there.")

        # Check if the current bar is here
        if not self.is_current:
            raise AttributeError("The current price isn't there.")

    def is_bar(self, _bar: dict):
        """Check if the dictionary is a bar

        Args:
            _bar (dict): The dictionary that we're checking.
        """
        assert isinstance(_bar, dict)
        assert 'close' in _bar
        assert isinstance(_bar['close'], float)

    @property
    def current_price(self) -> float:
        """Return the latest close price.

        Returns:
            float: Close price.
        """
        self.verify()
        return self._cprice

    @property
    def previous_price(self) -> float:
        """Return the last close price.

        Returns:
            float: The last close price.
        """
        self.verify(is_prev=True)
        return self._pprice
    
    @property
    def direction(self):
        """Get the direction change from the price between two points.

        Returns:
            int: 1 represents the price went up. 0 represents the price went down.
        """
        if self.current_price > self.previous_price:
            return 1
        return 0
    
    @property
    def percentage(self) -> float:
        """Get the percentage change between the current price and the last price. 

        Returns:
            float: The percentage change between the two points.
        """
        self.verify(is_both=True)
        return (((self.current_price - self.previous_price) / self.current_price) * 100)
    

    def __str__(self):
        return f"<PriceContainer is_previous={self.is_previous} is_current={self.is_current} close={self.current_price} >"