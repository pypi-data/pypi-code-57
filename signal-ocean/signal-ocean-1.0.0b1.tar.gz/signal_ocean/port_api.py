from typing import List, Iterable
from urllib.parse import urljoin

import requests

from .connection import Connection
from .port import Port
from .port_filter import PortFilter


class PortAPI:
    def __init__(self, connection: Connection = None):
        self.__connection = connection or Connection()

    def get_ports(self, port_filter: PortFilter = None) -> List[Port]:
        url = urljoin(
            self.__connection.api_host,
            'htl-api/historical-tonnage-list/ports'
        )

        response = requests.get(url, headers=self.__connection.headers)
        response.raise_for_status()

        ports = _parse_json(response.json())
        port_filter = port_filter or PortFilter()

        return list(port_filter._apply(ports))


def _parse_json(json) -> Iterable[Port]:
    return map(lambda p: Port(p.get('id'), p.get('name')), json)
