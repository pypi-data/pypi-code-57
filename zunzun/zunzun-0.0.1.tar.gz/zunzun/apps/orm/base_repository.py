from abc import ABC, abstractmethod
from .session import Session
from injector import inject


class BaseRepository(ABC):
    @inject
    def __init__(self, session: Session):
        self.session = session

    def __getattr__(self, name):
        return getattr(self.session, name)

    @abstractmethod
    def new(self, **kwargs):
        pass
