import typer
from uvicore import app, config


cli = typer.Typer()

@cli.command()
def version(version: bool = typer.Option(None, "--version", "-v")):
    """Uvicorn Version"""
    typer.echo('1.0.0')

    #server = import_module(app.name + '.http.server.Web')[0]()
    #server.run()


    #app.create_flask_app()
    #app.serve_flask()


# class Flask(import_name: str,
# static_url_path: Optional[str]=...,
# static_folder: Optional[str]=...,
# static_host: Optional[str]=...,
# host_matching: bool=...,
# subdomain_matching: bool=...,
# template_folder: str=...,
# instance_path: Optional[str]=...,
# instance_relative_config: bool=...,
# root_path: Optional[str]=...)
