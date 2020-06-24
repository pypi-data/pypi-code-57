import logging

import click

from tktl.commands.validate import validate_project_config

_logger = logging.getLogger("root")


@click.command()
@click.option(
    "--path", "-p", help="Directory where the new project will be created", default="."
)
def validate(path) -> None:
    """Validates a new project for the necessary scaffolding, as well as the supporting
        files needed. The directory structure of a new project, and the files within it
        should look like this::

            regression.py         # Regression starter file
            classification.py     # Classification starter file
            tktl.yaml             # Main project config file
            .gitignore            # Just in case
            Dockerfile.tfserving  # TFS' Dockerfile]
            Dockerfile.racket     # racket's Dockerfile. To be implemented
            docker-compose.yaml   # Docker-compose to start up TFS

        """

    validate_project_config(path=path)
