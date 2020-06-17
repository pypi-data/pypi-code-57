from abc import ABC, abstractmethod
class clientAbc(ABC):

    @abstractmethod
    def sendRequest(self, reqObj, respObj):
        pass