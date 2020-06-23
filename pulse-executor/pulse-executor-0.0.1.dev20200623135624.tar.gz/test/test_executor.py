import signal
from pulse_executor import executor, status

ROBOT = "localhost:8081"

def test_die_calls_os_kill(mocker):
    test_pid = "111111"
    mocker.patch("builtins.open", mocker.mock_open(read_data=test_pid))
    kill_patch = mocker.patch("os.kill")

    executor.die()

    kill_patch.assert_called_once_with(int(test_pid), signal.SIGINT)


def test_die_opens_pid_file(mocker):
    test_pid = "111111"
    open_patch = mocker.patch(
        "builtins.open", mocker.mock_open(read_data=test_pid)
    )
    mocker.patch("os.kill")

    executor.die()

    open_patch.assert_called_once_with(executor.ACTIVE_PROGRAM_PID_FILE)


def test_smart_stop_calls_os_kill(mocker):
    test_pid = "111111"
    mocker.patch("builtins.open", mocker.mock_open(read_data=test_pid))
    kill_patch = mocker.patch("os.kill")

    executor.smart_stop()

    kill_patch.assert_called_once_with(int(test_pid), signal.SIGQUIT)


def test_read_status_opens_status_file(mocker):
    open_patch = mocker.patch(
        "builtins.open", mocker.mock_open(read_data="test")
    )

    executor.read_status()

    open_patch.assert_called_once_with(executor.ACTIVE_PROGRAM_STATUS_FILE)


def test_read_error_opens_error_file(mocker):
    open_patch = mocker.patch(
        "builtins.open", mocker.mock_open(read_data="test")
    )

    executor.read_error()

    open_patch.assert_called_once_with(executor.ERROR_FILE)


def test_run_does_import_by_name(mocker):
    mocker.patch.object(executor, "_executor_is_running", return_value=False)
    mocker.patch.object(executor, "_subscribe_on_sigint")
    mocker.patch.object(executor, "_write_status")

    import_patch = mocker.patch("importlib.import_module")
    test_program_name = "some_program"

    executor.run(test_program_name, ROBOT)

    import_patch.assert_called_once_with(test_program_name + ".program")


def test_run_subscribes_on_sigint(mocker):
    mocker.patch.object(executor, "_executor_is_running", return_value=False)
    mocker.patch.object(executor, "_subscribe_on_sigquit")
    mocker.patch("importlib.import_module")
    mocker.patch.object(executor, "_write_status")

    signal_patch = mocker.patch("signal.signal")

    executor.run("test", ROBOT)

    signal_patch.assert_called_with(signal.SIGINT, mocker.ANY)


def test_run_subscribes_on_sigquit(mocker):
    mocker.patch.object(executor, "_executor_is_running", return_value=False)
    mocker.patch("importlib.import_module")
    mocker.patch.object(executor, "_write_status")
    
    signal_patch = mocker.patch("signal.signal")

    executor.run("test", ROBOT)
    
    signal_patch.assert_called_with(signal.SIGQUIT, mocker.ANY)


def test_run_writes_error_status_on_exception(mocker):
    mocker.patch.object(
        executor, "_executor_is_running", side_effect=Exception("Boom!")
    )
    mocker.patch("importlib.import_module")
    mocker.patch.object(executor, "_subscribe_on_sigint")
    mocker.patch("builtins.open", mocker.mock_open())

    write_patch = mocker.patch.object(executor, "_write_status")

    executor.run("test", ROBOT)

    write_patch.assert_called_with(status.Program.ERROR)


def test_run_writes_error_on_exception(mocker):
    exc = Exception("Boom!")
    mocker.patch.object(executor, "_executor_is_running", side_effect=exc)
    mocker.patch("importlib.import_module")
    mocker.patch.object(executor, "_subscribe_on_sigint")
    mocker.patch.object(executor, "_write_status")

    open_patch = mocker.patch("builtins.open", mocker.mock_open())

    executor.run("test", ROBOT)

    assert mocker.call().write(str(exc)) in open_patch.mock_calls

def test_run_stores_pid(mocker):
    mocker.patch.object(executor, "_executor_is_running", return_value=False)
    mocker.patch("importlib.import_module")
    mocker.patch.object(executor, "_write_status")
    mocker.patch.object(executor, "_subscribe_on_sigint")

    store_pid_patch = mocker.patch.object(executor, "_store_pid")

    executor.run("test", ROBOT)

    store_pid_patch.assert_called_once()
