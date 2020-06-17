"""Java API."""

from __future__ import annotations

from dataclasses import dataclass
from types import FunctionType
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import numpy as np
import pandas as pd

from ._measures.utils import convert_level_in_description
from ._path_utils import PathLike, to_absolute_path
from ._py4j_utils import (
    to_java_map,
    to_java_object_array,
    to_java_object_array_array,
    to_java_string_array,
    to_python_dict,
    to_python_list,
)
from ._query_plan import QueryAnalysis, QueryPlan, RetrievalData
from ._type_utils import Port, ScenarioName
from .comparator import Comparator
from .config import Auth, BasicAuthentication, OidcAuthentication, Role
from .exceptions import _java_api_call_wrapper
from .hierarchies import DEFAULT_DIMENSION_NAME
from .sampling import SamplingMode
from .types import AtotiType
from .vendor.atotipy4j.clientserver import (
    ClientServer,
    JavaParameters,
    PythonParameters,
)
from .vendor.atotipy4j.java_collections import JavaArray, JavaMap, ListConverter

if TYPE_CHECKING:
    from .cube import BucketRows, Cube
    from .hierarchy import Hierarchy
    from .level import Level
    from .simulation import Simulation
    from .store import Row, Store
    from .measure import Measure
    from ._measures.named_measure import NamedMeasure
    from .config._role import Restrictions

DataFrameDescription = Tuple[List[str], Sequence[Sequence[Any]]]


class ApiMetaClass(type):
    """Meta class for the API calls."""

    def __new__(
        cls, classname: str, bases: Tuple[type, ...], class_dict: Dict[str, Any]
    ):
        """Automatically wrap all of the classes methods.

        This class applies the api_call_wrapper to all of a particular classes methods.
        This allows for cleaner handling of Py4J related exceptions
        """
        new_class_dict = {}
        for attribute_name, attribute in class_dict.items():
            if isinstance(attribute, FunctionType):
                attribute = _java_api_call_wrapper(attribute)
            new_class_dict[attribute_name] = attribute
        return type.__new__(cls, classname, bases, new_class_dict)


