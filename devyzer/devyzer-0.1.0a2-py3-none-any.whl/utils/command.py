import inspect

# from devyzer_cli.compat import exec_command_rc, exec_command
import requests
from git import Repo, exc

from devyzer.constants import AUTOCOMPLETE_ENDPOINT
from devyzer.state import SessionState

try:
    WindowsError
except NameError:
    # No running on Windows
    WindowsError = FileNotFoundError


#
# def get_repo_revision():
#     path = os.path  # shortcut
#     gitdir = path.normpath(path.join(path.dirname(os.path.abspath(__file__)), '..', '..', '.git'))
#     cwd = os.path.dirname(gitdir)
#     if not path.exists(gitdir):
#         try:
#             from ._gitrevision import rev
#             if not rev.startswith('$'):
#                 # the format specifier has been substituted
#                 return '+' + rev
#         except ImportError:
#             pass
#         return ''
#     try:
#         # need to update index first to get reliable state
#         exec_command_rc('git', 'update-index', '-q', '--refresh', cwd=cwd)
#         recent = exec_command('git', 'describe', '--long', '--dirty', '--tag',
#                               cwd=cwd).strip()
#         if recent.endswith('-dirty'):
#             tag, changes, rev, dirty = recent.rsplit('-', 3)
#             rev = rev + '.mod'
#         else:
#             tag, changes, rev = recent.rsplit('-', 2)
#         if changes == '0':
#             return ''
#         # According to pep440 local version identifier starts with '+'.
#         return '+' + rev
#     except (FileNotFoundError, WindowsError):
#         # Be silent when git command is not found.
#         pass
#     return ''


def all_subclasses(cls):
    # type: (Any) -> List[Any]
    """Returns all known (imported) subclasses of a class."""

    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


def arguments_of(func):
    """Return the parameters of the function `func` as a list of their names."""

    try:
        # python 3.x is used
        return inspect.signature(func).parameters.keys()
    except AttributeError:
        pass


def filter_configuration_file(config):
    """Return project configuration after filtering"""
    if "accessToken" in config:
        del config['accessToken']
    if "lastConfig" in config:
        del config['lastConfig']
    if "history" in config:
        del config['history']
    return config


def is_command(text):
    URL = AUTOCOMPLETE_ENDPOINT + "/check_command"
    PARAMS = {'query': text, 'userid': SessionState.mac_ip, 'store': True}
    # Get list of words.
    result = requests.get(url=URL, params=PARAMS)
    data = result.json()
    return data["success"]


def is_git_repo(path):
    try:
        _ = Repo(path).git_dir
        return True
    except exc.InvalidGitRepositoryError:
        return False
