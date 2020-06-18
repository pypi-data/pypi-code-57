import click, os

try:
    from geccoi import GeccoiApp
    app = GeccoiApp()

except ModuleNotFoundError as err:
    click.echo("Some modules not found. \n    Installing them now:")
    for package in ["PySimpleGUI", "keyboard", "mouse", "opencv-contrib-python-headless", "numpy", "click"]:
        os.system(f"pip install {package}")

    from geccoi import GeccoiApp
    app = GeccoiApp()




@click.group()
@click.option("--description", is_flag=True, help="Show the description of this interface.")
def cli(description):
    if description:
        click.echo("GeCLI for interacting with the GeCCOI application.")


@click.command(help="The AI part of GeCCOI.")
@click.option("-s", "--start", "start", is_flag=True)
@click.option("-q", "--quit", "quit", is_flag=True)
@click.option("-d", "--debug", "debug", is_flag=True)
def ai(start, quit, debug):
    if start is True and quit is True:
        raise ValueError("Option -s/--start cannot be used with -q/--quit")

    if start:
        if debug:
            click.echo("AI Process Started")

    if quit:
        if debug:
            click.echo("AI Process Quit")


@click.command(help="The GUI part of GeCCOI.")
@click.option("-s", "--start", "start", is_flag=True)
@click.option("-d", "--debug", "debug", is_flag=True)
def gui(start, debug):
    if start:
        if debug:
            click.echo("GUI Process Started...")


        app.start_gui(debug)


        if debug:
            click.echo("GUI Closed")


cli.add_command(ai)
cli.add_command(gui)


if __name__ == '__main__':
    cli()