# pylint: disable=too-many-lines
class JavaApi(metaclass=ApiMetaClass):
    """API for communicating with the JVM."""

    def __init__(
        self, py4j_java_port: Optional[Port] = None, aws_region: Optional[str] = None
    ):
        """Create the Java gateway.

        Args:
            py4j_java_port: The port the Py4J server is running on
            aws_region: (Optional) The AWS region

        """
        self.gateway = JavaApi._create_py4j_gateway(py4j_java_port)
        self.java_session: Any = self.gateway.entry_point
        self.java_api = self.java_session.api()

        # Initialize the session.
        if aws_region:
            self.set_aws_region(aws_region)

    @staticmethod
    def _create_py4j_gateway(java_port: Optional[Port] = None) -> ClientServer:
        # Connnect to the Java side using the provided Java port
        # and start the Python callback server with a dynamic port.
        gateway = ClientServer(
            java_parameters=JavaParameters(port=java_port),
            python_parameters=PythonParameters(daemonize=True, port=0),
        )

        # Retrieve the port on which the python callback server was bound to.
        cb_server = gateway.get_callback_server()
        if cb_server is None:
            raise ValueError("Null callback server from py4j gateway")
        python_port = cb_server.get_listening_port()

        # Tell the Java side to connect to the Python callback server with the new Python port.
        gateway_server = gateway.java_gateway_server
        if gateway_server is None:
            raise ValueError("Null gateway server from py4j gateway")
        # ignore type next line because we do some Java calls
        gateway_server.resetCallbackClient(
            gateway_server.getCallbackClient().getAddress(), python_port  # type: ignore
        )

        return gateway

    def shutdown(self):
        """Shutdown the connection to the Java gateway."""
        self.gateway.shutdown()

    def refresh(self, force_start: bool = False):
        """Refresh the Java session.

        Args:
            force_start: start the dataStore without stopping it
                Defaults to False

        """
        self.java_session.refresh(force_start)

    def refresh_pivot(self):
        """Refresh the pivot."""
        self.java_api.refreshPivot()

    def clear_session(self):
        """Refresh the pivot."""
        self.java_api.clearSession()

    def get_session_port(self) -> int:
        """Return the port of the session."""
        return self.java_session.getPort()

    def get_session_url(self) -> str:
        """Return the URL of the session."""
        return self.java_session.getPublicUrl()

    def get_throwable_root_cause(self, throwable: Any) -> str:
        """Get the root cause of a java exception."""
        return self.java_api.getRootCause(throwable)

    def generate_admin_token(self) -> Optional[str]:
        """Return the admin token required to connect to this session."""
        return self.java_session.generateAdminToken()

    def set_metadata_db(self, metadata_db: str):
        """Set the session's metadata database description."""
        self.java_api.setMetadataDb(metadata_db)

    def _convert_restriction(self, restrictions: Restrictions) -> JavaMap:
        """Convert a restriction to a Java map."""
        restr = dict()
        for (field, restriction) in restrictions.items():
            members = restriction if isinstance(restriction, list) else [restriction]
            restr[field] = ListConverter().convert(
                members, self.gateway._gateway_client
            )
        return to_java_map(self.gateway, restr)

    def configure_roles(self, roles: Collection[Role]):
        """Configure the roles of the session."""
        restrictions = {
            role.name: self._convert_restriction(role.restrictions) for role in roles
        }
        java_restrictions = to_java_map(self.gateway, restrictions)
        self.java_api.addRoles(java_restrictions)

    def _convert_role_mapping(
        self, mapping: Optional[Mapping[str, Collection[str]]]
    ) -> JavaMap:
        """Convert a role mapping to java object."""
        if mapping is None:
            return to_java_map(self.gateway, dict())
        role_mapping = {
            name: ListConverter().convert(role, self.gateway._gateway_client)
            for (name, role) in mapping.items()
        }
        return to_java_map(self.gateway, role_mapping)

    def configure_authentication(self, auth: Auth, session_name: str, session_id: str):
        """Configure the roles of the session."""
        if isinstance(auth, BasicAuthentication):
            realm = (
                auth.realm
                if auth.realm is not None
                # Keep in sync with docstring in _auth_basic.py
                else f"{session_name} atoti session {session_id}"
            )
            passwords = {user.name: user.password for user in auth.users}
            jpasswords = to_java_map(self.gateway, passwords)
            role_mapping = {user.name: user.roles for user in auth.users}
            jrole_mapping = self._convert_role_mapping(role_mapping)
            self.java_api.addBasicSecurityProvider(jpasswords, jrole_mapping, realm)
        elif isinstance(auth, OidcAuthentication):
            check_oidc_config(auth)
            self.java_api.addOidcSecurityProvider(
                auth.provider_id,
                auth.issuer_url,
                auth.client_id,
                auth.client_secret,
                to_java_string_array(
                    self.gateway,
                    auth.paths_to_authorities
                    if auth.paths_to_authorities is not None
                    else [],
                ),
                self._convert_role_mapping(auth.role_mapping),
            )

    def start_application(self):
        """Start the application."""
        self.java_api.startSession()

    def _create_java_types(self, types: Mapping[str, AtotiType]) -> JavaMap:
        """Convert the python types to java types."""
        # pylint: disable=invalid-name
        atoti_package = self.gateway.jvm.com.activeviam.chouket  # type: ignore
        JavaColumnType: Any = atoti_package.loading.impl.TypeImpl  # type: ignore
        # pylint: enable=invalid-name
        converted = {
            field: JavaColumnType(type_value.java_type, type_value.nullable)
            for (field, type_value) in types.items()
        }
        return to_java_map(self.gateway, converted)

    def get_stores(self) -> List[str]:
        """List all the store of the session.

        Returns:
            A list of all the stores.

        """
        return to_python_list(self.java_api.getStores())

    def _java_sampling_mode(self, mode: SamplingMode) -> Any:
        """Convert the sampling mode to a Java sampling mode."""
        params = ListConverter().convert(mode.parameters, self.gateway._gateway_client)
        atoti_package: Any = self.gateway.jvm.com.activeviam.chouket  # type: ignore
        sampling_class: Any = atoti_package.loading.sampling.StoreSamplingPolicy  # type: ignore
        return sampling_class.get(mode.name, params)

    def create_store_params(
        self,
        keys: Optional[Sequence[str]],
        partitioning: Optional[str],
        types: Optional[Mapping[str, AtotiType]],
        sampling: SamplingMode,
    ) -> Any:
        """Create the store parameters."""
        java_keys = (
            ListConverter().convert(keys, self.gateway._gateway_client)
            if keys
            else None
        )
        if types is None:
            types = dict()
        java_types = self._create_java_types(types)
        java_sampling = self._java_sampling_mode(sampling)
        package: Any = self.gateway.jvm.com.activeviam.chouket.loading.impl  # type: ignore
        params = package.StoreParams(java_keys, partitioning, java_types, java_sampling)
        return params

    def create_loading_params(
        self,
        scenario_name: Optional[ScenarioName],
        in_all_scenarios: bool,
        watch: bool,
        truncate: bool,
    ) -> Any:
        """Create the loading parameters."""
        package: Any = self.gateway.jvm.com.activeviam.chouket.loading.impl  # type: ignore
        params = package.LoadingParams(None, in_all_scenarios, watch, truncate)
        if scenario_name is not None:
            params.setBranch(scenario_name)
        return params

    def create_csv_params(
        self,
        path: PathLike,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        array_sep: Optional[str],
        pattern: Optional[str],
    ) -> Any:
        """Create the CSV parameters."""
        package: Any = self.gateway.jvm.com.activeviam.chouket.loading.csv.impl  # type: ignore
        params = package.CsvLoaderParams(
            to_absolute_path(path), sep, encoding, process_quotes, array_sep, pattern
        )
        return params

    def create_store(
        self,
        schema: Mapping[str, AtotiType],
        store_name: str,
        keys: Optional[Sequence[str]],
        partitioning: Optional[str],
        sampling_mode: SamplingMode,
    ):
        """Create a java store from its schema.

        Args:
            schema: The schema to use to define the store's columns and their types
            store_name: The name to give to the store
            keys (optional): The key columns for the store
            partitioning (optional): The partitioning description
            sampling_mode (optional): The sampling mode
        """
        store_params = self.create_store_params(
            keys, partitioning, schema, sampling_mode
        )
        self.java_api.createStore(store_name, store_params)

    def create_store_from_csv(
        self,
        path: PathLike,
        store_name: str,
        keys: Optional[Sequence[str]],
        in_all_scenarios: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        partitioning: Optional[str],
        types: Optional[Mapping[str, AtotiType]],
        watch: bool,
        array_sep: Optional[str],
        pattern: Optional[str],
        sampling: SamplingMode,
    ):
        """Create a Java store from a CSV file or directory.

        Args:
            path: The path of the file or directory.
            store_name: The name to give to the store.
            keys (optional): The key columns for the store.
            in_all_scenarios: Whether to load the CSV in all existing scenarios. True by default.
            sep: Delimiter to use. If sep is None, the separator will automatically be detected.
            encoding: Encoding to use for UTF when reading.
            process_quotes: Whether double quotes should be processed to follow the official CSV
                specification:

                - Each field may or may not be enclosed in double quotes
                  (however some programs, such as Microsoft Excel, do not use double quotes at all).
                  If fields are not enclosed with double quotes, then double quotes may not appear
                  inside the fields
                - A double-quote appearing inside a field must be escaped by preceding it with
                  another double quote
                - Fields containing line breaks (CRLF), double quotes, and commas should be enclosed
                  in double-quotes

                When setting this parameter to false, all double-quotes within a field will be
                treated as any regular character, to follow Excel behavior.
                CAREFUL: in this mode, it is expected that fields are NOT enclosed in double quotes.
                It is also not possible to have a line break inside a field.
            partitioning: The partitioning description.
            types: Type for some of the columns.
            watch: Whether or not the source file or directory should be watched for changes. If
                this option is set to true, whenever you change the source, the changes will be
                reflected in the store.
            array_sep: Delimiter to use for arrays. Setting it to a non-None value will parse all
                the columns containing this separator as arrays.
            pattern: glob pattern used to specify which files to load if the provided path is a
                directory. If none is passed we match all csv files by default.
            sampling: The sampling mode.

        """
        store_params = self.create_store_params(keys, partitioning, types, sampling)
        load_params = self.create_loading_params(None, in_all_scenarios, watch, False)
        csv_params = self.create_csv_params(
            path, sep, encoding, process_quotes, array_sep, pattern
        )
        self.java_api.createStoreFromCsv(
            store_name, store_params, load_params, csv_params
        )

    def create_parquet_params(self, path: PathLike) -> Any:
        """Create the parquet params."""
        package: Any = self.gateway.jvm.com.activeviam.chouket.loading.parquet.impl  # type: ignore
        params = package.ParquetLoaderParams(to_absolute_path(path))
        return params

    def create_store_from_parquet(
        self,
        path: PathLike,
        store_name: str,
        keys: Optional[Sequence[str]],
        in_all_scenarios: bool,
        partitioning: Optional[str],
        sampling: SamplingMode,
        watch: bool,
    ):
        """Create a java store from a parquet file.

        Args:
            path: The path of the file or directory.
            store_name: The name to give to the store
            keys (optional): The key columns for the store
            in_all_scenarios: Whether to load the parquet in all existing scenarios.
                True by default.
            partitioning: The partitioning description.
            sampling: The sampling mode
            watch: Watch the provided path for changes and dynamically load them into the datastore.
                This should not be set to True if the provided path is not a directory.

        """
        store_params = self.create_store_params(keys, partitioning, None, sampling)
        load_params = self.create_loading_params(None, in_all_scenarios, watch, False)
        parquet_params = self.create_parquet_params(path)
        self.java_api.createStoreFromParquet(
            store_name, store_params, load_params, parquet_params
        )

    def load_csv_into_store(
        self,
        path: PathLike,
        store: Union[Store, Simulation],
        scenario_name: ScenarioName,
        in_all_scenarios: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: bool,
        truncate: bool,
        watch: bool,
        array_sep: Optional[str],
        pattern: Optional[str],
    ):
        """Load a csv into an existing store.

        Args:
            path: The path of the file or directory.
            store: The store to load the CSV into
            scenario_name: The name of the scenario to load the data into
            in_all_scenarios: load the data into all of the store's scenarios
            sep: Delimiter to use. If sep is None, the separator will automatically be detected.
            encoding: Encoding to use for UTF when reading.
            process_quotes: Whether double quotes should be processed to follow the official
              CSV specification.
            truncate: Whether the store should be emptied before loading the content of the CSV
            watch: Whether or not the source file or directory should be watched for changes. If
                this option is set to true, whenever you change the source, the changes will be
                reflected in the store.
            array_sep: Delimiter to use for arrays. Setting it to a non-None value will parse all
                the columns containing this separator as arrays.
            pattern: Glob pattern used to specify which files to load if the provided path is a
                directory. If no pattern is provided, we match all csv files by default.

        """
        load_params = self.create_loading_params(
            scenario_name, in_all_scenarios, watch, truncate
        )
        csv_params = self.create_csv_params(
            path, sep, encoding, process_quotes, array_sep, pattern
        )
        self.java_api.loadCsvIntoStore(store.name, load_params, csv_params)

    def load_parquet_into_store(
        self,
        path: PathLike,
        store: Store,
        scenario_name: ScenarioName,
        in_all_scenarios: bool = False,
        truncate: bool = False,
        watch: bool = False,
    ):
        """Load a Parquet into an existing store.

        Args:
            path: The path of the file or directory.
            store: The store to load the parquet into
            scenario_name: The name of the scenario to load the data into
            in_all_scenarios: load the data into all of the store's scenarios
            truncate: Whether the store should be emptied before loading the new content.
            watch: Watch the provided path for changes and dynamically load them into the datastore.
                This should not be set to True if the provided path is not a directory.

        """
        load_params = self.create_loading_params(
            scenario_name, in_all_scenarios, watch, truncate
        )
        parquet_params = self.create_parquet_params(path)
        self.java_api.loadParquetIntoStore(store.name, load_params, parquet_params)

    def create_scenario_csv_params(
        self,
        path: PathLike,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        array_sep: Optional[str],
        pattern: Optional[str],
        base_scenario_directory: str,
    ) -> Any:
        """Create the multi scenarios CSV parameters."""
        package: Any = self.gateway.jvm.com.activeviam.chouket.loading.csv.impl  # type: ignore
        params = package.MultiScenarioCsvLoaderParams(
            to_absolute_path(path),
            sep,
            encoding,
            process_quotes,
            array_sep,
            pattern,
            base_scenario_directory,
        )
        return params

    def load_scenarios_from_csv(
        self,
        scenario_directory_path: PathLike,
        store_name: str,
        base_scenario_directory: str,
        truncate: bool,
        watch: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        array_sep: Optional[str],
        pattern: Optional[str],
    ):
        """Load a directory of CSV files into a store while automatically generating scenarios.

        Args:
            scenario_directory_path: The path to the folder containing all the scenarios.
            store_name: The name of the store
            base_scenario_directory: The name of a folder whose data we will load into the base
                scenario instead of a new scenario with the original name of the folder
            truncate: Whether or not the content of the store should be truncated on each branch
            watch: Whether or not we should watch the source directory for changes, or simply
                or simply perform the initial load
            sep: Seperator to use, if None is set it will automatically be detected
            encoding: Encoding to use for UTF when reading, defaults to 'utf-8'
            process_quotes: Whether double quotes should be processed to follow the official CSV
                specification
            array_sep: Delimiter to use for arrays
            pattern: glob pattern used to specify which files to load if the provided path is a
                directory.

        """
        load_params = self.create_loading_params(None, False, watch, truncate)
        csv_params = self.create_scenario_csv_params(
            scenario_directory_path,
            sep,
            encoding,
            process_quotes,
            array_sep,
            pattern,
            base_scenario_directory,
        )
        self.java_api.loadScenariosFromCsv(store_name, load_params, csv_params)

    def create_scenario(
        self, scenario_name: ScenarioName, parent_scenario: ScenarioName
    ):
        """Create a new scenario on the store.

        Args:
            scenario_name: The name of the scenario to create
            parent_scenario: The name of the parent scenario

        """
        self.java_api.createBranch(scenario_name, parent_scenario)

    def get_scenarios(self) -> List[str]:
        """Get the list of scenarios defined in the current session."""
        return to_python_list(self.java_api.getBranches())

    def delete_scenario(self, scenario: ScenarioName):
        """Delete a scenario from the store.

        Args:
            scenario: The name of the scenario to delete

        """
        self.java_api.deleteBranch(scenario)

    @dataclass(frozen=True)
    class AggregatesCacheDescription:
        """Aggregates cache description."""

        capacity: int

    def get_aggregates_cache_description(self, cube: Cube) -> Any:
        """Return the description of the aggregates cache associated with a given cube.

        Args:
            cube: The target cube
        Returns:
            The aggregates cache description.

        """
        jcache_desc = self.java_api.getAggregatesCacheDescription(cube.name)
        return JavaApi.AggregatesCacheDescription(capacity=jcache_desc.getSize())

    def set_aggregates_cache(self, cube: Cube, capacity: int):
        """Set the aggregates cache description for a given cube.

        Args:
            cube: The target cube.
            capacity: The cache's capacity.

        """
        self.java_api.setAggregatesCache(cube.name, capacity)

    @dataclass(frozen=True)
    class ColumnDescription:
        """Store column description."""

        name: str
        column_type_name: str
        is_nullable: bool

    # https://github.com/Microsoft/pyright/issues/104 -> Unbound variables not detected
    def get_store_schema(self, store: Store) -> List[JavaApi.ColumnDescription]:  # type: ignore
        """Return the schema of the java store.

        Args:
            store: The store whose schema we want
        Returns:
            the Python schema of the store

        """
        schema = self.java_api.getStoreSchema(store.name)
        columns_descr = []
        for i in range(0, len(list(schema.fieldNames()))):
            columns_descr.append(
                JavaApi.ColumnDescription(
                    schema.fieldNames()[i],
                    schema.types()[i].literalType().getParser(),
                    schema.types()[i].nullable(),
                )
            )
        return columns_descr

    def set_source_simulation_enabled(self, store: Store, enabled: bool) -> None:
        """Set the sourceSimulationEnabled property of a store.

        If set to true, this enables source simulation modifications on this store
        from the application.

        Args:
            store: the store to set the property on.
            enabled: the value to give to the property.

        """
        self.java_api.setSourceSimulationEnabledOnStore(store.name, enabled)

    def get_source_simulation_enabled(self, store: Store) -> bool:
        """Get the value of the sourceSimulationEnabled property of a store.

        If the value is true, source simulation modifications can be performed on this store
        from the application.

        Args:
            store: The store whose property we want
        Returns:
            The value of the parameter on the requested store.

        """
        return self.java_api.getSourceSimulationEnabledOnStore(store.name)

    def get_key_columns(self, store: Store) -> Sequence[str]:
        """Return the list of key columns for the store.

        Args:
            store: The store whose key columns we want.
        """
        java_columns = self.java_api.getKeyFields(store.name)
        return to_python_list(java_columns)

    def create_cube_from_store(
        self,
        store: Store,
        cube_name: str,
        mode: str,
        default_dimension_name: str = DEFAULT_DIMENSION_NAME,
    ):
        """Create a java cube for a given store.

        Args:
            store: The base store for the cube
            cube_name: The name of the cube to create
            mode: The cube creation configuration
            default_dimension_name: The default dimension of the hierarchies

        """
        self.java_api.createCubeFromStore(
            store.name, cube_name, default_dimension_name, mode
        )

    def generate_cube_schema_image(self, cube_name: str) -> str:
        """Get the cube schema.

        Args:
            cube_name: The name of the cube to graph
        Returns:
            The path to the schema image.

        """
        return self.java_api.getCubeSchemaPath(cube_name)

    def generate_datastore_schema_image(self) -> str:
        """Get the datastore schema.

        Returns:
            The path to the schema image.

        """
        return self.java_api.getDatastoreSchemaPath()

    def delete_cube(self, cube: Cube) -> None:
        """Delete a cube from the current session.

        Args:
            cube: The cube we want to delete.

        """
        self.java_api.deleteCube(cube.name)

    def create_join(
        self, store: Store, other_store: Store, mappings: Optional[Mapping[str, str]],
    ):
        """Define a join between two stores.

        Args:
            store: The base store for the join.
            other_store: The second store for the join.
            mappings: The mapping to use.
        """
        # Convert mappings.
        jmappings = to_java_map(self.gateway, mappings) if mappings else mappings

        self.java_api.createReferences(store.name, other_store.name, jmappings)

    def get_store_size(self, store: Store) -> int:
        """Get the size of the store on the scenario of the store.

        Args:
            store: the store to get the size of
        Returns:
            The size of the store.

        """
        return self.java_api.getStoreSize(store.name, store.scenario)

    def insert_multiple_on_store_scenario(
        self,
        store: Union[Store, Simulation],
        scenario_name: ScenarioName,
        rows: Sequence[Row],
    ) -> None:
        """Insert multiple rows on a store scenario.

        Args:
            store: The store in which we want to insert the data
            scenario_name: The name of the scenario (i.e. branch) to use
            rows: The rows to add to the store

        """
        # Check the type of the row
        if isinstance(rows[0], dict):
            # We assume the all the other elements are dicts
            jrows = []
            for row in rows:
                row = cast(dict, row)
                jrows.append(to_java_map(self.gateway, row))
            jmap_rows = ListConverter().convert(jrows, self.gateway._gateway_client)
            self.java_api.insertMultipleOnStoreBranch(
                store.name, scenario_name, jmap_rows
            )
        elif isinstance(rows[0], tuple):
            obj_obj_arr = to_java_object_array_array(self.gateway, rows)
            self.java_api.insertMultipleOnStoreBranch(
                store.name, scenario_name, obj_obj_arr
            )

    def get_store_dataframe(
        self,
        store: Union[Store, Simulation],
        rows: int,
        scenario_name: Optional[ScenarioName] = None,
        keys: Optional[Sequence[str]] = None,
    ) -> pd.DataFrame:
        """Return the pandas DataFrame for a given store.

        Args:
            store: The store whose view we want
            scenario_name: The name of the scenario to use
            rows: The number of rows to return
            keys: Key fields to use as index
        Returns:
            the DataFrame corresponding to the store with its index if it has one

        """
        dfrh = self.java_api.dataFrameRowsAndHeaders(store.name, scenario_name, rows)

        headers = to_python_list(dfrh.getHeader())
        content = to_python_list(dfrh.getRows())
        dataframe = pd.DataFrame(
            data=np.array(content) if len(content) > 0 else [], columns=headers
        ).apply(pd.to_numeric, errors="ignore")

        if keys:
            dataframe.set_index(keys, inplace=True)

        return dataframe

    @staticmethod
    def _convert_from_java_levels(jlevels: Any) -> Dict[str, Level]:
        """Convert from java levels."""
        from .level import Level  # pylint: disable=redefined-outer-name

        jlevels_dict = to_python_dict(jlevels)
        levels = {}
        for (name, jlvl) in jlevels_dict.items():
            comparator_name = jlvl.getComparatorName()
            first_members = (
                list(jlvl.getFirstMembers())
                if jlvl.getFirstMembers() is not None
                else None
            )
            if comparator_name is None:
                comparator = None
            else:
                comparator = Comparator(comparator_name, first_members)
            levels[name] = Level(
                name,
                jlvl.getPropertyName(),
                jlvl.getType().replace("(nullable)", ""),
                _comparator=comparator,
            )
        return levels

    def create_or_update_hierarchy(
        self,
        cube: Cube,
        dimension: str,
        hierarchy_name: str,
        levels: Mapping[str, Level],
    ):
        """Create a hierarchy on a cube, or update the level of an existing hierarchy.

        Args:
            cube: The cube to create the hierarchy on
            dimension: The dimension of the cube to create the hierarchy on
            hierarchy_name: The name for the new hierarchy
            levels: map between the level and column names
        """
        level_names = list(levels.keys())
        column_names = [
            level._column_name  # pylint: disable=protected-access
            for level in levels.values()
        ]
        self.java_api.createHierarchyForCube(
            cube.name,
            dimension,
            hierarchy_name,
            ListConverter().convert(level_names, self.gateway._gateway_client),
            ListConverter().convert(column_names, self.gateway._gateway_client),
        )

    def update_hierarchy_coordinate(
        self, cube: Cube, hierarchy: Hierarchy, new_dim: str, new_hier: str
    ):
        """Change the coordinate of a hierarchy.

        Args:
            cube: The cube
            hierarchy: The hierarchy to update
            new_dim: The new dimension name
            new_hier: The new hierarchy name.
        """
        # pylint: disable=protected-access
        self.java_api.updateHierarchyCoordinate(
            cube.name, hierarchy._java_description, f"{new_hier}@{new_dim}"
        )

    def update_hierarchy_slicing(self, hierarchy: Hierarchy, slicing: bool):
        """Update whether the hierarchy is slicing or not.

        Args:
            hierarchy: The hierarchy to update
            slicing: Whether the hierarchy is slicing or not.
        """
        # pylint: disable=protected-access
        self.java_api.setHierarchySlicing(
            hierarchy._cube.name, hierarchy._java_description, slicing
        )

    def update_level_comparator(self, level: Level):
        """Change the level comparator.

        Args:
            level: The level to update.
        """
        # pylint: disable=protected-access
        comparator_name = (
            level.comparator._name if level.comparator is not None else None
        )
        first_members = None
        if level.comparator is not None and level.comparator._first_members is not None:
            first_members = to_java_object_array(
                self.gateway, level.comparator._first_members
            )

        if level._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {level.name}.")

        self.java_api.updateLevelComparator(
            level._hierarchy._cube.name,
            level._java_description,
            comparator_name,
            first_members,
        )
        # pylint: enable=protected-access

    def drop_level(self, level: Level):
        """Delete a level.

        Args:
            level: the level to delete

        """
        # pylint: disable=protected-access
        hier = level._hierarchy
        if hier is None:
            raise ValueError("No hierarchy for level " + level.name)
        self.java_api.deleteLevel(hier._cube.name, level._java_description)

    def drop_hierarchy(self, cube: Cube, hierarchy: Hierarchy):
        """Drop a hierarchy from the cube.

        Args:
            cube: The cube to drop the hierachy from
            dimension: The dimension to drop the hierachy from
            hierarchy: The hierarchy to drop

        """
        # pylint: disable=protected-access
        self.java_api.dropHierarchy(cube.name, hierarchy._java_description)

    def retrieve_hierarchies(self, cube: Cube) -> Mapping[Tuple[str, str], Hierarchy]:
        """Retrieve a cube's hierarchies."""
        from .hierarchy import Hierarchy  # pylint: disable=redefined-outer-name
        from .level import Level

        hierarchies: Dict[Tuple[str, str], Hierarchy] = {}
        java_hierarchies = self.java_api.retrieveHierarchies(cube.name)
        python_hierarchies = to_python_dict(java_hierarchies)
        for hierarchy in python_hierarchies.values():
            name = hierarchy.getName()
            dim_name = hierarchy.getDimensionName()
            levels: Dict[str, Level] = JavaApi._convert_from_java_levels(
                hierarchy.getLevels()
            )
            slicing = hierarchy.getSlicing()
            hierarchy = Hierarchy(name, levels, dim_name, slicing, cube, self)
            hierarchies[(dim_name, name)] = hierarchy
            for level in hierarchy.levels.values():
                level._hierarchy = hierarchy  # pylint: disable=protected-access

        return hierarchies

    def retrieve_hierarchy(
        self, cube: Cube, dimension: Optional[str], name: str
    ) -> List[Hierarchy]:
        """Retrieve a cube's hierarchy."""
        from .hierarchy import Hierarchy  # pylint: disable=redefined-outer-name

        # Get the hierarchy from the java side.
        java_hierarchies = to_python_list(
            self.java_api.retrieveHierarchy(cube.name, dimension, name)
        )

        # Convert it to a Python hierarchy.
        hierarchies = []
        for java_hierarchy in java_hierarchies:
            hierarchy = Hierarchy(
                name,
                JavaApi._convert_from_java_levels(java_hierarchy.getLevels()),
                java_hierarchy.getDimensionName(),
                java_hierarchy.getSlicing(),
                cube,
                self,
            )
            for level in hierarchy.levels.values():
                level._hierarchy = hierarchy  # pylint: disable=protected-access
            hierarchies.append(hierarchy)
        return hierarchies

    def set_measure_folder(
        self, cube_name: str, measure: Measure, folder: Optional[str]
    ):
        """Set the folder of a measure.

        Args:
            cube_name: The name of the cube
            measure: The measure to update
            folder: The folder to set. Use None to remove the folder.

        """
        self.java_api.setMeasureFolder(cube_name, measure.name, folder)

    def set_measure_formatter(
        self, cube_name: str, measure: Measure, formatter: Optional[str]
    ):
        """Set the formatter of a measure.

        Args:
            cube_name: The name of the cube
            measure: The measure to update
            formatter: The formatter to set.

        """
        self.java_api.setMeasureFormatter(cube_name, measure.name, formatter)

    def set_visible(self, cube_name: str, measure: Measure, visible: Optional[bool]):
        """Set the visibility of a measure.

        Args:
            cube_name: The name of the cube
            measure: The measure to update
            visible: The visibility to set.

        """
        self.java_api.setMeasureVisibility(cube_name, measure.name, visible)

    @dataclass(frozen=True)
    class MeasureDescription:
        """Description of a measure to build."""

        folder: str
        formatter: str
        visible: bool

    # https://github.com/Microsoft/pyright/issues/104
    def get_full_measures(
        self, cube: Cube
    ) -> Dict[str, JavaApi.MeasureDescription]:  # type: ignore
        """Retrieve the list of the cube's measures, including their required levels.

        Args:
            cube: The cube whose full measures we want
        Returns:
            A map from measure names to measure descriptions

        """
        java_measures = self.java_api.getFullMeasures(cube.name)
        measures = to_python_list(java_measures)
        final_measures: Dict[str, JavaApi.MeasureDescription] = {}
        for measure in measures:
            final_measures[measure.getName()] = JavaApi.MeasureDescription(
                measure.getFolder(), measure.getFormatter(), measure.isVisible(),
            )
        return final_measures

    # https://github.com/Microsoft/pyright/issues/104
    def get_measure(
        self, cube: Cube, measure_name: str
    ) -> JavaApi.MeasureDescription:  # type: ignore
        """Retrieve all the details about a measure defined in the cube.

        Args:
            cube: The cube to which the measure belongs to.
            measure_name: The name of the measure in the cube.
        """
        measure = self.java_api.getMeasure(cube.name, measure_name)
        return JavaApi.MeasureDescription(
            measure.getFolder(), measure.getFormatter(), measure.isVisible(),
        )

    def get_required_levels(self, measure: NamedMeasure) -> List[str]:
        """Get the required levels of a measure."""
        # pylint: disable=protected-access
        return to_python_list(
            self.java_api.getRequiredLevels(measure._cube.name, measure.name)
        )
        # pylint: enable=protected-access

    @staticmethod
    def create_retrieval(jretr: Any) -> RetrievalData:
        """Convert Java retrieval to Python."""
        loc_str = ", ".join(
            [
                str(loc.getDimension())
                + "@"
                + str(loc.getHierarchy())
                + "@"
                + "\\".join(to_python_list(loc.getLevel()))
                + ": "
                + "\\".join(str(x) for x in to_python_list(loc.getPath()))
                for loc in to_python_list(jretr.getLocation())
            ]
        )
        timings = to_python_dict(jretr.getTimingInfo())
        return RetrievalData(
            id=jretr.getRetrId(),
            retrieval_type=jretr.getType(),
            location=loc_str,
            measures=to_python_list(jretr.getMeasures()),
            start_times=list(timings.get("startTime", [])),
            elapsed_times=list(timings.get("elapsedTime", [])),
            retrieval_filter=str(jretr.getFilterId()),
            partitioning=jretr.getPartitioning(),
            measures_provider=jretr.getMeasureProvider(),
        )

    @staticmethod
    def create_query_plan(jplan: Any) -> QueryPlan:
        """Create a query plan."""
        jinfos = jplan.getPlanInfo()
        infos = {
            "ActivePivot": {
                "Type": jinfos.getPivotType(),
                "Id": jinfos.getPivotId(),
                "Branch": jinfos.getBranch(),
                "Epoch": jinfos.getEpoch(),
            },
            "Cube filters": to_python_list(jplan.getQueryFilters()),
            "Continuous": jinfos.isContinuous(),
            "Range sharing": jinfos.getRangeSharing(),
            "Missed prefetches": jinfos.getMissedPrefetchBehavior(),
            "Cache": jinfos.getAggregatesCache(),
            "Global timings (ms)": to_python_dict(jinfos.getGlobalTimings()),
        }
        retrievals = [
            JavaApi.create_retrieval(plan)
            for plan in to_python_list(jplan.getRetrievals())
        ]
        dependencies = {
            key: to_python_list(item)
            for key, item in to_python_dict(jplan.getDependencies()).items()
        }
        return QueryPlan(infos, retrievals, dependencies)

    def analyse_mdx(self, mdx: str, timeout: int) -> QueryAnalysis:
        """Analyse an MDX query on a given cube.

        Args:
            mdx: the MDX query
            timeout: the timeout in seconds
        Returns:
            the query info

        """
        jplans = to_python_list(self.java_api.analyseMdx(mdx, timeout))
        plans = [
            JavaApi.create_query_plan(jplan)
            for jplan in jplans
            if jplan.getPlanInfo().getClass().getSimpleName() == "PlanInfoData"
        ]
        return QueryAnalysis(plans)

    def copy_measure(self, cube_name: str, copied_measure: Measure, new_name: str):
        """Copy a measure.

        Args:
            cube_name: the name of the cube containing the measure to copy
            copied_measure: the existing measure to copy
            new_name: the name of the new copy

        """
        self.java_api.copyMeasure(cube_name, copied_measure.name, new_name)

    def aggregated_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        store_name: str,
        column_name: str,
        agg_function: str,
        levels: Collection[Level],
    ) -> str:
        """Create a new aggregated measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            store_name: The name of the store to use
            column_name: The name of the column to use
            agg_function: The aggregation function to use
            levels: The list of the measure's required levels
        Returns:
            The name of the newly created measure

        """
        java_levels = to_java_string_array(
            self.gateway, convert_level_in_description(levels)
        )
        return self.java_api.aggregatedMeasure(
            cube.name, measure_name, store_name, column_name, agg_function, java_levels,
        )

    def boolean_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        operation: str,
        underlyings: List[Any],
    ) -> str:
        """Create a new boolean measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            operation: The name of the operation to use
            underlyings: list of underlyings for the measure
        Returns:
            The name of the newly created measure

        """
        junderlyings = ListConverter().convert(
            underlyings, self.gateway._gateway_client
        )
        return self.java_api.booleanMeasure(
            cube.name, measure_name, operation, junderlyings
        )

    def not_measure(
        self, cube: Cube, measure_name: Optional[str], underlying_name: str
    ) -> str:
        """Create a new inverted boolean measure.

        Args:
            cube: the cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying_name: The name of the underlying measure

        Returns:
            The name of the newly created measure

        """
        return self.java_api.notMeasure(cube.name, measure_name, underlying_name)

    def calculated_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        operation: str,
        underlyings: List[Any],
    ) -> str:
        """Create a new calculated measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            operation: The name of the operation to use
            underlyings: The  list of underlyings for the measure
        Returns:
            The name of the newly created measure

        """
        junderlyings = ListConverter().convert(
            underlyings, self.gateway._gateway_client
        )
        return self.java_api.calculatedMeasure(
            cube.name, measure_name, operation, junderlyings
        )

    def quantile_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        mode: str,
        interpolation: str,
        underlyings: List[str],
    ) -> str:
        """Create a new quantile measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            mode: The calculation mode to use to determin the quantile's index
            interpolation: The interpolation method to use to determin the returned value
            underlyings: The list of underlyings for the measure
        Returns:
            The name of the newly created measure

        """
        junderlyings = ListConverter().convert(
            underlyings, self.gateway._gateway_client
        )
        return self.java_api.quantileMeasure(
            cube.name, measure_name, mode, interpolation, junderlyings
        )

    def where_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying_name: str,
        underlying_else_name: Optional[str],
        measure_conditions: List[str],
    ) -> str:
        """Create a new condition / if-then-else measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying_name: The name of the underlying measure when the conditions are true.
            underlying_else_name: The name of the underlying measure when the conditions are false.
            measure_conditions: The names of the measure conditions to apply
        Returns:
            The name of the newly created measure

        """
        java_conditions = ListConverter().convert(
            measure_conditions, self.gateway._gateway_client
        )
        return self.java_api.whereMeasure(
            cube.name,
            measure_name,
            underlying_name,
            underlying_else_name,
            java_conditions,
        )

    def filtered_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying_name: str,
        measure_filters: List[str],
    ) -> str:
        """Create a new filtered measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying_name: The name of the underlying measure
            measure_filters: The names of the measure filters to apply
        Returns:
            The name of the newly created measure

        """
        java_filters = ListConverter().convert(
            measure_filters, self.gateway._gateway_client
        )
        return self.java_api.filteredMeasure(
            cube.name, measure_name, underlying_name, java_filters
        )

    def level_value_filtered_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying_name: str,
        conditions: List[Dict[str, Any]],
    ) -> str:
        """Create a new filtered measure based on the value of a level.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying_name: The name of the underlying measure
            conditions: list of conditions containing the level on which they apply
        Returns:
            The name of the newly created measure

        """
        temp = [to_java_map(self.gateway, condition) for condition in conditions]
        java_conditions = ListConverter().convert(temp, self.gateway._gateway_client)
        return self.java_api.levelValueFilteredMeasure(
            cube.name, measure_name, underlying_name, java_conditions
        )

    def leaf_aggregated_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying_name: str,
        levels: Collection[Level],
        agg_function: str,
    ) -> str:
        """Create a new leaf aggregated measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying_name: The name of the underlying measure
            levels: list of levels to create the measure on
            agg_function: The aggregation function to use
        Returns:
            The name of the newly created measure

        """
        jlevels = to_java_string_array(
            self.gateway, convert_level_in_description(levels)
        )
        return self.java_api.leafAggregatedMeasure(
            cube.name, measure_name, underlying_name, jlevels, agg_function,
        )

    def leaf_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying_name: str,
        levels: Collection[Level],
    ) -> str:
        """Create a new leaf measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying_name: The name of the underlying measure
            levels: list of levels to create the measure on
        Returns:
            The name of the newly created measure

        """
        jlevels = to_java_string_array(
            self.gateway, convert_level_in_description(levels)
        )
        return self.java_api.leafMeasure(
            cube.name, measure_name, underlying_name, jlevels
        )

    def level_measure(
        self, cube: Cube, measure_name: Optional[str], level: Level
    ) -> str:
        """Create a new level measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name of the measure we are creating
            level: The level to use
        Returns:
            The name of the newly created measure

        """
        return self.java_api.levelMeasure(
            cube.name, measure_name, list(convert_level_in_description((level,)))[0]
        )

    def constant_measure(
        self, cube: Cube, measure_name: Optional[str], value: Any
    ) -> str:
        """Create a new constant measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            value: The value to give to the measure
        Returns:
            The name of the newly created measure

        """
        return self.java_api.literalMeasure(cube.name, measure_name, value)

    def time_period_aggegregated_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        level_description: str,
        back_range: Optional[str],
        forward_range: Optional[str],
        agg_fun: str,
    ) -> str:
        """Create a time period aggregation measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying: The name of the underlying measuret
            level_description: only level of the hierarchy on which to use the time period
            back_range: the period of time before each date to include in the window
            forward_range: The period of time after each date to include in the window
            agg_fun: The aggregation function to use.

        """
        return self.java_api.timePeriodAggregationMeasure(
            cube.name,
            measure_name,
            underlying,
            level_description,
            back_range,
            forward_range,
            agg_fun,
        )

    def window_aggregation_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        level_description: str,
        partitioning: Optional[Level],
        window: Optional[range],
        agg_function: str,
    ) -> str:
        """Create a new scope aggregation measure.

        Args:
            cube: The cube to create the measure on
            measure_name: The name for the measure we are creating
            underlying: The name of the underlying measure
            level_description: level to order by
            partitioning: level to partition by
            window: the range of values to take into account in the running aggregation for a
                given member. It must be a range with: a negative int representing the
                lower bound (inclusive) and a non-negative int representing its upper
                bound (inclusive). The default window represents (-inf, 0).
            agg_function: aggregation function to use
        Returns:
            The name of the newly created measure

        """
        partitioning_descr = (
            partitioning._java_description  # pylint: disable=protected-access
            if partitioning is not None
            else None
        )
        java_range = (
            to_java_object_array(self.gateway, (window.start, window.stop))
            if window
            else None
        )
        return self.java_api.windowAggregationMeasure(
            cube.name,
            measure_name,
            underlying,
            level_description,
            partitioning_descr,
            java_range,
            agg_function,
        )

    def array_element_at(
        self,
        cube_name: str,
        measure_name: Optional[str],
        array_measure: Measure,
        index_measure: Measure,
        levels: Collection[str],
    ) -> str:
        """Create a measure equal to the element at the given index of an array measure.

        Args:
            cube_name: The name of the cube
            measure_name: The name of the measure we are creating.
            array_measure: The underlying array measure.
            index_measure: The index specifying the index to take.
            levels: list of levels to create the measure on.

        """
        array_name = array_measure.name
        index_name = index_measure.name
        jlevels = to_java_string_array(self.gateway, levels)
        return self.java_api.getVectorElement(
            cube_name, measure_name, array_name, index_name, jlevels
        )

    def delete_measure(self, cube: Cube, measure_name: str) -> bool:
        """Delete a mesure.

        Args:
            cube: The cube to delete the measure from.
            measure_name: The name of the measure to delete.

        Returns:
            ``True`` if the measure has been found and deleted.
        """
        return self.java_api.deleteMeasure(cube.name, measure_name)

    def agg_siblings(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        hierarchy: Hierarchy,
        agg: str,
        exclude_self: bool,
    ) -> str:
        """Create a measure that aggregate the siblings.

        Args:
            cube: The cube to perform the operation on
            measure_name: The name for the measure we are creating
            underlying: The name of the underlying measure
            hierarchy: the hierarchy on which to take siblings
            agg: The aggregation function.
            exclude_self: whether to exclude the current member from the aggregation
        Returns:
            The name of the newly created measure.

        """
        return self.java_api.aggSiblings(
            cube.name,
            measure_name,
            underlying,
            hierarchy._java_description,  # pylint: disable=protected-access
            agg,
            exclude_self,
        )

    def parent_value(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        hierarchy: Hierarchy,
        total_measure: Optional[str],
        total_value: object,
        apply_filters: bool,
        degree: int,
    ) -> str:
        """Create the parent value measure.

        Args:
            cube: The cube to perform the operation on
            measure_name: The name for the measure we are creating
            underlying: The name of the underlying measure
            hierarchy: The hierarchies to drill up.
            total_measure: The name of the measure to take at the top level.
            total_value: The value to take at the top level.
            apply_filters: Apply filters on member of the parent value.
            degree: The relative position of the parent you want the value on.

        Returns:
            The name of the newly created measure.

        """
        return self.java_api.parentValue(
            cube.name,
            measure_name,
            underlying,
            hierarchy._java_description,  # pylint: disable=protected-access
            total_measure,
            total_value,
            apply_filters,
            degree,
        )

    def shift(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        hierarchy: Hierarchy,
        offset: int,
    ) -> str:
        """Create the shifted measure.

        Args:
            cube: The cube to perform the operation on.
            measure_name: The name for the measure we are creating.
            underlying: The name of the underlying measure.
            hierarchy: the hierarchy to shift on.
            offset: The number of element to shift.

        Returns:
            The name of the newly created measure.
        """
        # pylint: disable=protected-access
        return self.java_api.shift(
            cube.name, measure_name, underlying, hierarchy._java_description, offset
        )

    def min_member(
        self, cube: Cube, measure_name: Optional[str], underlying: str, level: Level
    ) -> str:
        """Create the min member measure.

        Args:
            cube: The cube to perform the operation on.
            measure_name: The name of the measure we are creating. Can be None for hidden measures.
            underlying: The name of the underlying measure.
            level: The level on which to perform the min member for the underlying measure.

        Returns:
            The name of the newly created measure.
        """
        return self.java_api.minMember(
            cube.name,
            measure_name,
            underlying,
            level._java_description,  # pylint: disable=protected-access
        )

    def max_member(
        self, cube: Cube, measure_name: Optional[str], underlying: str, level: Level
    ) -> str:
        """Create the max member measure.

        Args:
            cube: The cube to perform the operation on.
            measure_name: The name of the measure we are creating. Can be None for hidden measures.
            underlying: The name of the underlying measure.
            level: The level on which to perform the max member for the undrerlying measure.

        Returns:
            The name of the newly created measure.

        """
        return self.java_api.maxMember(
            cube.name,
            measure_name,
            underlying,
            level._java_description,  # pylint: disable=protected-access
        )

    def date_shift(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        level: Level,
        shift_string: str,
        method: str,
    ) -> str:
        """Create the shifted measure.

        Args:
            cube: The cube to perform the operation on
            measure_name: The name for the measure we are creating
            underlying: The name of the underlying measure
            level: Only level of the hierarchy on which to take to shifted value.
            shift_string: The shift string, made of numbers and date string aliases.
            method: The method to use when shifting (exact, previous/next fallback, interpolate).

        Returns:
            The name of the newly created measure.
        """
        return self.java_api.dateShift(
            cube.name,
            measure_name,
            underlying,
            level._java_description,  # pylint: disable=protected-access
            shift_string,
            method,
        )

    def at_level(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        levels_to_values: Dict[Level, Any],
    ) -> str:
        """Create the measure shifted at the given position.

        Args:
            cube: The cube to perform the operation on.
            measure_name: The name for the measure we are creating.
            underlying: The name of the underlying measure.
            levels_to_values: Mapping from the levels to shift on to the values
                to shift the levels to (either a fixed value or another level).

        Returns:
            The name of the newly created measure.
        """
        from .level import Level

        # Convert the levels_to_values map to the expected 3 aligned lists.
        levels: List[str] = []
        values: List[Any] = []
        target_levels: List[Optional[str]] = []
        for level, value in levels_to_values.items():
            levels.append(level._java_description)  # pylint: disable=protected-access
            if isinstance(value, Level):
                target_levels.append(
                    value._java_description  # pylint: disable=protected-access
                )
                values.append(None)
            else:
                target_levels.append(None)
                values.append(value)

        return self.java_api.levelAtMeasure(
            cube.name,
            measure_name,
            underlying,
            ListConverter().convert(levels, self.gateway._gateway_client),
            ListConverter().convert(values, self.gateway._gateway_client),
            ListConverter().convert(target_levels, self.gateway._gateway_client),
        )

    def rank_measure(
        self,
        cube: Cube,
        measure_name: Optional[str],
        underlying: str,
        hierarchy: Hierarchy,
        ascending: bool,
        apply_filters: bool,
    ):
        """Create a ranking measure.

         This measure ranks the members of a hierarchy based on the values of another measure.

        Args:
            cube: The cube to perform the operation on.
            measure_name: The name for the measure we are creating.
            underlying: The name of the underlying measure.
            hierarchy: The hierarchy containing the members to rank.
            ascending: Whether to sort the members ascending or descending.
            apply_filters: Whether to apply the filters before computing the ranks.

        """
        return self.java_api.rankMeasure(
            cube.name,
            measure_name,
            underlying,
            hierarchy._java_description,  # pylint: disable=protected-access
            ascending,
            apply_filters,
        )

    def do_create_simulation(
        self,
        cube: Cube,
        simulation_name: str,
        columns: Sequence[Level],
        multiply: Collection[Measure],
        replace: Collection[Measure],
        add: Collection[Measure],
        base_scenario_name: ScenarioName,
    ):
        """Create a family of simulatinos for the cube.

        Args:
            cube: The cube to create the simulation on.
            simulation_name: The name for the simulation we are creating.
            columns: Collection of levels to use for the simulation.
            multiply: Collection of measures whose values we want to multiply.
            replace: Colection of measures whose values we want to replace.
            add: Collection of measures whose values we want to increment.
            base_scenario_name: The name of the base scenario.

        Returns:
            The name of the store containing the simulation.
        """
        # Replace None values
        if not multiply:
            multiply = []
        if not replace:
            replace = []
        if not add:
            add = []

        # Convert to java objects
        jmultiply = to_java_string_array(
            self.gateway, [measure.name for measure in multiply]
        )
        jreplace = to_java_string_array(
            self.gateway, [measure.name for measure in replace]
        )
        jadd = to_java_string_array(self.gateway, [measure.name for measure in add])
        jcolumns = to_java_string_array(
            self.gateway, convert_level_in_description(columns)
        )
        self.java_api.doCreateSimulation(
            cube.name,
            simulation_name,
            jcolumns,
            jmultiply,
            jreplace,
            jadd,
            base_scenario_name,
        )

    def delete_simulation_scenario(
        self, simulation: Simulation, scenario_name: str
    ) -> None:
        """Delete a scenario from the given simulation.

        Args:
            simulation: The simulation to delete the scenario from.
            scenario_name: The name of the scenario to delete.

        """
        self.java_api.deleteScenario(simulation.name, scenario_name)

    def _get_java_rows_for_bucketing(
        self,
        # Contains pd.DataFrame which is untyped.
        rows: BucketRows,  # type: ignore
    ) -> JavaArray:
        """Convert the rows to the expected format for bucketing."""
        if isinstance(rows, list):
            java_rows = to_java_object_array_array(self.gateway, rows)
        elif isinstance(rows, dict):
            converted_rows = []
            for column_values, value in rows.items():
                for bucket, weight in value.items():
                    row: List[Any] = list(column_values)
                    row.append(bucket)
                    row.append(weight)
                    converted_rows.append(row)
            java_rows = to_java_object_array_array(self.gateway, converted_rows)
        elif isinstance(rows, pd.DataFrame):
            # Insertion is done after store creation.
            java_rows = to_java_object_array_array(self.gateway, [])
        else:
            raise ValueError("Rows are not in the expected format.")
        return java_rows

    def create_bucketing(
        self,
        cube: Cube,
        bucket_name: str,
        columns_seq: Sequence[Level],
        # Contains pd.DataFrame which is untyped.
        rows_for_bucket: BucketRows,  # type: ignore
        bucket_dimension: str,
        weight_name: str,
        weighted_measures: Sequence[Measure],
    ) -> str:
        """Create a new bucketing on a cube.

        Args:
            cube: The cube to create the bucketing on
            bucket_name: The name for the bucket we are creating
            columns_seq: The list of columsn_seq to use for the bucketing
            rows_for_bucket: The rows to use for the bucketing
            bucket_dimension: The name of the dimension to use for the bucketing
            weight_name: The name of the measure to use for the weights
            weighted_measures: List of measures to scale with the weight
        Returns:
            The name of the store containing the bucketing

        """
        jrows = self._get_java_rows_for_bucketing(rows_for_bucket)
        jlevels = to_java_string_array(
            self.gateway,
            [
                lvl._java_description  # pylint: disable=protected-access
                for lvl in columns_seq
            ],
        )
        jweighted_measures = ListConverter().convert(
            [m.name for m in weighted_measures], self.gateway._gateway_client
        )
        return self.java_api.createBucketing(
            cube.name,
            bucket_name,
            jlevels,
            jrows,
            bucket_dimension,
            weight_name,
            jweighted_measures,
        )

    def delete_simulation(self, simulation: Simulation) -> None:
        """Delete the given simulation from the JVM.

        Args:
            simulation: The simulation to delete.

        """
        self.java_api.deleteSimulation(simulation.name)

    def set_aws_region(self, region: str):
        """Set the AWS region."""
        self.java_api.setAwsRegion(region)

    def get_loading_mode(self, store: Store) -> SamplingMode:
        """Get the loading mode of the given store.

        Args:
            store: The store
        Returns:
            The loading mode.

        """
        java_mode = self.java_api.getSamplingMode(store.name)
        return SamplingMode(java_mode.getMode(), list(java_mode.getParameters()))

    def should_warn_for_store_sampling_policy(self, store: Store) -> bool:
        """Check whether we should warn because a store does not respect the policy.

        Args:
            store: the store to check.
        Retruns:
            Whether we should warn
        """
        return self.java_api.shouldWarnForSamplingPolicy(store.name)

    def load_all_data(self):
        """Trigger the full loading mode."""
        self.java_api.triggerFullLoad()


def check_oidc_config(oidc: OidcAuthentication):
    """Check that the authentication is valid."""
    if oidc.provider_id is None:
        raise ValueError("Missing provider_id in oidc configuration")
    if oidc.client_secret is None:
        raise ValueError("Missing client_secret in oidc configuration")
    if oidc.client_id is None:
        raise ValueError("Missing client_id in oidc configuration")
    if oidc.issuer_url is None:
        raise ValueError("Missing issuer_url in oidc configuration")
