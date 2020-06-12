import click

from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.sast.sastbox import SASTBox
from convisoappsec.flow import GitAdapter


@click.command()
@click.argument(
    'project-code',
    required=False,
)
@click.option(
    '-c',
    '--current-commit',
    required=False,
)
@click.option(
    '-p',
    '--previous-commit',
    required=False,
)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
)
@help_option
@pass_flow_context
def sast(flow_context, project_code, current_commit, previous_commit, repository_dir):
    try:
        git_adapater = GitAdapter(repository_dir)

        current_commit = current_commit if current_commit else git_adapater.current_commit
        previous_commit = previous_commit if previous_commit else git_adapater.previous_commit

        flow = flow_context.create_flow_api_client()
        token = flow.docker_registry.get_sast_token()
        sastbox = SASTBox()
        sastbox.login(token)
        reports = sastbox.run_scan_diff(
            repository_dir, current_commit, previous_commit
        )

        if project_code:
            default_report_type = "sast"
            commit_refs = git_adapater.show_commit_refs(
                current_commit
            )

            reports_files = [
                r.open() for r in reports
            ]
            reports_files_ctx = click.progressbar(
                reports_files,
                label="Sending sast reports to flow application"
            )

            with reports_files_ctx as reports:
                for report in reports:
                    flow.findings.create(
                        project_code,
                        commit_refs,
                        report,
                        default_report_type=default_report_type
                    )

        for r in reports:
            click.echo(r)

    except Exception as e:
        raise click.ClickException(str(e)) from e
