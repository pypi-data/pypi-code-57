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
import os
import re
from itertools import islice
import fileinput
import logging

from lb_utils.git_utils import GitUtils

log = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class FileUtils:

    @staticmethod
    def get_non_empty_filenames(path):
        """
        this function takes in as a parameter a path as a string
        and returns a list of filenames which corresponds to the
        files in path that have text in them

        :param path: str

        :return list[str, str, str, str....., str]
        """
        file_names = FileUtils.get_filenames(path)

        non_empty_filenames = []
        for file_name in file_names:
            if not FileUtils.is_empty('{}/{}'.format(path, file_name)):
                non_empty_filenames.append(file_name)

        return non_empty_filenames

    @staticmethod
    def get_filenames(path):
        """
        this function takes in as a parameter a path as a string
        and returns a list of filenames which corresponds to the
        files in path

        :param path: str
        
        :return list[str, str, str, str....., str]
        """
        file_names = []

        for (_, _, filenames) in os.walk(path):
            file_names.extend(filenames)
            break

        return file_names

    @staticmethod
    def is_empty(path):
        """
        takes in as a parameter a file path as a string
        and checks if the file is empty or has only spaces
        returns True if it empty otherwise False

        :param path: str
        
        :return bool
        """
        def only_blanks():
            with open(path) as f:
                for l in f:
                    if l.strip():
                        return False
            return True

        zero_size = os.stat(path).st_size == 0
        return zero_size or only_blanks()

    @staticmethod
    def write_to_file(file_name, content):
        """
        takes in as a parameter a file name as string
        and a string of content. Then writes the
        content inside the file given in file_name
        files in path

        :param file_name: str

        :param content: str
        
        :return void
        """
        with open(file_name, 'w') as file:
            file.write(content)

    @staticmethod
    def is_script(path):
        '''
        Check if a given file starts with the magic sequence '#!'.
        '''
        with open(path, 'rb') as f:
            return f.read(2) == b'#!'

    @staticmethod
    def get_language_family(path):
        '''
        Detect language family of a file.
        '''
        if re.match(r'.*\.(xml|xsd|dtd|html?|qm[ts]|ent)$', path):
            return 'xml'
        elif re.match(r'(.*\.(i?[ch](pp|xx|c)?|cc|hh|C|opts|js)|'
                    r'Jenkinsfile)$', path):
            return 'c'
        elif re.match(r'.*\.py$', path) or re.match(r'^#!.*python',
                                                    open(path).readline(120)):
            return 'py'
        else:
            return '#'


    @staticmethod
    def has_pattern(path, pattern):
        '''
        Check if there's a copyright signature in the first 100 lines of a file.
        '''
        with open(path) as f:
            return any(pattern.search(l) for l in islice(f, 100))
            # license_constants.COPYRIGHT_SIGNATURE

    @staticmethod
    def find_pattern_line(lines, pattern, limit=2):
        '''
        Look for encoding declaration line (PEP-263) in a file and return the index
        of the line containing it, or None if not found.
        '''
        for i, l in enumerate(islice(lines, limit)):
            if pattern.match(l):
                return i
                # license_constants.ENCODING_DECLARATION

    @staticmethod
    def to_check(path, filetypes_to_check):
        '''
        Check if path is meant to contain a copyright statement.
        '''
        return os.path.isfile(path) and (bool(filetypes_to_check.match(path))
                                        or FileUtils.is_script(path))
                                        # license_constants.CHECKED_FILES

    @staticmethod
    def delete_lines(file, start_line=0, end_line=1):
        for i, line in enumerate(fileinput.input([file], inplace=True)):
            if i not in range(start_line, end_line + 1):
                print(line, end='')


    @staticmethod
    def get_files(reference=None, filetypes_to_check='.+'):
        '''
        Return iterable with the list of names of files to check.
        '''
        files_tracked_in_repo = GitUtils.get_all_files_tracked_in_repo(
            reference)
        print(files_tracked_in_repo)
        files_to_check = set(filter(lambda path: FileUtils.to_check(path, filetypes_to_check), files_tracked_in_repo))
        print('files to check {}'.format(files_to_check))
        log.debug('files to check: {}'.format(files_to_check))

        return files_to_check

    @staticmethod
    def ensure_file_exists_in_repository(path, file, file_content=''):
        path = os.path.abspath(path)
        base = FileUtils.find_file_in_path(path, file)
        if base:
            log.debug('found %s in %s', file, base)
            return 0
        else:
            base = GitUtils.get_git_root(path)
            log.debug('found .git top dir in %s', base)
            if base:
                FileUtils.create_file(os.path.join(base.decode(), file),
                                      file_content)
                return 0
            return 1

    @staticmethod
    def find_file_in_path(path, file):
        while not os.path.isdir(path):
            path = os.path.dirname(path)
        while True:
            parent = os.path.dirname(path)
            if os.path.exists(os.path.join(path, file)):
                return path
            elif parent != path:
                path = parent
            else:
                return None  # root dir reached

    @staticmethod
    def create_file(dest, content, overwrite=False):
        '''Add `.clang-format` file.
        @param dest: destination filename
        @param overwrite: flag to decide if an already present file has to be kept
                        or not (default is False)
        '''
        if overwrite or not os.path.exists(dest):
            log.debug("Creating '%s'", dest)
            with open(dest, "w") as f:
                f.writelines(content)
            return True
        return False