import time
from collections.abc import Iterable

from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectPipeline, ProjectPipelineJob, ProjectJob
from gitlab.exceptions import GitlabGetError, GitlabCreateError, GitlabDeleteError

import yaml
import json
from typing import List, Union
from fa_common import force_async, get_current_app, get_settings
from fa_common import logger as LOG
from .utils import GitlabCIYAMLDumper
from .models import WorkflowRun, JobRun


class GitlabClient:
    """
    Singleton client for interacting with gitlab.
    Is a wrapper over the existing gitlab python client to provide specialist functions for the Job/Module
    workflow.

    Please don't use it directly, use `fa_common.workflow.utils.get_workflow_client`.
    """

    __instance = None
    gitlab: Gitlab = None

    def __new__(cls) -> "GitlabClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            app = get_current_app()
            cls.__instance.gitlab = app.gitlab  # type: ignore
        return cls.__instance

    async def project_exists(self, project_id: Union[int, str]) -> bool:
        try:
            self._get_project(project_id)
        except ValueError:
            return False
        return True

    async def _get_project(self, project_id: Union[int, str]) -> Project:
        if isinstance(project_id, int):
            try:
                project = await force_async(self.gitlab.projects.get)(project_id)
            except GitlabGetError:
                raise ValueError(f"No project found with the id {project_id}")
            return project
        else:
            return await self._get_project_by_name(project_id)

    async def _get_project_by_name(self, project_name: str):
        settings = get_settings()
        projects = await force_async(self.gitlab.projects.list)(
            search=project_name, owned=True
        )
        for proj in projects:
            group_id = proj.namespace["id"]
            if proj.name == project_name and group_id == settings.GITLAB_GROUP_ID:
                return proj
        raise ValueError(f"No project found with the name {project_name}")

    async def create_project(self, project_name: str) -> int:
        settings = get_settings()
        try:
            project = await force_async(self.gitlab.projects.create)(
                {
                    "name": project_name,
                    "namespace_id": settings.GITLAB_GROUP_ID,
                    "auto_cancel_pending_pipelines": False,
                }
            )
        except GitlabCreateError as err:
            LOG.warning(f"Create Error caught, retrying in 5 secs: {err}")
            time.sleep(5)
            project = await force_async(self.gitlab.projects.create)(
                {"name": project_name, "namespace_id": settings.GITLAB_GROUP_ID}
            )

        LOG.info(f"Created CI Project: {project.id}")
        LOG.debug(f"{project}")

        data = {
            "branch": "master",
            "commit_message": "First Commit",
            "actions": [
                {"action": "create", "file_path": ".gitlab-ci.yml", "content": ""}
            ],
        }
        commit = await force_async(project.commits.create)(data)
        LOG.info(f"Created CI Commit: {commit.id}")
        LOG.debug(f"{commit}")

        return project

    async def create_branch(self, project_id: int, branch_name: str):
        project = await self._get_project(project_id)
        branch = await force_async(project.branches.create)(
            {"branch": branch_name, "ref": "master"}
        )
        LOG.info(f"Created branch: {branch}")
        return branch

    async def delete_branch(self, project_id: int, branch_name: str):
        project = await self._get_project(project_id)
        try:
            await force_async(project.branches.delete)(branch_name)
            LOG.info(f"Deleted branch: {branch_name}")
        except GitlabDeleteError as err:
            if str(err.response_code) == "404":
                raise ValueError(
                    f"Trying to delete branch {branch_name} that doesn't exist."
                )
            raise err

    async def get_job(
        self, project_id: Union[str, int], job_id: int, include_log: bool = False
    ) -> JobRun:
        project = await self._get_project(project_id)
        try:
            job = await force_async(project.jobs.get)(job_id)
            log = None
            if include_log:
                log = job.trace()
        except GitlabGetError:
            raise ValueError(
                f"No job found with the id {job_id} in project {project_id}"
            )

        return self.job_to_job_run(job, log)

    async def get_job_log(self, project_id: Union[str, int], job_id: int) -> bytes:
        project = await self._get_project(project_id)
        job = await force_async(project.jobs.get)(job_id)
        return job.trace()

    async def update_ci(
        self,
        project_id: Union[str, int],
        branch_name: str,
        ci_file: dict,
        update_message: str = "No message",
    ):
        project = await self._get_project(project_id)
        data = {
            "branch": branch_name,
            "commit_message": update_message,
            "actions": [
                {
                    "action": "update",
                    "file_path": ".gitlab-ci.yml",
                    "content": yaml.dump(
                        ci_file, Dumper=GitlabCIYAMLDumper, default_flow_style=False
                    ),
                }
            ],
        }
        commit = await force_async(project.commits.create)(data)
        LOG.info(f"Created CI Commit: {commit.id}")
        LOG.debug(f"{commit}")

        return commit.id

    async def run_pipeline(
        self,
        project_id: Union[str, int],
        branch: str,
        variables: List[dict] = None,
        wait: bool = False,
    ) -> WorkflowRun:
        project = await self._get_project(project_id)
        pipeline = project.pipelines.create({"ref": branch, "variables": variables})
        if wait:
            while pipeline.finished_at is None:
                pipeline.refresh()
                time.sleep(2)
        jobs = pipeline.jobs.list()

        return await self.pipeline_to_workflow_run(pipeline, project, jobs)

    def job_to_job_run(self, job: ProjectJob, job_log: bytes = None) -> JobRun:
        output = None
        if hasattr(job, "artifacts_file") and job.artifacts_file is not None:
            try:
                output_bytes = None
                output_bytes = job.artifact("output/outputs.json")
                if output_bytes is not None:
                    output = json.loads(output_bytes)
                    if isinstance(output, Iterable):
                        output = List(output)
            except Exception as err:
                LOG.error(err)

        job_run = JobRun(
            id=job.id,
            workflow_id=job.pipeline["id"],
            workflow_status=job.pipeline["status"],
            status=job.status,
            started_at=job.started_at,
            finished_at=job.finished_at,
            duration=job.duration,
            name=job.name,
            stage=job.stage,
            output=output,
        )
        if job_log is not None:
            job_run.log = job_log

        return job_run

    async def pipeline_to_workflow_run(
        self,
        pipeline: ProjectPipeline,
        project: Project,
        jobs: List[ProjectPipelineJob] = [],
    ) -> WorkflowRun:
        job_runs: List[JobRun] = []
        for job in jobs:
            job_runs.append(await self.get_job(project.id, job.id))

        return WorkflowRun(
            id=pipeline.id,
            gitlab_project_id=project.id,
            gitlab_project_branch=pipeline.ref,
            commit_id=pipeline.sha,
            status=pipeline.status,
            started_at=pipeline.started_at,
            finished_at=pipeline.finished_at,
            duration=pipeline.duration,
            jobs=job_runs,
        )

    async def delete_project(self, project_id: int, wait: bool = True):
        await force_async(self.gitlab.projects.delete)(project_id)
        if wait:
            try:
                proj = await self._get_project(project_id)
                while proj is not None:
                    LOG.info(f"Waiting for project {project_id} to delete")
                    time.sleep(2)
                    proj = await self._get_project(project_id)
            except ValueError:
                LOG.info(f"Project {project_id} successfully deleted")
                return

    async def delete_project_by_name(self, project_name: str, wait: bool = True):
        settings = get_settings()
        projects = await force_async(self.gitlab.projects.list)(
            search=project_name, owned=True
        )
        LOG.info(f"Found projects: {projects}")
        for proj in projects:
            group_id = proj.namespace["id"]
            LOG.info(f"Checking project: {proj.id}, {proj.name}, {group_id}")
            if proj.name == project_name and group_id == settings.GITLAB_GROUP_ID:
                LOG.info(f"Deleting project: {proj.id}")
                await self.delete_project(proj.id, wait)
                return
        raise ValueError(f"No project found with the name {project_name}")
