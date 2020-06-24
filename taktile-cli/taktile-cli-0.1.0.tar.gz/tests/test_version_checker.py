from tktl.version import TaktileVersionChecker


def test_get_version():
    v = TaktileVersionChecker.look_for_new_version()
    assert v == '0.1.0'

