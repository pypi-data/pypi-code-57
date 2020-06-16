from subprocess import CalledProcessError

import pytest

from zypper_patch_status_collector._zypper import (
    Patch,
    check_needs_reboot,
    get_applicable_patches,
    get_lifecycle_info,
    get_services_needing_restart,
)
from .mock import (
    assert_needs_reboot_use,
    assert_ps_mock_use,
    assert_zypper_mock_use,
    mock_needs_reboot_call,
    mock_ps_call,
    mock_zypper_call,
)


def test_no_patches(mocker):
    zypper_mock = mock_zypper_call(mocker, 'tests/fixtures/empty.xml')

    assert len(get_applicable_patches()) == 0

    assert_zypper_mock_use(zypper_mock)


def test_all_categories_and_severities(mocker):
    zypper_mock = mock_zypper_call(mocker, 'tests/fixtures/all.xml')

    patches = get_applicable_patches()
    assert len(patches) == 8
    assert Patch('security', 'important') in patches
    assert Patch('document', 'unspecified') in patches
    assert Patch('yast', 'important') not in patches

    assert_zypper_mock_use(zypper_mock)


def test_compatibility():
    """Test that we don't crash when calling the sytem's zypper application"""
    get_applicable_patches()


def test_needs_reboot(mocker):
    zypper_mock = mock_needs_reboot_call(mocker, True)

    assert check_needs_reboot()

    assert_needs_reboot_use(zypper_mock)


def test_needs_no_reboot(mocker):
    zypper_mock = mock_needs_reboot_call(mocker, False)

    assert not check_needs_reboot()

    assert_needs_reboot_use(zypper_mock)


def test_needs_reboot_failed(mocker):
    mock_needs_reboot_call(mocker, False, True)

    with pytest.raises(CalledProcessError):
        check_needs_reboot()


def test_lifecycle():
    eols = get_lifecycle_info()
    assert(len(eols) >= 1)


@pytest.mark.parametrize(
    'expected', [
        {'apache', 'postgresql'},
        set(),
    ]
)
def test_get_services_needing_restart(mocker, expected):
    zypper_mock = mock_ps_call(mocker, *expected)

    assert expected == get_services_needing_restart()

    assert_ps_mock_use(zypper_mock)
