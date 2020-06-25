import os
import signal


def kill_multiprocess(cmd: str):
    """
    kill processes with the same command
    """
    assert isinstance(cmd, str)

    # kill processes with the same command
    os.system(
        'for pid in $(ps -ef | grep ' + cmd +
        '| awk \'{print $2}\'); do kill -9 $pid; done')


def kill_process(pid: str):
    """
    kill a process given its PID
    """
    assert isinstance(pid, str)
    os.kill(pid, signal.SIGKILL)
