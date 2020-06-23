import argparse
import pytest

from pulse_executor import cli, executor

ROBOT = "localhost:8080"
cli.ROBOT_ADDRESS = ROBOT

def test_cli_stop_calls_executor_die(mocker):
    die_patch = mocker.patch.object(executor, "die")
    
    cli.stop()

    die_patch.assert_called_once()


def test_cli_status_calls_executor_status(mocker):
    status_patch = mocker.patch.object(executor, "read_status")
    
    cli.status()

    status_patch.assert_called_once()


def test_cli_read_error_calls_executor_read_error(mocker):
    read_error_patch = mocker.patch.object(executor, "read_error")
    
    cli.read_error()

    read_error_patch.assert_called_once()


def test_cli_run_calls_executor_run(mocker):
    run_patch = mocker.patch.object(executor, "run")
    mocker.patch.object(
        cli, "parse_args", return_value=argparse.Namespace(executable="test")
    )
    
    cli.main()
    
    run_patch.assert_called_once_with("test", ROBOT)


def test_cli_fails_on_empty_robot_address(mocker):
    mocker.patch.object(
        cli, "parse_args", return_value=argparse.Namespace(executable="test")
    )

    cli.ROBOT_ADDRESS = None

    with pytest.raises(EnvironmentError):
        cli.main()

def test_cli_smart_stop_calls_executor_smart_stop(mocker):
    smart_stop_patch = mocker.patch.object(executor, "smart_stop")
    
    cli.smart_stop()
    
    smart_stop_patch.assert_called_once()
