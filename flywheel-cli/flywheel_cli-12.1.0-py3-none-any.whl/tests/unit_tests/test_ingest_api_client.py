import datetime
import importlib
import io
import os
from unittest.mock import call
from uuid import UUID, uuid4


import pytest
from requests.exceptions import ConnectionError as ReqConnError
from requests.exceptions import RetryError

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.client import api as api_client


_BASE_URL = "http://base_url.com"
_API_KEY = "apikey"


def test_instantiate_client(mock_get_api_key, client):
    assert isinstance(client, api_client.APIClient)
    assert client.url == _BASE_URL
    assert client._ingest_id is None
    assert mock_get_api_key.called_once()
    assert client.session.headers["Authorization"] == mock_get_api_key.return_value


def test_create_from_url(mock_get_api_key):
    client = api_client.APIClient.from_url(_BASE_URL)

    assert isinstance(client, api_client.APIClient)
    assert client.url == _BASE_URL
    assert mock_get_api_key.called_once()
    assert client.session.headers["Authorization"] == mock_get_api_key.return_value
    assert client._ingest_id is None


def test_create_from_url_with_uuid(mock_get_api_key):
    uuid = uuid4()
    client = api_client.APIClient.from_url(_BASE_URL, uuid)

    assert isinstance(client, api_client.APIClient)
    assert client.url == _BASE_URL
    assert mock_get_api_key.called_once()
    assert client.session.headers["Authorization"] == mock_get_api_key.return_value
    assert client._ingest_id == uuid


def test_call_api(mock_request, client):
    response = "sample_response"
    mock_request.return_value = MockResponse(response, 200)

    resp = client.call_api('GET', '/foo')
    assert resp == response
    assert_mock_call(mock_request, 'GET', '/foo')

    mock_request.reset_mock()

    resp = client.call_api('GET', '/foo', stream=True)
    assert isinstance(resp, MockResponse)
    assert resp.json_data == response
    assert_mock_call(mock_request, 'GET', '/foo', stream=True)


def test_call_api_retry_statuses(mocker, mock_get_api_key):
    time = mocker.patch("urllib3.util.retry.time")
    client = api_client.APIClient("https://httpbin.org")
    with pytest.raises(RetryError):
        client.call_api("GET", f"/status/502")
    # sleeptime is 0 on 1st retry, then backoff * 2^(retry-1)
    assert time.sleep.mock_calls == [call(0.2), call(0.4), call(0.8), call(1.6)]


def test_call_api_error_is_retried(mocker, mock_get_api_key):
    sleep_mock = mocker.patch('urllib3.util.retry.Retry.sleep')
    client = api_client.APIClient(_BASE_URL)

    with pytest.raises(ReqConnError):
        client.session.get("https://flywheel.test")
    assert sleep_mock.call_count == client.TOTAL_RETRIES


def test_create_ingest(mock_request, client):
    response = {
        "id": '18f61a79-208f-4201-91cc-5adff8d600f0',
        "label": "label",
        "fw_host": "fw_host",
        "fw_user": "fw_user",
        "config": {"src_fs": "/tmp"},
        'strategy_config': {
            'dicom': 'dicom',
            'root_dirs': 0,
            'no_subjects': False,
            'no_sessions': False,
            'strategy_name': 'folder',
        },
        "status": 'created',
        "timestamp": 0,
        "history": [("created", 0)],
        "created": "2020-01-01 10:00:00"
    }
    mock_request.return_value = MockResponse(response, 200)

    cfg = config.IngestConfig(
        src_fs="/tmp"
    )

    fw_auth = T.FWAuth(
        api_key="api_key",
        host="flywheel.test",
        user="test@flywheel.test",
        is_admin=True,
    )
    strg = config.FolderConfig()

    ingest = client.create_ingest(cfg, strg, fw_auth)
    payload = {
        "config": cfg.dict(exclude_none=True),
        "strategy_config": strg.dict(exclude_none=True)
    }
    assert_mock_call(mock_request, 'POST', '/ingests', json=payload)

    # check bind
    assert str(client.ingest_id) == response['id']
    assert str(ingest.id) == response['id']

    assert_ingest(ingest, response)


