from datetime import datetime
from unittest.mock import Mock, PropertyMock
from freezegun import freeze_time
from moto import mock_s3

from dli.aws import create_refreshing_session


@mock_s3
def test_session_refreshes():
    dli_client = Mock()
    # This is how you give an attribute a side effect
    auth_key = PropertyMock(return_value='abc')
    type(dli_client.session).auth_key = auth_key 

    dli_client.session.token_expires_on = datetime(2000, 1, 2, 0, 0, 0)
    session = create_refreshing_session(dli_client.session).resource('s3')

    with freeze_time(datetime(2000, 1, 1, 0, 0, 0)):
        assert auth_key.call_count == 1
        session.meta.client.list_buckets()
        assert auth_key.call_count == 1
        session.meta.client.list_buckets()
        assert auth_key.call_count == 1

    with freeze_time(datetime(2000, 1, 3, 0, 0, 0)):
        dli_client.session.token_expires_on = datetime(2000, 1, 4, 0, 0, 0)
        assert auth_key.call_count == 1
        session.meta.client.list_buckets()
        assert auth_key.call_count == 2
        session.meta.client.list_buckets()
        assert auth_key.call_count == 2
