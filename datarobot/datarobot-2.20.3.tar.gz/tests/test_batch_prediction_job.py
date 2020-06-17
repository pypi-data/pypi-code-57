# -*- encoding: utf-8 -*-

import io
import json
import mock
import pytest
import responses
import threading
import trafaret as t

from datarobot import BatchPredictionJob, Credential


@pytest.fixture
def batch_prediction_jobs_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "count": 4,
        "previous": None,
        "next": None,
        "data": [{
            "status": "INITIALIZING",
            "percentageCompleted": 0,
            "elapsedTimeSec": 7747,
            "links": {
                "download": (
                    "https://host_name.com/batchPredictions/"
                    "5ce1204b962d741661907ea0/download/"
                ),
                "self": (
                    "https://host_name.com/batchPredictions/"
                    "5ce1204b962d741661907ea0/",
                ),
                "csvUpload": (
                    "https://host_name.com/batchPredictions/"
                    "5ce1204b962d741661907ea0/csvUpload/"
                ),
            },
            "jobSpec": {
                "numConcurrent": 1,
                "thresholdHigh": None,
                "thresholdLow": None,
                "filename": "",
                "deploymentId": "5ce1138c962d7415e076d8c6",
                "passthroughColumns": [],
                "passthroughColumnsSet": None,
                "maxExplanations": None,
            },
            "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
        }, {
            "id": "5ce1204b962d741661907ea0",
            "status": "INITIALIZING",
            "percentageCompleted": 0,
            "elapsedTimeSec": 7220,
            "links": {
                "download": "",
                "self": (
                    "https://host_name.com/batchPredictions/"
                    "5ce1225a962d741661907eb3/",
                )
            },
            "jobSpec": {
                "numConcurrent": 1,
                "thresholdHigh": None,
                "thresholdLow": None,
                "filename": "",
                "deploymentId": "5ce1138c962d7415e076d8c6",
                "passthroughColumns": [],
                "passthroughColumnsSet": None,
                "maxExplanations": None
            },
            "statusDetails": "Job submitted at 2019-05-19 09:31:06.724000"
        }]
    })


