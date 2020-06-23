import os

import pytest
import socket

from fastapi import FastAPI
from fa_common.auth import AuthUser
from fa_common.storage import get_storage_client
from fa_common.workflow import (
    get_workflow_client,
    create_workflow_project,
    WorkflowProject,
)
from fa_common import force_sync, logger as LOG, create_app, start_app, utils
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
env_file = os.path.join(dirname, ".env")
secrets_env_file = os.path.join(dirname, ".env.secret")
minio_env_file = os.path.join(dirname, ".env-minio")

hostname = socket.gethostname().replace("_", "-").replace(".", "-").lower()
TEST_GITLAB_PROJECT = f"test-user-{hostname}"
TEST_GITLAB_BRANCH = "test_project"
TEST_USER_BUCKET = f"test-user-{hostname}"


def get_env_file() -> str:
    clean_env()
    if os.path.exists(secrets_env_file):
        load_dotenv(dotenv_path=env_file)
        return secrets_env_file
    else:
        return env_file


@pytest.fixture(scope="module")
def env_path(scope="module") -> str:
    return get_env_file()


@pytest.fixture(scope="module")
def minio_env_path(scope="module") -> str:
    clean_env()
    if os.path.exists(secrets_env_file):
        load_dotenv(dotenv_path=minio_env_file)
        return secrets_env_file
    else:
        return minio_env_file


@pytest.fixture
def ensure_no_test_gitlab():
    client = get_workflow_client()
    try:
        project = force_sync(client._get_project_by_name)(TEST_GITLAB_PROJECT)
    except ValueError:
        LOG.info(f"No project called {TEST_GITLAB_PROJECT}")
        return

    force_sync(client.delete_project)(project.id, True)
    LOG.info(f"Deleted {project.id}")


@pytest.fixture
def ensure_test_gitlab() -> WorkflowProject:
    client = get_workflow_client()
    try:
        project_id = (force_sync(client._get_project_by_name)(TEST_GITLAB_PROJECT)).id
        return WorkflowProject(
            name=TEST_GITLAB_BRANCH,
            user_id=TEST_GITLAB_PROJECT,
            bucket_id=TEST_USER_BUCKET,
            gitlab_project_id=project_id,
        )
    except Exception as err:
        LOG.info(err)
        return force_sync(create_workflow_project)(
            TEST_GITLAB_PROJECT, TEST_GITLAB_BRANCH, TEST_USER_BUCKET
        )


@pytest.fixture
def ensure_test_bucket():
    app = create_app(get_env_file())
    force_sync(start_app)(app)
    utils.current_app = app

    assert isinstance(app, FastAPI)
    client = get_storage_client()
    force_sync(client.make_bucket)(TEST_USER_BUCKET)
    assert force_sync(client.bucket_exists)(TEST_USER_BUCKET)
    return client


def clean_env():
    os.environ.pop("STORAGE_TYPE", None)
    os.environ.pop("BUCKET_PREFIX", None)
    os.environ.pop("BUCKET_NAME", None)
    os.environ.pop("BUCKET_USER_FOLDER", None)
    os.environ.pop("DATABASE_TYPE", None)
    # os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    os.environ.pop("ENABLE_FIREBASE", None)
    os.environ.pop("MINIO_ENDPOINT", None)
    os.environ.pop("MINIO_ACCESS_KEY", None)
    os.environ.pop("MINIO_SECRET_KEY", None)


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({})".format(previousfailed.name))


async def get_test_user() -> AuthUser:
    payload = {
        "sub": f"{hostname}-sub",
        "name": "Test User",
        "email": "test.user@test.com",
        "nickname": "test.user",
        "email_verified": True,
        "picture": None,
        "updated_at": None,
        "scopes": [],
    }

    return AuthUser(**payload)
