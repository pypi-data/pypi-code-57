from pyshellrunner import run

def test_run_echo():
    assert run("echo -n 'test'").stdout == 'test'