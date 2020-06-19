from typing import Any, List, Dict
from dataclasses import dataclass, asdict
import json
import pickle


class Status:
    SUCCESS = 0
    ERROR = 1
    METHOD = 2


class Method:
    GET = 'get'
    SET = 'set'
    CALL = 'call'
    REGISTER = 'register'
    LOCK = 'lock'
    UNLOCK = 'unlock'
    AVAILABLE = 'available'


@dataclass
class Message:
    id: int = 0
    data: Any = None

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        return cls(**json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_pickle(self) -> bytes:
        return pickle.dumps(self)


@dataclass
class Response(Message):
    status: int = Status.SUCCESS


@dataclass
class Request(Message):
    method: str = Method.GET
