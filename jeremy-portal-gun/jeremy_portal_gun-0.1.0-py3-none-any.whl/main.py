import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    :return:
    """


@app.command()
def shoot():
    """SHOOT GUN"""
    typer.echo("shoot")


@app.command()
def load():
    "Load the portal gun"
    typer.echo("loading the protal gunnnn")
