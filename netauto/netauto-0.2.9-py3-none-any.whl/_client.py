from typing import Union

import httpx

from ._auth import Auth
from ._digi import Digi
from ._tools import Tools
from ._snmp import SNMP
from ._mac import Mac
from ._cpe import CPE


class BaseClient:

    def __init__(self, netauto_url: str, api_version: int, sync: bool, username: str, password: str,
                 cert_path: Union[str, bool] = False,
                 connect_timeout: int = 5, write_timeout: int = 5, read_timeout: int = 60, pool_timeout: int = 60,
                 max_keepalive: int = 10, max_connections: int = 50):

        base_url = f"{netauto_url}/api/v{api_version}/"

        timeout = httpx.Timeout(connect_timeout=connect_timeout, write_timeout=write_timeout, read_timeout=read_timeout,
                                pool_timeout=pool_timeout)
        pool_limits = httpx.PoolLimits(max_keepalive=max_keepalive, max_connections=max_connections)
        client_settings = dict(base_url=base_url, pool_limits=pool_limits, timeout=timeout, verify=cert_path)
        if sync:
            self._session = httpx.Client(**client_settings)
        else:
            self._session = httpx.AsyncClient(**client_settings)

        self.auth = Auth(session=self._session, username=username, password=password)
        self.tools = Tools(session=self._session)
        self.digi = Digi(session=self._session)
        self.snmp = SNMP(session=self._session)
        self.mac = Mac(session=self._session)
        self.cpe = CPE(session=self._session)


class Client(BaseClient):

    def __init__(self, netauto_url: str, api_version: int, username: str, password: str,
                 cert_path: Union[str, bool] = False,
                 connect_timeout: int = 5, write_timeout: int = 5, read_timeout: int = 60, pool_timeout: int = 60,
                 max_keepalive: int = 10, max_connections: int = 50):
        super().__init__(netauto_url=netauto_url, api_version=api_version, sync=True, username=username,
                         password=password, cert_path=cert_path,
                         connect_timeout=connect_timeout, write_timeout=write_timeout, read_timeout=read_timeout,
                         pool_timeout=pool_timeout, max_keepalive=max_keepalive, max_connections=max_connections)

    def __enter__(self):
        self.auth.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session: httpx.Client
        self._session.close()

    def close_session(self):
        self._session: httpx.Client
        self._session.close()


class AsyncClient(BaseClient):

    def __init__(self, netauto_url: str, api_version: int, username: str, password: str,
                 cert_path: Union[str, bool] = False,
                 connect_timeout: int = 5, write_timeout: int = 5, read_timeout: int = 60, pool_timeout: int = 60,
                 max_keepalive: int = 10, max_connections: int = 50):
        super().__init__(netauto_url=netauto_url, api_version=api_version, sync=False, username=username,
                         password=password, cert_path=cert_path,
                         connect_timeout=connect_timeout, write_timeout=write_timeout, read_timeout=read_timeout,
                         pool_timeout=pool_timeout, max_keepalive=max_keepalive, max_connections=max_connections)

    async def __aenter__(self):
        await self.auth.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.aclose()

    async def close_session(self):
        await self._session.aclose()
