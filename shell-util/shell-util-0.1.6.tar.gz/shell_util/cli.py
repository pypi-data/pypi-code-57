import click
from shell_util import shell


@click.group()
def cli():
    return True


@cli.command()
@click.argument('command_args', nargs=-1)
def run_command(command_args):

    command = ' '.join(command_args)
    shell.run_command(command)


@cli.command()
@click.argument('command_args', nargs=-1, required=True)
def run_command_and_get_result_object(command_args):

    command = ' '.join(command_args)
    result = shell.run_command_and_get_shell_result(command)
    print(result.command)
    print(result)
    print(result.output)


if __name__ == '__main__':
    cli()
