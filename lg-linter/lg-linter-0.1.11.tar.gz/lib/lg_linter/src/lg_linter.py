import os
from pathlib import Path
from dataclasses import dataclass

import git

from lg_linter.src.file_linters import (lint_cpp_file, lint_python_file,
                                        lint_shell_file)

DASHED_DOUBLE_LINE = ('========================================================'
                      '========================')


@dataclass
class LinterConfig:
    directory_path: Path
    lint_all: bool = False


def lint(config: LinterConfig):
    """
    Run complete linter.
    """
    print(DASHED_DOUBLE_LINE)
    print('Running linter...')

    if config.lint_all:
        files = get_all_files(config.directory_path)
    else:
        files = get_staged_files(config.directory_path)

    success = True
    outputs = []

    for file in files:
        print(f'Linting {file}... ', end='')
        file_is_ok, stdout = lint_file(file)
        if file_is_ok:
            print('[\033[92mOK\033[0m]')
        else:
            print('[\033[91mFAIL\033[0m]')
            success = False
            outputs.append(stdout)

    if success:
        print('\nHurray linted succesfully!')

    else:
        print('\nFound the following errors:')
        print(DASHED_DOUBLE_LINE)
        for output in outputs:
            print(output)
            print(DASHED_DOUBLE_LINE)

    return success


def get_staged_files(repo_path: Path):
    repo = git.Repo(repo_path)
    assert not repo.bare

    modified_files = repo.index.diff(None)
    staged_files = repo.index.diff('HEAD')
    if files_were_modified_after_staging(modified_files, staged_files):
        raise RuntimeError(
            'Found files which were modified after staging. Please'
            ' stage all modifications first.')

    for staged_file in staged_files:
        # Do not lint if the file was deleted. It seems as if pythongit has
        # a bug and has new_file and deleted_file confused.
        if not staged_file.new_file:
            yield repo_path / staged_file.a_path


def get_all_files(dir_path: Path):
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            yield Path(root) / filename


def files_were_modified_after_staging(modified_files, staged_files):
    for modified_file in modified_files:
        if modified_file.a_path in [
                staged_file.a_path for staged_file in staged_files
        ]:
            return True

    return False


def lint_file(file_path: Path) -> (bool, str):
    file_type = get_file_type(file_path)

    if file_type == 'cpp':
        return lint_cpp_file(file_path)
    if file_type == 'python':
        return lint_python_file(file_path)
    if file_type == 'shell':
        return lint_shell_file(file_path)

    return True, (f'WARNING: File {file_path} has unknown type and was '
                  'ignored.')


def get_file_type(file_path: Path):
    _, extension = os.path.splitext(file_path)

    if extension:
        return get_file_type_from_extension(extension)

    return get_file_type_from_shebang(file_path)


def get_file_type_from_extension(extension: str) -> str:
    EXTENSIONS = {
        'cpp': ['.h', '.hpp', '.cc', '.cpp'],
        'python': ['.py'],
        'shell': ['.sh', '.bash']
    }

    for (file_type, extensions_for_type) in EXTENSIONS.items():
        if extension in extensions_for_type:
            return file_type

    return None


def get_file_type_from_shebang(file_path: Path) -> str:
    SHEBANG_KEYWORDS = {
        'cpp': [],
        'python': ['python'],
        'shell': ['sh', 'bash']
    }

    try:
        first_line = open(file_path).readline()
    except UnicodeDecodeError:
        # Ignore binary files.
        return None

    if not '#!' in first_line:
        return None

    for (file_type, keywords_for_type) in SHEBANG_KEYWORDS.items():
        for keyword in keywords_for_type:
            if keyword in first_line:
                return file_type
    return None
