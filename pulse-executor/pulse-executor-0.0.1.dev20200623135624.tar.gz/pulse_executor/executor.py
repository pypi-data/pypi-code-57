import sys
import signal
import importlib
import os
import pathlib

from pulse_executor import status

HOME_DIR = pathlib.Path.home() / ".pulse-program-executor"

ACTIVE_PROGRAM_PID_FILE = HOME_DIR / "active-program-pid"
ERROR_FILE = HOME_DIR / "active-program-error.log"
ACTIVE_PROGRAM_STATUS_FILE = HOME_DIR / "active-program-status"

PROGRAM_EXECUTOR_STATUS = status.Executor.ACTIVE

def _store_pid() -> None:
    with open(ACTIVE_PROGRAM_PID_FILE, "w") as pidfile:
        pidfile.write(str(os.getpid()))


def _cleanup() -> None:
    if os.path.exists(ACTIVE_PROGRAM_PID_FILE):
        os.remove(ACTIVE_PROGRAM_PID_FILE)


def _prepare_directories() -> None:
    os.makedirs(HOME_DIR, exist_ok=True)


def _subscribe_on_sigint(program_instance) -> None:
    def wrap_after_all(signum, frame):
        try:
            program_instance.after_all()
        except Exception as e:
            _write_status(status.Program.ERROR)
            _write_error_file(e)
            program_instance.on_error(e)
        else:
            _write_status(status.Program.CANCELLED)
        finally:
            _cleanup()
        sys.exit()

    signal.signal(signal.SIGINT, wrap_after_all)


def _subscribe_on_sigquit() -> None:
    def smart_stop_on_sigquit(signum, frame):
        global PROGRAM_EXECUTOR_STATUS
        PROGRAM_EXECUTOR_STATUS = status.Executor.SMART_STOP

    signal.signal(signal.SIGQUIT, smart_stop_on_sigquit)


def _write_status(program_status: status.Program) -> None:
    with open(ACTIVE_PROGRAM_STATUS_FILE, "w") as sf:
        sf.write(program_status.value)


def _write_error_file(exc_value):
    with open(ERROR_FILE, "w") as ef:
        ef.write(str(exc_value))


def _executor_is_running():
    global PROGRAM_EXECUTOR_STATUS
    return PROGRAM_EXECUTOR_STATUS is status.Executor.ACTIVE


def run(program_name: str, robot_address: str) -> None:
    program = importlib.import_module(program_name + ".program")
    try:
        _prepare_directories()
        _store_pid()
        with program.Instance(robot_address) as p:
            _subscribe_on_sigint(p)
            _subscribe_on_sigquit()
            _write_status(status.Program.RUNNING)

            p.before_all()
            while _executor_is_running():
                p.before_each()
                p.execute()
                p.after_each()
            p.after_all()
            _cleanup()
    except Exception as e:
        _write_status(status.Program.ERROR)
        _write_error_file(e)
    else:
        _write_status(status.Program.FINISHED)


def die() -> None:
    with open(ACTIVE_PROGRAM_PID_FILE) as pidfile:
        pid = int(pidfile.read().strip())
        os.kill(pid, signal.SIGINT)


def read_status() -> str:
    with open(ACTIVE_PROGRAM_STATUS_FILE) as sf:
        return sf.read().strip()


def read_error() -> str:
    with open(ERROR_FILE) as ef:
        return ef.read()


def smart_stop() -> str:
    with open(ACTIVE_PROGRAM_PID_FILE) as pidfile:
        pid = int(pidfile.read().strip())
        os.kill(pid, signal.SIGQUIT)
