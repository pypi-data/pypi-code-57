import trafaret as t
from datarobot.utils.pagination import unpaginate

from datarobot.models.sharing import SharingAccess

from datarobot.models.api_object import APIObject
from ..utils import encode_utf8_if_py2, parse_time


class FeatureEngineeringGraph(APIObject):
    """ A Feature Engineering Graph for the Project.
    A Feature Engineering Graph is graph which allow to specify relationships
    between two or more tables so it can automatically generate features from that

    Attributes
    ----------
    id : str
        the id of the created feature engineering graph
    name: str
        name of the feature engineering graph
    description: str
        description of the feature engineering graph
    created: datetime.datetime
        creation date of the feature engineering graph
    creator_user_id: str
        id of the user who created the feature engineering graph
    creator_full_name: str
        full name of the user who created the feature engineering graph
    last_modified: datetime.datetime
        last modification date of the feature engineering graph
    last_modified_user_id: str
        id of the user who last modified the feature engineering graph
    modifier_full_name: str
        full name of the user who last modified the feature engineering graph
    number_of_projects: int
        number of projects that are used in the feature engineering graph
    linkage_keys: list os str
        a list of strings specifying the name of the columns that link
        the feature engineering graph with the primary table.
    table_definitions: list
        each element is a table_definition for a table.
    relationships: list
        each element is a relationship between two tables
    time_unit: str, or None
        time unit of the feature derivation window. Supported
        values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
        If present, the feature engineering Graph will perform time-aware joins.
    feature_derivation_window_start: int, or None
        how many time_units of each table's primary temporal key into the past relative
        to the datetimePartitionColumn the feature derivation window should begin.
        Will be a negative integer,
        If present, the feature engineering Graph will perform time-aware joins.
    feature_derivation_window_end: int, or None
        how many timeUnits of each table's record
        primary temporal key into the past relative to the datetimePartitionColumn the feature
        derivation window should end.  Will be a non-positive integer, if present.
        If present, the feature engineering Graph will perform time-aware joins.
    is_draft: bool (default=True)
        a draft (is_draft=True) feature engineering graph can be updated,
        while a non-draft(is_draft=False) feature engineering graph is immutable

    The `table_defintions` structure is

    identifier: str
        alias of the table (used directly as part of the generated feature names)
    catalog_id: str, or None
        identifier of the catalog item
    catalog_version_id: str
        identifier of the catalog item version
    feature_list_id: str, or None
        identifier of the feature list. This decides which columns in the table are
        used for feature generation
    primary_temporal_key: str, or None
        name of the column indicating time of record creation
    snapshot_policy: str
        policy to use  when creating a project or making predictions.
        Must be one of the following values:
        'specified': Use specific snapshot specified by catalogVersionId
        'latest': Use latest snapshot from the same catalog item
        'dynamic': Get data from the source (only applicable for JDBC datasets)
    feature_lists: list
        list of feature list info
    data_source: dict
        data source info if the table is from data source
    is_deleted: bool or None
        whether the table is deleted or not

    The `relationship` structure is

    table1_identifier: str or None
        identifier of the first table in this relationship.
        This is specified in the indentifier field of table_definition structure.
        If None, then the relationship is with the primary dataset.
    table2_identifier: str
        identifier of the second table in this relationship.
        This is specified in the identifier field of table_definition schema.
    table1_keys: list of str (max length: 10 min length: 1)
        column(s) from the first table which are used to join to the second table
    table2_keys: list of str (max length: 10 min length: 1)
        column(s) from the second table that are used to join to the first table

    The `feature list info` structure is

    id : str
        the id of the featurelist
    name : str
        the name of the featurelist
    features : list of str
        the names of all the Features in the featurelist
    dataset_id : str
        the project the featurelist belongs to
    creation_date : datetime.datetime
        when the featurelist was created
    user_created : bool
        whether the featurelist was created by a user or by DataRobot automation
    created_by: str
        the name of user who created it
    description : str
        the description of the featurelist.  Can be updated by the user
        and may be supplied by default for DataRobot-created featurelists.
    dataset_id: str
        dataset which is associated with the feature list
    dataset_version_id: str or None
        version of the dataset which is associated with feature list.
        Only relevant for Informative features

    The `data source info` structured is

    data_store_id: str
        the id of the data store.
    data_store_name : str
        the user-friendly name of the data store.
    url : str
        the url used to connect to the data store.
    dbtable : str
        the name of table from the data store.
    schema: str
        schema definition of the table from the data store
    """
    _path = 'featureEngineeringGraphs/'
    data_source_trafaret = t.Dict(
        {
            t.Key('data_store_name'): t.String,
            t.Key('data_store_id'): t.String,
            t.Key('url'): t.String,
            t.Key('dbtable'): t.String | t.Null,
            t.Key('schema', optional=True): t.String | t.Null,
        }
    )

    feature_list_info = t.Dict(
        {
            t.Key('id'): t.String,
            t.Key('features'): t.List(t.String),
            t.Key('name'): t.String,
            t.Key('description'): t.String,
            t.Key('dataset_id'): t.String,
            t.Key('user_created'): t.Bool,
            t.Key('creation_date'): parse_time,
            t.Key('created_by'): t.String,
            t.Key('dataset_version_id', optional=True): t.String
        }
    )

    table_definition_trafaret = t.Dict(
        {
            t.Key('identifier'): t.String(
                min_length=3, max_length=20
            ),
            t.Key('catalog_version_id'): t.String,
            t.Key('catalog_id', optional=True): t.String,
            t.Key('primary_temporal_key', optional=True): t.String | t.Null,
            t.Key('feature_list_id', optional=True): t.String | t.Null,
            t.Key('feature_lists', optional=True): t.List(feature_list_info),
            t.Key('snapshot_policy', optional=True, default='latest'): t.Enum(
                'latest', 'specified', 'dynamic'),
            t.Key('data_source', optional=True): data_source_trafaret | t.Null,
            t.Key('is_deleted', optional=True): t.Bool | t.Null,
        }
    )

    relationships_trafaret = t.Dict(
        {
            t.Key('table1_identifier', optional=True): t.String | t.Null,
            t.Key('table2_identifier'): t.String,
            t.Key('table1_keys'): t.List(t.String, min_length=1, max_length=10),
            t.Key('table2_keys'): t.List(t.String, min_length=1, max_length=10),
        }
    )
    _converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('name'): t.String(max_length=100, allow_blank=False),
        t.Key('description'): t.String(max_length=300, allow_blank=False),
        t.Key('created'): parse_time,
        t.Key('last_modified'): parse_time,
        t.Key('creator_full_name'): t.String,
        t.Key('modifier_full_name'): t.String,
        t.Key('creator_user_id'): t.String,
        t.Key('last_modified_user_id'): t.String,
        t.Key('number_of_projects'): t.Int,
        t.Key('linkage_keys'): t.List(t.String),
        t.Key('table_definitions'): t.List(table_definition_trafaret, min_length=1),
        t.Key('relationships', optional=True): t.List(relationships_trafaret),
        t.Key('time_unit', optional=True): t.String,
        t.Key('feature_derivation_window_start', optional=True): t.Int(lt=0),
        t.Key('feature_derivation_window_end', optional=True): t.Int(lte=0),
        t.Key('is_draft', optional=True): t.Bool()
    }).ignore_extra('*')

    def __init__(self, id=None, name=None, description=None,
                 created=None, last_modified=None, creator_full_name=None,
                 modifier_full_name=None, creator_user_id=None,
                 last_modified_user_id=None, number_of_projects=None,
                 linkage_keys=None, table_definitions=None, relationships=None,
                 time_unit=None, feature_derivation_window_start=None,
                 feature_derivation_window_end=None, is_draft=True):
        self.feature_engineering_graph_id = id
        self.name = name
        self.description = description
        self.created = created
        self.last_modified = last_modified
        self.creator_full_name = creator_full_name
        self.modifier_full_name = modifier_full_name
        self.creator_user_id = creator_user_id
        self.last_modified_user_id = last_modified_user_id
        self.number_of_projects = number_of_projects
        self.linkage_keys = linkage_keys
        self.table_definitions = table_definitions
        self.relationships = relationships
        self.time_unit = time_unit
        self.feature_derivation_window_start = feature_derivation_window_start
        self.feature_derivation_window_end = feature_derivation_window_end
        self.is_draft = is_draft

    def __repr__(self):
        return encode_utf8_if_py2(u'{}()'.format(self.__class__.__name__))

    def _build_url(self, feature_engineering_graph_id):
        return '{}{}/'.format(self._path, feature_engineering_graph_id)

    @classmethod
    def _create_payload(cls,
                        name,
                        description,
                        table_definitions,
                        relationships,
                        time_unit,
                        feature_derivation_window_start,
                        feature_derivation_window_end,
                        is_draft):
        """
        Create the payload to create feature engineering graph

        Parameters
        ----------
        name: str
            name of the feature engineering graph
        description: str
            description of the fearture engineering graph
        table_definitions: list
            each element is a table_definition for a table.
        relationships: list
            each element is a relationship between two tables
        time_unit: str or None
            time unit of the feature derivation window. Supported
            values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
            If present, the feature engineering Graph will perform time-aware joins.
        feature_derivation_window_start: int, or None
            how many time_units of each table's primary temporal key into the past relative
            to the datetimePartitionColumn the feature derivation window should begin.
            Will be a negative integer,
            If present, the feature engineering Graph will perform time-aware joins.
        feature_derivation_window_end: int, or None
            how many timeUnits of each table's record
            primary temporal key into the past relative to the datetimePartitionColumn the feature
            derivation window should end.  Will be a non-positive integer, if present.
            If present, the feature engineering Graph will perform time-aware joins.
        is_draft: bool (default=True)
            a draft (is_draft=True) feature engineering graph can be updated,
            while a non-draft(is_draft=False) feature engineering graph is immutable
        Returns
        -------
        payload: dict
            payload for the feature engineering graph
        """
        payload = {
            'name': name,
            'description': description,
            'tableDefinitions': table_definitions,
            'relationships': relationships
        }

        if time_unit is not None:
            payload['timeUnit'] = time_unit

        if feature_derivation_window_start is not None:
            payload['featureDerivationWindowStart'] = feature_derivation_window_start

        if feature_derivation_window_end is not None:
            payload['featureDerivationWindowEnd'] = feature_derivation_window_end

        payload['isDraft'] = is_draft
        return payload

    @classmethod
    def create(cls,
               name,
               description,
               table_definitions,
               relationships,
               time_unit=None,
               feature_derivation_window_start=None,
               feature_derivation_window_end=None,
               is_draft=True):
        """
        Create a feature engineering graph.

        Parameters
        ----------
        name : str
            the name of the feature engineering graph
        description : str
            the description of the feature engineering graph
        table_definitions: list of dict
            each element is a TableDefinition for a table.
            The `TableDefinition` schema is

            identifier: str
                alias of the table (used directly as part of the generated feature names)
            catalog_id: str, or None
                identifier of the catalog item
            catalog_version_id: str
                identifier of the catalog item version
            feature_list_id: str, or None
                identifier of the feature list. This decides which columns in the table are
                used for feature generation
            primary_temporal_key: str, or None
                name of the column indicating time of record creation
            snapshot_policy: str
                policy to use  when creating a project or making predictions.
                Must be one of the following values:
                'specified': Use specific snapshot specified by catalogVersionId
                'latest': Use latest snapshot from the same catalog item
                'dynamic': Get data from the source (only applicable for JDBC datasets)
        relationships: list of dict
            each element is a Relationship between two tables
            The `Relationship` schema is

            table1_identifier: str or None
                identifier of the first table in this relationship.
                This is specified in the indentifier field of table_definition structure.
                If None, then the relationship is with the primary dataset.
            table2_identifier: str
                identifier of the second table in this relationship.
                This is specified in the identifier field of table_definition schema.
            table1_keys: list of str (max length: 10 min length: 1)
                column(s) from the first table which are used to join to the second table
            table2_keys: list of str (max length: 10 min length: 1)
                column(s) from the second table that are used to join to the first table
        time_unit: str, or None
            time unit of the feature derivation window. Supported
            values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
            If present, the feature engineering Graph will perform time-aware joins.
        feature_derivation_window_start: int, or None
            how many time_units of each table's primary temporal key into the past relative
            to the datetimePartitionColumn the feature derivation window should begin.
            Will be a negative integer,
            If present, the feature engineering Graph will perform time-aware joins.
        feature_derivation_window_end: int, or None
            how many timeUnits of each table's record
            primary temporal key into the past relative to the datetimePartitionColumn the feature
            derivation window should end.  Will be a non-positive integer, if present.
            If present, the feature engineering Graph will perform time-aware joins.
        is_draft: bool (default=True)
            a draft (is_draft=True) feature engineering graph can be updated,
            while a non-draft(is_draft=False) feature engineering graph is immutable

        Returns
        -------
        feature_engineering_graphs: FeatureEngineeringGraph
            the created feature engineering graph
        """
        payload_data = cls._create_payload(
            name=name,
            description=description,
            table_definitions=table_definitions,
            relationships=relationships,
            time_unit=time_unit,
            feature_derivation_window_start=feature_derivation_window_start,
            feature_derivation_window_end=feature_derivation_window_end,
            is_draft=is_draft)

        response = cls._client.post(cls._path, data=payload_data).json()
        return FeatureEngineeringGraph.from_server_data(response)

    def replace(self,
                id,
                name,
                description,
                table_definitions,
                relationships,
                time_unit=None,
                feature_derivation_window_start=None,
                feature_derivation_window_end=None,
                is_draft=True):
        """
        Replace a feature engineering graph.

        Parameters
        ----------
        id : str
            the id of the created feature engineering graph
        name : str
            the name of the feature engineering graph
        description : str
            the description of the feature engineering graph
        items: list of dict
            each element is a TableDefinition for a table.
            The `TableDefinition` schema is

            identifier: str
                alias of the table (used directly as part of the generated feature names)
            catalog_id: str, or None
                identifier of the catalog item
            catalog_version_id: str
                identifier of the catalog item version
            feature_list_id: str, or None
                identifier of the feature list. This decides which columns in the table are
                used for feature generation
            primary_temporal_key: str, or None
                name of the column indicating time of record creation
            snapshot_policy: str
                policy to use  when creating a project or making predictions.
                Must be one of the following values:
                'specified': Use specific snapshot specified by catalogVersionId
                'latest': Use latest snapshot from the same catalog item
                'dynamic': Get data from the source (only applicable for JDBC datasets)
        relationships: list of dict
            each element is a Relationship between two tables
            The `Relationship` schema is

            table1_identifier: str or None
                identifier of the first table in this relationship.
                This is specified in the indentifier field of table_definition structure.
                If None, then the relationship is with the primary dataset.
            table2_identifier: str
                identifier of the second table in this relationship.
                This is specified in the identifier field of table_definition schema.
            table1_keys: list of str (max length: 10 min length: 1)
                column(s) from the first table which are used to join to the second table
            table2_keys: list of str (max length: 10 min length: 1)
                column(s) from the second table that are used to join to the first table
        time_unit: str, or None
            time unit of the feature derivation window. Supported
            values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
            If present, the feature engineering Graph will perform time-aware joins.
        feature_derivation_window_start: int, or None
            how many time_units of each table's primary temporal key into the past relative
            to the datetimePartitionColumn the feature derivation window should begin.
            Will be a negative integer,
            If present, the feature engineering Graph will perform time-aware joins.
        feature_derivation_window_end: int, or None
            how many timeUnits of each table's record
            primary temporal key into the past relative to the datetimePartitionColumn the feature
            derivation window should end.  Will be a non-positive integer, if present.
            If present, the feature engineering Graph will perform time-aware joins.
        is_draft: bool (default=True)
            a draft (is_draft=True) feature engineering graph can be updated,
            while a non-draft(is_draft=False) feature engineering graph is immutable

        Returns
        -------
        feature_engineering_graphs: FeatureEngineeringGraph
            the updated feature engineering graph
        """
        payload_data = self._create_payload(
            name=name,
            description=description,
            table_definitions=table_definitions,
            relationships=relationships,
            time_unit=time_unit,
            feature_derivation_window_start=feature_derivation_window_start,
            feature_derivation_window_end=feature_derivation_window_end,
            is_draft=is_draft)

        response = self._client.put(self._build_url(feature_engineering_graph_id=id),
                                    json=payload_data).json()
        return FeatureEngineeringGraph.from_server_data(response)

    def update(self, name, description):
        """
        Update the Feature engineering graph name and description.

        Parameters
        ----------
        name : str
            the name of the feature engineering graph
        description : str
            the description of the feature engineering graph
        """
        payload = {
            'name': name,
            'description': description
        }
        build_url = self._build_url(feature_engineering_graph_id=self.feature_engineering_graph_id)
        self._client.patch(build_url, data=payload)

    @classmethod
    def get(cls, feature_engineering_graph_id):
        """
        Retrieve a single feature engineering graph

        Parameters
        ----------
        feature_engineering_graph_id : str
            The ID of the feature engineering graph to retrieve.

        Returns
        -------
        feature_engineering_graph : FeatureEngineeringGraph
            The requested feature engineering graph
        """
        return cls.from_location('{}{}/'.format(cls._path, feature_engineering_graph_id))

    @classmethod
    def list(cls, project_id=None, secondary_dataset_id=None, include_drafts=None):
        """
        Returns list of feature engineering graphs.

        Parameters
        ----------
        project_id: str, optional
            The Id of project to filter the feature engineering graph list for returning
            only those feature engineering Graphs which are related to this project
            If not specified, it will return all the feature engineering graphs
            irrespective of the project
        secondary_dataset_id: str, optional
            ID of the dataset to filter feature engineering graphs which use the
            dataset as the secondary dataset
            If not specified, return all the feature engineering graphs without filtering on
            secondary dataset id.
        include_drafts: bool (default=False)
            include draft feature engineering graphs
            If `True`, return all the draft (mutable) as well as non-draft (immutable)
            feature engineering graphs

        Returns
        -------
        feature_engineering_graphs : list of FeatureEngineeringGraph instances
            a list of available feature engineering graphs.
        """
        kwargs = {}
        if project_id:
            kwargs['projectId'] = project_id
        if secondary_dataset_id:
            kwargs['secondaryDatasetId'] = secondary_dataset_id
        if include_drafts:
            kwargs['includeDrafts'] = include_drafts

        r_data = cls._client.get(cls._path, params=kwargs).json()
        return [FeatureEngineeringGraph.from_server_data(item) for item in r_data['data']]

    def delete(self):
        """
        Delete the Feature Engineering Graph
        """
        self._client.delete('{}{}/'.format(self._path, self.feature_engineering_graph_id))

    def share(self, access_list):
        """
        Modify the ability of users to access this feature engineering graph

        Parameters
        ----------
        access_list : list of :class:`SharingAccess <datarobot.SharingAccess>`
            the modifications to make.

        Raises
        ------
        datarobot.ClientError :
            if you do not have permission to share this feature engineering graph or
            if the user you're sharing with doesn't exist

        """
        payload = {'permissions': [access.collect_payload() for access in access_list]}
        self._client.patch('{}{}/accessControls/'.format(self._path,
                                                         self.feature_engineering_graph_id),
                           data=payload,
                           keep_attrs={'role'})

    def get_access_list(self):
        """
        Retrieve what users have access to this feature engineering graph

        Returns
        -------
        list of :class:`SharingAccess <datarobot.SharingAccess>`
        """
        url = '{}{}/accessControls/'.format(self._path, self.feature_engineering_graph_id)
        return [SharingAccess.from_server_data(datum)
                for datum in unpaginate(url, {}, self._client)]
