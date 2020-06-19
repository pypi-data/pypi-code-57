import sys
from typing import Optional, List

from envvarconf.inspection import get_settings_variables
from envvarconf.printing import get_tty_width, truncatestring
from envvarconf.validation import validate_definition, validation_errors

from envvarconf.loaders.base import BaseLoader


class BaseSettings:
    def __init__(self, appname: str = ""):
        self.appname = appname
        validate_definition(self)

    def load(self, loaders: List[BaseLoader], failfast=True, truncate_width: Optional[int] = None):
        """
        Load settings using `loader`

        :param loaders: List of loaders instance, see `loaders` module
        :param truncate_width: Truncate output width, default using terminal width
        :param failfast: If settings is not valid print help then exit, else do nothing
        """

        for loader in loaders:
            loader.load(self)

        errors = validation_errors(self)
        if errors:
            print("There is errors in settings")
            print("\n".join([f" * {x}" for x in errors]))
            print()

            if failfast:
                self.print_detailed_settings(truncate_width=truncate_width)
                sys.exit(1)

    def print_detailed_settings(self, truncate_width: Optional[int] = None):
        """
        Pring each settings variable and value

        :param truncate_width: Truncate output width, default using terminal width
        """
        if truncate_width is None:
            truncate_width = get_tty_width()
        print(f"{self.appname or 'Application'} settings:")

        for varname, vartype in get_settings_variables(self).items():
            varval = str(getattr(self, varname, "NOT DEFINED!"))
            print(truncatestring(f"{varname}:{vartype.__name__} = {varval}", width=truncate_width, placeholder="..."))

    def __str__(self):
        vs = [f"{var_name}={getattr(self, var_name, '?')}" for var_name in get_settings_variables(self).keys()]
        return f"<{self.__class__.__name__} {', '.join(vs)}>"
