from loguru import logger
from addict import Dict as Addict
from typing import List, Any, Union, Optional
from see137.common import Pipeline
from see137.common import ComponentAbstract


class AddictPipeline(Pipeline):
    def __init__(self,
                 steps: List[Union['Pipeline', 'ComponentAbstract']] = [],
                 name: str = None,
                 processor=None):
        super().__init__(steps, name=name, processor=processor)

    def step(self,
             dict_item: dict,
             override: bool = False,
             is_loud: bool = True,
             **kwargs):
        addict_dict = Addict(**dict_item)
        
        kwargs.update({"override": override, "is_loud": is_loud})
        result = super().step(addict_dict, **kwargs)
        return result
    
    def __repr__(self):
        return f"<Pipeline={self.name}>"