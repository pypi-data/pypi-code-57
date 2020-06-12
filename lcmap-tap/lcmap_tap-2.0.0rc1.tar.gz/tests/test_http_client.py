"""
Unit tests for lcmap_tap/RetrieveData/http_client.py
"""
from contextlib import ExitStack as does_not_raise
import pytest
import requests
from lcmap_tap.RetrieveData import http_client
from lcmap_tap.storage import ceph


@pytest.mark.parametrize(
    "retry, backoff, result",
    [
        (3, 1, requests.sessions.Session),
        (-3, -1, requests.sessions.Session),
        (None, None, requests.sessions.Session),
    ],
)
def test_setup_session(retry, backoff, result):
    """
    Verify a valid session object is returned.
    """
    assert isinstance(http_client.setup_session(retry, backoff), result)


@pytest.mark.parametrize(
    "key, result",
    [
        ("segment/-408585-2327805.json", does_not_raise()),
        ("segment/123456-789012.json", pytest.raises(IndexError)),
    ],
)
def test_try_download(key, result):
    """Test downloading an object from storage."""
    session = http_client.setup_session()
    obj_key = ceph.object_key(key, ceph.config)
    with result:
        assert http_client.try_download(session, obj_key)[0]["thint"] is not None


@pytest.mark.parametrize(
    "key, http_status",
    [("segment/-408585-2327805.json", 200), ("segment/123456-789012.json", 404),],
)
def test_get_object(key, http_status):
    """Test downloading an object from storage."""
    session = http_client.setup_session()
    obj_key = ceph.object_key(key, ceph.config)
    assert http_client.get_object(session, obj_key).status_code == http_status


@pytest.mark.parametrize(
    "key, json_result",
    [
        ("segment/-408585-2327805.json", does_not_raise()),
        ("segment/123456-789012.json", pytest.raises(IndexError)),
    ],
)
def test_decode(key, json_result):
    """Validate json decoding a session object."""
    session = http_client.setup_session()
    obj_key = ceph.object_key(key, ceph.config)
    result = http_client.get_object(session, obj_key)
    with json_result:
        assert http_client.decode(result)[0]["thint"] is not None
