from httpx import Client
from .exceptions import RegexAndNoneRegexParm, FailedRequest
from .models.mac import MacInDBList, MacInDB, MacDeleted
from .models.mac import Mac as MacModel


class Mac:

    def __init__(self, session: Client):
        self._session = session

    def get_mac(self, active: bool = None, mac_address: str = None, switch_ip: str = None,
                switch_serial_number: str = None, switch_port_id: str = None, oui: str = None, vlan_id: int = None,
                regex_mac_address: str = None, regex_switch_ip: str = None, kit_printer: bool = None,
                limit: int = 10) -> MacInDBList:

        params = {"active": active, "mac_address": mac_address, "switch_ip": switch_ip,
                  "switch_serial_number": switch_serial_number, "switch_port_id": switch_port_id, "oui": oui,
                  "vlan_id": vlan_id, "kit_printer": kit_printer, "limit": limit}

        if regex_mac_address:
            if mac_address:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["mac_address"] = f"~{regex_mac_address}"
        if regex_switch_ip:
            if switch_ip:
                raise RegexAndNoneRegexParm("it is not allowed to have both regex and none regex")
            else:
                params["switch_ip"] = f"~{regex_switch_ip}"

        for k, v in params.copy().items():
            if v is None:
                del params[k]

        r = self._session.get(url="mac/", params=params)
        if r.status_code != 200:
            raise FailedRequest(r.text)
        return MacInDBList(**r.json())

    def create_or_update_mac(self, active: bool, mac_address: str, switch_ip: str, switch_serial_number: str,
                             switch_port_id: int, vlan_id: int, update_time: bool = True) -> MacInDB:
        mac_data_input = MacModel(active=active, mac_address=mac_address, switch_ip=switch_ip,
                                  switch_serial_number=switch_serial_number, switch_port_id=switch_port_id,
                                  vlan_id=vlan_id)
        params = {"update_time": update_time}
        r = self._session.put(url="mac/", json=mac_data_input.dict(), params=params)
        if r.status_code != 201:
            raise FailedRequest(r.text)
        return MacInDB(**r.json())

    def delete_mac(self, mac_address: str) -> MacDeleted:
        params = {"mac_address": mac_address}
        r = self._session.delete(url="mac/", params=params)
        if r.status_code != 200:
            raise FailedRequest(r.text)
        return MacDeleted(**r.json())

    def update_kit_printer(self, mac_address: str, kit_printer: bool) -> MacInDB:
        params = {"mac_address": mac_address, "kit_printer": kit_printer}
        r = self._session.put(url="mac/kit-printer/", params=params)
        if r.status_code != 200:
            raise FailedRequest(r.text)
        return MacInDB(**r.json())
