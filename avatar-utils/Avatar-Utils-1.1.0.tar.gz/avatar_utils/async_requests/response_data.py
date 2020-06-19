from dataclasses import dataclass
from typing import Optional, Sequence

from aiohttp import ClientResponse


@dataclass
class ResponseData:

    url: str

    started_at: float
    elapsed: float = None

    request_schema: str = None
    host: str = None
    port: int = None
    route: str = None
    route_params: str = None

    finished_at: Optional[float] = None

    text: Optional[str] = None
    json: Sequence = None

    response: Optional[ClientResponse] = None
    exception: Optional[Exception] = None

    def __post_init__(self):
        if self.finished_at:
            self.elapsed = self.finished_at - self.started_at

        self.request_schema, self.host = self.url.split('//', 1)
        self.port = 443 if self.request_schema.lower() == 'https' else 80

        if '/' in self.host:
            self.host, self.route = self.host.split('/', 1)

        self.route = '/' + self.route

        if ':' in self.host:
            self.host, self.port = self.host.split(':', 1)

        if '?' in self.route:
            self.route, self.route_params = self.host.split('?', 1)
