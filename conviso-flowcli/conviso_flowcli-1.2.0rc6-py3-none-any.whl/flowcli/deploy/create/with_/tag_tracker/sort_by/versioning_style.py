import click

from convisoappsec.flow import api
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flow.version_searchers import SortedByVersioningStyle
from convisoappsec.flow.version_control_system_adapter import GitAdapter
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli import common

from convisoappsec.flowcli.deploy.create.with_.tag_tracker.context import (
    pass_tag_tracker_context
)

@click.command()
@click.argument("project-code", required=True)
@click.argument('current-tag', required=False)
@click.option(
    '-i',
    '--ignore-prefix',
    required=False,
    default='v',
    show_default=True,
    help="Prefix to be ignored on parsing to versioning style.",
)
@click.option(
    '-s',
    '--style',
    required=False,
    type=click.Choice(SortedByVersioningStyle.STYLES),
    default=SortedByVersioningStyle.SEMANTIC_VERSIONING_STYLE,
    show_default=True,
    help="Versioning style type used at repository.",
)
@click.option(
    "--attach-diff/--no-attach-diff",
    default=True,
    show_default=True,
    required=False,
)
@help_option
@pass_tag_tracker_context
@pass_flow_context
def versioning_style(
    flow_context, tag_tracker_context, ignore_prefix, style,
    project_code, current_tag, attach_diff
):
    try:
        repository_dir = tag_tracker_context.repository_dir
        git_adapter = GitAdapter(repository_dir)

        searcher = SortedByVersioningStyle(
            git_adapter,
            ignore_prefix,
            style,
            current_tag,
        )

        result = searcher.find_current_and_previous_version()
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

        common.notify_created_deploy(deploy)
    except Exception as e:
        raise click.ClickException(str(e)) from e
