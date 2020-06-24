from tktl.commands import BaseDeploymentApiCommand
from tktl.core.clients.http_client import TaktileResponse
from tktl.core.config import settings
from tktl.core.schemas.deployment import DeploymentBase


class GetDeployment(BaseDeploymentApiCommand):
    def execute(self, commit_sha: str, branch_name: str, status_name: str):
        params = {}
        if branch_name:
            params.update({"branch_name": branch_name})
        if status_name:
            params.update({"status": status_name})
        response = self.client.get(
            f"{settings.API_V1_STR}/deployments/{commit_sha}", params=params
        )
        return TaktileResponse.interpret_response(
            response=response, model=DeploymentBase
        )


class GetDeploymentId(GetDeployment):
    def execute(self, commit_sha: str, branch_name: str, status_name: str):
        return (
            super()
            .execute(
                commit_sha=commit_sha, branch_name=branch_name, status_name=status_name
            )
            .id
        )


class GetDeploymentEcr(GetDeployment):
    def execute(self, commit_sha: str, branch_name: str, status_name: str):
        return (
            super()
            .execute(
                commit_sha=commit_sha, branch_name=branch_name, status_name=status_name
            )
            .ecr_repo_url
        )


class PatchDeploymentStatus(GetDeployment):
    def execute(self, deployment_id: str, status_name: str, **kwargs):
        response = self.client.patch(
            f"{settings.API_V1_STR}/deployments/{deployment_id}/status",
            params={"updated_status": status_name},
        )
        return TaktileResponse.interpret_response(response, DeploymentBase)


class ListDeploymentsCommand(BaseDeploymentApiCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        # TODO: implement list deployments and show as table

        # with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
        #     instances = self._get_instances(**kwargs)

        raise NotImplemented


class GetDeploymentDetails(BaseDeploymentApiCommand):
    def _get_table_data(self, instance):
        pass

    def execute(self, id_):
        # TODO: get deployment details
        raise NotImplemented


class GetDeploymentMetricsCommand(BaseDeploymentApiCommand):
    def execute(
        self, deployment_id, start, end, interval, built_in_metrics, *args, **kwargs
    ):
        # TODO: stream metrics
        raise NotImplemented


class StreamDeploymentMetricsCommand(BaseDeploymentApiCommand):
    def execute(self, **kwargs):
        # TODO: stream metrics
        raise NotImplemented


class DeploymentLogsCommand(BaseDeploymentApiCommand):
    def execute(self, **kwargs):
        # TODO: get logs
        raise NotImplemented

    def _get_log_row_string(self, id, log):
        raise NotImplemented

    def _make_table(self, logs, id):
        raise NotImplemented