def test_list_ingests(mock_request, client):
    response = [
        {
            "id": '18f61a79-208f-4201-91cc-5adff8d600f0',
            "label": "label",
            "fw_host": "fw_host",
            "fw_user": "fw_user",
            "config": {"src_fs": "/tmp"},
            'strategy_config': {
                'dicom': 'dicom',
                'root_dirs': 0,
                'no_subjects': False,
                'no_sessions': False,
                'strategy_name': 'folder',
            },
            "status": 'created',
            "timestamp": 0,
            "history": [("created", 0)],
            "created": "2020-01-01 10:00:00"
        },
        {
            "id": '11111111-2222-3333-4444-555555555555',
            "label": "label",
            "src_fs": "src_fw",
            "fw_host": "fw_host",
            "fw_user": "fw_user",
            "config": {"src_fs": "/tmp"},
            'strategy_config': {
                'dicom': 'dicom',
                'root_dirs': 0,
                'no_subjects': False,
                'no_sessions': False,
                'strategy_name': 'folder',
            },
            "status": 'created',
            "timestamp": 0,
            "history": [("created", 0)],
            "created": "2020-01-01 10:00:00"
        }
    ]
    mock_request.return_value = MockResponse(response, 200)

    ingests = list(client.list_ingests())
    assert_mock_call(mock_request, 'GET', '/ingests')

    assert len(ingests) == 2

    for i in range(len(ingests)):
        assert_ingest(ingests[i], response[i])


