from pydantic import ValidationError

from tktl.core.exceptions.exceptions import (
    NoContentsFoundException,
    UserRepoValidationException,
)
from tktl.core.loggers import CliLogger
from tktl.core.managers.project import ProjectManager
from tktl.core.schemas.project import ProjectValidationOutput
from tktl.core.validation.outputs import (
    ProjectValidationFailure,
    ConfigFileValidationFailure,
)

logger = CliLogger()


def validate_project_config(path: str):
    try:
        ProjectManager.validate_project_config(path)
    except ValidationError as e:
        validation_output = ProjectValidationOutput(
            title=ConfigFileValidationFailure.title,
            summary=ConfigFileValidationFailure.summary,
            text=ConfigFileValidationFailure.format_step_results(validation_errors=e),
        )
        log_failure(validation_output)
        return
    except (NoContentsFoundException, UserRepoValidationException) as e:
        validation_output = ProjectValidationOutput(
            title=ProjectValidationFailure.title,
            summary=ProjectValidationFailure.summary,
            text=ProjectValidationFailure.format_step_results(validation_errors=e),
        )
        log_failure(validation_output)
        return
    logger.log(f"Project scaffolding is valid!", color="green")


def log_failure(validation_output: ProjectValidationOutput):
    logger.log(
        f"Project scaffolding is invalid: {validation_output.title}", color="red"
    )
    logger.log(validation_output.summary, color="red", err=True)
    logger.log(validation_output.text, color="red", err=True)
