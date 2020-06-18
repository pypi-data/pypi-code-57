from httpx import Client
from netauto._exceptions import FailedRequest

from netauto.models.snmp import ReturnGetData, ReturnBulkData, SnmpRequestData


class SNMP:

    def __init__(self, session: Client):
        self._session = session

    def get(self, snmp_version: int, ip_list: list, oids: list) -> ReturnGetData:
        data = SnmpRequestData(snmp_version=snmp_version, ip_list=ip_list, oids=oids)
        r = self._session.post(url="snmp/get/", json=data.dict(), timeout=15)
        if r.status_code != 201:
            raise FailedRequest(r.text)
        else:
            return ReturnGetData(**r.json())

    def bulk_walk(self, snmp_version: int, ip_list: list, oids: list) -> ReturnBulkData:
        data = SnmpRequestData(snmp_version=snmp_version, ip_list=ip_list, oids=oids)
        r = self._session.post(url="snmp/bulk_walk/", json=data.dict(), timeout=15)
        if r.status_code != 201:
            raise FailedRequest(r.text)
        else:
            return ReturnBulkData(**r.json())
