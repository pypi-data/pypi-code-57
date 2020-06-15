
import subprocess
import shlex

from shell_util.shell_result import ShellResult


def run_command(command, stdout=None, in_dir=None):

    command_split = shlex.split(command)
    result = subprocess.call(command_split, stdout=stdout, cwd=in_dir)

    return result


def run_command_and_get_shell_result(command):

    command_split = shlex.split(command)
    status, output = subprocess.getstatusoutput(command_split)
    shell_result = ShellResult(status, output, command)

    return shell_result


