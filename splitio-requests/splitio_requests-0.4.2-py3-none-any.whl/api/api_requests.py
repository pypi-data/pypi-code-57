from abc import ABC
from typing import Optional, Dict, Tuple, NoReturn, Union
from requests import Session


class APIRequests(ABC):
    def __init__(
            self,
            token: str,
            hostname: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> None:
        self._hostname = hostname or 'https://api.split.io/internal/api/v2'
        self._headers = headers or {'Authorization': token, 'Content-Type': 'application/json'}

    def _requests_retry_session(
            self,
            retries: int = 5,
            backoff_factor: float = 0.3,
            status_forcelist: Tuple[int, ...] = (429, 500, 502, 503, 504),
            session: Optional[Session] = None
    ) -> Union[NoReturn, Session]:
        raise NotImplementedError
