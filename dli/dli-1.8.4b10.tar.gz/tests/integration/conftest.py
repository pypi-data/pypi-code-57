import pytest
import os
import boto3
import jwt as pyjwt
import urllib.parse
import copy

from contextlib import contextmanager
from dli.client.builders import DatasetBuilder
from dli.client.dli_client import DliClient, Session

from tests.integration import random_name


def pytest_generate_tests(metafunc):
    metafunc.parametrize('client', ('QA',), indirect=['client'],
                         scope='function')
    metafunc.parametrize('jwt', ('QA',), indirect=['jwt'], scope='function')


class aws_envs:
    DEV = '116944431457'
    PROD = '867407613858'


@pytest.fixture
def jwt(request):
    # The env variable QA_OIDC_AUD can be found in gitlab under
    # the settings:CI/CD:Variables section and set locally.
    aud = os.environ[f'{request.param}_OIDC_AUD']
    return {
        "datalake": {
            "user_id": "3e1c688b-86f3-4b60-b988-15cb2d9b0133",
            "accounts": {
                "datalake-test1": "rw",
                "datalake-test2": "rw",
                "datalake-ops": "rw",
            },
            "groups": [],
            "organisation_id": os.environ['QA_ORG_ID']
        },
        "sub": "api:rollo-qa@ihsmarkit.com",
        "exp": 9564743138,
        "aud": aud
    }


class TestDliClient(DliClient):
    def __init__(self, api_root=None,
                 auth_key=None, host=None,
                 debug=False, jwt=None, secret=None,
                 access_id='noop', secret_key='noop'):
        self.jwt = jwt
        self.auth_key = auth_key
        self.secret = secret
        self.api_root = api_root
        super().__init__(api_root, host=host, debug=debug,
                         access_id=access_id,
                         secret_key=secret_key)

    def _new_session(self):
        return Session(
            None,
            self.secret_key,
            self._environment,
            self.host,
            self.auth_key,
        )

    @contextmanager
    def with_accounts(self, accounts):
        new_jwt = copy.deepcopy(self.jwt)
        new_jwt['datalake']['accounts'] = {
            account: 'rw' for account in accounts
        }

        auth_key = pyjwt.encode(new_jwt, self.secret).decode('utf8')
        yield TestDliClient(
            access_id=self.access_id,
            secret_key=self.secret_key,
            api_root=self.api_root,
            auth_key=auth_key
        )


@pytest.fixture
def client(monkeypatch, jwt, request):
    # This is the S3 address used for the QA environment.
    api_root = os.environ[f'{request.param}_API_URL']
    secret = os.environ[f'{request.param}_OIDC_SECRET']
    auth_key = pyjwt.encode(jwt, secret).decode('utf8')
    client = TestDliClient(
        api_root=api_root,
        auth_key=auth_key,
        secret=secret,
        jwt=jwt
    )
    yield client


@pytest.fixture
def aws_roles(client):
    """
    Ensures that the AWS roles are set up correctly. Sometimes
    QA messes with this setting.
    """
    aws_account = {
        'awsAccountId': aws_envs.PROD,
        'awsAccountName': 'dl_prod_aws_account',
        'awsRoleArn': 'arn:aws:iam::867407613858:role/trust-entity-dev-test',
        'awsRegion': 'eu-west-1',
        'accountIds': ['datalake-test1', 'datalake-test2', 'datalake-mgmt']
    }

    client.session.post(
        '__api/me/aws-accounts', json=aws_account
    )


@pytest.fixture
def package(client):
    package = client.register_package(
        name=random_name(),
        description="my package description",
        topic="Automotive",
        access="Restricted",
        internal_data="Yes",
        data_sensitivity="Public",
        terms_and_conditions="Terms",
        publisher="my publisher",
        access_manager_id='datalake-ops',
        tech_data_ops_id='datalake-test2',
        manager_id='datalake-test2'
    )
    yield package
    client.delete_package(package.id)


@pytest.fixture
def csv_dataset_builder(package):
    dataset_builder = DatasetBuilder(
        package_id=package.id,
        name='dataset-files-test-' + random_name(),
        description="My dataset description",
        content_type="Pricing",
        data_format='CSV',
        publishing_frequency="Weekly",
        taxonomy=[]
    )

    dataset_builder = dataset_builder.with_external_s3_storage(
        bucket_name='test-datalake-read-write-bucket-1',
        aws_account_id=aws_envs.PROD,
        prefix='abc',
    )
    yield dataset_builder


@pytest.fixture
def empty_dataset(client, aws_roles, csv_dataset_builder):
    dataset = client.register_dataset(csv_dataset_builder)
    yield dataset


@pytest.fixture
def csv_dataset(client, aws_roles, csv_dataset_builder):
    dataset = client.register_dataset(csv_dataset_builder)
    # NOTE register_s3_datafile both registers the datafile in the
    # datalake and it uploads the file to the bucket.
    client.register_s3_datafile(
        dataset_id=dataset.dataset_id,
        name='csv_dataset',
        files=['tests/integration/data/AAPL.csv'],
        s3_prefix='abc',
        data_as_of='2000-01-01'
    )
    yield dataset
