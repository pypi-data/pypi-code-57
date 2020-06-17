"""Query Authentication."""

from typing import Callable, Mapping, Optional

HttpHeaders = Optional[Mapping[str, str]]

Auth = Callable[[str], HttpHeaders]
"""Called with the URL of the request and return the HTTP headers necessary to authenticate it."""
