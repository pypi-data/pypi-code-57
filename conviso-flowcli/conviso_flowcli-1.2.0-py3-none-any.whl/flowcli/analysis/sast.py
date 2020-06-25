import click

from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.sast.sastbox import SASTBox
from convisoappsec.flow import GitAdapter
from convisoappsec.flowcli.common import project_code_option

@click.command()
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False,
)
@click.option(
    '-c',
    '--current-commit',
    required=False,
    help="If no value is set so the HEAD commit from the current branch is used",
)
@click.option(
    '-p',
    '--previous-commit',
    required=False,
    help="If no value is set so the empty tree hash commit is used."
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
    help="The source code repository directory.",
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    help="Enable or disable the ability of send analysis result reports to flow. When --send-to-flow option is set the --project-code option is required"
)
@help_option
@pass_flow_context
def sast(
    flow_context, project_code, current_commit,
    previous_commit, repository_dir, send_to_flow
):
    '''
      This command will perform SAST analysis at the source code. The analysis results can
      be reported or not to flow application. The analysis can be applied to specific
      commit range.

      This command will write the analysis reports files paths to stdout.
    '''
    if send_to_flow and not project_code:
        raise click.MissingParameter(
            'It is required when sending reports to flow api.',
            param_type='option',
            param_hint='--project-code',
         )

    try:
        git_adapater = GitAdapter(repository_dir)

        current_commit = current_commit if current_commit else git_adapater.head_commit
        previous_commit = previous_commit if previous_commit else git_adapater.empty_repository_tree_commit

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

        if send_to_flow:
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

command = 'flow analysis sast'

sast.short_help = "Perform SAST analysis".format(
    command=command
)

sast.epilog = '''
Examples:

  \b
  1 - Reporting the results to flow api:
    1.1 - Running an analysis at all commit range:
      $ export FLOW_API_KEY='your-api-key'
      $ export FLOW_PROJECT_CODE='your-project-code'
      $ {command}

    \b
    1.2 - Running an analysis at specific commit range:
      $ # running sast at head commit and 5 behind commits
      $ export FLOW_API_KEY='your-api-key'
      $ export FLOW_PROJECT_CODE='your-project-code'
      $ {command} --current-commit "$(git rev-parse HEAD)" --previous-commit "$(git rev-parse HEAD~5)"

  \b
  2 - Not Reporting the results to flow api:
    Note that when not reporting the results the FLOW_PROJECT_CODE is not necessary.

    \b
    2.1 - Running an analysis at all commit range:
      $ export FLOW_API_KEY='your-api-key'
      $ {command} --no-send-to-flow

    \b
    2.2 - Running an analysis at specific commit range:
      $ # running sast at head commit and 5 behind commits
      $ export FLOW_API_KEY='your-api-key'
      $ {command} --no-send-to-flow --current-commit "$(git rev-parse HEAD)" --previous-commit "$(git rev-parse HEAD~5)"

'''.format(
    command=command,
)
