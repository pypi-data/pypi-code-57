import json
import os
import textwrap
import uuid
import warnings
import pandas
import pyarrow
import boto3

from typing import List
from urllib.parse import urljoin
from tabulate import tabulate
from s3transfer.manager import TransferManager

from dli.aws import create_refreshing_session
from dli.models import log_public_functions_calls_using, SampleData, \
    AttributesDict
from dli.client.aspects import analytics_decorator, logging_decorator
from dli.client.components.urls import consumption_urls, dataset_urls
from dli.client.exceptions import DataframeStreamingException, \
    UnAuthorisedAccessException
from dli.models.dictionary_model import DictionaryModel
from dli.models.file_model import get_or_create_os_path


@log_public_functions_calls_using(
    [analytics_decorator, logging_decorator], class_fields_to_log=['dataset_id']
)
class DatasetModel(AttributesDict):

    @property
    def sample_data(self):
        return SampleData(self)

    @property
    def id(self):
        return self.dataset_id

    def __init__(self, **kwargs):
        super().__init__(**kwargs,)
        self.instances = self._client._InstancesCollection(dataset=self)
        self.fields_metadata = None

    @classmethod
    def _from_v2_response(cls, response_json):
        return cls._construct_dataset_using(
            response_json['data']['attributes'], response_json['data']['id']
        )

    @classmethod
    def _from_v2_response_unsheathed(cls, response_json):
        return cls._construct_dataset_using(
            response_json['attributes'], response_json['id']
        )

    @classmethod
    def _from_v1_response_to_v2(cls, v1_response):
        response = cls._client.session.get(
            dataset_urls.v2_by_id.format(
                id=v1_response['properties']['datasetId']
            )
        )

        return cls._from_v2_response(response.json())

    @classmethod
    def _from_v2_list_response(cls, response_json):
        return [
            cls._construct_dataset_using(
                dataset['attributes'], dataset['id']
            )
            for dataset in response_json['data']
        ]

    @classmethod
    def _construct_dataset_using(cls, attributes, dataset_id):
        location = attributes.pop('location')
        # In the interests of not breaking backwards compatability.
        # TODO find a way to migrate this to the new nested API.
        if not location:
            location = None
        else:
            location = location[next(iter(location))]
        return cls(
            **attributes,
            location=location,
            dataset_id=dataset_id
        )

    def download(self, destination_path, flatten=False, filter_path=None):
        """
        Downloads all files from the latest instance into the provided
        destination path.
        This is a short-cut function for:
        `Dataset.instances.latest().download(destination_path)`

        :param destination_path: required. The path on the system, where the
            files should be saved. Must be a directory, if doesn't exist, will
            be created.

        :param bool flatten: The default behaviour (=False) is to use the s3
            file structure when writing the downloaded files to disk. Example:
            [
              'storm/climate/storm_data/storm_fatalities/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
              'storm/climate/storm_data/storm_fatalities/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
            ]

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:
            [
              './storm-flattened/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
              './storm-flattened/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
            ]

        :return: the list of the downloaded files
        """

        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

        s3_resource = create_refreshing_session(
            dli_client_session=self._client.session
        ).resource(
            's3',
            endpoint_url=f'https://{self._client._environment.s3_proxy}'
        )

        s3_client = s3_resource.meta.client

        with TransferManager(s3_client) as transfer_manager:

            bucket = s3_resource.Bucket(
                self.organisation_short_code
            )

            _paths = []

            filter_prefix = self.short_code + (
                    '' if self.short_code.endswith('/') else '/'
            )

            if filter_path:
                filter_prefix = filter_prefix + filter_path.lstrip('/')

            # TODO parallelize this again?
            for object_summary in bucket.objects.filter(
                # Prefix searches for exact matches and folders
                Prefix=filter_prefix
            ):
                if not object_summary.key.endswith('/'):
                    to_path = get_or_create_os_path(
                        object_summary.key,
                        to=destination_path,
                        flatten=flatten
                    )

                    print(f'Downloading {object_summary.key} to: {to_path}...')

                    if os.path.exists(to_path):
                        warnings.warn(
                            'File already exists. Overwriting.'
                        )

                    # returns a future
                    transfer_manager.download(
                        self.organisation_short_code,
                        object_summary.key,
                        to_path
                    )

                    _paths.append(to_path)

            return _paths

    def _dataframe(self, nrows=None, partitions: List[str] = None, raise_=True):
        warnings.warn(
            'This method is deprecated. Please use `dataframe` (note the '
            'underscore has been removed)',
            DeprecationWarning
        )
        self.dataframe(nrows=nrows, partitions=partitions, raise_=raise_)

    def dataframe(self, nrows=None, partitions: List[str] = None, raise_=True):
        """
        Return the data from the files in the latest instance of the dataset
        as a pandas DataFrame.

        We currently support .csv and .parquet as our data file formats. The
        data files in the latest instance could all be .csv format or all be
        .parquet format. If there is a mix of .csv and .parquet or some other
        file format then we will not be able to parse the data and will
        return an error message.

        :param int nrows: Optional. The max number of rows to return.
            We use the nrows parameter to limit the amount of rows that are
            returned, otherwise for very large dataset it will take a long time
            or you could run out of RAM on your machine!
            If you want all of the rows, then leave this parameter set to the
            default None.

        :param List[str] partitions: Optional. A dict of filters (partitions) to
            apply to the dataframe request in the form of: ["a=12","b>20190110"]
            - will permit whitespace and equality operators [<=, <, =, >, >=]

        :param bool raise_: Optional. Raise exception if the dataframe stream
            stopped prematurely

        :returns: Pandas DataFrame.
        :rtype: pandas.DataFrame
        """

        if not self.has_access:
            raise Exception(
                'Unfortunately the user you are using '
                'does not have access to this dataset. '
                'Please request access to the package/dataset '
                "to be able to retrieve this content."
            )

        params = {}

        if nrows is not None:
            params['filter[nrows]'] = nrows

        if partitions is not None:
            params['filter[partitions]'] = partitions

        dataframe_url = urljoin(
            self._client._environment.consumption,
            consumption_urls.consumption_dataframe.format(id=self.id)
        )

        # Generate request_id on the SDK side for use in Consumption log
        # messages. This is useful for debugging what seems like a success
        # (no exception) but is not what the user wanted e.g. not the data
        # they expected.
        request_id = str(uuid.uuid1())

        tracing = os.environ.get('DLI_TRACE', '')
        if tracing and tracing.lower() == 'true':
            print(f"DEBUG: Your REQUEST ID is {request_id}")

        response = self._client.session.get(
            dataframe_url, stream=True,
            params=params,
            headers={'X-Request-ID': request_id},
        )

        # Don't decode content. We would like to keep the raw
        # probably gziped steam. Otherwise the stream.read(n) will
        # return a string of length != n.
        response.raw.decode_content = False

        native_file = pyarrow.PythonFile(response.raw, mode='rb')

        # If the response is gzip we need to wrap the
        # encoding in a decompressor.
        if 'Content-Encoding' in response.headers:
            if response.headers['Content-Encoding'] == 'gzip':
                native_file = pyarrow.CompressedInputStream(
                    native_file, 'gzip'
                )

        reader = pyarrow.ipc.open_stream(native_file)
        dataframe = reader.read_pandas()

        # The pyarrow buffered stream reader stops once it
        # reaches the end of the IPC message. Afterwards we
        # get the rest of the data which contains the summary
        # of what we've downloaded including an error message.
        summary_string = native_file.read()
        if summary_string:
            summary = json.loads(summary_string)

            if summary['status'] >= 400:
                exception = DataframeStreamingException(
                    summary, dataframe_url, response=response,
                )

                # Optionally ignore bad data
                if raise_:
                    raise exception
                else:
                    warnings.warn(
                        str(exception),
                        UserWarning
                    )

        return dataframe

    def _partitions(self):
        warnings.warn(
            'This method is deprecated. Please use `partitions` (note the '
            'underscore has been removed)',
            DeprecationWarning
        )
        self.partitions()

    def partitions(self):
        """
        Retrieves the list of available partitions for a given dataset.

        The data onboarding team have structured the file paths on S3 with
        simple partitions e.g. `as_of_date` or `location`.

        Their aim was to separate the data to reduce the size of the
        individual files. For example, data that has a `location` column with
        the options `us`, `eu` and `asia` can be separated into S3 paths like
        so:

            package-name/dataset/as_of_date=2019-09-10/location=eu/filename.csv
            package-name/dataset/as_of_date=2019-09-10/location=us/filename.csv

        in this case the `partitions` will be returned as:

            {'as_of_date': ['2019-09-10'], 'location': ['eu', 'us]}
        """
        response = self._client.session.get(
            urljoin(
                self._client._environment.consumption,
                consumption_urls.consumption_partitions.format(id=self.id)
            )
        )

        return response.json()["data"]["attributes"]["partitions"]

    def contents(self):
        """
        Print IDs for all the instances in this dataset.

        Example output:

            INSTANCE 1111aaa-11aa-11aa-11aa-111111aaaaaa
        """
        for p in self.instances.all():
            print(str(p))

    def dictionary(self) -> List[dict]:

        if self.fields_metadata is None:
            # we have to do two calls
            # to get the latest dictionary id for the dataset
            try:
                response = self._client.session.get(
                    dataset_urls.dictionary_by_dataset_lastest.format(id=self.id)
                ).json()
            except:
                print("There is no current dictionary available.")
                return []

            # followed by the fields for the dictionary...


            self.fields_metadata = DictionaryModel(
                {'id': response["data"]["id"], 'attributes': {}}, client=self._client
            ).fields

            def subdict(field_dict, keep):
                return{k: v for k, v in field_dict.items() if k in keep}

            self.fields_metadata = list(
                map(lambda field: subdict(field, ["name", "nullable", "type"]),
                    self.fields_metadata)
            )

        return self.fields_metadata

    def info(self):
        fields = self.dictionary()

        df = pandas.DataFrame(fields)
        if df.shape[1] > 0:
            df["type"] = df.apply(
                lambda row: row["type"] + (" (Nullable)" if row["nullable"] else ""),
                axis=1)
            df = df[["name", "type"]]

            print(tabulate(df, showindex=False, headers=df.columns))
        else:
            print("No columns/info available.")

    def __repr__(self):
        return f'<Dataset short_code={self.short_code}>'

    def __str__(self):
        separator = "-" * 80
        splits = "\n".join(textwrap.wrap(self.description))

        return f"\nDATASET \"{self.short_code}\" [{self.data_format}]\n" \
               f">> Shortcode: {self.short_code}\n"\
               f">> Available Date Range: {self.first_datafile_at} to {self.last_datafile_at}\n" \
               f">> ID: {self.id}\n" \
               f">> Published: {self.publishing_frequency} by {self.organisation_name}\n" \
               f">> Accessible: {self.has_access}\n" \
               f"\n" \
               f"{splits}\n" \
               f"{separator}"
