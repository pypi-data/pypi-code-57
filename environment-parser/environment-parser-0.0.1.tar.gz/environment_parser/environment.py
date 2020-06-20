from os import environ
from .parse import parse_string
from .sources import DOTENV, SHELL


class Environment:
    """
    Object used to manage environment variables.
    """

    def __init__(self, sources=[SHELL, DOTENV]):
        """
        Object simplifying manipulation of environment variables.

        Arguments:
            items {list} -- list of dict-like items to the format [(key, val), ..., (key, val)]
        """
        self.items = {}

        for source in sources:
            if type(source) == SHELL or source == SHELL:
                self.load_from_shell()
            elif type(source) == DOTENV or source == DOTENV:
                self.load_dotenv(filepath=source.path)

    def __getitem__(self, variable):
        return self.items[variable]

    def extract_child_from_prefix(self, prefix: str, remove_prefix=False):
        """
        Create child environment from variables prefixed with given string.

        Arguments:
            prefix {str} -- substring prefixing child env variables
        """
        offset = len(prefix) * remove_prefix
        new_env = Environment(sources=[])
        new_env.add_variables([
            (item[0][offset:], item[1])
            for item in self.items.items()
            if item[0].startswith(prefix)
        ])
        return new_env

    def get(self, variable, default=None):
        """
        Get environment variable by key. Return default value if not found.

        Arguments:
            varible -- Environment variable name
            default -- (opt) Value returned if variable is not defined 
        """
        try:
            return self[variable]
        except KeyError:
            return default

    def add_variables(self, items: list):
        """
        Add a list of variables to the current environment.

        Arguments:
            items {list} -- list of (variable, value) pairs
                items[i][0] -- name of the variable
                items[i][1] -- string value of the variable
        """
        for key, value in items:
            self.items[key] = parse_string(value)

    def load_from_shell(self):
        """
        Add a list of variables defined in current shell session.
        """
        self.add_variables(environ.items())

    def load_dotenv(self, filepath='.env'):
        """
        Add a list of variables defined in a .env file.

        Arguments:
            filepath -- (opt, default to ./.env) complete or relative path to the environment file
        """
        content = open(filepath, 'rb').read().decode('utf-8')
        items = [raw_row.split('#')[0].split('=')
                 for raw_row in content.strip().split('\n')]
        self.add_variables(items)

    def __str__(self):
        """
        String tabular representation of this environment's content.
        """
        return '\n'.join(
            (
                '%-30s%-20s' % (key, str(val))
                for key, val in self.items.items()
            )
        )
