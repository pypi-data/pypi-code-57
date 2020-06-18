from typing import Optional, Dict, Any

from jamboree.handlers  import TimeHandler
from darwin_ml.handlers import StateTransformerAbstract
from darwin_ml.handlers import PriceStateTransformer
from darwin_ml.utils import Injectable




class OnlineStateSpace(Injectable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__price: Optional[PriceStateTransformer] = None
        self.__allocation: Optional[StateTransformerAbstract] = None
        self.__predictions: Optional[PriceStateTransformer] = None

        self.episode: Optional[str] = None
        self.userid: Optional[str] = None
        self.assetid: Optional[str] = None
        self.live: bool = False

    @property
    def price(self) -> StateTransformerAbstract:
        return self.__price

    @property
    def predictions(self) -> StateTransformerAbstract:
        return self.__predictions

    @property
    def allocation(self) -> StateTransformerAbstract:
        return self.__allocation

    def check_null(self):
        if self.episode is None:
            raise AttributeError("An episode needs to be set")
        if self.userid is None:
            raise AttributeError("A userid needs to be set")
        if self.assetid is None:
            raise AttributeError("An asset id needs to be set")

    def set_userid(self, userid: str):
        if not isinstance(userid, str): raise TypeError("UserId is not a string type")
        self.userid = userid
        return self

    def set_episode(self, episode: str):
        if not isinstance(episode, str): raise TypeError("EpisodeId is not a string type")
        self.episode = episode
        return self

    def set_live(self, live: bool):
        if not isinstance(live, bool): raise TypeError("Live is not a bool type")
        self.live = live
        return self

    def set_assetid(self, assetid: str):
        if not isinstance(assetid, str): raise TypeError("AssetId is not a string type")
        self.assetid = assetid
        return self

    def set_params(self,
                   user_id: Optional[str] = None,
                   episode: Optional[str] = None,
                   live=False,
                   assetid: Optional[str] = None):
        if user_id is not None: self.set_userid(user_id)
        if episode is not None: self.set_episode(episode)
        if live is not None: self.set_live(live)
        if assetid is not None: self.set_assetid(assetid)

    def reset(self):
        self.price.reset()
        self.allocation.reset()
        self.predictions.reset()
    
    def initialization(self):
        pass


    def step(self) -> Dict[str, Any]:
        allocation_stats = self.allocation.step()