@pytest.fixture
def batch_prediction_job_initializing_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "INITIALIZING",
        "percentageCompleted": 0,
        "elapsedTimeSec": 7747,
        "links": {
            "download": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/download/"
            ),
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
            "csvUpload": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/csvUpload/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": [],
            "passthroughColumnsSet": None,
            "maxExplanations": None
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_s3_initializing_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "INITIALIZING",
        "percentageCompleted": 0,
        "elapsedTimeSec": 7747,
        "links": {
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": [],
            "passthroughColumnsSet": None,
            "maxExplanations": None,
            "intake_settings": {"name": "s3", "url": "s3://bucket/source_key"},
            "output_settings": {"name": "s3", "url": "s3://bucket/target_key"}
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_running_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "RUNNING",
        "scored_rows": 400,
        "failed_rows": 0,
        "percentageCompleted": 40,
        "elapsedTimeSec": 7747,
        "links": {
            "download": "",
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": [],
            "passthroughColumnsSet": None,
            "maxExplanations": None
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_completed_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "COMPLETED",
        "scored_rows": 400,
        "failed_rows": 0,
        "percentageCompleted": 100,
        "elapsedTimeSec": 7747,
        "links": {
            "download": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/download/"
            ),
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": [],
            "passthroughColumnsSet": None,
            "maxExplanations": None
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_completed_passthrough_columns_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "COMPLETED",
        "scored_rows": 400,
        "failed_rows": 0,
        "percentageCompleted": 100,
        "elapsedTimeSec": 7747,
        "links": {
            "download": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/download/"
            ),
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": ["a", "b"],
            "passthroughColumnsSet": None,
            "maxExplanations": None
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_completed_passthrough_columns_set_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "COMPLETED",
        "scored_rows": 400,
        "failed_rows": 0,
        "percentageCompleted": 100,
        "elapsedTimeSec": 7747,
        "links": {
            "download": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/download/"
            ),
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": [],
            "passthroughColumnsSet": "all",
            "maxExplanations": None
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_s3_completed_json():
    return json.dumps({
        "id": "5ce1204b962d741661907ea0",
        "status": "COMPLETED",
        "scored_rows": 400,
        "failed_rows": 0,
        "percentageCompleted": 100,
        "elapsedTimeSec": 7747,
        "links": {
            "self": (
                "https://host_name.com/batchPredictions/"
                "5ce1204b962d741661907ea0/"
            ),
        },
        "jobSpec": {
            "numConcurrent": 1,
            "thresholdHigh": None,
            "thresholdLow": None,
            "filename": "",
            "deploymentId": "5ce1138c962d7415e076d8c6",
            "passthroughColumns": [],
            "passthroughColumnsSet": None,
            "maxExplanations": None,
            "intake_settings": {"type": "s3", "url": "s3://bucket/source_key"},
            "output_settings": {"type": "s3", "url": "s3://bucket/target_key"}
        },
        "statusDetails": "Job submitted at 2019-05-19 09:22:19.779000"
    })


@pytest.fixture
def batch_prediction_job_data_csv():
    return b"""readmitted_1.0_PREDICTION,readmitted_0.0_PREDICTION,readmitted_PREDICTION,THRESHOLD,POSITIVE_CLASS,prediction_status
0.219181314111,0.780818685889,0.0,0.5,1.0,OK
0.341459780931,0.658540219069,0.0,0.5,1.0,OK
0.420107662678,0.579892337322,0.0,0.5,1.0,OK"""


@responses.activate
@pytest.mark.usefixtures('client')
def test_list_batch_prediction_jobs_by_status(batch_prediction_jobs_json):
    responses.add(
        responses.GET,
        'https://host_name.com/batchPredictions/',
        body=batch_prediction_jobs_json)

    job_statuses = BatchPredictionJob.list_by_status()

    assert 2 == len(job_statuses)


@responses.activate
@pytest.mark.usefixtures('client')
@pytest.mark.parametrize(
    ['job_fixture', 'expected_status', 'expected_percentage_completed'],
    [
        pytest.param(
            'batch_prediction_job_initializing_json',
            'INITIALIZING',
            0,
        ),
        pytest.param(
            'batch_prediction_job_completed_passthrough_columns_json',
            'COMPLETED',
            100,
        ),
        pytest.param(
            'batch_prediction_job_completed_passthrough_columns_set_json',
            'COMPLETED',
            100,
        ),
        pytest.param(
            'batch_prediction_job_s3_completed_json',
            'COMPLETED',
            100,
        ),
    ]
)
def test_get_batch_prediction_job_status(
        request, job_fixture, expected_status, expected_percentage_completed):

    responses.add(
        responses.GET,
        'https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/',
        body=request.getfixturevalue(job_fixture)
    )

    job = BatchPredictionJob.get('5ce1204b962d741661907ea0')
    job_status = job.get_status()

    assert job_status['status'] == expected_status
    assert job_status['percentage_completed'] == expected_percentage_completed


@responses.activate
@pytest.mark.usefixtures('client')
def test_get_result_when_done(
        batch_prediction_job_initializing_json,
        batch_prediction_job_running_json,
        batch_prediction_job_completed_json,
        batch_prediction_job_data_csv):

    responses.add(
        responses.GET,
        'https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/',
        body=batch_prediction_job_initializing_json)

    responses.add(
        responses.GET,
        'https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/',
        body=batch_prediction_job_running_json)

    responses.add(
        responses.GET,
        'https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/',
        body=batch_prediction_job_completed_json)

    responses.add(
        responses.GET,
        'https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/download/',
        body=batch_prediction_job_data_csv)

    job = BatchPredictionJob.get('5ce1204b962d741661907ea0')

    assert job.get_result_when_complete() == batch_prediction_job_data_csv


@responses.activate
@pytest.mark.usefixtures('client')
def test_score_to_file(
    tmpdir,
    batch_prediction_job_initializing_json,
    batch_prediction_job_completed_json,
    batch_prediction_job_data_csv
):

    responses.add(
        responses.POST,
        "https://host_name.com/batchPredictions/",
        body=batch_prediction_job_initializing_json,
        headers={
            "Location": "https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/",
        },
    )

    responses.add(
        responses.GET,
        "https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/download/",
        body=batch_prediction_job_data_csv,
    )

    responses.add(
        responses.PUT,
        "https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/csvUpload/",
        body="",
        status=202,
    )

    responses.add(
        responses.GET,
        "https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/",
        body=batch_prediction_job_completed_json,
    )

    output_file = str(tmpdir.mkdir("sub").join("scored.csv"))

    thread_count_before = threading.activeCount()

    BatchPredictionJob.score_to_file(
        "5ce1138c962d7415e076d8c6",
        io.BytesIO(b"foo\nbar"),
        output_file,
    )

    assert open(output_file, "rb").read() == batch_prediction_job_data_csv
    assert thread_count_before == threading.activeCount(), 'Thread leak'


@responses.activate
@pytest.mark.usefixtures('client')
def test_score_s3(
    batch_prediction_job_s3_initializing_json,
    batch_prediction_job_s3_completed_json
):

    responses.add(
        responses.POST,
        "https://host_name.com/batchPredictions/",
        body=batch_prediction_job_s3_initializing_json,
        headers={
            "Location": "https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/",
        },
    )

    responses.add(
        responses.GET,
        "https://host_name.com/batchPredictions/5ce1204b962d741661907ea0/",
        body=batch_prediction_job_s3_completed_json,
    )

    job = BatchPredictionJob.score_s3(
        deployment="5ce1138c962d7415e076d8c6",
        source_url='s3://bucket/source_key',
        destination_url='s3://bucket/target_key',
        credential=Credential('key_id'),
    )

    job.wait_for_completion()


@pytest.mark.usefixtures('client')
@pytest.mark.parametrize([
    'score_args',
    'expected_exception',
    'expected_message'
], [
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {'type': 'unknown'}
        },
        ValueError,
        'Unsupported type parameter for intake_settings',
        id='unsupported-intake-option',
    ),
    pytest.param(
        {
            'deployment': 'foo',
        },
        ValueError,
        'Missing source data',
        id='missing-source-data',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {'type': 's3'}
        },
        t.DataError,
        None,
        id='missing-s3-intake-configuration',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {'type': 's3', 'url': 's3://bucket/source_key'},
            'output_settings': {'type': 's3'}
        },
        t.DataError,
        None,
        id='missing-s3-output-configuration',
    ),
])
def test_score_errors(score_args, expected_exception, expected_message):
    with pytest.raises(expected_exception, match=expected_message):
        BatchPredictionJob.score(**score_args)


