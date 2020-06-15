from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)  # type: ignore
class Event(ABC):
    id: str = field(init=False, default_factory=lambda: str(uuid4()))
    created_at: str = field(init=False, default_factory=lambda: str(datetime.now()))

    @classmethod
    def fqn(cls) -> str:
        return f"{cls.__module__}.{cls.__name__}"
