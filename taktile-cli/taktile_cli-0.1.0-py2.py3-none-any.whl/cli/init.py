import logging

import click

from tktl.commands.init import init_project

_logger = logging.getLogger("root")


@click.command()
@click.option("--name", help="Name of the project", default="tktl-serving")
@click.option(
    "--path", help="Directory where the new project will be created", default="."
)
def init(path: str, name: str) -> None:
    """Creates a new project with the necessary scaffolding, as well as the supporting
        files needed. The directory structure of a new project , and the files within it
        will look like this::

            regression.py         # Regression starter file
            classification.py     # Classification starter file
            racket.yaml           # Main project config file
            .gitignore            # Just in case
            Dockerfile.tfserving  # TFS' Dockerfile]
            Dockerfile.racket     # racket's Dockerfile. To be implemented
            docker-compose.yaml   # Docker-compose to start up TFS
            serialized/           # Where the serialized models will be stored

        """
    init_project(path=path, name=name)
