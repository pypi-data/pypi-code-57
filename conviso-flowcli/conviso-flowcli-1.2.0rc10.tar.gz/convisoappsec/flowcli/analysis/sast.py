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
        log_func('Checking SASTBox authorization...')
        sastbox.login(token)

        with click.progressbar(length=sastbox.size, label='Performing SASTBox download...') as progressbar:
            for downloaded_chunk in sastbox.pull():
                progressbar.update(downloaded_chunk)

        log_func('Starting SASTBox scandiff...')

        reports = sastbox.run_scan_diff(
            repository_dir, current_commit, previous_commit, log=log_func
        )

        log_func('SASTBox scandiff done')

        report_names = [
            str(r) for r in reports
        ]

        if project_code:
            default_report_type = "sast"
            commit_refs = git_adapater.show_commit_refs(
                current_commit
            )

            report_names_ctx = click.progressbar(
                report_names,
                label="Sending SASTBox reports to flow application"
            )

            with report_names_ctx as reports:
                for report_name in reports:
                    report_file = open(report_name)

                    flow.findings.create(
                        project_code,
                        commit_refs,
                        report_file,
                        default_report_type=default_report_type
                    )

                    report_file.close()

        for r in report_names:
            click.echo(r)


    except Exception as e:
        raise click.ClickException(str(e)) from e

def log_func(msg, new_line=True, clear=False):
    click.echo(msg, nl=new_line, err=True)
