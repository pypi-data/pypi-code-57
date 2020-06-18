class ValidationError(Exception):
    pass


class MissingParameters(ValidationError):
    pass
