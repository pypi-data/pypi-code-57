from typing import List, Union

import httpx

from netauto._validate import validate_201
from netauto.models.tools import PortScanResp, SendMail


class Tools:
    def __new__(cls, session: Union[httpx.Client, httpx.AsyncClient]):
        if isinstance(session, httpx.Client):
            return ToolsSync(session=session)
        elif isinstance(session, httpx.AsyncClient):
            return ToolsAsync(session=session)


class BaseTools:

    def __init__(self, session: Union[httpx.Client, httpx.AsyncClient]):
        self._session = session
        self._base_url = "tools/"


class ToolsSync(BaseTools):

    def __init__(self, session: httpx.Client):
        super().__init__(session=session)

    def port_scan(self, ip: str, port: int) -> PortScanResp:
        params = {"ip": ip, "port": port}
        r = self._session.post(url=f"{self._base_url}port_scan/", params=params)
        validate_201(r=r)
        return PortScanResp(**r.json())

    def send_mail(self, to: List[str], subject: str, content: str) -> SendMail:
        data = {"to": to, "subject": subject, "content": content}
        r = self._session.post(url=f"{self._base_url}send_mail/", json=data)
        validate_201(r=r)
        return SendMail(**r.json())


class ToolsAsync(BaseTools):

    def __init__(self, session: httpx.AsyncClient):
        super().__init__(session=session)

    async def port_scan(self, ip: str, port: int) -> PortScanResp:
        params = {"ip": ip, "port": port}
        r = await self._session.post(url=f"{self._base_url}port_scan/", params=params)
        validate_201(r=r)
        return PortScanResp(**r.json())

    async def send_mail(self, to: List[str], subject: str, content: str) -> SendMail:
        data = {"to": to, "subject": subject, "content": content}
        r = await self._session.post(url=f"{self._base_url}send_mail/", json=data)
        validate_201(r=r)
        return SendMail(**r.json())
