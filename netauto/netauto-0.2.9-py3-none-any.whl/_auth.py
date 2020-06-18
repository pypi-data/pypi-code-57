from typing import Union

import httpx

from netauto._validate import validate_201


class Auth:

    def __new__(cls, session: Union[httpx.Client, httpx.AsyncClient], **kwargs):
        if isinstance(session, httpx.Client):
            return AuthSync(session=session, **kwargs)
        elif isinstance(session, httpx.AsyncClient):
            return AuthAsync(session=session, **kwargs)


class BaseAuth:

    def __init__(self, session: Union[httpx.Client, httpx.AsyncClient], username: str, password: str):
        self._session = session
        self._username = username
        self._password = password
        self._base_url = "auth/"
        self._user_data = {"username": self._username, "password": self._password}


class AuthSync(BaseAuth):

    def __init__(self, session: httpx.Client, username: str, password: str):
        super().__init__(session=session, username=username, password=password)

    def login(self) -> None:
        r = self._session.post(url=self._base_url, data=self._user_data, timeout=20)
        validate_201(r)
        self._session.headers["Authorization"] = f"Bearer {r.json()['access_token']}"


class AuthAsync(BaseAuth):

    def __init__(self, session: httpx.AsyncClient, username: str, password: str):
        super().__init__(session=session, username=username, password=password)

    async def login(self) -> None:
        r = await self._session.post(url=self._base_url, data=self._user_data, timeout=20)
        validate_201(r)
        self._session.headers["Authorization"] = f"Bearer {r.json()['access_token']}"
