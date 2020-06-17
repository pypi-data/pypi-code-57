"""Basic Authentication."""

from base64 import b64encode
from dataclasses import dataclass


@dataclass(frozen=True)
class BasicAuthentication:
    """Basic Authentication.

    It can be used on the server sandbox for instance.
    """

    username: str
    password: str

    def __call__(self, url: str):
        """Return the authentication headers for the passed URL."""
        plain_credentials = f"{self.username}:{self.password}"
        encoded_credentials = str(b64encode(plain_credentials.encode("ascii")), "utf8")
        return {"Authorization": f"Basic {encoded_credentials}"}
