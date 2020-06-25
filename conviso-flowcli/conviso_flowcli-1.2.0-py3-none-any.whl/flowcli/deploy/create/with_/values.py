import click

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.deploy.create.context import pass_create_context
from convisoappsec.flow import GitAdapter
from convisoappsec.flow import api
from convisoappsec.flowcli.common import project_code_option

@click.command()
@help_option
@project_code_option()
@click.option(
    "-c",
    "--current-commit",
    required=False,
    help="If no value is given the HEAD commit of branch is used.",
)
@click.option(
    "-p",
    "--previous-commit",
    required=False,
    help="If no value is given the value is retrieved from the lastest deploy at flow application.",
)
@click.option(
    "-r",
    "--repository-dir",
    required=False,
    type=click.Path(exists=True, resolve_path=True),
    default='.',
    show_default=True,
    help="Repository directory.",
)
@click.option(
    "--attach-diff/--no-attach-diff",
    default=True,
    show_default=True,
    required=False,
)
@pass_create_context
@pass_flow_context
def values(
    flow_context, create_context, repository_dir, project_code,
    current_commit, previous_commit, attach_diff
):
    try:
        flow = flow_context.create_flow_api_client()
        git_adapter = GitAdapter(repository_dir=repository_dir)
        current_commit = current_commit or git_adapter.head_commit

        if not previous_commit:
            try:
                latest_deploy = flow.deploys.get_latest(project_code)
                previous_commit = latest_deploy.get('current_commit')
            except api.DeployNotFoundException:
                previous_commit = git_adapter.empty_repository_tree_commit

        diff_content = None

        if attach_diff:
            diff_content = git_adapter.diff(
                previous_commit,
                current_commit,
            )

        deploy = flow.deploys.create(
            project_code,
            current_version={'commit': current_commit},
            previous_version={'commit': previous_commit},
            diff_content=diff_content,
        )

        click.echo(
            create_context.output_formatter.format(deploy)
        )
    except Exception as e:
        raise click.ClickException(str(e)) from e