def test_ingest(mock_request, client):
    response = {
        "id": '18f61a79-208f-4201-91cc-5adff8d600f0',
        "label": "label",
        "fw_host": "fw_host",
        "fw_user": "fw_user",
        "config": {"src_fs": "/tmp"},
        'strategy_config': {
            'dicom': 'dicom',
            'root_dirs': 0,
            'no_subjects': False,
            'no_sessions': False,
            'strategy_name': 'folder',
        },
        "status": "created",
        "timestamp": 0,
        "history": [("created", 0)],
        "created": "2020-01-01 10:00:00"
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = response['id']
    client.bind(uuid)

    ingest = client.ingest
    assert_mock_call(mock_request, 'GET', '/ingests/' + uuid)

    assert str(ingest.id) == uuid


def test_load_subject_csv(mock_request, client):
    response = "ok"
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    f = io.BytesIO(b"file_content")
    client.load_subject_csv(f)
    assert_mock_call(mock_request, 'POST', f'/ingests/{uuid}/subjects', files={'subject_csv': f})


def test_start(mock_request, client):
    response = {
        "id": '18f61a79-208f-4201-91cc-5adff8d600f0',
        "label": "label",
        "fw_host": "fw_host",
        "fw_user": "fw_user",
        "config": {"src_fs": "/tmp"},
        'strategy_config': {
            'dicom': 'dicom',
            'root_dirs': 0,
            'no_subjects': False,
            'no_sessions': False,
            'strategy_name': 'folder',
        },
        "status": "created",
        "timestamp": 0,
        "history": [("created", 0)],
        "created": "2020-01-01 10:00:00"
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = response['id']
    client.bind(uuid)

    ingest = client.start()

    assert_ingest(ingest, response)
    assert_mock_call(mock_request, 'POST', f'/ingests/{uuid}/start')


def test_review(mock_request, client):
    response = {
        "id": '18f61a79-208f-4201-91cc-5adff8d600f0',
        "label": "label",
        "fw_host": "fw_host",
        "fw_user": "fw_user",
        "config": {"src_fs": "/tmp"},
        'strategy_config': {
            'dicom': 'dicom',
            'root_dirs': 0,
            'no_subjects': False,
            'no_sessions': False,
            'strategy_name': 'folder',
        },
        "status": 'in_review',
        "timestamp": 0,
        "history": [("in_review", 0)],
        "created": "2020-01-01 10:00:00"
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = response['id']
    client.bind(uuid)

    changes = {"change": "change"}
    ingest = client.review(changes)

    assert_ingest(ingest, response)
    assert_mock_call(mock_request, 'POST', f'/ingests/{uuid}/review', json=changes)


def test_abort(mock_request, client):
    response = {
        "id": '18f61a79-208f-4201-91cc-5adff8d600f0',
        "label": "label",
        "fw_host": "fw_host",
        "fw_user": "fw_user",
        "config": {"src_fs": "/tmp"},
        'strategy_config': {
            'dicom': 'dicom',
            'root_dirs': 0,
            'no_subjects': False,
            'no_sessions': False,
            'strategy_name': 'folder',
        },
        "status": 'aborted',
        "timestamp": 0,
        "history": [("aborted", 0)],
        "created": "2020-01-01 10:00:00"
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = response['id']
    client.bind(uuid)

    ingest = client.abort()

    assert_ingest(ingest, response)
    assert_mock_call(mock_request, 'POST', f'/ingests/{uuid}/abort')


def test_progress(mock_request, client):
    response = {
        "scans": {
            "scanned": 1,
            "pending": 2,
        },
        "items": {
            "finished": 8,
            "total": 9,
        },
        "files": {
            "scanned": 1,
            "failed": 4,
            "canceled": 5,
            "total": 9,
        },
        "bytes": {
            "scanned": 1,
            "pending": 2,
            "completed": 6,
            "skipped": 7,
        }
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    progress = client.progress
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/progress')

    assert isinstance(progress, T.Progress)
    for key1 in ['scans', 'items', 'files', 'bytes']:
        v1 = getattr(progress, key1)
        m1 = response[key1]
        for key2 in ['scanned', 'pending', 'running', 'failed', 'canceled', 'completed', 'skipped', 'finished', 'total']:
            value = getattr(v1, key2)
            if key2 in m1:
                assert value == m1[key2]
            else:
                assert value == 0


def test_summary(mock_request, client):
    response = {
        'groups': 1,
        'projects': 2,
        'subjects': 3,
        'sessions': 4,
        'acquisitions': 5,
        'files': 6,
        'packfiles': 7,
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    summary = client.summary
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/summary')

    assert isinstance(summary, T.Summary)
    for key in ['groups', 'projects', 'subjects', 'sessions', 'acquisitions', 'files', 'packfiles']:
        assert getattr(summary, key) == response[key]


def test_report(mock_request, client):
    response = {
        'status': 'created',
        'elapsed': {},
        'errors': [],
    }
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    report = client.report
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/report')

    assert isinstance(report, T.Report)
    assert isinstance(report.status, T.IngestStatus)


def test_tree(mock_request, client):
    response = (
        '{"id":"18f61a79-208f-4201-91cc-5adff8d600f0",'
        '"ingest_id":"18f61a79-208f-4201-91cc-5adff8d600f0",'
        '"files_cnt":5,'
        '"bytes_sum":6,'
        '"parent_id":"18f61a79-208f-4201-91cc-5adff8d600f0",'
        '"path":"str",'
        '"level":2,'
        '"src_context":[],'
        '"dst_context":[],'
        '"dst_path":"str"}'
        "\n"
    )
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    tree = list(client.tree)
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/tree', stream=True)

    assert len(tree) == 1
    tree = tree[0]
    assert isinstance(tree, T.ContainerOut)


def test_audit_logs(mock_request, client):
    response = "\n\n\nline1\n\n\n\n\n\nline2\nline3\n\nline4\n\n\n"
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    logs = list(client.audit_logs)
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/audit', stream=True)

    assert logs == ['line1\n', 'line2\n', 'line3\n', 'line4\n']


def test_deid_logs(mock_request, client):
    response = "\n\n\nline1\n\n\n\n\n\nline2\nline3\n\nline4\n\n\n"
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    logs = list(client.deid_logs)
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/deid', stream=True)

    assert logs == ['line1\n', 'line2\n', 'line3\n', 'line4\n']


def test_subjects(mock_request, client):
    response = "\n\n\nline1\n\n\n\n\n\nline2\nline3\n\nline4\n\n\n"
    mock_request.return_value = MockResponse(response, 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'
    client.bind(uuid)

    logs = list(client.subjects)
    assert_mock_call(mock_request, 'GET', f'/ingests/{uuid}/subjects', stream=True)

    assert logs == ['line1\n', 'line2\n', 'line3\n', 'line4\n']


def test_delete_ingest(mock_request, client):
    mock_request.return_value = MockResponse("", 200)

    uuid = '18f61a79-208f-4201-91cc-5adff8d600f0'

    client.delete_ingest(uuid)
    assert_mock_call(mock_request, 'POST', f'/ingests/{uuid}/delete')


def test_connect_timeout_env(mock_request, mocker):
    os.environ["FLYWHEEL_CLI_CONNECT_TIMEOUT"] = "40"
    # prevent pydantic to raise duplicate validator function error when reloading config module
    mocker.patch("pydantic.class_validators.in_ipython", return_value=True)
    # reimport beacuse of module level timeout vars
    importlib.reload(config)

    client = api_client.APIClient(_BASE_URL)

    response = "sample_response"
    mock_request.return_value = MockResponse(response, 200)

    resp = client.call_api('GET', '/foo')
    assert resp == response
    mock_request.assert_called_once_with(
        'GET',
        _BASE_URL + '/foo',
        timeout=(40, 60)
    )

    del os.environ["FLYWHEEL_CLI_CONNECT_TIMEOUT"]


def test_connect_timeout_env_raise(mock_request, mocker):
    os.environ["FLYWHEEL_CLI_CONNECT_TIMEOUT"] = "abc"
    # prevent pydantic to raise duplicate validator function error when reloading config module
    mocker.patch("pydantic.class_validators.in_ipython", return_value=True)
    with pytest.raises(ValueError):
        importlib.reload(config)

    del os.environ["FLYWHEEL_CLI_CONNECT_TIMEOUT"]

    os.environ["FLYWHEEL_CLI_READ_TIMEOUT"] = "abc"
    with pytest.raises(ValueError):
        importlib.reload(config)

    del os.environ["FLYWHEEL_CLI_READ_TIMEOUT"]


def test_read_timeout_env(mock_request, mocker):
    os.environ["FLYWHEEL_CLI_READ_TIMEOUT"] = "32"
    # prevent pydantic to raise duplicate validator function error when reloading config module
    mocker.patch("pydantic.class_validators.in_ipython", return_value=True)
    # reimport beacuse of module level timeout vars
    importlib.reload(config)

    client = api_client.APIClient(_BASE_URL)

    response = "sample_response"
    mock_request.return_value = MockResponse(response, 200)

    resp = client.call_api('GET', '/foo')
    assert resp == response
    mock_request.assert_called_once_with('GET', f"{_BASE_URL}/foo", timeout=(30, 32))

    del os.environ["FLYWHEEL_CLI_READ_TIMEOUT"]


@pytest.fixture(scope="function")
def mock_request(mocker):
    mocker.patch('flywheel_cli.ingest.utils.get_api_key', return_value=_API_KEY)
    return mocker.patch('requests.Session.request')


@pytest.fixture(scope="function")
def mock_get_api_key(mocker):
    return mocker.patch('flywheel_cli.ingest.utils.get_api_key', return_value=_API_KEY)


@pytest.fixture(scope="function")
def client():
    return api_client.APIClient(_BASE_URL)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception(f"Response code is not 200 ({self.status_code})")

    def json(self):
        return self.json_data

    def iter_lines(self):
        lines = self.json_data.split("\n")
        for line in lines:
            line = line.strip().encode("utf-8")
            yield line


def assert_ingest(ingest: T.IngestOutAPI, ingest_json):
    assert isinstance(ingest, T.IngestOutAPI)
    assert isinstance(ingest.id, UUID)
    assert isinstance(ingest.created, datetime.datetime)
    assert ingest.status == ingest_json["status"]
    assert ingest.config.src_fs == ingest_json["config"]["src_fs"]
    assert ingest.fw_host == ingest_json["fw_host"]
    assert ingest.fw_user == ingest_json["fw_user"]
    assert ingest.created.strftime("%Y-%m-%d %H:%M:%S") == ingest_json["created"]
    # TODO assert strategy_config


def assert_mock_call(mocked_function, method, path, base_url=_BASE_URL, **kwargs):
    calls = call(method, base_url + path, timeout=(30, 60), **kwargs)
    assert mocked_function.mock_calls == [calls]
