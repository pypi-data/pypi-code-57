import json
import os
from typing import Any, Dict

from click import ClickException
import jsonschema
import ray

from anyscale.util import slugify


# Pathnames specific to Ray's project directory structure.
PROJECT_ID_BASENAME = "project-id"
RAY_PROJECT_DIRECTORY = "ray-project"


def validate_project_schema(project_config: Dict[str, str]) -> Any:
    """Validate a project config against the project schema.
    Args:
        project_config (dict): Parsed project yaml.
    Raises:
        jsonschema.exceptions.ValidationError: This exception is raised
            if the project file is not valid.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir, "ProjectConfig.json")) as f:
        schema = json.load(f)

    jsonschema.validate(instance=project_config, schema=schema)


def load_project_or_throw() -> Any:
    ray.projects.projects.validate_project_schema = validate_project_schema
    try:
        project = ray.projects.ProjectDefinition(os.getcwd())
    except (jsonschema.exceptions.ValidationError, ValueError) as e:
        raise ClickException(e)  # type: ignore

    dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir, "anyscale_schema.json")) as f:
        schema = json.load(f)

    # Validate the project file.
    try:
        jsonschema.validate(instance=project.config, schema=schema)
    except (jsonschema.exceptions.ValidationError, ValueError) as e:
        raise ClickException(e)  # type: ignore

    # Normalize project name
    project.config["name"] = slugify(project.config["name"])

    return project


def get_project_id(project_dir: str) -> int:
    """
    Args:
        project_dir: Project root directory.

    Returns:
        The ID of the associated Project in the database.

    Raises:
        ValueError: If the current project directory does
            not contain a project ID.
    """
    project_id_filename = os.path.join(
        project_dir, RAY_PROJECT_DIRECTORY, PROJECT_ID_BASENAME
    )
    if not os.path.isfile(project_id_filename):
        raise ClickException(
            "Ray project in {} not registered yet. "
            "Did you run 'any project create'?".format(project_dir)
        )
    with open(project_id_filename, "r") as f:
        project_id = f.read()
    try:
        result = int(project_id)
    except ValueError:
        raise ClickException(
            "{} does not contain a valid project ID".format(project_id_filename)
        )
    return result
