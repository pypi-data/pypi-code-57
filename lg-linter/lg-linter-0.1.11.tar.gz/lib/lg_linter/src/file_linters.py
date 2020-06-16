import os
import subprocess
from pathlib import Path


def lint_cpp_file(file_path: Path) -> (bool, str):
    os.system(f'clang-format -i {file_path}')
    os.system(f'git add {file_path}')
    completed_process = subprocess.run(['cpplint', file_path],
                                       check=False,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

    if completed_process.returncode == 0:
        return True, ''

    # cpplint prints to stderr.
    return False, completed_process.stderr.decode('utf-8')


def lint_python_file(file_path: Path) -> (bool, str):
    os.system(f'yapf -i {file_path}')
    os.system(f'git add {file_path}')
    completed_process = subprocess.run(['pylint', '--reports=n', file_path],
                                       check=False,
                                       stdout=subprocess.PIPE)

    if completed_process.returncode == 0:
        return True, ''

    return False, completed_process.stdout.decode('utf-8')


def lint_shell_file(file_path: Path) -> (bool, str):
    completed_process = subprocess.run(['shellcheck', file_path],
                                       check=False,
                                       stdout=subprocess.PIPE)

    if completed_process.returncode == 0:
        return True, ''

    return False, completed_process.stdout.decode('utf-8')
