import io
import uuid
from copy import deepcopy
from typing import Union, Tuple, List

import requests
from ibm_boto3 import resource
from pandas import DataFrame
from watson_machine_learning_client.utils.autoai.enums import PredictionType, DataConnectionTypes
from watson_machine_learning_client.utils.autoai.errors import (
    MissingAutoPipelinesParameters, UseWMLClient, MissingCOSStudioConnection, MissingProjectLib,
    HoldoutSplitNotSupported, InvalidCOSCredentials
)
from watson_machine_learning_client.utils.autoai.utils import try_load_dataset
from watson_machine_learning_client.wml_client_error import ApiRequestFailure

from .base_connection import BaseConnection
from .base_data_connection import BaseDataConnection
from .base_location import BaseLocation

__all__ = [
    "DataConnection",
    "S3Connection",
    "S3Location",
    "FSLocation",
    "DSLocation"
]


# TODO: read/write support only for small files, need to implement large files support
class DataConnection(BaseDataConnection):
    """
    Data Storage Connection class needed for WML training metadata (input data).

    Parameters
    ----------
    connection: Union[S3Connection], required
        connection parameters of specific type

    location: Union[S3Location], required
        location parameters of specific type
    """

    def __init__(self,
                 location: Union['S3Location', 'FSLocation', 'DSLocation'],
                 connection: Union['S3Connection'] = None):

        if isinstance(connection, S3Connection):
            self.type = DataConnectionTypes.S3

        elif isinstance(location, FSLocation):
            self.type = DataConnectionTypes.FS

        elif isinstance(location, DSLocation):
            self.type = DataConnectionTypes.DS

        self.connection = connection
        self.location = location

        self.auto_pipeline_params = None  # note: needed parameters for recreation of autoai holdout split
        self._wml_client = None
        self._run_id = None

    @classmethod
    def from_studio(cls, path: str) -> List['DataConnection']:
        """
        Create DataConnections from the credentials stored (connected) in Watson Studio. Only for COS.

        Parameters
        ----------
        path: str, required
            Path in COS bucket to the training dataset.

        Returns
        -------
        List with DataConnection objects.

        Example
        -------
        >>> data_connections = DataConnection.from_studio(path='iris_dataset.csv')
        """
        try:
            from project_lib import Project

        except ModuleNotFoundError:
            raise MissingProjectLib("Missing project_lib package.")

        else:
            data_connections = []
            for name, value in globals().items():
                if isinstance(value, Project):
                    connections = value.get_connections()

                    if connections:
                        for connection in connections:
                            asset_id = connection['asset_id']
                            connection_details = value.get_connection(asset_id)

                            if ('url' in connection_details and 'access_key' in connection_details and
                                    'secret_key' in connection_details and 'bucket' in connection_details):
                                data_connections.append(
                                    cls(connection=S3Connection(endpoint_url=connection_details['url'],
                                                                access_key_id=connection_details['access_key'],
                                                                secret_access_key=connection_details['secret_key']),
                                        location=S3Location(bucket=connection_details['bucket'],
                                                            path=path))
                                )

            if data_connections:
                return data_connections

            else:
                raise MissingCOSStudioConnection(
                    "There is no any COS Studio connection. "
                    "Please create a COS connection from the UI and insert "
                    "the cell with project API connection (Insert project token)")

    def _to_dict(self) -> dict:
        """
        Convert DataConnection object to dictionary representation.

        Returns
        -------
        Dictionary
        """
        _dict = {"type": self.type}

        if self.connection is not None:
            _dict['connection'] = deepcopy(self.connection.to_dict())

        else:
            _dict['connection'] = {}

        _dict['location'] = deepcopy(self.location.to_dict())
        return _dict

    def __repr__(self):
        return str(self._to_dict())

    def __str__(self):
        return str(self._to_dict())

    @classmethod
    def _from_dict(cls, _dict: dict) -> 'DataConnection':
        """
        Create a DataConnection object from dictionary

        Parameters
        ----------
        _dict: dict, required
            A dictionary data structure with information about data connection reference.

        Returns
        -------
        DataConnection
        """
        if _dict['type'] == DataConnectionTypes.S3:
            data_connection: 'DataConnection' = cls(
                connection=S3Connection(
                    access_key_id=_dict['connection']['access_key_id'],
                    secret_access_key=_dict['connection']['secret_access_key'],
                    endpoint_url=_dict['connection']['endpoint_url']
                ),
                location=S3Location(
                    bucket=_dict['location']['bucket'],
                    path=_dict['location']['path']
                )
            )
        elif _dict['type'] == DataConnectionTypes.FS:
            data_connection: 'DataConnection' = cls(
                location=FSLocation._set_path(path=_dict['location']['path'])
            )

        else:
            data_connection: 'DataConnection' = cls(
                location=DSLocation._set_path(href=_dict['location']['href'])
            )

        return data_connection

    def _fill_experiment_parameters(self, prediction_type: str, prediction_column: str, test_size: float,
                                    csv_separator: str = ',', excel_sheet: Union[str, int] = 0) -> None:
        """
        To be able to recreate a holdout split, this method need to be called.
        """
        self.auto_pipeline_params = {
            'prediction_type': prediction_type,
            'prediction_column': prediction_column,
            'test_size': test_size,
            'csv_separator': csv_separator,
            'excel_sheet': excel_sheet
        }

    def read(self, with_holdout_split: bool = False) -> Union['DataFrame', Tuple['DataFrame', 'DataFrame']]:
        """
        Download dataset stored in remote data storage.

        Parameters
        ----------
        with_holdout_split: bool, optional
            If True, data will be split to train and holdout dataset as it was by AutoAI.

        Returns
        -------
        pandas.DataFrame contains dataset from remote data storage or Tuple[pandas.DataFrame, pandas.DataFrame]
            containing training data and holdout data from remote storage
            (only if only_holdout == True and auto_pipeline_params was passed)
        """

        from sklearn.model_selection import train_test_split

        if with_holdout_split and self.auto_pipeline_params is None:
            raise MissingAutoPipelinesParameters(
                self.auto_pipeline_params,
                reason=f"To be able to recreate an original holdout split, you need to schedule a training job or "
                       f"if you are using historical runs, just call historical_optimizer.get_data_connections()")

        data = DataFrame()
        if self.type == DataConnectionTypes.S3:
            cos_client = self._init_cos_client()

            try:
                file = cos_client.Object(self.location.bucket,
                                         self.location.path).get()
                buffer = io.BytesIO(file['Body'].read())
                data = try_load_dataset(buffer=buffer,
                                        sheet_name=self.auto_pipeline_params.get('excel_sheet', 0),
                                        separator=self.auto_pipeline_params.get('csv_separator', ','))

            except Exception as cos_access_exception:
                raise ConnectionError(
                    f"Unable to access data object in cloud object storage with credentials supplied. "
                    f"Error: {cos_access_exception}")

        elif self.type == DataConnectionTypes.DS:
            # note: as we need to load a data into the memory,
            # we are using pure requests and helpers from the WML client
            asset_id = self.location.href.split('?')[0].split('/')[-1]

            # note: download data asset details
            asset_response = requests.get(self._wml_client.data_assets._href_definitions.get_data_asset_href(asset_id),
                                          params=self._wml_client._params(),
                                          headers=self._wml_client._get_headers(),
                                          verify=False)

            asset_details = self._wml_client.data_assets._handle_response(200, u'get assets', asset_response)

            # note: read the csv url
            attachment_url = asset_details['attachments'][0]['handle']['key']

            # note: make the whole url pointing out the csv
            artifact_content_url = (f"{self._wml_client.data_assets._href_definitions.get_wsd_model_attachment_href()}"
                                    f"{attachment_url}")

            # note: stream the whole CSV file
            csv_response = requests.get(artifact_content_url,
                                        params=self._wml_client._params(),
                                        headers=self._wml_client._get_headers(),
                                        stream=True,
                                        verify=False)

            if csv_response.status_code != 200:
                raise ApiRequestFailure(u'Failure during {}.'.format("downloading model"), csv_response)

            downloaded_asset = csv_response.content

            # note: read the csv/xlsx file from the memory directly into the pandas DataFrame
            buffer = io.BytesIO(downloaded_asset)
            data = try_load_dataset(buffer=buffer,
                                    sheet_name=self.auto_pipeline_params.get('excel_sheet', 0),
                                    separator=self.auto_pipeline_params.get('csv_separator', ','))

        if isinstance(data, DataFrame) and 'Unnamed: 0' in data.columns.tolist():
            data.drop(['Unnamed: 0'], axis=1, inplace=True)

        if with_holdout_split:
            if not isinstance(data, DataFrame):
                raise HoldoutSplitNotSupported(
                    None,
                    reason="SDK currently does not support a local holdout split with xlsx files without sheet_name "
                           "provided.")

            if self.auto_pipeline_params.get('train_sample_rows_test_size'):
                pass

            # note: 'classification' check left for backward compatibility
            if (self.auto_pipeline_params['prediction_type'] == PredictionType.BINARY
                    or self.auto_pipeline_params['prediction_type'] == PredictionType.MULTICLASS
                    or self.auto_pipeline_params['prediction_type'] == 'classification'):
                x, x_holdout, y, y_holdout = train_test_split(
                    data.drop([self.auto_pipeline_params['prediction_column']], axis=1),
                    data[self.auto_pipeline_params['prediction_column']].values,
                    test_size=self.auto_pipeline_params['test_size'],
                    random_state=33,
                    stratify=data[self.auto_pipeline_params['prediction_column']].values)
            else:
                x, x_holdout, y, y_holdout = train_test_split(
                    data.drop([self.auto_pipeline_params['prediction_column']], axis=1),
                    data[self.auto_pipeline_params['prediction_column']].values,
                    test_size=self.auto_pipeline_params['test_size'],
                    random_state=33)

            data_train = DataFrame(data=x, columns=data.columns.tolist())
            data_train[self.auto_pipeline_params['prediction_column']] = y

            data_holdout = DataFrame(data=x_holdout, columns=data.columns.tolist())
            data_holdout[self.auto_pipeline_params['prediction_column']] = y_holdout

            return data_train, data_holdout

        return data

    def write(self, data: Union[str, 'DataFrame'], remote_name: str) -> None:
        """
        Upload file to a remote data storage.

        Parameters
        ----------
        data: str, required
            Local path to the dataset or pandas.DataFrame with data.

        remote_name: str, required
            Name that dataset should be stored with in remote data storage.
        """
        if self.type == DataConnectionTypes.S3:
            cos_resource_client = self._init_cos_client()
            if isinstance(data, str):
                with open(data, "rb") as file_data:
                    cos_resource_client.Object(self.location.bucket, remote_name).upload_fileobj(
                        Fileobj=file_data)

            elif isinstance(data, DataFrame):
                # note: we are saving csv in memory as a file and stream it to the COS
                buffer = io.StringIO()
                data.to_csv(buffer, index=False)
                buffer.seek(0)

                with buffer as f:
                    cos_resource_client.Object(self.location.bucket, remote_name).upload_fileobj(
                        Fileobj=io.BytesIO(bytes(f.read().encode())))

            else:
                raise TypeError("data should be either of type \"str\" or \"pandas.DataFrame\"")

        elif self.type == DataConnectionTypes.DS:
            raise UseWMLClient('DataConnection.write()',
                               reason="If you want to upload any data to CP4D instance, "
                                      "firstly please get the WML client by calling "
                                      "\"client = WMLInstance().get_client()\" "
                                      "then call the method: \"client.data_asset.create()\"")

    def _init_cos_client(self) -> 'resource':
        """Initiate COS client for further usage."""
        from ibm_botocore.client import Config
        if hasattr(self.connection, 'auth_endpoint') and hasattr(self.connection, 'api_key'):
            cos_client = resource(
                service_name='s3',
                ibm_api_key_id=self.connection.api_key,
                ibm_auth_endpoint=self.connection.auth_endpoint,
                config=Config(signature_version="oauth"),
                endpoint_url=self.connection.endpoint_url
            )

        else:
            cos_client = resource(
                service_name='s3',
                endpoint_url=self.connection.endpoint_url,
                aws_access_key_id=self.connection.access_key_id,
                aws_secret_access_key=self.connection.secret_access_key
            )
        return cos_client


