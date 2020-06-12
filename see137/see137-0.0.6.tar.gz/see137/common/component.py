from typing import Any
from abc import ABC, abstractmethod
from see137.common.injectable import InjectableObject

class ComponentAbstract(ABC, InjectableObject):
    
    @abstractmethod
    def set_settings(self, **kwargs):
        raise NotImplementedError("No way to manage dynamic component settings.")

    @abstractmethod
    def step(self, item:Any, **kwargs):
        raise NotImplementedError("Execute hasn't been implemented")