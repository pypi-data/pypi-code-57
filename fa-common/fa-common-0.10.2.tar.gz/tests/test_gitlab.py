import os
import pytest
import json
import copy
import time

from fa_common import create_app, start_app, utils, force_sync
from fa_common.workflow import (
    run_job,
    ScidraModule,
    get_job_run,
    get_job_log,
    create_workflow_project,
    WorkflowProject,
    get_workflow_client,
    get_workflow,
    delete_workflow,
    job_action,
    JobAction,
)
from fa_common.storage import File
from .conftest import (
    get_env_file,
    TEST_GITLAB_PROJECT,
    TEST_GITLAB_BRANCH,
    TEST_USER_BUCKET,
)

dirname = os.path.dirname(__file__)
test_data_path = os.path.join(dirname, "data")

app = create_app(env_path=get_env_file())
force_sync(start_app)(app)
utils.current_app = app


@pytest.mark.asyncio
async def test_gitlab_create(ensure_no_test_gitlab):
    workflow_project = await create_workflow_project(
        TEST_GITLAB_PROJECT, TEST_GITLAB_BRANCH, TEST_USER_BUCKET
    )

    assert workflow_project.gitlab_project_id > 0
    assert workflow_project.name == TEST_GITLAB_BRANCH


@pytest.mark.asyncio
async def test_job_create(ensure_test_gitlab):

    project = ensure_test_gitlab
    assert project.gitlab_project_id > 0

    module = ScidraModule(
        name="noise-detection",
        docker_image="registry.gitlab.com/csiro-geoanalytics/gpt/modules/noise-detection:latest",
    )
    job_data = {
        "window_channels": 4,
        "window_size": 20,
        "channel_step": 2,
        "window_step": 10,
        "variation_threshold": 0.01,
        "crossover_threshold": 0.003,
    }
    files = [
        File(
            id="data_file",
            name="data_file.csv",
            url="https://firebasestorage.googleapis.com/v0/b/gp-toolkit-staging.appspot.com/o/"
            + "unit_test_data%2Fnd_test_data.csv?alt=media&token=96a65aa1-9e34-4a37-9bc7-7eac4f14847e",
        )
    ]

    work_run = await run_job(
        project,
        "Sync Unit Test",
        module,
        job_data,
        runner="csiro-swarm",
        upload=False,
        files=files,
        sync=True,
    )

    assert work_run.status == "success"
    assert work_run.jobs[0].output is not None

    job_run2 = await get_job_run(
        project.user_id, TEST_USER_BUCKET, work_run.jobs[0].id, False,
    )

    assert job_run2.id == work_run.jobs[0].id

    job_logs = await get_job_log(project.user_id, job_run2.id)
    assert job_logs is not None


@pytest.mark.asyncio
async def test_job_create_async(ensure_test_gitlab):
    project = ensure_test_gitlab
    assert project.gitlab_project_id > 0

    module = ScidraModule(
        name="noise-detection",
        docker_image="registry.gitlab.com/csiro-geoanalytics/gpt/modules/noise-detection:latest",
    )
    job_data = {
        "window_channels": 4,
        "window_size": 20,
        "channel_step": 2,
        "window_step": 10,
        "variation_threshold": 0.01,
        "crossover_threshold": 0.003,
    }
    files = [
        File(
            id="data_file",
            name="data_file.csv",
            url="https://firebasestorage.googleapis.com/v0/b/gp-toolkit-staging.appspot.com/o/"
            + "unit_test_data%2Fnd_test_data.csv?alt=media&token=96a65aa1-9e34-4a37-9bc7-7eac4f14847e",
        )
    ]

    work_run = await run_job(
        project, "Async Unit Test", module, job_data, runner="csiro-swarm", files=files
    )

    job_run2 = await get_job_run(project.user_id, TEST_USER_BUCKET, work_run.jobs[0].id)

    assert job_run2.id == work_run.jobs[0].id


@pytest.mark.asyncio
async def test_large_job_create_async(ensure_test_gitlab):
    project = ensure_test_gitlab
    assert project.gitlab_project_id > 0

    module = ScidraModule(
        name="galei-inversion",
        docker_image="registry.gitlab.com/csiro-geoanalytics/gpt/modules/galei-inversion-module:latest",
        cpu_limit="4000m",
        cpu_request="2000m",
        memory_limit_gb=16,
        memory_request_gb=4,
    )
    job_data = {"test": "subset"}

    job_run = await run_job(
        project, "Inversion Test", module, job_data, runner="csiro-easi-hub"
    )

    assert job_run.id is not None


@pytest.mark.asyncio
async def test_multi_job_retry(ensure_test_gitlab, ensure_test_bucket):
    client = ensure_test_bucket

    project = ensure_test_gitlab
    assert project.gitlab_project_id > 0
    module = ScidraModule(
        name="sensi-module",
        docker_image="registry.gitlab.com/csiro-geoanalytics/gpt/modules/sensi-seismic-module:latest",
        cpu_limit="1000m",
        cpu_request="500m",
        memory_limit_gb=4,
        memory_request_gb=2,
    )

    with open(os.path.join(dirname, "data", "test_sensi.json")) as json_file:
        sensi_data = json.load(json_file)

    depth_list = sensi_data["config"]["hypocenterDepth"]

    params_list = []
    for depth in depth_list:
        params = copy.deepcopy(sensi_data)
        params["config"]["hypocenterDepth"] = depth
        params_list.append(params)

    work_run = await run_job(
        project,
        f"test_multi_job_create_async Test",
        module,
        params_list,
        # runner="csiro-easi-hub",
        runner="csiro-swarm",
        files=[],
        upload=True,
    )

    rt_job = work_run.jobs[1]
    rt_job = await job_action(TEST_GITLAB_PROJECT, rt_job.id, JobAction.CANCEL)
    assert rt_job.status == "canceled"
    new_job = await job_action(TEST_GITLAB_PROJECT, rt_job.id, JobAction.RETRY)

    while work_run.finished_at is None:
        time.sleep(8)
        work_run = await get_workflow(
            TEST_GITLAB_PROJECT, TEST_USER_BUCKET, work_run.id
        )

    assert work_run.hidden_jobs is not None and work_run.hidden_jobs[0].id == rt_job.id
    assert work_run.jobs[1].id == new_job.id  # Assert order remains the same
    assert work_run.status == "success"
    assert await client.file_exists(
        TEST_USER_BUCKET, f"job_data/{work_run.id}/{work_run.jobs[0].id}/outputs.json",
    )
    job_run = await get_job_run(
        TEST_GITLAB_PROJECT, TEST_USER_BUCKET, work_run.jobs[0].id
    )
    assert job_run.output is not None
    assert len(job_run.files) > 0

    await delete_workflow(TEST_GITLAB_PROJECT, TEST_USER_BUCKET, work_run.id)
    assert not await client.file_exists(
        TEST_USER_BUCKET, f"job_data/{work_run.id}/{work_run.jobs[0].id}/outputs.json",
    )


@pytest.mark.asyncio
async def test_delete_workflow_project(ensure_test_gitlab):
    client = get_workflow_client()
    try:
        project = await client._get_project_by_name(TEST_GITLAB_PROJECT)
    except ValueError:
        return

    await client.delete_project(project.id, False)