class S3Connection(BaseConnection):
    """
    Connection class to COS data storage in S3 format.

    Parameters
    ----------
    endpoint_url: str, required
        S3 data storage url (COS)

    access_key_id: str, optional
        access_key_id of the S3 connection (COS)

    secret_access_key: str, optional
        secret_access_key of the S3 connection (COS)

    api_key: str, optional
        API key of the S3 connection (COS)

    service_name: str, optional
        Service name of the S3 connection (COS)

    auth_endpoint: str, optional
        Authentication endpoint url of the S3 connection (COS)
    """

    def __init__(self, endpoint_url: str, access_key_id: str = None, secret_access_key: str = None,
                 api_key: str = None, service_name: str = None, auth_endpoint: str = None) -> None:
        self.endpoint_url = endpoint_url
        self.access_key_id = access_key_id

        if (access_key_id is None or secret_access_key is None) and (api_key is None or auth_endpoint is None):
            raise InvalidCOSCredentials(reason='You need to specify (access_key_id and secret_access_key) or'
                                               '(api_key and auth_endpoint)')

        if secret_access_key is not None:
            self.secret_access_key = secret_access_key

        if api_key is not None:
            self.api_key = api_key

        if service_name is not None:
            self.service_name = service_name

        if auth_endpoint is not None:
            self.auth_endpoint = auth_endpoint


