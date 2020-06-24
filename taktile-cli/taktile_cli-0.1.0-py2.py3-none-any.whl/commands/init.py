import os

from tktl.core.loggers import CliLogger
from tktl.core.managers.project import ProjectManager

logger = CliLogger()


def init_project(path: str, name: str):
    ProjectManager.init_project(path, name)
    logger.log(
        f"Project scaffolding created successfully "
        f"at {os.path.abspath(path)}/{name}",
        color="green",
    )
