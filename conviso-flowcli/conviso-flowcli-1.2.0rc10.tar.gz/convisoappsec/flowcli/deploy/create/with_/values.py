import click

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli import common


@click.command()
@help_option
@click.argument("project-code", required=True)
@click.argument("current-commit", required=True)
@click.argument("previous-commit", required=True)
@pass_flow_context
def values(flow_context, current_commit, previous_commit, project_code):
    try:
        flow = flow_context.create_flow_api_client()
        deploy = flow.deploys.create(
            project_code,
            current_version={'commit': current_commit},
            previous_version={'commit': previous_commit},
        )
        common.notify_created_deploy(deploy)
    except Exception as e:
        raise click.ClickException(str(e)) from e