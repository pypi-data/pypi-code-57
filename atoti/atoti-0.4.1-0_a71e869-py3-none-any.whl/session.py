"""Session."""

from __future__ import annotations

import logging
from pathlib import Path
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Mapping,
    Optional,
    Sequence,
    Type,
    Union,
)

import pandas as pd
from typing_extensions import Literal

from atoti.sampling import DEFAULT_SAMPLING_MODE

from ._docs_utils import (
    CSV_KWARGS,
    PARQUET_KWARGS,
    STORE_CREATION_KWARGS,
    STORE_SHARED_KWARGS,
    doc,
)
from ._file_utils import _split_path_and_pattern
from ._java_api import JavaApi
from ._pandas_utils import get_csv_sep_for_pandas_read_load, pandas_to_temporary_csv
from ._path_utils import stem_path
from ._query_plan import QueryAnalysis
from ._repr_utils import convert_repr_json_to_html, repr_json_session
from ._server_subprocess import ServerSubprocess
from ._type_utils import BASE_SCENARIO, Port, ScenarioName, check_literal
from .config import SessionConfiguration
from .cube import Cube
from .cubes import Cubes
from .exceptions import AtotiException, AtotiJavaException
from .logs import Logs
from .query import open_query_session
from .query.session import _QUERY_MDX_ARGS, _QUERY_MDX_DOC
from .store import Store, _create_store
from .stores import Stores
from .types import AtotiType
from .vendor.atotipy4j.java_gateway import DEFAULT_PORT as _PY4J_DEFAULT_PORT

if TYPE_CHECKING:
    from .query.session import QuerySession
    from .sampling import SamplingMode

    # Numpy is only imported for type checking as we don't want it as a dependency
    import numpy as np
    import pathlib

    # Spark is only imported for type checking as we don't want it as a dependency
    from pyspark.sql import DataFrame as SparkDataFrame

_CubeCreationMode = Literal[  # pylint: disable=invalid-name
    "auto", "manual", "no_measures"
]


def _resolve_metadata_db(metadata_db: str) -> str:
    if metadata_db.startswith("jdbc"):
        raise NotImplementedError("jdbc URLs are not yet supported.")

    # Make sure the parent directory exists.
    path = Path(metadata_db)
    if path.exists() and not path.is_dir():
        raise ValueError(f"metadata_db is not a directory: {metadata_db}")
    path.mkdir(exist_ok=True)

    # Return the fully resolved path.
    return str(path.resolve())


