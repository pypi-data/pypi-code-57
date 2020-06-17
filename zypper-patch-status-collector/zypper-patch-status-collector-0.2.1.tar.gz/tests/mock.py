from subprocess import CalledProcessError
from unittest.mock import NonCallableMock


def mock_zypper_call(mocker, result_filename):
    mock = mocker.patch(
        'subprocess.check_output'
    )
    mock.return_value = open(result_filename).read()
    return mock


def assert_zypper_mock_use(mock):
    assert mock.call_args[0][0][0] == 'zypper'
    assert mock.call_args[0][0][-1] == 'list-patches'
    assert '--xmlout' in mock.call_args[0][0]


def mock_needs_reboot_call(mocker, needs_reboot: bool, fail: bool = False):
    mock = mocker.patch(
        'subprocess.run'
    )
    mock.return_value = NonCallableMock(**{
        'returncode': 1 if fail else 102 if needs_reboot else 0,
        'check_returncode.side_effect': CalledProcessError(
            1,
            'zypper'
        )
    })
    return mock


def assert_needs_reboot_use(mock):
    assert mock.call_args[0][0][0] == 'zypper'
    assert mock.call_args[0][0][-1] == 'needs-rebooting'


def mock_ps_call(mocker, *services):
    mock = mocker.patch(
        'subprocess.check_output'
    )
    mock.return_value = '\n'.join(services) + '\n'
    return mock


def assert_ps_mock_use(mock):
    assert mock.call_args[0][0][0] == 'zypper'
    assert mock.call_args[0][0][1] == 'ps'
    assert '-sss' in mock.call_args[0][0]
