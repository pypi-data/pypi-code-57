import click

from tktl.cli.common import ClickGroup
from tktl.commands import deployments as deployments_commands
from tktl.core.config import settings
from tktl.core.loggers import CliLogger
from tktl.core.t import DeploymentStatesT
from tktl.login import validate_decorator


@click.group(
    "deployments",
    help="Manage deployments",
    cls=ClickGroup,
    **settings.HELP_COLORS_DICT
)
def deployments():
    pass


_deployment_shared_options = [
    click.option("-c", "--commit-sha", help="SHA commit"),
    click.option("-b", "--branch-name", help="Branch Name"),
    click.option("-s", "--status-name", help="Status in which deployment is",),
]


def deployment_shared_options(func):
    for option in reversed(_deployment_shared_options):
        func = option(func)
    return func


@deployments.command("get-id", help="Create new deployment")
@deployment_shared_options
@validate_decorator
def get_id(commit_sha: str, branch_name: str, status_name: str, **kwargs):
    logger_ = CliLogger()
    command = deployments_commands.GetDeploymentId()
    result = command.execute(
        commit_sha=commit_sha, branch_name=branch_name, status_name=status_name
    )
    logger_.log(result)


@deployments.command("get-ecr-repo", help="Create new deployment")
@deployment_shared_options
@validate_decorator
def get_ecr_repo(commit_sha: str, branch_name: str, status_name: str, **kwargs):
    logger_ = CliLogger()
    command = deployments_commands.GetDeploymentEcr()
    result = command.execute(
        commit_sha=commit_sha, branch_name=branch_name, status_name=status_name
    )
    logger_.log(result)


@deployments.command("patch-status", help="Create new deployment")
@click.option(
    "-id", "--deployment-id", help="Deployment id", required=True,
)
@click.option(
    "-s",
    "--status-name",
    help="Patch the status of a deployment",
    type=click.Choice(DeploymentStatesT.list()),
)
@validate_decorator
def patch_status(deployment_id: str, status_name: str, **kwargs):
    logger_ = CliLogger()
    command = deployments_commands.PatchDeploymentStatus()
    result = command.execute(deployment_id=deployment_id, status_name=status_name)
    logger_.log(result)
