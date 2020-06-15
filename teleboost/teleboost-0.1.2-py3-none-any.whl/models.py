from typing import Optional

from pydantic import BaseModel

__all__ = ("ViewResult",)


class ViewResult(BaseModel):
    ok: bool
    proxy: str
    error: Optional[str] = None
