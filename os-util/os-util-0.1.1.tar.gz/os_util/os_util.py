
from shell_util import shell
from os_util.result import Result


def which(command):

    shell_command = f"which {command}"
    shell_result = shell.run_command_and_get_shell_result(shell_command)
    result = Result(status=shell_result.status, value=shell_result.output)

    return result


