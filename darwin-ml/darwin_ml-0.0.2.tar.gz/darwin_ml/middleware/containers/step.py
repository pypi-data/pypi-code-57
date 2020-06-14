from typing import Optional, Dict, Any
from jamboree.utils import omit

class StepSettings(object):
    def __init__(self, user_id:str, episode:str, is_live=False):
        self.__user_id:str = user_id
        self.__episode:str = episode
        self.__live:bool = is_live
        self.__asset: Optional[str] = None
        

    @property
    def user_id(self) -> str:
        """The user_id of the asset we're looking for.

        Returns:
            str: The user_id
        """
        return self.__user_id
    
    @property
    def episode(self) -> str:
        return self.__episode
    

    @property
    def live(self) -> bool:
        return self.__live
    

    @property
    def asset_id(self) -> str:
        return self.__asset

    @asset_id.setter
    def asset_id(self, _asset:str):
        self.__asset = _asset