class S3Location(BaseLocation):
    """
    Connection class to COS data storage in S3 format.

    Parameters
    ----------
    bucket: str, required
        COS bucket name

    path: str, required
        COS data path in the bucket

    model_location: str, optional
        Path to the pipeline model in the COS.

    training_status: str, optional
        Path t the training status json in COS.
    """

    def __init__(self, bucket: str, path: str, **kwargs) -> None:
        self.bucket = bucket
        self.path = path

        if kwargs.get('model_location') is not None:
            self._model_location = kwargs['model_location']

        if kwargs.get('training_status') is not None:
            self._training_status = kwargs['training_status']


class FSLocation(BaseLocation):
    """
    Connection class to File Storage in CP4D.
    """

    def __init__(self) -> None:
        self.path = "{option}/{id}" + f"/assets/auto_ml/autoai_sdk_{uuid.uuid4()}/wml_data"

    @classmethod
    def _set_path(cls, path: str) -> 'FSLocation':
        location = cls()
        location.path = path
        return location


class DSLocation(BaseLocation):
    """
    Connection class to data assets in CP4D.

    Parameters
    ----------
    asset_id: str, required
        Asset ID from the project on CP4D.
    """

    def __init__(self, asset_id: str) -> None:
        self.href = f'/v2/assets/{asset_id}?' + '{option}' + '=' + '{id}'

    @classmethod
    def _set_path(cls, href: str) -> 'DSLocation':
        location = cls('.')
        location.href = href
        return location
