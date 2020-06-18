from unittest.mock import Mock, patch
from pytest import raises
from lb_utils.shell_utils import ShellUtils
from subprocess import Popen, CalledProcessError


@patch('lb_utils.shell_utils.Popen')
def test_run_in_shell_with_input(mock_popen):
    process_mock = Mock()
    attrs = {
        'communicate.return_value': ('output'.encode(), 'error'),
        'returncode': None
    }
    process_mock.configure_mock(**attrs)

    mock_popen.return_value = process_mock
    output = ShellUtils.run_in_shell(['ls'], 'some input')

    assert mock_popen.called
    assert output == 'output'


@patch('lb_utils.shell_utils.Popen')
def test_run_in_shell_without_input(mock_popen):
    process_mock = Mock()
    attrs = {
        'communicate.return_value': ('output'.encode(), 'error'),
        'returncode': None
    }
    process_mock.configure_mock(**attrs)

    mock_popen.return_value = process_mock
    output = ShellUtils.run_in_shell(['ls'])

    assert mock_popen.called
    assert output == None


@patch('lb_utils.shell_utils.Popen')
def test_run_in_shell_raises_error(mock_popen):
    process_mock = Mock()
    attrs = {'communicate.return_value': ('output'.encode(), 'error')}
    process_mock.configure_mock(**attrs)

    mock_popen.return_value = process_mock

    with raises(CalledProcessError):
        ShellUtils.run_in_shell(['ls'], 'some input')
