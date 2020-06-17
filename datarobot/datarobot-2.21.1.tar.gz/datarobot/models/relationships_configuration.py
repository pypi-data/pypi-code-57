import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2, parse_time


class AllowedTimeUnitsSAFER(object):
    """ Enum for SAFER allowed time units
    """

    MILLISECOND = "MILLISECOND"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"

    ALL = t.Enum(MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR)


class RelationshipsConfiguration(APIObject):
    """ A Relationships configuration specifies a set of secondary datasets as well as
    the relationships among them. It is used to configure Feature Discovery for a project
    to generate features automatically from these datasets.

    Attributes
    ----------
    id : str
        the id of the created relationships configuration
    dataset_definitions: list
        each element is a dataset_definitions for a dataset.
    relationships: list
        each element is a relationship between two datasets

    The `dataset_defintions` structure is

    identifier: str
        alias of the dataset (used directly as part of the generated feature names)
    catalog_id: str, or None
        identifier of the catalog item
    catalog_version_id: str
        identifier of the catalog item version
    primary_temporal_key: str, or None
        name of the column indicating time of record creation
    feature_list_id: str, or None
        identifier of the feature list. This decides which columns in the dataset are
        used for feature generation
    snapshot_policy: str
        policy to use  when creating a project or making predictions.
        Must be one of the following values:
        'specified': Use specific snapshot specified by catalogVersionId
        'latest': Use latest snapshot from the same catalog item
        'dynamic': Get data from the source (only applicable for JDBC datasets)
    feature_lists: list
        list of feature list info
    data_source: dict
        data source info if the dataset is from data source
    is_deleted: bool or None
        whether the dataset is deleted or not

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

    The `relationships` schema is

    dataset1_identifier: str or None
        identifier of the first dataset in this relationship.
        This is specified in the indentifier field of dataset_definition structure.
        If None, then the relationship is with the primary dataset.
    dataset2_identifier: str
        identifier of the second dataset in this relationship.
        This is specified in the identifier field of dataset_definition schema.
    dataset1_keys: list of str (max length: 10 min length: 1)
        column(s) from the first dataset which are used to join to the second dataset
    dataset2_keys: list of str (max length: 10 min length: 1)
        column(s) from the second dataset that are used to join to the first dataset
    time_unit: str, or None
        time unit of the feature derivation window. Supported
        values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
        If present, the feature engineering Graph will perform time-aware joins.
    feature_derivation_window_start: int, or None
        how many time_units of each dataset's primary temporal key into the past relative
        to the datetimePartitionColumn the feature derivation window should begin.
        Will be a negative integer,
        If present, the feature engineering Graph will perform time-aware joins.
    feature_derivation_window_end: int, or None
        how many timeUnits of each dataset's record
        primary temporal key into the past relative to the datetimePartitionColumn the
        feature derivation window should end.  Will be a non-positive integer, if present.
        If present, the feature engineering Graph will perform time-aware joins.
    feature_derivation_window_time_unit: int or None
        time unit of the feature derivation window. Supported values are
        MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
        If present, time-aware joins will be used.
        Only applicable when dataset1Identifier is not provided.
    prediction_point_rounding: int, or None
        closest value of prediction_point_rounding_time_unit to round the prediction point
        into the past when applying the feature derivation window. Will be a positive integer,
        if present.Only applicable when dataset1_identifier is not provided.
    prediction_point_rounding_time_unit: str, or None
        time unit of the prediction point rounding. Supported values are
        MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
        Only applicable when dataset1_identifier is not provided.
    """

    _path = "relationshipsConfigurations/"
    data_source_trafaret = t.Dict(
        {
            t.Key("data_store_name"): t.String,
            t.Key("data_store_id"): t.String,
            t.Key("url"): t.String,
            t.Key("dbtable"): t.String | t.Null,
            t.Key("schema", optional=True): t.String | t.Null,
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
    dataset_definitions_trafaret = t.Dict(
        {
            t.Key("identifier"): t.String(min_length=3, max_length=20),
            t.Key("catalog_version_id"): t.String,
            t.Key("catalog_id"): t.String,
            t.Key("primary_temporal_key", optional=True): t.String | t.Null,
            t.Key("feature_list_id", optional=True): t.String | t.Null,
            t.Key("snapshot_policy", optional=True, default="latest"): t.Enum(
                "latest", "specified", "dynamic"
            ),
            t.Key('feature_lists', optional=True): t.List(feature_list_info),
            t.Key("data_source", optional=True): data_source_trafaret | t.Null,
            t.Key("is_deleted", optional=True): t.Bool | t.Null,
        }
    )

    relationships_trafaret = t.Dict(
        {
            t.Key("dataset1_identifier", optional=True): t.String | t.Null,
            t.Key("dataset2_identifier"): t.String,
            t.Key("dataset1_keys"): t.List(t.String, min_length=1, max_length=10),
            t.Key("dataset2_keys"): t.List(t.String, min_length=1, max_length=10),
            t.Key("feature_derivation_window_start", optional=True): t.Int(lt=0),
            t.Key("feature_derivation_window_end", optional=True): t.Int(lte=0),
            t.Key(
                "feature_derivation_window_time_unit", optional=True
            ): AllowedTimeUnitsSAFER.ALL,
            t.Key("prediction_point_rounding", optional=True): t.Int(gt=0, lte=30),
            t.Key(
                "prediction_point_rounding_time_unit", optional=True
            ): AllowedTimeUnitsSAFER.ALL,
        }
    )
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("dataset_definitions"): t.List(
                dataset_definitions_trafaret, min_length=1
            ),
            t.Key("relationships"): t.List(relationships_trafaret, min_length=1),
        }
    ).ignore_extra("*")

    def __init__(self, id, dataset_definitions=None, relationships=None):
        self.id = id
        self.dataset_definitions = dataset_definitions
        self.relationships = relationships

    def __repr__(self):
        return encode_utf8_if_py2(u"{}()".format(self.__class__.__name__))

    @classmethod
    def create(cls, dataset_definitions, relationships):
        """ Create a Relationships Configuration

        Parameters
        ----------
        dataset_definitions: list of dict
            each element is a DatasetDefinition .
            The `DatasetDefinition` schema is

            identifier: str
                alias of the table (used directly as part of the generated feature names)
            catalog_id: str, or None
                identifier of the catalog item
            catalog_version_id: str
                identifier of the catalog item version
            feature_list_id: str, or None
                identifier of the feature list. This decides which columns in the table are
                used for feature generation
            snapshot_policy: str
                policy to use  when creating a project or making predictions.
                Must be one of the following values:
                'specified': Use specific snapshot specified by catalogVersionId
                'latest': Use latest snapshot from the same catalog item
                'dynamic': Get data from the source (only applicable for JDBC datasets)
        relationships: list of dict
            each element is a Relationship between two datasets
            The `Relationship` schema is

            dataset1_identifier: str or None
                identifier of the first dataset in this relationship.
                This is specified in the indentifier field of dataset_definition structure.
                If None, then the relationship is with the primary dataset.
            dataset2_identifier: str
                identifier of the second dataset in this relationship.
                This is specified in the identifier field of dataset_definition schema.
            dataset1_keys: list of str (max length: 10 min length: 1)
                column(s) from the first dataset which are used to join to the second dataset
            dataset2_keys: list of str (max length: 10 min length: 1)
                column(s) from the second dataset that are used to join to the first dataset
            time_unit: str, or None
                time unit of the feature derivation window. Supported
                values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
                If present, the feature engineering Graph will perform time-aware joins.
            feature_derivation_window_start: int, or None
                how many time_units of each dataset's primary temporal key into the past relative
                to the datetimePartitionColumn the feature derivation window should begin.
                Will be a negative integer,
                If present, the feature engineering Graph will perform time-aware joins.
            feature_derivation_window_end: int, or None
                how many timeUnits of each dataset's record
                primary temporal key into the past relative to the datetimePartitionColumn the
                feature derivation window should end.  Will be a non-positive integer, if present.
                If present, the feature engineering Graph will perform time-aware joins.
            feature_derivation_window_time_unit: int or None
                time unit of the feature derivation window. Supported values are
                MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
                If present, time-aware joins will be used.
                Only applicable when dataset1Identifier is not provided.
            prediction_point_rounding: int, or None
                closest value of prediction_point_rounding_time_unit to round the prediction point
                into the past when applying the feature derivation window. Will be a positive
                integer, if present.Only applicable when dataset1_identifier is not provided.
            prediction_point_rounding_time_unit: str, or None
                time unit of the prediction point rounding. Supported values are
                MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
                Only applicable when dataset1_identifier is not provided.

        Returns
        -------
        relationships_configuration: RelationshipsConfiguration
            the created relationships configuration
        """
        payload_data = {
            "dataset_definitions": dataset_definitions,
            "relationships": relationships,
        }
        response = cls._client.post(cls._path, data=payload_data).json()
        return RelationshipsConfiguration.from_server_data(response)

    def get(self):
        """ Retrieve the Relationships configuration for a given id

        Returns
        -------
        relationships_configuration: RelationshipsConfiguration
            The requested relationships configuration

        Raises
        ------
        ClientError
            Raised if an invalid relationships config id is provided.

        Examples
        --------
        .. code-block:: python

            relationships_config = dr.RelationshipsConfiguration(valid_config_id)
            result = relationships_config.get()
            >>> result.id
            '5c88a37770fc42a2fcc62759'
        """
        return self.from_location("{}{}/".format(self._path, self.id))

    def replace(self, dataset_definitions, relationships):
        """ Update the Relationships Configuration which is not used in
        the feature discovery Project

        Parameters
        ----------
        dataset_definitions: list of dict
            each element is a DatasetDefinition .
            The `DatasetDefinition` schema is

            identifier: str
                alias of the table (used directly as part of the generated feature names)
            catalog_id: str, or None
                identifier of the catalog item
            catalog_version_id: str
                identifier of the catalog item version
            feature_list_id: str, or None
                identifier of the feature list. This decides which columns in the table are
                used for feature generation
            snapshot_policy: str
                policy to use  when creating a project or making predictions.
                Must be one of the following values:
                'specified': Use specific snapshot specified by catalogVersionId
                'latest': Use latest snapshot from the same catalog item
                'dynamic': Get data from the source (only applicable for JDBC datasets)
        relationships: list of dict
            each element is a Relationship between two datasets
            The `Relationship` schema is

            dataset1_identifier: str or None
                identifier of the first dataset in this relationship.
                This is specified in the indentifier field of dataset_definition structure.
                If None, then the relationship is with the primary dataset.
            dataset2_identifier: str
                identifier of the second dataset in this relationship.
                This is specified in the identifier field of dataset_definition schema.
            dataset1_keys: list of str (max length: 10 min length: 1)
                column(s) from the first dataset which are used to join to the second dataset
            dataset2_keys: list of str (max length: 10 min length: 1)
                column(s) from the second dataset that are used to join to the first dataset
            time_unit: str, or None
                time unit of the feature derivation window. Supported
                values are MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
                If present, the feature engineering Graph will perform time-aware joins.
            feature_derivation_window_start: int, or None
                how many time_units of each dataset's primary temporal key into the past relative
                to the datetimePartitionColumn the feature derivation window should begin.
                Will be a negative integer,
                If present, the feature engineering Graph will perform time-aware joins.
            feature_derivation_window_end: int, or None
                how many timeUnits of each dataset's record
                primary temporal key into the past relative to the datetimePartitionColumn the
                feature derivation window should end.  Will be a non-positive integer, if present.
                If present, the feature engineering Graph will perform time-aware joins.
            feature_derivation_window_time_unit: int or None
                time unit of the feature derivation window. Supported values are
                MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
                If present, time-aware joins will be used.
                Only applicable when dataset1Identifier is not provided.
            prediction_point_rounding: int, or None
                closest value of prediction_point_rounding_time_unit to round the prediction point
                into the past when applying the feature derivation window. Will be a positive
                integer, if present.Only applicable when dataset1_identifier is not provided.
            prediction_point_rounding_time_unit: str, or None
                time unit of the prediction point rounding. Supported values are
                MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
                Only applicable when dataset1_identifier is not provided.

        Returns
        -------
        relationships_configuration: RelationshipsConfiguration
            the updated relationships configuration
        """
        payload_data = {
            "datasetDefinitions": dataset_definitions,
            "relationships": relationships,
        }
        url = '{}{}/'.format(self._path, self.id)
        response = self._client.put(url, json=payload_data).json()
        return RelationshipsConfiguration.from_server_data(response)

    def delete(self):
        """
        Delete the Relationships configuration

        Raises
        ------
        ClientError
            Raised if an invalid relationships config id is provided.

        Examples
        --------
        .. code-block:: python

            # Deleting with a valid id
            relationships_config = dr.RelationshipsConfiguration(valid_config_id)
            status_code = relationships_config.delete()
            status_code
            >>> 204
            relationships_config.get()
            >>> ClientError: Relationships Configuration not found
        """
        self._client.delete('{}{}/'.format(self._path, self.id))
