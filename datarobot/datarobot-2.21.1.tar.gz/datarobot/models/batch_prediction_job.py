import datetime
import threading
import time
import warnings

import trafaret as t

from datarobot import errors
from datarobot.models.job import AbstractSpecificJob
from datarobot.models.credential import Credential
from datarobot.utils import (
    get_id_from_response,
    recognize_sourcedata,
    pagination,
    to_api
)
from ..enums import JOB_TYPE, QUEUE_STATUS, AVAILABLE_STATEMENT_TYPES
from ..utils import parse_time


class BatchPredictionJob(AbstractSpecificJob):
    """
    A Batch Prediction Job is used to score large data sets on
    prediction servers using the Batch Prediction API.

    Attributes
    ----------
    id : str
        the id of the job
    """
    _job_spec = t.Dict({
        t.Key('num_concurrent'): t.Int(),
        t.Key('threshold_high', optional=True): t.Float(),
        t.Key('threshold_low', optional=True): t.Float(),
        t.Key('deployment_id'): t.String(),
        t.Key('passthrough_columns', optional=True): t.List(t.String(allow_blank=True)),
        t.Key('passthrough_columns_set', optional=True): t.String(),
        t.Key('max_explanations', optional=True): t.Int(),
        t.Key('prediction_warning_enabled', optional=True): t.Bool(),
        t.Key('intake_settings', optional=True): t.Dict().allow_extra("*"),
        t.Key('output_settings', optional=True): t.Dict().allow_extra("*"),
        t.Key('timeseries_settings', optional=True): t.Dict().allow_extra("*"),
    }).allow_extra('*')
    _links = t.Dict({
        t.Key('download', optional=True): t.String(allow_blank=True),
        t.Key('self'): t.String(),
    }).allow_extra('*')
    _converter_extra = t.Dict({
        t.Key('status'): t.String(),
        t.Key('percentage_completed'): t.Float(),
        t.Key('elapsed_time_sec'): t.Int(),
        t.Key('links'): _links,
        t.Key('job_spec'): _job_spec,
        t.Key('status_details'): t.String()
    }).allow_extra('*')

    _converter_common = t.Dict({
        t.Key('id', optional=True): t.String,
        t.Key('status', optional=True): t.Enum(
            QUEUE_STATUS.ABORTED,
            QUEUE_STATUS.COMPLETED,
            QUEUE_STATUS.ERROR,
            QUEUE_STATUS.INPROGRESS,
            QUEUE_STATUS.QUEUE,
            QUEUE_STATUS.RUNNING,
            QUEUE_STATUS.INITIALIZING),
        t.Key('project_id', optional=True): t.String,
        t.Key('is_blocked', optional=True): t.Bool,
    })

    _s3_settings = t.Dict({
        t.Key('url'): t.String(),
        t.Key('credential_id', optional=True): t.String(),
    })

    _jdbc_intake_settings = t.Dict({
        t.Key('data_store_id'): t.String(),
        t.Key('query', optional=True): t.String(),
        t.Key('table', optional=True): t.String(),
        t.Key('schema', optional=True): t.String(),
        t.Key('fetch_size', optional=True): t.Int(),
        t.Key('credential_id', optional=True): t.String(),
    })

    _jdbc_output_settings = t.Dict({
        t.Key('data_store_id'): t.String(),
        t.Key('table'): t.String(),
        t.Key('schema', optional=True): t.String(),
        t.Key('statement_type'): t.Enum(
            AVAILABLE_STATEMENT_TYPES.INSERT,
            AVAILABLE_STATEMENT_TYPES.UPDATE,
            AVAILABLE_STATEMENT_TYPES.INSERT_UPDATE,
            AVAILABLE_STATEMENT_TYPES.CREATE_TABLE
        ),
        t.Key('update_columns', optional=True): t.List(t.String),
        t.Key('where_columns', optional=True): t.List(t.String),
        t.Key('credential_id', optional=True): t.String(),
    })

    _timeseries_settings = t.Dict({
        t.Key('type'): t.Atom('forecast'),
        t.Key('forecast_point', optional=True): parse_time,
        t.Key('relax_known_in_advance_features_check', optional=True): t.Bool(),
    }) | t.Dict({
        t.Key('type'): t.Atom('historical'),
        t.Key('predictions_start_date', optional=True): parse_time,
        t.Key('predictions_end_date', optional=True): parse_time,
        t.Key('relax_known_in_advance_features_check', optional=True): t.Bool(),
    })

    _csv_settings = t.Dict({
        t.Key('delimiter', optional=True): t.Atom('tab') | t.String(min_length=1, max_length=1),
        t.Key('quotechar', optional=True): t.String(),
        t.Key('encoding', optional=True): t.String(),
    })

    _prediction_instance = t.Dict({
        t.Key('hostName'): t.String(),
        t.Key('sslEnabled', optional=True): t.Bool(),
        t.Key('datarobotKey', optional=True): t.String(),
        t.Key('apiKey', optional=True): t.String(),
    })

    _column_names_remapping = t.Mapping(t.String, t.String | t.Null())

    @classmethod
    def _job_type(cls):
        return JOB_TYPE.BATCH_PREDICTIONS

    @classmethod
    def _jobs_path(cls):
        return 'batchPredictions/'

    @classmethod
    def _job_path(cls, project_id, batch_prediction_job_id):
        return 'batchPredictions/{}/'.format(batch_prediction_job_id)

    @classmethod
    def _from_existing_path(cls):
        return 'batchPredictions/fromExisting/'

    @classmethod
    def score(
        cls,
        deployment,
        intake_settings=None,
        output_settings=None,
        csv_settings=None,
        timeseries_settings=None,
        num_concurrent=None,
        passthrough_columns=None,
        passthrough_columns_set=None,
        max_explanations=None,
        threshold_high=None,
        threshold_low=None,
        prediction_warning_enabled=None,
        include_prediction_status=False,
        skip_drift_tracking=False,
        prediction_instance=None,
        abort_on_error=True,
        column_names_remapping=None,
        include_probabilities=True,
        include_probabilities_classes=None,
    ):
        """
        Create new batch prediction job, upload the scoring dataset and
        return a batch prediction job.

        The default intake and output options are both `localFile` which
        requires the caller to pass the `file` parameter and either
        download the results using the `download()` method afterwards or
        pass a path to a file where the scored data will be downloaded to
        afterwards.

        Attributes
        ----------
        deployment : Deployment or string ID
            Deployment which will be used for scoring.

        intake_settings : dict (optional)
            A dict configuring how data is coming from. Supported options:

                - type : string, either `localFile`, `s3`, `azure`, `gcp`, `dataset` or `jdbc`

            To score from a local file, add the this parameter to the
            settings:

                - file : file-like object, string path to file or a
                  pandas.DataFrame of scoring data

            To score from S3, add the next parameters to the settings:

                - url : string, the URL to score (e.g.: `s3://bucket/key`)
                - credential_id : string (optional)

            .. _batch_predictions_jdbc_creds_usage:

            To score from JDBC, add the next parameters to the settings:

                - data_store_id : string, the ID of the external data store connected
                  to the JDBC data source (see
                  :ref:`Database Connectivity <database_connectivity_overview>`).
                - query : string (optional if `table` and `schema` is specified),
                  a self-supplied SELECT statement of the data set you wish to predict.
                - table : string (optional if `query` is specified),
                  the name of specified database table.
                - schema : string (optional if `query` is specified),
                  the name of specified database schema.
                - fetch_size : int (optional),
                  Changing the `fetchSize` can be used to balance throughput and memory
                  usage.
                - credential_id : string (optional) the ID of the credentials holding
                  information about a user with read-access to the JDBC data source (see
                  :ref:`Credentials <credentials_api_doc>`).

        output_settings : dict (optional)
            A dict configuring how scored data is to be saved. Supported
            options:

                - type : string, either `localFile`, `s3` or `jdbc`

            To save scored data to a local file, add this parameters to the
            settings:

                - path : string (optional), path to save the scored data
                  as CSV. If a path is not specified, you must download
                  the scored data yourself with `job.download()`.
                  If a path is specified, the call will block until the
                  job is done. if there are no other jobs currently
                  processing for the targeted prediction instance,
                  uploading, scoring, downloading will happen in parallel
                  without waiting for a full job to complete. Otherwise,
                  it will still block, but start downloading the scored
                  data as soon as it starts generating data. This is the
                  fastest method to get predictions.

            To save scored data to S3, add the next parameters to the settings:

                - url : string, the URL for storing the results
                  (e.g.: `s3://bucket/key`)
                - credential_id : string (optional)

            To save scored data to JDBC, add the next parameters to the settings:

                - `data_store_id` : string, the ID of the external data store connected to
                  the JDBC data source (see
                  :ref:`Database Connectivity <database_connectivity_overview>`).
                - `table` : string,  the name of specified database table.
                - `schema` : string (optional), the name of specified database schema.
                - `statement_type` : string, the type of insertion statement to create,
                  one of ``datarobot.enums.AVAILABLE_STATEMENT_TYPES``.
                - `update_columns` : list(string) (optional),  a list of strings containing
                  those column names to be updated in case `statement_type` is set to a
                  value related to update or upsert.
                - `where_columns` : list(string) (optional), a list of strings containing
                  those column names to be selected in case `statement_type` is set to a
                  value related to insert or update.
                - `credential_id` : string, the ID of the credentials holding information about
                  a user with write-access to the JDBC data source (see
                  :ref:`Credentials <credentials_api_doc>`).

        csv_settings : dict (optional)
            CSV intake and output settings. Supported options:

            - `delimiter` : string (optional, default `,`), fields are delimited by
              this character. Use the string `tab` to denote TSV (TAB separated values).
              Must be either a one-character string or the string `tab`.
            - `quotechar` : string (optional, default `"`), fields containing the
              delimiter must be quoted using this character.
            - `encoding` : string (optional, default `utf-8`), encoding for the CSV
              files. For example (but not limited to): `shift_jis`, `latin_1` or
              `mskanji`.

        timeseries_settings : dict (optional)
            Configuration for time-series scoring. Supported options:

            - `type` : string, must be `forecast` or `historical` (default if
              not passed is `forecast`). `forecast` mode makes predictions using
              `forecast_point` or rows in the dataset without target. `historical`
              enables bulk prediction mode which calculates predictions for all
              possible forecast points and forecast distances in the dataset within
              `predictions_start_date`/`predictions_end_date` range.
            - `forecast_point` : datetime (optional), forecast point for the dataset,
              used for the forecast predictions, by default value will be inferred
              from the dataset. May be passed if ``timeseries_settings.type=forecast``.
            - `predictions_start_date` : datetime (optional), used for historical
              predictions in order to override date from which predictions should be
              calculated. By default value will be inferred automatically from the
              dataset. May be passed if ``timeseries_settings.type=historical``.
            - `predictions_end_date` : datetime (optional), used for historical
              predictions in order to override date from which predictions should be
              calculated. By default value will be inferred automatically from the
              dataset. May be passed if ``timeseries_settings.type=historical``.
            - `relax_known_in_advance_features_check` : bool, (default `False`).
              If True, missing values in the known in advance features are allowed
              in the forecast window at the prediction time. If omitted or False,
              missing values are not allowed.

            .. warning:: This is an early release **beta feature**. While the API is stable,
              we are still working on ensuring the best performance possible of
              the scoring pipeline.

        num_concurrent : int (optional)
            Number of concurrent chunks to score simultaneously. Defaults to
            the available number of cores of the deployment. Lower it to leave
            resources for real-time scoring.

        passthrough_columns : list[string] (optional)
            Keep these columns from the scoring dataset in the scored dataset.
            This is useful for correlating predictions with source data.

        passthrough_columns_set : string (optional)
            To pass through every column from the scoring dataset, set this to
            `all`. Takes precedence over `passthrough_columns` if set.

        max_explanations : int (optional)
            Compute prediction explanations for this amount of features.

        threshold_high : float (optional)
            Only compute prediction explanations for predictions above this
            threshold. Can be combined with `threshold_low`.

        threshold_low : float (optional)
            Only compute prediction explanations for predictions below this
            threshold. Can be combined with `threshold_high`.

        prediction_warning_enabled : boolean (optional)
            Add prediction warnings to the scored data. Currently only
            supported for regression models.

        include_prediction_status : boolean (optional)
            Include the prediction_status column in the output, defaults to `False`.

        skip_drift_tracking : boolean (optional)
            Skips drift tracking on any predictions made from this job. This is useful when running
            non-production workloads to not affect drift tracking and cause unnecessary alerts.
            Defaults to `False`.

        prediction_instance : dict (optional)
            Defaults to instance specified by deployment or system configuration.
            Supported options:

                - `hostName` : string
                - `sslEnabled` : boolean (optional, default `true`). Set to `false` to
                  run prediction requests from the batch prediction job without SSL.
                - `datarobotKey` : string (optional), if running a job against a prediction
                  instance in the Managed AI Cloud, you must provide the organization level
                  DataRobot-Key
                - `apiKey` : string (optional), by default, prediction requests will use the
                  API key of the user that created the job. This allows you to make requests
                  on behalf of other users.

        abort_on_error : boolean (optional)
             Default behaviour is to abort the job if too many rows fail scoring. This will free
             up resources for other jobs that may score successfully. Set to `false` to
             unconditionally score every row no matter how many errors are encountered.
             Defaults to `True`.

        column_names_remapping : dict (optional)
            Mapping with column renaming for output table. Defaults to `{}`.

        include_probabilities : boolean (optional)
            Flag that enables returning of all probability columns. Defaults to `True`.

        include_probabilities_classes : list (optional)
            List the subset of classes if a user doesn't want all the classes. Defaults to `[]`.

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """
        try:
            dep_id = deployment.id
        except AttributeError:
            dep_id = deployment

        job_data = {'deploymentId': dep_id}

        if num_concurrent is not None:
            job_data['numConcurrent'] = int(num_concurrent)

        if max_explanations is not None:
            job_data['maxExplanations'] = int(max_explanations)

        if threshold_high is not None:
            job_data['thresholdHigh'] = float(threshold_high)

        if threshold_low is not None:
            job_data['thresholdLow'] = float(threshold_low)

        if include_prediction_status:
            job_data['includePredictionStatus'] = bool(include_prediction_status)

        if skip_drift_tracking:
            job_data['skipDriftTracking'] = bool(skip_drift_tracking)

        if not abort_on_error:
            job_data['abortOnError'] = bool(abort_on_error)

        if not include_probabilities:
            job_data['includeProbabilities'] = bool(include_probabilities)

        if prediction_warning_enabled is not None:
            job_data['predictionWarningEnabled'] = \
                bool(prediction_warning_enabled)

        if passthrough_columns_set == 'all':
            job_data['passthroughColumnsSet'] = 'all'
        elif passthrough_columns is not None:
            job_data['passthroughColumns'] = passthrough_columns

        if prediction_instance is not None:
            cls._prediction_instance.check(prediction_instance)
            job_data['predictionInstance'] = to_api(prediction_instance)

        if column_names_remapping is not None:
            cls._column_names_remapping.check(column_names_remapping)
            job_data['columnNamesRemapping'] = dict(column_names_remapping)

        if include_probabilities_classes:
            job_data['includeProbabilitiesClasses'] = list(include_probabilities_classes)

        if timeseries_settings is not None:
            warnings.warn(
                'Time Series Batch Predictions an early release beta feature. '
                'While the API is stable, we are still working on ensuring the '
                'best performance possible of the scoring pipeline.'
            )
            timeseries_settings = cls._timeseries_settings.check(timeseries_settings)

            if timeseries_settings['type'] == 'historical':

                start_date = timeseries_settings.get('predictions_start_date')
                end_date = timeseries_settings.get('predictions_end_date')

                if start_date and not isinstance(start_date, datetime.datetime):
                    raise ValueError(
                        'The value provided for predictions_start_date was '
                        'not a valid format.'
                    )

                if end_date and not isinstance(end_date, datetime.datetime):
                    raise ValueError(
                        'The value provided for predictions_end_date was '
                        'not a valid format.'
                    )

                if start_date and not end_date:
                    raise ValueError(
                        'You must also provide predictions_end_date if you '
                        'provide predictions_start_date'
                    )

                if start_date and start_date > end_date:
                    raise ValueError(
                        'The value provided for predictions_end_date must be after '
                        'the value provided for predictions_start_date'
                    )

            if timeseries_settings['type'] == 'forecast':

                forecast_point = timeseries_settings.get('forecast_point')

                if forecast_point and not isinstance(forecast_point, datetime.datetime):
                    raise ValueError(
                        'The value provided for forecast_point was '
                        'not a valid format.'
                    )

            job_data['timeseriesSettings'] = to_api(timeseries_settings)

        if intake_settings is None:
            intake_settings = {'type': 'localFile'}

        intake_file = None

        # Validate the intake settings

        if intake_settings.get('type') not in ('localFile', 'azure', 'gcp', 's3', 'jdbc'):

            raise ValueError('Unsupported type parameter for intake_settings: %s' % (
                intake_settings.get('type'),
            ))

        elif intake_settings['type'] == 'localFile':

            # This intake option requires us to upload the source
            # data ourselves

            if intake_settings.get('file') is None:

                raise ValueError(
                    'Missing source data. Either supply the `file` '
                    'parameter or switch to an intake option that does not '
                    'require it.'
                )

            intake_file = recognize_sourcedata(
                intake_settings.pop('file'),
                'prediction.csv',
            )

        elif intake_settings['type'] == 's3':

            del intake_settings['type']
            intake_settings = cls._s3_settings.check(intake_settings)
            intake_settings['type'] = 's3'

        elif intake_settings['type'] == 'jdbc':

            del intake_settings['type']
            intake_settings = cls._jdbc_intake_settings.check(intake_settings)
            intake_settings['type'] = 'jdbc'

        job_data['intakeSettings'] = to_api(intake_settings)

        if output_settings is None:
            output_settings = {'type': 'localFile'}

        output_file = None

        # Validate the output settings

        if output_settings.get('type') not in ('localFile', 'azure', 'gcp', 's3', 'jdbc'):

            raise ValueError('Unsupported type parameter for output_settings: %s' % (
                output_settings.get('type'),
            ))

        elif output_settings['type'] == 'localFile':

            if output_settings.get('path') is not None:
                output_file = open(output_settings.pop('path'), 'wb')

        elif output_settings['type'] == 's3':

            del output_settings['type']
            output_settings = cls._s3_settings.check(output_settings)
            output_settings['type'] = 's3'

        elif output_settings['type'] == 'jdbc':

            del output_settings['type']
            output_settings = cls._jdbc_output_settings.check(output_settings)
            output_settings['type'] = 'jdbc'

        job_data['outputSettings'] = to_api(output_settings)

        if csv_settings is not None:
            cls._csv_settings.check(csv_settings)
            job_data['csvSettings'] = to_api(csv_settings)

        response = cls._client.post(
            url=cls._jobs_path(),
            json=job_data,
        )

        job_response = response.json()
        job_id = get_id_from_response(response)

        upload_thread = None

        if intake_file is not None:

            # There is source data to upload, so spin up a thread to handle
            # the upload concurrently and for thread safety issues, make
            # a copy of the REST client object

            _upload_client = cls._client.copy()

            def _uploader():

                if 'file_path' in intake_file:
                    fileobj = open(intake_file['file_path'], 'rb')
                else:
                    fileobj = intake_file['filelike']
                    fileobj.seek(0)

                try:
                    _upload_client.put(
                        url=job_response['links']['csvUpload'],
                        data=fileobj,
                        headers={'content-type': 'text/csv'},
                    )
                finally:
                    if hasattr(fileobj, 'close'):
                        fileobj.close()

            if output_file is not None:

                # If output_file is specified, we upload and download
                # concurrently

                upload_thread = threading.Thread(target=_uploader)
                upload_thread.setDaemon(True)
                upload_thread.start()

            else:

                # Otherwise, upload is synchronous

                _uploader()

        job = BatchPredictionJob.get(job_id)

        if output_file is not None:

            # We must download the result to `output_file`
            # And clean up any thread we spawned during uploading
            try:
                job.download(output_file)
            finally:
                output_file.close()
                if upload_thread is not None:
                    upload_thread.join()

        return job

    @classmethod
    def score_to_file(cls, deployment, intake_path, output_path, **kwargs):
        """
        Create new batch prediction job, upload the scoring dataset and
        download the scored CSV file concurrently.

        Will block until the entire file is scored.

        Refer to the `create` method for details on the other `kwargs`
        parameters.

        Attributes
        ----------
        deployment : Deployment or string ID
            Deployment which will be used for scoring.

        intake_path : file-like object/string path to file/pandas.DataFrame
              Scoring data

        output_path : str
            Filename to save the result under

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """
        kwargs['intake_settings'] = {
            'type': 'localFile',
            'file': intake_path,
        }

        kwargs['output_settings'] = {
            'type': 'localFile',
            'path': output_path,
        }

        return cls.score(deployment, **kwargs)

    @classmethod
    def score_s3(
        cls,
        deployment,
        source_url,
        destination_url,
        credential=None,
        **kwargs
    ):
        """
        Create new batch prediction job, with a scoring dataset from S3
        and writing the result back to S3.

        This returns immediately after the job has been created. You
        must poll for job completion using `get_status()` or
        `wait_for_completion()`.

        Refer to the `create` method for details on the other `kwargs`
        parameters.

        Attributes
        ----------
        deployment : Deployment or string ID
            Deployment which will be used for scoring.

        source_url : string
            The URL for the prediction dataset (e.g.: `s3://bucket/key`)

        destination_url : string
            The URL for the scored dataset (e.g.: `s3://bucket/key`)

        credential : string or Credential (optional)
            The AWS Credential object or credential id

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """
        intake_settings = {
            'type': 's3',
        }

        if credential is not None:
            if isinstance(credential, Credential):
                intake_settings['credential_id'] = credential.credential_id
            else:
                intake_settings['credential_id'] = credential

        output_settings = intake_settings.copy()

        intake_settings['url'] = source_url
        output_settings['url'] = destination_url

        kwargs.update({
            'intake_settings': intake_settings,
            'output_settings': output_settings,
        })

        return cls.score(deployment, **kwargs)

    @classmethod
    def score_azure(
        cls,
        deployment,
        source_url,
        destination_url,
        credential=None,
        **kwargs
    ):
        """
        Create new batch prediction job, with a scoring dataset from Azure blob
        storage and writing the result back to Azure blob storage.

        This returns immediately after the job has been created. You
        must poll for job completion using `get_status()` or
        `wait_for_completion()`.

        Refer to the `create` method for details on the other `kwargs`
        parameters.

        Attributes
        ----------
        deployment : Deployment or string ID
            Deployment which will be used for scoring.

        source_url : string
            The URL for the prediction dataset
            (e.g.: `https://storage_account.blob.endpoint/container/blob_name`)

        destination_url : string
            The URL for the scored dataset
            (e.g.: `https://storage_account.blob.endpoint/container/blob_name`)

        credential : string or Credential (optional)
            The Azure Credential object or credential id

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """
        intake_settings = {
            'type': 'azure',
        }

        if credential is not None:
            if isinstance(credential, Credential):
                intake_settings['credential_id'] = credential.credential_id
            else:
                intake_settings['credential_id'] = credential

        output_settings = intake_settings.copy()

        intake_settings['url'] = source_url
        output_settings['url'] = destination_url

        kwargs.update({
            'intake_settings': intake_settings,
            'output_settings': output_settings,
        })

        return cls.score(deployment, **kwargs)

    @classmethod
    def score_gcp(
        cls,
        deployment,
        source_url,
        destination_url,
        credential=None,
        **kwargs
    ):
        """
        Create new batch prediction job, with a scoring dataset from Google Cloud Storage
        and writing the result back to one.

        This returns immediately after the job has been created. You
        must poll for job completion using `get_status()` or
        `wait_for_completion()`.

        Refer to the `create` method for details on the other `kwargs`
        parameters.

        Attributes
        ----------
        deployment : Deployment or string ID
            Deployment which will be used for scoring.

        source_url : string
            The URL for the prediction dataset
            (e.g.: `http(s)://storage.googleapis.com/[bucket]/[object]`)

        destination_url : string
            The URL for the scored dataset
            (e.g.: `http(s)://storage.googleapis.com/[bucket]/[object]`)

        credential : string or Credential (optional)
            The GCP Credential object or credential id

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """
        intake_settings = {
            'type': 'gcp',
        }

        if credential is not None:
            if isinstance(credential, Credential):
                intake_settings['credential_id'] = credential.credential_id
            else:
                intake_settings['credential_id'] = credential

        output_settings = intake_settings.copy()

        intake_settings['url'] = source_url
        output_settings['url'] = destination_url

        kwargs.update({
            'intake_settings': intake_settings,
            'output_settings': output_settings,
        })

        return cls.score(deployment, **kwargs)

    @classmethod
    def score_from_existing(cls, batch_prediction_job_id):
        """ Create a new batch prediction job based on the settings from a previously created one

        Attributes
        ----------
        batch_prediction_job_id: str
            ID of the previous batch prediction job

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """

        batch_job = super(BatchPredictionJob, cls).get(None, batch_prediction_job_id)

        job_data = {'predictionJobId': batch_job.id}

        response = cls._client.post(
            url=cls._from_existing_path(),
            json=job_data,
        )

        job_id = get_id_from_response(response)
        return BatchPredictionJob.get(job_id)

    @classmethod
    def get(cls, batch_prediction_job_id):
        """ Get batch prediction job

        Attributes
        ----------
        batch_prediction_job_id: str
            ID of batch prediction job

        Returns
        -------
        BatchPredictionJob
            Instance of BatchPredictonJob
        """
        batch_job = super(BatchPredictionJob, cls).get(
            None, batch_prediction_job_id)
        batch_job.id = batch_prediction_job_id

        return batch_job

    def download(self, fileobj):
        """ Downloads the CSV result of a prediction job

        Attributes
        ----------
        fileobj: file-like object
            Write CSV data to this file-like object

        """
        status = None
        for n in range(120):
            status = self.get_status()

            if status['status'] == 'ABORTED':
                raise RuntimeError('Job %s was aborted: %s' % (
                    self.id,
                    status['status_details'],
                ))

            if 'download' in status['links']:
                break
            time.sleep(1)

        if 'download' not in status['links']:
            raise RuntimeError('Could not detect download URL for job %s' % (
                self.id
            ))

        download_iter = self._client.get(
            status['links']['download'],
            stream=True,
        ).iter_content(chunk_size=8192)

        for chunk in download_iter:
            if chunk:
                fileobj.write(chunk)

    def delete(self):
        """
        Cancel this job. If this job has not finished running, it will be
        removed and canceled.
        """
        status = self.get_status()

        prediction_job_id = status['links']['self'].split('/')[-2]
        self._client.delete(self._job_path(None, prediction_job_id))

    def get_status(self):
        """Get status of batch prediction job

        Returns
        -------
        BatchPredictionJob status data
            Dict with job status
        """

        batch_job = super(BatchPredictionJob, self).get(None, self.id)
        batch_job.id = self.id

        return batch_job._safe_data

    @classmethod
    def list_by_status(cls, statuses=None):
        """Get jobs collection for specific set of statuses

        Attributes
        ----------
        statuses
            List of statuses to filter jobs ([ABORTED|COMPLETED...])
            if statuses is not provided, returns all jobs for user

        Returns
        -------
        BatchPredictionJob statuses
            List of job statses dicts with specific statuses
        """
        if statuses is not None:
            params = {'status': statuses}
        else:
            params = {}

        return list(
            pagination.unpaginate(cls._jobs_path(), params, cls._client))

    def _make_result_from_location(self, location, **kwargs):
        server_data = self._client.get(location)
        if server_data.status_code == 200:
            return server_data.content

    @classmethod
    def _data_and_completed_url_for_job(cls, url):
        response = cls._client.get(url, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            if 'download' in data['links']:
                completed_url = data['links']['download']
            else:
                completed_url = data['links']['self']
            return data, completed_url
        else:
            e_msg = 'Server unexpectedly returned status code {}'
            raise errors.AsyncFailureError(
                e_msg.format(response.status_code))

    def __repr__(self):
        return 'BatchPredictionJob({}, \'{}\', status={})'.format(
            self.job_type, self.id, self.status
        )
