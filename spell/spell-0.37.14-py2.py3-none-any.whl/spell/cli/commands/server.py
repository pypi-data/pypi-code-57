import click

from spell.cli.exceptions import api_client_exception_handler
from spell.cli.utils import (
    HiddenOption,
    tabulate_rows,
)

from spell.cli.commands.model_servers import (
    get,
    logs,
    remove,
    start,
    stop,
    update,
    serve,
)


@click.group(
    name="server",
    short_help="Manage model servers",
    help="""Manage model servers

             With no subcommand, displays all of your model servers""",
    invoke_without_command=True,
)
@click.option(
    "--raw", help="display output in raw format", is_flag=True, default=False, cls=HiddenOption
)
@click.pass_context
def server(ctx, raw):
    if not ctx.invoked_subcommand:
        client = ctx.obj["client"]
        with api_client_exception_handler():
            model_servers = client.get_model_servers()
        if len(model_servers) == 0:
            click.echo("There are no model servers to display.")
        else:
            data = [
                (
                    ms.get_specifier(),
                    ms.url,
                    "{}/{}".format(len([p for p in ms.pods if p.ready_at]), len(ms.pods)),
                    ms.get_age(),
                )
                for ms in model_servers
            ]
            tabulate_rows(data, headers=["NAME", "URL", "PODS (READY/TOTAL)", "AGE"], raw=raw)


server.add_command(get)
server.add_command(logs)
server.add_command(remove)
server.add_command(start)
server.add_command(stop)
server.add_command(update)
server.add_command(serve)
