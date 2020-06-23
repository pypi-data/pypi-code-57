"""Official Python client for Driverless AI."""

import copy
import importlib
import json
import os
import re
from typing import Any, Union

import requests

from driverlessai import __version__
from driverlessai import _datasets
from driverlessai import _experiments
from driverlessai import _recipes
from driverlessai import _server


###############################
# Custom Exceptions
###############################

# Client exceptions
class ClientException(Exception):
    pass


# If we're not able to communicate with the DAI
# server, this exception is thrown.
class ServerDownException(ClientException):
    pass


# If we're not able to scrape server version
class ServerVersionExtractionFailed(ClientException):
    pass


class ServerVersionNotSupported(ClientException):
    pass


###############################
# Helper Functions
###############################


def is_server_up(address: str, verify: Union[bool, str] = False) -> bool:
    """Checks if a Driverless AI server is running.

    Args:
        address: full URL of the Driverless AI server to connect to
        verify: when using https on the Driverless AI server, setting this to
            False will disable SSL certificates verification. A path to
            cert(s) can also be passed to verify, see:
            https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification
    """
    try:
        requests.get(address, verify=verify)
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False


###############################
# DAI Python Client
###############################


class Client:
    """Connect to and interact with a Driverless AI server.

    Args:
        address: full URL of the Driverless AI server to connect to
        username: username for authentication on the Driverless AI server
        password: password for authentication on the Driverless AI server
        verify: when using https on the Driverless AI server, setting this to
            False will disable SSL certificates verification. A path to
            cert(s) can also be passed to verify, see:
            https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification
        backend_version_override: version of client backend to use, overrides
            Driverless AI server version detection. Specify ``"latest"`` to get
            the most recent backend supported. In most cases the user should
            rely on Driverless AI server version detection and leave this as
            the default ``None``.

    Attributes:
        connectors (Connectors): for interacting with connectors on the
            Driverless AI server
        datasets (Datasets): for interacting with datasets on the
            Driverless AI server
        experiments (Experiments): for interacting with experiments on the
            Driverless AI server
        recipes (Recipes): for interacting with recipes on the
            Driverless AI server
        server (Server): for getting information about the Driverless AI server
    """

    def __init__(
        self,
        address: str,
        username: str,
        password: str,
        verify: Union[bool, str] = True,
        backend_version_override: str = None,
    ) -> None:
        # We should check if the server is up first.
        # If we're unable to ping it, we fail.
        if not is_server_up(address, verify=verify):
            raise ServerDownException(
                "Unable to communicate with Driverless AI server. "
                "Please make sure the server is running and the address is correct."
            )

        if backend_version_override is None:
            # If the response status was not 200, we are dealing with a version of DAI
            # older than 1.8.2. If we got a response other than 200 we attempt
            # to extract the version by scraping the login page.
            try:
                response = requests.get(address + "/serverversion", verify=verify)
                if response.status_code == 200:
                    json_response = json.loads(response.text)
                    server_version = json_response["result"]["version"]
                else:
                    server_version = re.search(
                        "DRIVERLESS AI ([0-9.]+)",
                        requests.get(address, verify=verify).text,
                    )[1]
            except Exception:
                raise ServerVersionExtractionFailed(
                    "Unable to extract server version. "
                    "Please specify server version when initializing client."
                )
        else:
            if backend_version_override == "latest":
                backend_version_override = re.search("[0-9.]+", __version__)[0]
            server_version = backend_version_override

        server_module_path = (
            f"driverlessai._h2oai_client_{server_version.replace('.', '_')}"
        )
        try:
            self._server_module = importlib.import_module(
                server_module_path
            )  # type: Any
        except ModuleNotFoundError:
            raise ServerVersionNotSupported(
                f"Server version {server_version} is not supported, "
                "try updating to the latest client."
            )

        self._backend = self._server_module.protocol.Client(
            address=address, username=username, password=password, verify=verify
        )

        self.connectors = _datasets.Connectors(self)
        self.datasets = _datasets.Datasets(self)
        self.experiments = _experiments.Experiments(self)
        self.recipes = _recipes.Recipes(self)
        self.server = _server.Server(
            self, address, username, self._backend.get_app_version().version
        )

        # Warns if license is missing/expired/about to expire
        self.server.license.is_valid()

    def __repr__(self) -> str:
        return f"{self.__class__} {self!s}"

    def __str__(self) -> str:
        return self.server.address

    def _download(
        self,
        server_path: str,
        dst_dir: str,
        overwrite: bool = False,
        timeout: float = 5,
        verbose: bool = True,
    ) -> str:
        dst_path = os.path.join(dst_dir, os.path.basename(server_path))
        if overwrite or not os.path.exists(dst_path):
            s = requests.Session()
            url = self.server.address + "/files/" + server_path
            if hasattr(self._backend, "_session"):
                cookies = copy.deepcopy(self._backend._session.cookies)
                verify = copy.deepcopy(self._backend._session.verify)
            else:
                cookies = copy.deepcopy(self._backend._cookies)
                verify = copy.deepcopy(self._backend._verify)
            res = s.get(url, cookies=cookies, verify=verify, timeout=timeout)
            res.raise_for_status()
            with open(dst_path, "wb") as f:
                f.write(res.content)
        else:
            raise FileExistsError(
                dst_path + " already exists. Use `overwrite` to force download."
            )
        if verbose:
            print("Downloaded '", dst_path, "'", sep="")
        return dst_path
