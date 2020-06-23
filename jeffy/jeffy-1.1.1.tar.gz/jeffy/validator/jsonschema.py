from typing import Any, Dict

from jeffy.validator import ValidationError, Validator

import jsonschema


class JsonSchemaValidator(Validator):
    """JSON scheme validator."""

    def __init__(self, schema: Dict):
        """
        Initialize JsonSchemeValidator.

        Parameters
        ----------
        schema: Dict
        """
        self.schema = schema

    def validate(self, data: Any) -> None:
        """
        Validate the data by JSON schema.

        Parameters
        ----------
        data: Any

        Raises
        ------
        jeffy.validator.ValidationError
        """
        try:
            jsonschema.validate(data, self.schema)
        except jsonschema.ValidationError as e:
            raise ValidationError(e)
