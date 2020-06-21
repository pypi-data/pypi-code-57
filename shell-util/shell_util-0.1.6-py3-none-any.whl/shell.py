
import subprocess
import shlex
from subprocess import check_output, STDOUT, CalledProcessError

from shell_util.shell_result import ShellResult


def run_command(command, stdout=None, in_dir=None):

    command_split = shlex.split(command)
    result = subprocess.call(command_split, stdout=stdout, cwd=in_dir)

    return result


def run_command_and_get_shell_result(command):

    command_split = shlex.split(command)
    shell_status, output = _get_status_and_output(command_split)
    shell_result = ShellResult(shell_status, output, command)

    return shell_result


def _get_status_and_output(command_split):

    try:
        data = check_output(command_split, universal_newlines=True, stderr=STDOUT)
        exitcode = 0
    except CalledProcessError as ex:
        data = ex.output
        exitcode = ex.returncode
    if data[-1:] == '\n':
        data = data[:-1]
    return exitcode, data

