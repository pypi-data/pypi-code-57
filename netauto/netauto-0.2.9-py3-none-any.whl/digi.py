from httpx import Client

from netauto._exceptions import FailedRequest
from netauto.models.digi import DigiList


class Digi:

    def __init__(self, session: Client):
        self._session = session

    def reboot_digi(self, ip: str) -> bool:
        params = {"ip": ip}
        r = self._session.post(url="digi/reboot/", params=params)
        if r.status_code != 201:
            return False
        else:
            return True

    def get_all_digi(self) -> DigiList:
        r = self._session.get(url="digi/")
        if r.status_code != 200:
            raise FailedRequest(r.text)
        else:
            return DigiList(**r.json())
