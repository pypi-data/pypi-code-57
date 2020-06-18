from typing import Union

import httpx

from ._exceptions import RegexAndNoneRegexParm
from ._validate import validate_200, validate_201
from .models.mac import MacInDBList, MacInDB, MacDeleted
from .models.mac import Mac as MacModel


class Mac:
    def __new__(cls, session: Union[httpx.Client, httpx.AsyncClient]):
        if isinstance(session, httpx.Client):
            return MacSync(session=session)
        elif isinstance(session, httpx.AsyncClient):
            return MacAsync(session=session)


class BaseMac:

    def __init__(self, session: Union[httpx.Client, httpx.AsyncClient]):
        self._session = session
        self._base_url = "mac/"

    @staticmethod
    def _regex_params(params: dict, regex_mac_address: Union[None, str],
                      regex_switch_ip: Union[None, str]) -> dict:

        if regex_mac_address:
            if params["mac_address"]:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["mac_address"] = f"~{regex_mac_address}"
        if regex_switch_ip:
            if params["switch_ip"]:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["switch_ip"] = f"~{regex_switch_ip}"

        for k, v in params.copy().items():
            if v is None:
                del params[k]

        return params


class MacSync(BaseMac):

    def __init__(self, session: httpx.Client):
        super().__init__(session=session)

    def get_mac(self,
                active: bool = None,
                mac_address: str = None,
                switch_ip: str = None,
                switch_serial_number: str = None,
                switch_port_id: str = None,
                oui: str = None,
                vlan_id: int = None,
                regex_mac_address: str = None,
                regex_switch_ip: str = None,
                kit_printer: bool = None,
                limit: int = 10) -> MacInDBList:

        params = {"active": active, "mac_address": mac_address, "switch_ip": switch_ip,
                  "switch_serial_number": switch_serial_number, "switch_port_id": switch_port_id, "oui": oui,
                  "vlan_id": vlan_id, "kit_printer": kit_printer, "limit": limit}

        params = self._regex_params(params=params, regex_mac_address=regex_mac_address, regex_switch_ip=regex_switch_ip)
        r = self._session.get(url=self._base_url, params=params)
        validate_200(r=r)
        return MacInDBList(**r.json())

    def create_or_update_mac(self, mac: MacModel, update_time: bool = True) -> MacInDB:
        params = {"update_time": update_time}
        r = self._session.put(url=self._base_url, json=mac.dict(), params=params)
        validate_201(r=r)
        return MacInDB(**r.json())

    def delete_mac(self, mac_address: str) -> MacDeleted:
        params = {"mac_address": mac_address}
        r = self._session.delete(url=self._base_url, params=params)
        validate_200(r=r)
        return MacDeleted(**r.json())

    def update_kit_printer(self, mac_address: str, kit_printer: bool) -> MacInDB:
        params = {"mac_address": mac_address, "kit_printer": kit_printer}
        r = self._session.put(url=f"{self._base_url}kit-printer/", params=params)
        validate_200(r=r)
        return MacInDB(**r.json())


class MacAsync(BaseMac):
    def __init__(self, session: httpx.AsyncClient):
        super().__init__(session=session)

    async def get_mac(self,
                      active: bool = None,
                      mac_address: str = None,
                      switch_ip: str = None,
                      switch_serial_number: str = None,
                      switch_port_id: str = None,
                      oui: str = None,
                      vlan_id: int = None,
                      regex_mac_address: str = None,
                      regex_switch_ip: str = None,
                      kit_printer: bool = None,
                      limit: int = 10) -> MacInDBList:
        params = {"active": active, "mac_address": mac_address, "switch_ip": switch_ip,
                  "switch_serial_number": switch_serial_number, "switch_port_id": switch_port_id, "oui": oui,
                  "vlan_id": vlan_id, "kit_printer": kit_printer, "limit": limit}

        params = self._regex_params(params=params, regex_mac_address=regex_mac_address, regex_switch_ip=regex_switch_ip)
        r = await self._session.get(url=self._base_url, params=params)

        validate_200(r=r)
        return MacInDBList(**r.json())

    async def create_or_update_mac(self, mac: MacModel, update_time: bool = True) -> MacInDB:
        params = {"update_time": update_time}
        r = await self._session.put(url=self._base_url, json=mac.dict(), params=params)
        validate_201(r=r)
        return MacInDB(**r.json())

    async def delete_mac(self, mac_address: str) -> MacDeleted:
        params = {"mac_address": mac_address}
        r = await self._session.delete(url=self._base_url, params=params)
        validate_200(r=r)
        return MacDeleted(**r.json())

    async def update_kit_printer(self, mac_address: str, kit_printer: bool) -> MacInDB:
        params = {"mac_address": mac_address, "kit_printer": kit_printer}
        r = await self._session.put(url=f"{self._base_url}kit-printer/", params=params)
        validate_200(r=r)
        return MacInDB(**r.json())
