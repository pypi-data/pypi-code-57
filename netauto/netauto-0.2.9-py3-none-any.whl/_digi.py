from typing import Union

import httpx

from netauto.models.digi import DigiList
from netauto._validate import validate_200, validate_201


class Digi:
    def __new__(cls, session: Union[httpx.Client, httpx.AsyncClient]):
        if isinstance(session, httpx.Client):
            return DigiSync(session=session)
        elif isinstance(session, httpx.AsyncClient):
            return DigiAsync(session=session)


class BaseDigi:

    def __init__(self, session: Union[httpx.Client, httpx.AsyncClient]):
        self._session = session
        self._base_url = "digi/"


class DigiSync(BaseDigi):

    def __init__(self, session: httpx.Client):
        super().__init__(session=session)

    def reboot_digi(self, ip: str) -> bool:
        params = {"ip": ip}
        r = self._session.post(url=f"{self._base_url}reboot/", params=params)
        validate_201(r=r)
        return True

    def get_all_digi(self) -> DigiList:
        r = self._session.get(url=self._base_url, timeout=20)
        validate_200(r=r)
        return DigiList(**r.json())


class DigiAsync(BaseDigi):
    def __init__(self, session: httpx.AsyncClient):
        super().__init__(session=session)

    async def reboot_digi(self, ip: str) -> bool:
        params = {"ip": ip}
        r = await self._session.post(url=f"{self._base_url}reboot/", params=params)
        validate_201(r=r)
        return True

    async def get_all_digi(self) -> DigiList:
        print(self._session.headers["Authorization"])
        r = await self._session.get(url=self._base_url, timeout=20)
        validate_200(r=r)
        return DigiList(**r.json())
