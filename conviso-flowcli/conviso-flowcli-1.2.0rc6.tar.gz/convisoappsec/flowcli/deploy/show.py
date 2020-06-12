import click

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import DeployFormatter


@click.command()
@help_option
@click.argument('project-code', required=True)
@click.argument('current-tag', required=True)
@click.option(
    '-o',
    '--output-format',
    required=False,
    type=click.Choice(DeployFormatter.FORMATS()),
    default=DeployFormatter.DEFAULT,
    show_default=True,
)
@pass_flow_context
def show(flow_context, project_code, current_tag, output_format):
    try:
        flow = flow_context.create_flow_api_client()
        deploy = flow.deploys.get(project_code, current_tag)
        formatter = DeployFormatter(deploy)
        click.echo(
            formatter.format_as(output_format)
        )
    except Exception as e:
        raise click.ClickException(str(e)) from e

