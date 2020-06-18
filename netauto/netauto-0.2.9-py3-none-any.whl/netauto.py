import urllib3

from httpx import Client

from netauto._auth import Auth
from netauto._digi import Digi
from netauto._tools import Tools
from netauto._snmp import SNMP
from netauto._mac import Mac


class NetAuto:

    def __init__(self, netauto_url: str, api_version: int, username: str, password: str, cert_path: str = ""):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._base_url = f"{netauto_url}/api/v{api_version}/"
        if cert_path:
            self._session = Client(verify=cert_path, base_url=self._base_url)
        else:
            self._session = Client(verify=False, base_url=self._base_url)

        self.auth = Auth(session=self._session, username=username, password=password)
        self.tools = Tools(session=self._session)
        self.digi = Digi(session=self._session)
        self.snmp = SNMP(session=self._session)
        self.mac = Mac(session=self._session)

    def __enter__(self):
        self.auth.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def close_session(self):
        self._session.close()
