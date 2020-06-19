from typing import List

from envvarconf.converters.base import ALLOWED_TYPES
from envvarconf.inspection import get_settings_variables


def validate_definition(settings):
    """
    Check class definition is valid

    :raises: TypeError when class definition is wrong
    """
    for varname, vartype in get_settings_variables(settings).items():
        if vartype not in ALLOWED_TYPES:
            raise TypeError(f"Variable {varname} marked {vartype}, that not allowed for settings use")


def validation_errors(settings) -> List[str]:
    """
    Get settings validation_errors

    :return: List of strings, representing errors detail
    """
    errs = []
    for varname, vartype in get_settings_variables(settings).items():
        if not hasattr(settings, varname):
            errs.append(f"{varname} is not defined")
    return errs
