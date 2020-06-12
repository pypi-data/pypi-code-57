import numpy as np
from typing import Optional, Dict, Any
from jamboree.utils import omit

class FeaturesContainer(object):
    def __init__(self, latest_feature: Dict[str, Any], prior_feature: Optional[Dict[str, Any]] = None):

        self._current = self.remove_timestamps(latest_feature)
        self._prior:Optional[Dict[str, Any]] = None
        
        
        if bool(prior_feature):
            self._prior = self.remove_timestamps(prior_feature, name="PriorFeature")
    
    def is_dict(self, _feature:dict, name:str="CurrentFeature"):
        assert isinstance(_feature, dict), f"{name} is not a dict"

    @property
    def current(self) -> Dict[str, Any]:
        """Get the latest bar.

        Returns:
            Dict[str, Any]: The latest bar.
        """
        # self.verify()
        return self._current

    @property
    def previous(self) -> Dict[str, Any]:
        """The previous price bar.

        Returns:
            Dict[str, Any]: The previous price bar.
        """
        # self.verify(is_prev=True)
        return self._prior

    @property
    def is_none(self) -> bool:
        """Checks if both variables are empty.

        Returns:
            bool: Are both variables there.
        """
        return (not bool(self.current)) and (not bool(self.previous))

    @property
    def is_current(self) -> bool:
        """Determines if the event has only the current bar.

        Returns:
            bool: if this is the current bar.
        """
        return bool(self.current)

    @property
    def is_both(self) -> bool:
        """Determines if both features are there

        Returns:
            bool: if this is the current bar.
        """
        return bool(self.current) and bool(self.previous)
    @property
    def is_previous(self) -> bool:
        return bool(self.previous)
    
    @property
    def features(self):
        curr = []
        if self.is_current:
            curr = list(self.current.values())
        return np.array(curr)


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
        if not self.is_none:
            raise AttributeError("None of the variables have been set.")

        # If we're looking for both variables, and one isn't set, we raise a value error
        if (is_both or is_prev) and not self.is_both:
            raise AttributeError("One of the two expected values isn't there.")

        # Check if the current bar is here
        if not self.is_current:
            raise AttributeError("The current price isn't there.")
    
    def remove_timestamps(self, feature_dict:Dict[str, Any], name="CurrentFeature"):
        self.is_dict(feature_dict, name=name)
        return omit(['timestamp', 'time'], feature_dict)
    
    def __str__(self):
        features = self.features
        feats = []
        if len(features) > 3:
            feats = features[-3:]
        return f"<PriceContainer is_previous={self.is_previous} is_current={self.is_current} features={feats} >"