from typing import List

from httpx import Client

from netauto._exceptions import FailedRequest
from netauto.models.tools import PortScanResp, SendMail


class Tools:

    def __init__(self, session: Client):
        self._session = session

    def port_scan(self, ip: str, port: int) -> PortScanResp:
        params = {"ip": ip, "port": port}
        r = self._session.post(url="tools/port_scan/", params=params)
        if r.status_code != 201:
            raise FailedRequest(r.text)
        else:
            return PortScanResp(**r.json())

    def send_mail(self, to: List[str], subject: str, content: str) -> SendMail:
        data = {"to": to, "subject": subject, "content": content}
        r = self._session.post(url="tools/send_mail/", json=data)
        if r.status_code != 201:
            raise FailedRequest(r.text)
        else:
            return SendMail(**r.json())
