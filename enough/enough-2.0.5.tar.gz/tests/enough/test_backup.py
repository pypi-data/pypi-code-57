from enough import cmd


def test_backup_restore(mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.Enough.restore_remote')
    assert cmd.main(['--debug', 'backup', 'restore', 'name']) == 0
