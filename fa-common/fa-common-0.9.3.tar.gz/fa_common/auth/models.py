from datetime import datetime
from typing import List, Optional

from pydantic import AnyUrl, EmailStr

from fa_common.models import CamelModel


class AuthUser(CamelModel):
    sub: str
    name: str = "Unknown User"
    email: Optional[EmailStr]
    nickname: Optional[str] = None
    email_verified: bool = False
    picture: Optional[AnyUrl] = None
    updated_at: Optional[datetime] = None
    scopes: List[str] = []
