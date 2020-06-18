###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from os.path import basename, exists, abspath
from os import mkdir
from shutil import rmtree
import tempfile
from uuid import uuid1
from unittest.mock import Mock, patch
import os
import re

from lb_utils.file_utils import FileUtils
from tests.temporary_directory_handler import TemporaryDirecotryHandler

TEST_CHECKED_FILE_TYPES = re.compile(
    r'.*(\.(i?[ch](pp|xx|c)?|cc|hh|py|C|cmake|[yx]ml|qm[ts]|dtd|xsd|ent|bat|[cz]?sh|js|html?)|'
    r'CMakeLists.txt|Jenkinsfile)$')

TEST_PATTERN = re.compile(r'\bcopyright\b', re.I)

def test_get_filenames_in_path():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        temp1 = tempfile.NamedTemporaryFile(
            prefix="temp1", suffix=".txt", dir=folder_name
        )
        temp2 = tempfile.NamedTemporaryFile(
            prefix="temp2", suffix=".txt", dir=folder_name
        )
        file_names = [basename(temp1.name), basename(temp2.name)]

        files_in_path = FileUtils.get_filenames(folder_name)

        assert file_names.sort() == files_in_path.sort()



def test_get_non_empty_filenames():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        temp1 = tempfile.NamedTemporaryFile(
            delete=False, prefix="temp1", suffix=".txt", dir="{}".format(folder_name)
        )
        temp2 = tempfile.NamedTemporaryFile(
            prefix="temp2", suffix=".txt", dir="{}".format(folder_name))

        temp1.write(b"some string")
        temp1.close()

        file_names = [basename(temp1.name)]

        non_empty_files_in_path = FileUtils.get_non_empty_filenames(
            "./{}".format(folder_name))
        assert file_names == non_empty_files_in_path

def test_is_empty():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = './{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert FileUtils.is_empty(file_name)

def test_is_empty_only_spaces_returns_true():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = './{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.write('            ')
        temp_file.close()

        assert FileUtils.is_empty(file_name)

def test_is_empty_has_test_returns_false():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = './{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.write('this is some text')
        temp_file.close()

        assert not FileUtils.is_empty(file_name)


def test_write_to_file():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = './{}/some_file.py'.format(folder_name)
        FileUtils.write_to_file(file_name, 'some text')

        with open(file_name, 'r') as f:
            data = f.read()

        assert data == 'some text'


def test_is_script():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.write('#!/bin/bash\ni am a script')
        temp_file.close()


        assert FileUtils.is_script(file_name)

def test_is_script_no_shebang():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.write('i am a script without shebang')
        temp_file.close()


        assert not FileUtils.is_script(file_name)

def test_is_script_false_shebang_too_low():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.write('i am a script\n but my shebang\n is too far down\n in the file\n#!/bin/bash')
        temp_file.close()


        assert not FileUtils.is_script(file_name)

def test_get_language_family_python():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert FileUtils.get_language_family(file_name) == 'py'

def test_get_language_family_c():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.c'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert FileUtils.get_language_family(file_name) == 'c'

def test_get_language_family_xml():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.xml'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert FileUtils.get_language_family(file_name) == 'xml'

def test_get_language_family_random_extension():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.random_extension'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert FileUtils.get_language_family(file_name) == '#'

def test_has_copyright():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.writelines('# copyright statement\nrest of the script')
        temp_file.close()

        assert FileUtils.has_pattern(file_name, TEST_PATTERN)

def test_has_copyright_false():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.writelines('this is a script')
        temp_file.close()

        assert not FileUtils.has_pattern(file_name, TEST_PATTERN)

def test_to_check():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.py'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert FileUtils.to_check(file_name, TEST_CHECKED_FILE_TYPES)

def test_to_check_bad_extension():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.random_extension'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.close()

        assert not FileUtils.to_check(file_name, TEST_CHECKED_FILE_TYPES)

def test_to_check_not_a_file():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:

        assert not FileUtils.to_check(folder_name, TEST_CHECKED_FILE_TYPES)

def test_to_check_bad_extension_but_is_script():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = '{}/some_file.random_extension'.format(folder_name)
        temp_file = open(file_name, "w+")
        temp_file.writelines('#!/bin/bash\ni am a script')
        temp_file.close()

        assert FileUtils.to_check(file_name, TEST_CHECKED_FILE_TYPES)

def test_delete_lines():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = get_temp_file('{}/some_file1.py'.format(folder_name), 'this is a script\nwith alotuva lines\nand even more line')

        FileUtils.delete_lines(file_name, 0, 1)

        with open(file_name) as file:
            lines = file.readlines()

        assert lines == ['and even more line']

def test_delete_lines_default_values():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file_name = get_temp_file('{}/some_file1.py'.format(folder_name), 'this is a script\nwith alotuva lines\nand even more line')

        FileUtils.delete_lines(file_name)

        with open(file_name) as file:
            lines = file.readlines()

        assert lines == ['and even more line']

@patch(
    'lb_utils.git_utils.GitUtils.get_all_files_tracked_in_repo')
def test_get_files_no_reference(mock_get_all_files_tracked_in_repo):

    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file1 = get_temp_file('{}/some_file.py'.format(folder_name))
        file2 = get_temp_file('{}/some_other_file.c'.format(folder_name))
        file3 = get_temp_file('{}/yet_another_file.xml'.format(folder_name))

        mock_get_all_files_tracked_in_repo.return_value = [file1, file2, file3]

        result = [
            '{}/some_file.py'.format(folder_name),
            '{}/some_other_file.c'.format(folder_name),
            '{}/yet_another_file.xml'.format(folder_name)
        ]

        assert set(result) == FileUtils.get_files(filetypes_to_check=TEST_CHECKED_FILE_TYPES)

def test_create_file():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file = '{}/some_file.py'.format(folder_name)
        FileUtils.create_file(file, 'some text')

        assert os.path.exists(file)


def test_create_file_overwrite_false_and_file_exists():
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file = '{}/some_file.py'.format(folder_name)
        get_temp_file(file)

        result = FileUtils.create_file(file, 'some text', False)

        assert result is False


@patch('lb_utils.file_utils.GitUtils.get_git_root')
def test_ensure_file_exists_in_repository_already_exists(mock_get_git_root):
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file = '{}/some_file.py'.format(folder_name)
        get_temp_file(file)

        result = FileUtils.ensure_file_exists_in_repository(folder_name, file)

        assert result == 0
        assert not mock_get_git_root.called


@patch('lb_utils.file_utils.GitUtils.get_git_root')
def test_ensure_file_exists_in_repository_no_file_no_git_root(
    mock_get_git_root):
    mock_get_git_root.return_value = None
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file = '{}/some_file.py'.format(folder_name)

        result = FileUtils.ensure_file_exists_in_repository(folder_name, file)

        assert result == 1


@patch('lb_utils.file_utils.FileUtils.create_file')
@patch('lb_utils.file_utils.GitUtils.get_git_root')
def test_ensure_file_exists_in_repository(mock_get_git_root, mock_create_file):
    mock_get_git_root.return_value = b'some_dir'
    with TemporaryDirecotryHandler.create_temp_directory() as folder_name:
        file = '{}/some_file.py'.format(folder_name)

        result = FileUtils.ensure_file_exists_in_repository(folder_name, file)

        assert result == 0
        assert mock_create_file.called

def get_temp_file(path, content=None):
    temp_file1 = open(path, "w+")
    if content:
        temp_file1.writelines(content)
    temp_file1.close()

    return path