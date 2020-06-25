import click

from convisoappsec.flow import api
from convisoappsec.flow.version_searchers import TimeBasedVersionSearcher
from convisoappsec.flow.version_control_system_adapter import GitAdapter
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import project_code_option
from convisoappsec.flowcli.deploy.create.context import pass_create_context
from convisoappsec.flowcli.deploy.create.with_.tag_tracker.context import (
    pass_tag_tracker_context
)


@click.command('time')
@help_option
@project_code_option()
@click.option(
    "--attach-diff/--no-attach-diff",
    default=True,
    show_default=True,
    required=False,
)
@pass_tag_tracker_context
@pass_create_context
@pass_flow_context
def time_(flow_context, create_context, tag_tracker_context, project_code, attach_diff):
    try:
        repository_dir = tag_tracker_context.repository_dir
        git_adapter = GitAdapter(repository_dir)

        version_searcher = TimeBasedVersionSearcher(
            git_adapter
        )

        result = version_searcher.find_current_and_previous_version()
        current_version = result.current_version
        previous_version = result.previous_version
        diff_content = None

        if attach_diff:
            diff_content = git_adapter.diff(
                    previous_version.get('commit'),
                    current_version.get('commit'),
            )

        flow = flow_context.create_flow_api_client()

        deploy = flow.deploys.create(
            project_code,
            current_version=current_version,
            previous_version=previous_version,
            diff_content=diff_content,
        )

        click.echo(
            create_context.output_formatter.format(deploy)
        )
    except Exception as e:
        raise click.ClickException(str(e)) from e
