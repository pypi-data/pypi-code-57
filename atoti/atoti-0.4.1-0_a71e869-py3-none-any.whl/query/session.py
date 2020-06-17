"""Making MDX queries on existing sessions."""

import json
from typing import Any, Mapping, Optional, Union
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pandas as pd

from .._docs_utils import doc
from .._repr_utils import convert_repr_json_to_html, repr_json_session
from ._cellset import Cellset, cellset_to_pandas
from ._discovery import Discovery
from ._discovery_utils import create_cubes_from_discovery
from .auth import Auth
from .cubes import QueryCubes

SUPPORTED_VERSIONS = ["5", "5.Z1", "4"]

_Context = Mapping[str, Any]

_QUERY_MDX_ARGS = """Args:
            mdx: The MDX ``SELECT`` query to execute.
                Requirements to guarantee that the DataFrame is well shaped:

                * No more than two axes.
                * No grand or sub totals.
                * Nothing else but measures on the ``COLUMNS`` axis.
            timeout: The query timeout in seconds.
"""

_QUERY_MDX_DOC = f"""Execute an MDX query and return its result as a pandas DataFrame.

        {_QUERY_MDX_ARGS}
"""


class QuerySession:
    """Used to query an existing session."""

    def __init__(self, url: str, auth: Auth, name: str):
        """Init.

        Args:
            url: The server base URL.
            auth: The authentication to use.
            name: The name to give to the session.
        """
        self._url = url
        self._name = name
        self._auth = auth
        self._version = self._fetch_version()
        self._discovery = self._fetch_discovery()
        self._cubes = create_cubes_from_discovery(self._discovery, self)

    @property
    def cubes(self) -> QueryCubes:
        """Cubes of the session."""
        return self._cubes

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    def url(self) -> str:
        """URL of the session."""
        return self._url

    def _execute_json_request(self, url: str, body: Optional[Any] = None) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self._auth(url) or {})
        data = json.dumps(body).encode("utf8") if body else None
        # The user can send any URL, wrapping it in a request object makes it a bit safer
        request = Request(url, data=data, headers=headers)
        try:
            response = urlopen(request)  # nosec
            return json.loads(response.read().decode("utf8"))
        except HTTPError as error:
            error_json = error.read()
            error_data = json.loads(error_json)
            raise RuntimeError("Request failed", error_data)

    def _fetch_version(self) -> str:
        url = f"{self._url}/versions/rest"
        response = self._execute_json_request(url)
        exposed_versions = [
            version["id"] for version in response["apis"]["pivot"]["versions"]
        ]
        try:
            return next(
                version for version in SUPPORTED_VERSIONS if version in exposed_versions
            )
        except:
            raise RuntimeError(
                f"Exposed versions: {exposed_versions}"
                f" don't match supported ones: {SUPPORTED_VERSIONS}"
            )

    def _fetch_discovery(self) -> Discovery:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/discovery"
        response = self._execute_json_request(url)
        return Discovery._from_dict(response["data"])

    @doc(_QUERY_MDX_DOC)
    def query_mdx(self, mdx: str, *, timeout: int = 30, **kwargs: Any,) -> pd.DataFrame:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/query/mdx"
        # We use kwargs to hide uncommon features from the public API.
        context: _Context = kwargs.get("context", {})
        if timeout is not None:
            context = {"queriesTimeLimit": timeout, **context}
        body: Mapping[str, Union[str, _Context]] = {"context": context, "mdx": mdx}
        response = self._execute_json_request(url, body)
        cellset = Cellset._from_dict(response["data"])
        get_level_data_types = kwargs.get("get_level_data_types")
        return cellset_to_pandas(cellset, self._discovery, get_level_data_types)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_session(self)