class Session:
    """Holds a connection to the Java gateway."""

    def __init__(
        self, name: str, *, config: SessionConfiguration, **kwargs: Any,
    ):
        """Create the session and the Java gateway.

        Args:
            name: The name of the session.
            config: The configuration of the session.

        """
        self._name = name
        self._sampling_mode = (
            config.sampling_mode
            if config.sampling_mode is not None
            else DEFAULT_SAMPLING_MODE
        )
        self._config = config
        self._create_java_api(**kwargs,)
        try:
            self._configure_session()
        except AtotiJavaException as ave:
            # Raise an exception if the session configuration fails
            raise AtotiException(
                f"{ave.java_traceback}\n"
                f"An error occured while configuring the session.\n"
                f"The logs are availbe at {self.logs_path}"
            )
        self._cubes = Cubes(self._java_api)
        self._closed = False

    def _create_java_api(
        self, **kwargs: Any,
    ):
        py4j_java_port: Port
        if kwargs.get("use_remote_process", False):
            py4j_java_port = Port(_PY4J_DEFAULT_PORT)
            self._server_subprocess = None
            logging.getLogger("atoti.process").warning(
                "use_remote_process is True. Expecting a running server with Py4J listening on port %d",  # pylint: disable=line-too-long
                py4j_java_port,
            )
        else:
            self._server_subprocess = ServerSubprocess(
                port=Port(self._config.port) if self._config.port else None,
                url_pattern=self._config.url_pattern,
                max_memory=self._config.max_memory,
                java_args=self._config.java_args,
                **kwargs,
            )
            py4j_java_port = self._server_subprocess.py4j_java_port
        self._java_api: JavaApi = JavaApi(
            py4j_java_port, aws_region=kwargs.get("aws_region", None)
        )

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    def cubes(self) -> Cubes:
        """Cubes of the session."""
        return self._cubes

    @property
    def stores(self) -> Stores:  # noqa: D401
        """Stores of the session."""
        return Stores(
            self._java_api,
            {
                store: Store(store, self._java_api)
                for store in self._java_api.get_stores()
            },
        )

    @property
    def logs_path(self) -> Path:
        """Path to the session logs file."""
        if not self._server_subprocess:
            raise NotImplementedError(
                "The logs path is not available when using a query server process"
            )
        return self._server_subprocess.logs_path

    def logs_tail(self, n: int = 20) -> Logs:
        """Return the n last lines of the logs or all the lines if ``n <= 0``."""
        with open(self.logs_path) as logs:
            lines = logs.readlines()
            last_lines = lines[-n:] if n > 0 else lines
            # Wrap in a Logs to display nicely.
            return Logs(last_lines)

    def _configure_session(self):
        """Configure the session."""
        if self._config.metadata_db:
            self._java_api.set_metadata_db(
                _resolve_metadata_db(self._config.metadata_db)
            )

        if self._config.roles is not None:
            self._java_api.configure_roles(self._config.roles)

        if self._config.authentication is not None:
            # The session ID is used to make the default basic authentication realm unique so that
            # multiple sessions running on the same machine can have different users and roles.
            #
            # We used to provide this uniqueness by suffixing the session port to the realm but we
            # cannot do this anymore because the session needs to be started to retrieve its port.
            #
            # We use the Py4J Java port instead since it is guaranteed to be unique
            # for each session running on a single machine too.
            session_id = str(
                self._server_subprocess.py4j_java_port
                if self._server_subprocess
                else _PY4J_DEFAULT_PORT
            )
            self._java_api.configure_authentication(
                self._config.authentication, self.name, session_id
            )

        # Other configuration
        self._java_api.start_application()

    def __enter__(self) -> Session:
        """Enter this session's context manager.

        Returns:
            self: to assign it to the "as" keyword.

        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit this session's context manager.

        Close the session.

        """
        self.close()

    def _clear(self):
        """Clear this session and free all the associated resources."""
        self._java_api.clear_session()

    @property
    def closed(self) -> bool:
        """Return whether the session is closed or not."""
        return self._closed

    def close(self):
        """Close this session and free all the associated resources."""
        self._java_api.shutdown()
        if self._server_subprocess:
            self.wait()
        self._closed = True

    def wait(self) -> None:
        """Wait for the underlying server subprocess to terminate.

        This will prevent the Python process to exit.
        """
        if self._server_subprocess is None:
            raise ValueError("Server subprocess is not defined")
        self._server_subprocess.wait()

    @doc(**STORE_CREATION_KWARGS)
    def create_store(
        self,
        types: Mapping[str, AtotiType],
        store_name: str,
        *,
        keys: Optional[Sequence[str]] = None,
        partitioning: Optional[str] = None,
        sampling_mode: Optional[SamplingMode] = None,
    ) -> Store:
        """Create a store from a schema.

        Args:
            types: Types for all columns of the store. This defines the columns which will be
                expected in any future data loaded into the store.
            {store_name}
            {keys}
            {partitioning}
            {sampling_mode}

        """
        mode = sampling_mode if sampling_mode is not None else self._sampling_mode
        self._java_api.create_store(types, store_name, keys, partitioning, mode)
        return _create_store(self._java_api, store_name)

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS})
    def read_pandas(
        self,
        dataframe: pd.DataFrame,  # type: ignore
        store_name: str,
        *,
        keys: Optional[Sequence[str]] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        types: Optional[Mapping[str, AtotiType]] = None,
        **kwargs: Any,
    ) -> Store:
        """Read a pandas DataFrame into a store.

        All the named indices of the DataFrame are included into the store.
        Multilevel columns are flattened into a single string name.

        Args:
            dataframe: The DataFrame to load.
            {keys}
            {store_name}
            {in_all_scenarios}
            {partitioning}
            types: Types for some or all columns of the store.
                Types for non specified columns will be inferred.

        Returns:
            The created store holding the content of the DataFrame.
        """
        # set sep to | because can contains list with sep , [x, y, ...]
        sep, kwargs = get_csv_sep_for_pandas_read_load(kwargs)
        file_path, atoti_types_mapping = pandas_to_temporary_csv(
            dataframe, sep, prefix=store_name
        )
        if types is not None:
            atoti_types_mapping = {**atoti_types_mapping, **types}

        return self.read_csv(
            file_path,
            keys=keys,
            in_all_scenarios=in_all_scenarios,
            store_name=store_name,
            partitioning=partitioning,
            types=atoti_types_mapping,
            sep=sep,
            **kwargs,
        )

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS})
    def read_spark(
        self,
        dataframe: SparkDataFrame,  # type: ignore
        store_name: str,
        *,
        keys: Optional[Sequence[str]] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
    ) -> Store:
        """Read a Spark DataFrame into a store.

        Args:
            dataframe: The DataFrame to load.
            {keys}
            {store_name}
            {in_all_scenarios}
            {partitioning}

        Returns:
            The created store holding the content of the DataFrame.
        """
        from ._spark_utils import spark_to_temporary_parquet

        # Create a Parquet and read it
        file_name = spark_to_temporary_parquet(dataframe, store_name)
        return self.read_parquet(
            path=file_name,
            keys=keys,
            store_name=store_name,
            in_all_scenarios=in_all_scenarios,
            partitioning=partitioning,
        )

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS, **CSV_KWARGS})
    def read_csv(
        self,
        path: Union[pathlib.Path, str],
        *,
        keys: Optional[Sequence[str]] = None,
        store_name: Optional[str] = None,
        in_all_scenarios: bool = True,
        sep: Optional[str] = None,
        encoding: str = "utf-8",
        process_quotes: Optional[bool] = None,
        partitioning: Optional[str] = None,
        types: Optional[Mapping[str, AtotiType]] = None,
        watch: bool = False,
        array_sep: Optional[str] = None,
        sampling_mode: Optional[SamplingMode] = None,
    ) -> Store:
        """Read a CSV file into a store.

        Args:
            {path}
            {keys}
            store_name: The name of the store to create. Defaults to the final component of the given ``path``.
            {in_all_scenarios}
            {sep}
            {encoding}
            {process_quotes}
            {partitioning}
            types: Types for some or all columns of the store.
                Types for non specified columns will be inferred from the first 1,000 lines.
            {watch}
            {array_sep}
            {sampling_mode}

        Returns:
            The created store holding the content of the CSV file(s).
        """
        path, pattern = _split_path_and_pattern(path)

        store_name = store_name or stem_path(path)

        # Load the CSV into the store
        mode = sampling_mode if sampling_mode is not None else self._sampling_mode

        self._java_api.create_store_from_csv(
            path,
            store_name,
            keys,
            in_all_scenarios,
            sep,
            encoding,
            process_quotes,
            partitioning,
            types,
            watch,
            array_sep,
            pattern,
            mode,
        )

        return _create_store(self._java_api, store_name)

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS, **PARQUET_KWARGS})
    def read_parquet(
        self,
        path: Union[pathlib.Path, str],
        *,
        keys: Optional[Sequence[str]] = None,
        store_name: Optional[str] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        sampling_mode: Optional[SamplingMode] = None,
        watch: bool = False,
    ) -> Store:
        """Read a Parquet file into a store.

        Args:
            {path}
            {keys}
            store_name: The name of the store to create. Defaults to the final component of the given ``path``.
            {in_all_scenarios}
            {partitioning}
            {sampling_mode}
            {watch}

        Returns:
            The created store holding the content of the Parquet file(s).
        """
        store_name = store_name or stem_path(path)
        mode = sampling_mode if sampling_mode is not None else self._sampling_mode
        # Load the parquet into the store
        self._java_api.create_store_from_parquet(
            path, store_name, keys, in_all_scenarios, partitioning, mode, watch
        )
        return _create_store(self._java_api, store_name)

    @doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS})
    def read_numpy(
        self,
        array: np.ndarray,  # type: ignore
        columns: Sequence[str],
        store_name: str,
        *,
        keys: Optional[Sequence[str]] = None,
        in_all_scenarios: bool = True,
        partitioning: Optional[str] = None,
        **kwargs: Any,
    ) -> Store:
        """Read a NumPy 2D array into a new store.

        Args:
            array: The NumPy 2D ndarray to read the data from.
            columns: The names to use for the store's columns.
                They must be in the same order as the values in the NumPy array.
            {keys}
            {store_name}
            {in_all_scenarios}
            {partitioning}

        Returns:
            The created store holding the content of the array.
        """
        from ._numpy_utils import numpy_to_temporary_csv

        # We start by checking the provided parameters are of the correct dimension:
        if not len(array.shape) == 2:
            raise AssertionError("Provided array must be 2 dimensional")
        if not len(columns) == array.shape[1]:
            raise AssertionError(
                "Length of columns must be the same as the length of the provided rows"
            )
        sep = kwargs.get("sep", "|")
        path = numpy_to_temporary_csv(array, columns, sep, prefix=store_name)
        return self.read_csv(
            path,
            store_name=store_name,
            sep="|",
            keys=keys,
            in_all_scenarios=in_all_scenarios,
            partitioning=partitioning,
        )

    def create_cube(
        self,
        base_store: Store,
        name: Optional[str] = None,
        *,
        mode: _CubeCreationMode = "auto",
    ) -> Cube:
        """Create a cube using based on the passed store.

        Args:
            base_store: The cube's base store.
            name: The name of the created cube.
                Defaults to the name of the base store.
            mode: The cube creation mode:

                * ``auto``: Creates hierarchies for every non-numeric column, and measures for every numeric column.
                * ``manual``: Does not create any hierarchy or measure (except from the count).
                * ``no_measures``: Creates the hierarchies like ``auto`` but does not create any measures.
        """
        if name is None:
            name = base_store.name

        check_literal("mode", mode, _CubeCreationMode)

        self._java_api.create_cube_from_store(base_store, name, mode.upper())
        self._java_api.refresh(force_start=True)
        self.cubes[name] = Cube(self._java_api, name, base_store, self)

        return self.cubes[name]

    def create_scenario(self, name: str, *, origin: str = BASE_SCENARIO):
        """Create a new source scenario in the datastore.

        Args:
            name: The name of the scenario.
            origin: The scenario to fork.
        """
        self._java_api.create_scenario(ScenarioName(name), ScenarioName(origin))

    def load_all_data(self):
        """Trigger the :data:`full <atoti.sampling.FULL>` loading of the data.

        Calling this method will change the :mod:`sampling mode <atoti.sampling>` to :data:`atoti.sampling.FULL`
        which triggers the loading of all the data. All subsequent loads, including new stores, will not
        be sampled.

        When building a project, this method should be called as late as possible.
        """
        self._java_api.load_all_data()
        self._java_api.refresh()

    def _open_query_session(self) -> QuerySession:
        token = self._generate_token()
        auth = (
            lambda url: {"Authorization": f"AdminToken {token}"}
            if token is not None
            else None
        )
        return open_query_session(f"http://localhost:{self.port}", auth=auth)

    @doc(_QUERY_MDX_DOC)
    def query_mdx(self, mdx: str, *, timeout: int = 30) -> pd.DataFrame:
        return self._open_query_session().query_mdx(
            mdx,
            timeout=timeout,
            get_level_data_types=lambda cube_name, level_coords: self.cubes[  # pylint: disable=protected-access
                cube_name
            ]._get_level_data_types(
                level_coords
            ),
        )

    @doc(args=_QUERY_MDX_ARGS)
    def explain_mdx_query(self, mdx: str, *, timeout: int = 30) -> QueryAnalysis:
        """Explain an MDX query.

        {args}
        """
        return self._java_api.analyse_mdx(mdx, timeout)

    def _refresh(self):
        """Refresh the session."""
        self._java_api.refresh(False)

    def _generate_token(self) -> Optional[str]:
        """Return a token that can be used to authenticate against the server."""
        return self._java_api.generate_admin_token()

    @property
    def port(self) -> int:
        """Port on which the session is exposed.

        Can be set in the session's :class:`configuration <atoti.config.SessionConfiguration>`.
        """
        return self._java_api.get_session_port()

    @property
    def url(self) -> str:
        """Public URL of the session.

        Can be set in the session's :class:`configuration <atoti.config.SessionConfiguration>`.
        """
        return self._java_api.get_session_url()

    @property
    def excel_url(self) -> str:
        """URL of the Excel endpoint.

        To connect to the session in Excel, create a new connection to an Analysis Services.
        Use this URL for the `server` field and choose to connect with "User Name
        and Password":

        * Without authentication, leave these fields blank.
        * With Basic authentication, fill them with your username and password.
        * Other authentication types (such as Auth0) are not supported by Excel.
        """
        return f"{self.url}/xmla"

    def delete_scenario(self, scenario: str) -> None:
        """Delete the source scenario with the provided name if it exists."""
        _scenario = ScenarioName(scenario)
        if _scenario == BASE_SCENARIO:
            raise ValueError("Cannot delete the base scenario")
        self._java_api.delete_scenario(_scenario)

    @property
    def scenarios(self) -> Collection[str]:  # noqa: D401
        """Collection of source scenarios of the session."""
        return self._java_api.get_scenarios()

    def _repr_html(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_session(self)
