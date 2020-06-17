import six
import trafaret as t

from datarobot import errors
from datarobot.models.api_object import APIObject


class SecondaryDataset(object):
    """A secondary dataset to be used for feature discovery

    .. versionadded:: v2.20

    Attributes
    ----------
    identifier: str
        a short name of this secondary dataset (will be used as part of the generated feature names)
    catalog_id: str
        catalog Id of the secondary dataset
    catalog_version_id: str
        catalog version Id of the secondary dataset
    snapshot_policy: str (default: `latest`)
        policy to be used by the secondary dataset when making predictions
        Must be one of the following values:
            'specified': Use specific snapshot specified by catalogVersionId
            'latest': Use latest snapshot from the same catalog item
            'dynamic': Get data from the source (only applicable for JDBC datasets)
    """

    def __init__(
        self, identifier, catalog_id, catalog_version_id, snapshot_policy='latest'
    ):
        self.identifier = identifier
        self.catalog_id = catalog_id
        self.catalog_version_id = catalog_version_id
        self.snapshot_policy = snapshot_policy

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'catalogId': self.catalog_id,
            'catalogVersionId': self.catalog_version_id,
            'snapshotPolicy': self.snapshot_policy,
        }


class DatasetConfiguration(object):
    """Specify a dataset configuration

    .. versionadded:: v2.20

    Attributes
    ----------
    feature_engineering_graph_id: str
        id of the feature engineering graph
    secondary_datasets: list of SecondaryDataset
        list of secondary datasets

    """

    def __init__(self, feature_engineering_graph_id=None, secondary_datasets=None):
        self.feature_engineering_graph_id = feature_engineering_graph_id
        self.secondary_datasets = secondary_datasets

    def to_dict(self):
        return {
            'featureEngineeringGraphId': self.feature_engineering_graph_id,
            'secondaryDatasets': [dataset.to_dict() for dataset in self.secondary_datasets],
        }


class SecondaryDatasetConfigurations(APIObject):
    """ Create secondary dataset configurations for a given project

    .. versionadded:: v2.20

    Attributes
    ----------
    id : str
        id of this secondary dataset configuration
    project_id : str
        id of the associated project.
    config: list of DatasetConfiguration
        list of secondary dataset configurations
    """

    _base_url = 'projects/{}/secondaryDatasetsConfigurations/'
    _secondary_dataset_converter = t.Dict(
        {
            t.Key('identifier'): t.String(min_length=3, max_length=20),
            t.Key('catalog_version_id'): t.String,
            t.Key('catalog_id'): t.String,
            t.Key('snapshot_policy', optional=True, default='latest'): t.Enum(
                'latest', 'specified', 'dynamic')
        }
    )

    _dataset_configuration_converter = t.Dict(
        {
            t.Key('feature_engineering_graph_id'): t.String(),
            t.Key('secondary_datasets'): t.List(_secondary_dataset_converter),
        }
    ).ignore_extra('*')

    _converter = t.Dict(
        {
            t.Key('id'): t.String(),
            t.Key('project_id'): t.String(),
            t.Key('config'): t.List(_dataset_configuration_converter),
        }
    ).ignore_extra('*')

    def __init__(self, id=None, project_id=None, config=None):
        self.id = id
        self.project_id = project_id
        self.config = config

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'config': [c.to_dict() for c in self.config],
        }

    @classmethod
    def from_data(cls, data):
        checked = cls._converter.check(data)
        safe_data = cls._filter_data(checked)

        id = safe_data.get('id', None)
        project_id = safe_data.get('project_id', None)
        dataset_configs = safe_data.get('config', None)
        conf_list = []
        for conf in dataset_configs:
            graph_id = conf.get('feature_engineering_graph_id', None)
            datasets = conf.get('secondary_datasets', None)
            dataset_list = []
            for d in datasets:
                dataset = SecondaryDataset(**d)
                dataset_list.append(dataset)
            dataset_configuration = DatasetConfiguration(graph_id, dataset_list)
            conf_list.append(dataset_configuration)
        return SecondaryDatasetConfigurations(id, project_id, conf_list)

    @classmethod
    def create(cls, project_id, dataset_configurations):
        """ create secondary dataset configurations

        .. versionadded:: v2.20

        Parameters
        ----------
        project_id : str
            id of the associated project.
        dataset_configurations: list of DatasetConfiguration
            list of dataset configurations

        Returns
        -------
        an instance of SecondaryDatasetConfigurations

        Raises
        ------
        ClientError
            raised if incorrect configuration parameters are provided
        """
        if not project_id:
            raise errors.ClientError(six.text_type('project_id cannot be None or empty'), 422)
        if not dataset_configurations:
            raise errors.ClientError(
                six.text_type('dataset_configurations cannot be None or empty'),
                422,
            )

        url = cls._base_url.format(project_id)
        payload = {'conf': [conf.to_dict() for conf in dataset_configurations]}
        response = cls._client.post(url, data=payload)

        status = response.status_code
        if status == 201:
            return cls.from_server_data(response.json())
        else:
            error_msg = response.json().get(
                'message', six.text_type('error in processing secondary dataset configuration')
            )
            raise errors.ClientError(
                error_msg + six.text_type(' with server returned status {}').format(status),
                status,
            )

    def delete(self):
        """ Removes the Secondary datasets configuration

        .. versionadded:: v2.21

        Raises
        ------
        ClientError
            Raised if an invalid or already deleted secondary dataset config id is provided

        Examples
        --------
        .. code-block:: python

            # Deleting with a valid secondary_dataset_config id
            status_code = dr.SecondaryDatasetConfigurations.delete(some_config_id)
            status_code
            >>> 204
        """
        url = self._base_url.format(self.project_id)
        self._client.delete('{}{}/'.format(url, self.id))

    def get(self):
        """ Retrieve a single secondary dataset configuration for a given id

        .. versionadded:: v2.21

        Returns
        -------
        secondary_dataset_configurations : SecondaryDatasetConfigurations
            The requested secondary dataset configurations
        """
        url = self._base_url.format(self.project_id)
        return self.from_location('{}{}/'.format(url, self.id))
