import click

try:
    from geccoi import GeccoiApp
    app = GeccoiApp()

except ModuleNotFoundError as err:
    click.echo(err)



@click.command(help="The Gecco")
@click.option("-s", "--start", "start", is_flag=True, help="Launches the Geccoi user interface")
@click.option("-d", "--debug", "debug", is_flag=True, help="Will turn the debug mode on, if launched.")
@click.option("--description", is_flag=True, help="Shows the description of this interface.")
def cli(start, debug, description):
    if description:
        click.echo("Geccoi CLI")

    if start:
        if debug:
            click.echo("Geccoi Started...")

        app.start_gui(debug)

        if debug:
            click.echo("Geccoi Closed.")


if __name__ == '__main__':
    cli()

