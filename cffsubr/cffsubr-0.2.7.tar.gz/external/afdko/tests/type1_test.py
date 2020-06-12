import pytest
import subprocess

from runner import main as runner
from differ import main as differ
from test_utils import get_expected_path

TOOL = 'type1'


# -----
# Tests
# -----

@pytest.mark.parametrize('arg', ['-h'])
def test_exit_known_option(arg):
    assert subprocess.call([TOOL, arg]) == 0


@pytest.mark.parametrize('arg', ['-v', '-u'])
def test_exit_unknown_option(arg):
    assert subprocess.call([TOOL, arg]) == 1


def test_run_on_txt_data():
    actual_path = runner(['-t', TOOL, '-s', '-f', 'type1.txt'])
    expected_path = get_expected_path('type1.pfa')
    assert differ([expected_path, actual_path])
