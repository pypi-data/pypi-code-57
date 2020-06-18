import os
import json
from datetime import datetime
from typing import List, Union
from .models import ScidraModule, JobRun, WorkflowProject, WorkflowRun
from .utils import get_workflow_client
from fa_common import logger as LOG, get_settings
from fa_common.storage import File, get_storage_client
import oyaml as yaml
import copy

dirname = os.path.dirname(__file__)


async def create_workflow_project(
    user_id: str, project_name: str, bucket_id: str = None
) -> WorkflowProject:
    client = get_workflow_client()
    try:
        project = await client._get_project_by_name(user_id)
    except ValueError:
        LOG.info(f"Workflow User {user_id} does not exist, creating.")
        project = await client.create_project(user_id)

    branch = await client.create_branch(project.id, project_name)

    return WorkflowProject(
        name=branch.name,
        user_id=user_id,
        bucket_id=bucket_id,
        gitlab_project_id=project.id,
        created=str(datetime.now()),
    )


async def delete_workflow_project(user_id: str, project_name: str):
    client = get_workflow_client()

    try:
        await client.delete_branch(user_id, project_name)
    except ValueError:
        LOG.error(
            f"Trying to delete workflow project {project_name} does not exist for user {user_id}."
        )
        raise ValueError(f"Workflow Project {project_name} does not exist.")


async def delete_workflow_user(user_id: str, wait: bool = False):
    client = get_workflow_client()
    try:
        await client.delete_project_by_name(user_id, wait)
    except ValueError:
        LOG.error(f"Workflow User {user_id} does not exist.")
        raise ValueError(f"Workflow User {user_id} does not exist.")


async def run_job(
    project: WorkflowProject,
    description: str,
    module: ScidraModule,
    job_data: Union[dict, List[dict]],
    runner: str = "csiro-swarm",
    files: List[File] = [],
    sync: bool = False,
    upload: bool = False,
    upload_runner: str = None,
) -> WorkflowRun:

    settings = get_settings()
    file_refs = [_file.dict() for _file in files]
    with open(os.path.join(dirname, "job.yml")) as yaml_file:
        job_yaml = yaml.safe_load(yaml_file)

    if not isinstance(job_data, List):
        job_data = [job_data]

    job_yaml["run-job"]["tags"] = [runner]
    job_yaml["run-job"]["image"] = module.docker_image
    job_yaml["run-job"]["variables"]["TZ"] = project.timezone
    job_yaml["run-job"]["variables"]["FILE_REFS"] = json.dumps(file_refs)
    job_yaml["run-job"]["variables"]["MODULE_NAME"] = module.name
    job_yaml["run-job"]["variables"]["KUBERNETES_CPU_REQUEST"] = module.cpu_request
    job_yaml["run-job"]["variables"]["KUBERNETES_CPU_LIMIT"] = module.cpu_limit
    job_yaml["run-job"]["variables"][
        "KUBERNETES_MEMORY_REQUEST"
    ] = f"{module.memory_request_gb}Gi"
    job_yaml["run-job"]["variables"][
        "KUBERNETES_MEMORY_LIMIT"
    ] = f"{module.memory_limit_gb}Gi"

    if len(job_data) > 1:
        for i, params in enumerate(job_data):
            run_job_i = copy.deepcopy(job_yaml["run-job"])
            job_yaml[f"run-job{i}"] = run_job_i
            job_yaml[f"run-job{i}"]["variables"]["JOB_PARAMETERS"] = json.dumps(params)
        del job_yaml["run-job"]
    else:
        job_yaml[f"run-job"]["variables"]["JOB_PARAMETERS"] = json.dumps(job_data[0])

    if not upload:
        del job_yaml["upload-data"]
    else:
        upload_uri = get_storage_client().get_uri(
            project.bucket_id, settings.WORKFLOW_UPLOAD_PATH
        )
        job_yaml["upload-data"]["variables"]["UPLOAD_PATH"] = upload_uri
        if upload_runner is None:
            upload_runner = runner
        job_yaml["upload-data"]["tags"] = [runner]

    client = get_workflow_client()

    await client.update_ci(
        project.gitlab_project_id, project.name, job_yaml, description
    )
    workflow_run = await client.run_pipeline(
        project.gitlab_project_id, project.name, wait=sync
    )
    return workflow_run


async def get_job_run(user_id: str, job_id: int, include_log: bool = False) -> JobRun:
    client = get_workflow_client()
    return await client.get_job(user_id, job_id, include_log)


async def get_job_log(user_id: str, job_id: int) -> bytes:
    client = get_workflow_client()
    logs = await client.get_job_log(user_id, job_id)
    return logs


async def delete_job(user_id: str, job_id: int):
    client = get_workflow_client()
    await client.delete_job(user_id, job_id)


async def get_workflow(
    user_id: str, workflow_id: int, verbose: bool = False
) -> WorkflowRun:
    client = get_workflow_client()
    return await client.get_pipeline(user_id, workflow_id, verbose)


async def delete_workflow(project: WorkflowProject, workflow_id: int):
    client = get_workflow_client()
    await client.delete_pipeline(project.user_id, workflow_id)
    storage = get_storage_client()
    await storage.delete_file(
        project.bucket_id, f"{get_settings().WORKFLOW_UPLOAD_PATH}/{workflow_id}", True
    )
