"""Cube of a Session."""

from __future__ import annotations

from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import pandas as pd

from ._docs_utils import doc
from ._ipython_utils import run_from_ipython
from ._level_conditions import LevelCondition
from ._measures.named_measure import NamedMeasure
from ._multi_condition import MultiCondition
from ._query_plan import QueryAnalysis
from ._repr_utils import convert_repr_json_to_html, repr_json_cube
from ._type_utils import BASE_SCENARIO, ScenarioName
from ._widget import display_widget
from .aggregates_cache import AggregatesCache
from .hierarchies import Hierarchies
from .level import Level
from .levels import Levels
from .measure import Measure
from .measures import Measures
from .query._cellset import LevelCoordinates
from .query.cube import _QUERY_ARGS_DOC, _QUERY_DOC
from .query.level import QueryLevel
from .query.measure import QueryMeasure
from .simulation import Simulation
from .simulations import Simulations
from .types import INT, AtotiType

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .session import Session
    from .store import Store

BucketRows = Union[Dict[Tuple[Any, ...], Dict[str, Any]], pd.DataFrame, List[List[Any]]]


class Cube:
    """Cube of a Session."""

    def __init__(
        self, java_api: JavaApi, name: str, base_store: Store, session: Session
    ):
        """Init."""
        self._name = name
        self._java_api = java_api
        self._base_store = base_store
        self._session = session
        self._agg_cache = AggregatesCache(java_api, self)
        self._hierarchies = Hierarchies(java_api, self)
        self._levels = Levels(self._hierarchies)
        self._measures = Measures(java_api, self)
        self._simulations = Simulations(java_api)

    @property
    def name(self) -> str:
        """Name of the cube."""
        return self._name

    @property
    def hierarchies(self) -> Hierarchies:
        """Hierarchies of the cube."""
        return self._hierarchies

    @property
    def levels(self) -> Levels:
        """Levels of the cube."""
        return self._levels

    @property
    def measures(self) -> Measures:
        """Measures of the cube."""
        return self._measures

    @property
    def simulations(self) -> Simulations:  # noqa: D401
        """Simulations of the cube."""
        return self._simulations

    @property
    def aggregates_cache(self) -> AggregatesCache:  # noqa: D401
        """Aggregates cache of the cube."""
        return self._agg_cache

    @property
    def schema(self) -> Any:
        """Return the schema of the cube's stores as an SVG graph.

        Note:
            Graphviz is required to display the graph. It can be installed
            with Conda: ``conda install graphviz`` or by following the
            `download instructions <https://www.graphviz.org/download/>`_.

        Returns:
            An SVG image in IPython and a Path to the SVG file otherwise.
        """
        path = self._java_api.generate_cube_schema_image(self.name)
        if run_from_ipython():
            from IPython.display import SVG

            return SVG(filename=path)
        return Path(path)

    def _get_level_data_types(self, level_coords: List[LevelCoordinates]) -> List[str]:
        return [
            "object"
            if level_coord == ("Epoch", "Branch")
            else self.levels[level_coord].data_type
            for level_coord in level_coords
        ]

    def _generate_mdx(
        self,
        measures: Sequence[NamedMeasure],
        scenario: ScenarioName,
        *,
        levels: Optional[Union[Level, Sequence[Level]]] = None,
        condition: Optional[Union[LevelCondition, MultiCondition]] = None,
    ) -> str:
        query_measures = [
            QueryMeasure(
                measure.name, measure.visible, measure.folder, measure.formatter
            )
            for measure in measures
        ]
        query_levels = (
            [QueryLevel(levels.name, levels.dimension, levels.hierarchy)]
            if isinstance(levels, Level)
            else [
                QueryLevel(level.name, level.dimension, level.hierarchy)
                for level in (levels or [])
            ]
        )
        return (
            self._session._open_query_session()  # pylint: disable=protected-access
            .cubes[self.name]
            ._generate_mdx(query_measures, query_levels, scenario, condition=condition)
        )

    @doc(_QUERY_DOC)
    def query(
        self,
        *measures: NamedMeasure,
        levels: Optional[Union[Level, Sequence[Level]]] = None,
        condition: Optional[Union[LevelCondition, MultiCondition]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> pd.DataFrame:
        mdx = self._generate_mdx(
            measures, ScenarioName(scenario), levels=levels, condition=condition
        )
        return self._session.query_mdx(mdx, timeout=timeout)

    @doc(args=_QUERY_ARGS_DOC)
    def explain_query(
        self,
        *measures: NamedMeasure,
        levels: Optional[Union[Level, Sequence[Level]]] = None,
        condition: Optional[Union[LevelCondition, MultiCondition]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> QueryAnalysis:
        """Run the query but return an explanation of the query instead of the result.

        The explanation contains a summary, global timings and the query plan with
        all the retrievals.

        {args}

        Returns:
            The query explanation.
        """
        mdx = self._generate_mdx(
            measures, ScenarioName(scenario), levels=levels, condition=condition
        )
        return self._java_api.analyse_mdx(mdx, timeout)

    def setup_simulation(
        self,
        name: str,
        *,
        base_scenario: str = BASE_SCENARIO,
        levels: Optional[Sequence[Level]] = None,
        multiply: Optional[Collection[Measure]] = None,
        replace: Optional[Collection[Measure]] = None,
        add: Optional[Collection[Measure]] = None,
    ) -> Simulation:
        """Create a simulation store for the given measures.

        Simulations can have as many scenarios as desired.

        The same measure cannot be passed in several methods.

        Args:
            name: The name of the simulation.
            base_scenario: The name of the base scenario.
            levels: The levels to simulate on.
            multiply: Measures whose values will be multiplied.
            replace: Measures whose values will be replaced.
            add: Measures whose values will be added (incremented).

        Returns:
            The simulation on which scenarios can be made.
        """
        simulation = Simulation(
            name,
            levels or [],
            multiply or [],
            replace or [],
            add or [],
            ScenarioName(base_scenario),
            self,
            self._java_api,
        )
        self.simulations[name] = simulation
        return simulation

    # Make public when we'll have more use cases
    # to know if this is the right design.
    def _setup_bucketing(
        self,
        name: str,
        # Why is this named columns while it's a sequence of levels?
        columns: Sequence[Level],
        *,
        # Would be better not to accept this parameter and
        # let users add data through the regular API of the returned store.
        rows: BucketRows = None,  # type: ignore
        bucket_dimension: str = "Buckets",
        weight_name: Optional[str] = None,
        weighted_measures: Optional[Sequence[Measure]] = None,
    ) -> Store:
        """Create a bucketing store.

        The bucketing is done by mapping one or several columns to buckets with weights.
        This mapping is done in a store with all the columns of the mapping, a column with the
        bucket and a column for the weight:

            +---------+---------+---------+-----------+------------------+
            | Column1 | Column2 | Column3 | My Bucket | My Bucket_weight |
            +=========+=========+=========+===========+==================+
            | a       | b       | c       | BucketA   |             0.25 |
            +---------+---------+---------+-----------+------------------+
            | a       | b       | c       | BucketB   |             0.75 |
            +---------+---------+---------+-----------+------------------+
            | d       | e       | f       | BucketA   |              1.0 |
            +---------+---------+---------+-----------+------------------+
            | g       | h       | i       | BucketB   |              1.0 |
            +---------+---------+---------+-----------+------------------+

        There are multiple ways to feed this store

        * with a pandas DataFrame corresponding to the store
        * with a list of the rows::

            [
                ["a", "b", "c", "BucketA", 0.25],
                ["a", "b", "c", "BucketB", 0.75],
                ...
            ]

        * with a dict::

            {
                ("a", "b", "c") : {"BucketA": 0.25, "BucketB": 0.75},
                ("d", "e", "f") : {"BucketA": 1.0},
                ...
            }

        Some measures can be overriden automatically to be scaled with the weights.

        Args:
            name: The name of the bucket. It will be used as the name of the column in the bucket
                store and as the name of the bucket hierarchy.
            columns: The columns to bucket on.
            weighted_measures: Measures that will be scaled with the weight.
            rows: The mapping between the columns and the bucket.
                It can either be a list of rows, or a pandas DataFrame.
            bucket_dimension: The name of the dimension to put the bucket hierarchy in.
            weight_name: the name of the measure for the weights.

        Returns:
            The store that can be modified to change the bucketing dynamically.
        """
        from .store import Store  # pylint: disable=redefined-outer-name

        if rows is None:
            rows = [[]]
        if weight_name is None:
            weight_name = name + "_weight"
        if weighted_measures is None:
            weighted_measures = []

        bucket_store_name = self._java_api.create_bucketing(
            self, name, columns, rows, bucket_dimension, weight_name, weighted_measures
        )

        bucket_store = Store(bucket_store_name, self._java_api)

        # We need to refresh the DS and the cube
        self._java_api.refresh(False)

        if isinstance(rows, pd.DataFrame):
            bucket_store.load_pandas(rows)

        return bucket_store

    def create_parameter_hierarchy(
        self,
        name: str,
        members: Sequence[Any],
        *,
        data_type: Optional[AtotiType] = None,
        index_measure: Optional[str] = None,
        indices: Optional[Sequence[int]] = None,
        store_name: Optional[str] = None,
    ):
        """Create an arbitrary single-level static hierarchy with the given members.

        It can be used as a parameter hierarchy in advanced analyses.

        Args:
            name: The name of hierarchy and its single level.
            members: The members of the hierarchy.
            data_type: The type with which the members will be stored.
                Automatically inferred by default.
            index_measure: The name of the indexing measure to create for this hierarchy, if any.
            indices: The custom indices for each member in the new hierarchy.
                They are used when accessing a member through the ``index_measure``.
                Defaults to ``range(len(members))``.
            store_name: The name of the store backing the parameter hierarchy.
                Defaults to the passed ``name`` argument.
        """
        index_column = f"{name}__index"

        indices = list(range(len(members))) if not indices else indices
        parameter_df = pd.DataFrame({name: members, index_column: indices})

        types = {index_column: INT}
        if data_type:
            types[name] = data_type
        elif all(
            isinstance(member, int) and -(2 ** 31) <= member < 2 ** 31
            for member in members
        ):
            types[name] = INT

        parameter_store = self._session.read_pandas(
            parameter_df, store_name or name, keys=[name], types=types,
        )

        self._base_store.join(parameter_store)

        if index_column in self.hierarchies:
            del self.hierarchies[index_column]

        if index_measure:
            self.measures[index_measure] = parameter_store[index_column]

        self.hierarchies[name].slicing = True

        self._java_api.refresh_pivot()

    def visualize(self, name: Optional[str] = None):
        """Display an atoti widget to explore the cube interactively.

        This is only supported in JupyterLab and requires the atoti extension
        to be installed and enabled.

        The widget state will be stored in the cell metadata.
        This state should not have to be edited but, if desired, it can be found in JupyterLab
        by opening the "Notebook tools" sidebar and expanding the the "Advanced Tools" section.

        Args:
            name: The name of the widget.
        """
        display_widget(self.name, self._session.name, name)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_cube(self)
