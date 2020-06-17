import pytest
import responses

from datarobot import Credential
from datarobot.utils import parse_time


@pytest.fixture
def credentials_server_resp():
    return {
        u'count': 2,
        u'data': [
            {
                u'creationDate': u'2020-02-03T10:13:27.411000Z',
                u'credentialId': u'5e37f247cf8a5f73842f6eab',
                u'credentialType': u's3',
                u'description': u'',
                u'name': u'my_s3_cred_1'
            },
            {
                u'creationDate': u'2020-02-10T14:52:07.258000Z',
                u'credentialId': u'5e416e17cf8a5f6e7afcc52f',
                u'credentialType': u'basic',
                u'description': u'???',
                u'name': u'my_basic_cred_1'
            },
        ],
        u'next': None,
        u'previous': None,
        u'totalCount': 2,
    }


@pytest.fixture
def s3_credential_server_resp(credentials_server_resp):
    return credentials_server_resp['data'][0]


@pytest.fixture
def basic_credential_server_resp(credentials_server_resp):
    return credentials_server_resp['data'][1]


@responses.activate
def test_list(credentials_endpoint, credentials_server_resp):
    responses.add(responses.GET, credentials_endpoint, json=credentials_server_resp)

    creds = Credential.list()

    for cred, server_payload in zip(creds, credentials_server_resp['data']):
        assert cred.credential_id == server_payload['credentialId']
        assert cred.name == server_payload['name']
        assert cred.credential_type == server_payload['credentialType']
        assert cred.creation_date == parse_time(server_payload['creationDate'])
        assert cred.description == server_payload['description']


@responses.activate
def test_get(credentials_endpoint, s3_credential_server_resp):
    credential_id = s3_credential_server_resp['credentialId']
    responses.add(
        responses.GET,
        '{}{}/'.format(credentials_endpoint, credential_id),
        json=s3_credential_server_resp
    )

    cred = Credential.get(credential_id)

    assert cred.credential_id == s3_credential_server_resp['credentialId']
    assert cred.name == s3_credential_server_resp['name']
    assert cred.credential_type == s3_credential_server_resp['credentialType']
    assert cred.creation_date == parse_time(s3_credential_server_resp['creationDate'])
    assert cred.description == s3_credential_server_resp['description']


@responses.activate
def test_create_basic(credentials_endpoint, basic_credential_server_resp):
    responses.add(responses.POST, credentials_endpoint, json=basic_credential_server_resp)

    cred = Credential.create_basic(
        name=basic_credential_server_resp['name'],
        user='USERNAME',
        password='PASSWORD',
        description=basic_credential_server_resp['description'],
    )

    assert cred.credential_id == basic_credential_server_resp['credentialId']
    assert cred.name == basic_credential_server_resp['name']
    assert cred.credential_type == basic_credential_server_resp['credentialType']
    assert cred.creation_date == parse_time(basic_credential_server_resp['creationDate'])
    assert cred.description == basic_credential_server_resp['description']


@responses.activate
def test_create_s3(credentials_endpoint, s3_credential_server_resp):
    responses.add(responses.POST, credentials_endpoint, json=s3_credential_server_resp)

    cred = Credential.create_s3(
        name=s3_credential_server_resp['name'],
        aws_access_key_id='?',
        aws_secret_access_key='!',
        description=s3_credential_server_resp['description'],
    )

    assert cred.credential_id == s3_credential_server_resp['credentialId']
    assert cred.name == s3_credential_server_resp['name']
    assert cred.credential_type == s3_credential_server_resp['credentialType']
    assert cred.creation_date == parse_time(s3_credential_server_resp['creationDate'])
    assert cred.description == s3_credential_server_resp['description']


@responses.activate
def test_delete(credentials_endpoint, s3_credential_server_resp):
    credential_id = s3_credential_server_resp['credentialId']
    responses.add(
        responses.GET,
        '{}{}/'.format(credentials_endpoint, credential_id),
        json=s3_credential_server_resp
    )
    responses.add(
        responses.DELETE,
        '{}{}/'.format(credentials_endpoint, credential_id),
    )

    cred = Credential.get(credential_id)
    cred.delete()
