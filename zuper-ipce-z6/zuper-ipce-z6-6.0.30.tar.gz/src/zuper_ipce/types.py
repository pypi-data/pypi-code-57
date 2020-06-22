from datetime import datetime
from typing import Dict, List, Union

from zuper_typing import is_Any, TypeLike

__all__ = ["IPCE", "TypeLike", "ModuleName", "QualName"]

IPCE = Union[int, str, float, bytes, datetime, List["IPCE"], Dict[str, "IPCE"], type(None)]

ModuleName = QualName = str

_ = TypeLike


def is_unconstrained(t: TypeLike):
    assert t is not None
    return is_Any(t) or (t is object)