@pytest.mark.parametrize([
    'score_args',
    'expected_job_data',
], [
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
        },
        id='deployment-id',
    ),
    pytest.param(
        {
            'deployment': mock.MagicMock(id='bar'),
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
        },
        {
            'deploymentId': 'bar',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
        },
        id='deployment',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {'type': 's3', 'url': 's3://bucket/source_key'},
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 's3', 'url': 's3://bucket/source_key'},
            'outputSettings': {'type': 'local_file'},
        },
        id='s3-intake-settings',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {'type': 's3', 'url': 's3://bucket/source_key'},
            'output_settings': {'type': 's3', 'url': 's3://bucket/target_key'},
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 's3', 'url': 's3://bucket/source_key'},
            'outputSettings': {'type': 's3', 'url': 's3://bucket/target_key'},
        },
        id='s3-intake-output-settings',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 's3',
                'url': 's3://bucket/source_key',
                'credential_id': 'key_id',
            },
            'output_settings': {
                'type': 's3',
                'url': 's3://bucket/target_key',
                'credential_id': 'key_id',
            },
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {
                'type': 's3',
                'url': 's3://bucket/source_key',
                'credentialId': 'key_id',
            },
            'outputSettings': {
                'type': 's3',
                'url': 's3://bucket/target_key',
                'credentialId': 'key_id',
            },
        },
        id='full-s3-intake-output-settings',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'threshold_high': 0.95,
            'threshold_low': 0.05,
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'thresholdHigh': 0.95,
            'thresholdLow': 0.05,
        },
        id='thresholds',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'passthrough_columns': ['a', 'b', 'c'],
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'passthroughColumns': ['a', 'b', 'c'],
        },
        id='passthrough-columns',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'passthrough_columns_set': 'all',
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'passthroughColumnsSet': 'all',
        },
        id='passthrough-columns-set-all',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'passthrough_columns': ['a', 'b', 'c'],
            'passthrough_columns_set': 'all',
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'passthroughColumnsSet': 'all',
        },
        id='passthrough-columns-set-override',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'num_concurrent': 10
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'numConcurrent': 10
        },
        id='num-concurrent',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'max_explanations': 10
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'maxExplanations': 10
        },
        id='max-explanations',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'local_file',
                'file': io.BytesIO(b'foo\nbar'),
            },
            'prediction_warning_enabled': True
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {'type': 'local_file'},
            'outputSettings': {'type': 'local_file'},
            'predictionWarningEnabled': True,
        },
        id='prediction-warning-enabled',
    ),
    pytest.param(
        {
            'deployment': 'foo',
            'intake_settings': {
                'type': 'jdbc',
                'table': 'test',
                'schema': 'public',
                'data_store_id': 'abcd1234',
                'credential_id': 'key_id',
            },
            'output_settings': {
                'type': 'jdbc',
                'table': 'test2',
                'schema': 'public',
                'statement_type': 'insert',
                'data_store_id': 'abcd1234',
                'credential_id': 'key_id',
            },
        },
        {
            'deploymentId': 'foo',
            'intakeSettings': {
                'type': 'jdbc',
                'table': 'test',
                'schema': 'public',
                'dataStoreId': 'abcd1234',
                'credentialId': 'key_id',
            },
            'outputSettings': {
                'type': 'jdbc',
                'table': 'test2',
                'schema': 'public',
                'statementType': 'insert',
                'dataStoreId': 'abcd1234',
                'credentialId': 'key_id',
            },
        },
        id='full-jdbc-intake-output-settings',
    ),
])
@mock.patch('datarobot.BatchPredictionJob._client')
def test_score_job_data(mock_client, score_args, expected_job_data):

    # Using an exception to short-circuit the score function and test
    # the contents of the job data without proceeding with the rest
    # of the function

    mock_client.post.side_effect = RuntimeError('short-circuit')

    with pytest.raises(RuntimeError, match='short-circuit'):
        BatchPredictionJob.score(**score_args)

    mock_client.post.assert_called_once_with(
        url=BatchPredictionJob._jobs_path(),
        json=expected_job_data,
    )
