
# Base


class ApplicationError(Exception):
    """Application's base error class."""


# Repositories


class RepositoryError(ApplicationError):
    """Repositories' base error class."""


class EntityNotFoundError(RepositoryError):
    """The entity was not found in the repository."""


class EntityValidationError(RepositoryError):
    """Entity consistency validation error"""


# Coordinators


class CoordinatorError(ApplicationError):
    """Coordinators' base error class."""


class DataValidationError(CoordinatorError):
    """Data Validation Error."""
