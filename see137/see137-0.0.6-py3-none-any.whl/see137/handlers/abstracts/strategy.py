from abc import ABC
from typing import Any

class StrategyAbstract(ABC):
    def __init__(self):
        self._data = None
        self._processed = None
    
    @property
    def preprocessed(self):
        if self._processed is None:
            raise AttributeError("Preprocessed data hasn't been set")
        return self._processed
    
    @property
    def information(self):
        if self._data is None:
            raise AttributeError("Data hasn't been set yet")
        return self._data
    
    @information.setter
    def information(self, _data:Any):
        self._data = _data

    def data_check(self):
        raise NotImplementedError("Data check isn't there")

    def process_data(self) -> Any:
        """ Store preprocess the data and ensure it's stored here """
        raise NotImplementedError

    def get_decision(self) -> Any:
        """ Get the preprocessed data and ensure"""
        raise NotImplementedError

    def step(self, data:Any):
        """ Should return an action tuple. 
            
            parameter:
                data: Any

            return:
                action: tuple
                    ([0 - 2], [0 - 99]) 
        """
        self._data = data
        self.data_check()
        self.process_data()
        return self.get_decision()
        
    
    def reset(self):
        self._data = None
        self._processed = None

class ExampleStrategy(StrategyAbstract):
    def process_data(self):
        self.information = self.information + 1
    
    def data_check(self):
        pass

    def get_decision(self):

        if self.information == 1:
            return 0
        elif self.information == 2:
            return 1
        else:
            return 2