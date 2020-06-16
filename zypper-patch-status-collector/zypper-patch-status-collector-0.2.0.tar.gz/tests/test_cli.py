# encoding=utf-8

import subprocess

import pytest

from zypper_patch_status_collector._cli import main

from .mock import mock_zypper_call


def test_license(capsys):
    main(['--license'])
    output = capsys.readouterr().out
    assert 'GNU General Public License' in output
    assert 'WITHOUT ANY WARRANTY' in output


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        main(['--version'])
    assert e.value.code == 0
    output = capsys.readouterr()
    assert output.out + output.err != ''


def test_success(capsys, mocker):
    mock_zypper_call(mocker, 'tests/fixtures/all.xml')

    main()

    output = capsys.readouterr()
    assert 'zypper_scrape_success 1' in output.out
    assert 'zypper_applicable_patches{category="optional",severity="moderate"} 2' in output.out


def test_zypper_fail(capsys, mocker):
    zypper = mock_zypper_call(mocker, 'tests/fixtures/all.xml')
    zypper.side_effect = subprocess.CalledProcessError(1, 'zypper list-patches')

    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code != 0

    output = capsys.readouterr()
    assert 'zypper_scrape_success 0' in output.out
    assert 'Failed' in output.err
