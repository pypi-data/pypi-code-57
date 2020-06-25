# Copyright 2011-2014 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module keeps track of the version of the currently used Fastr framework.
It can check its version from mercurial or a saved file
"""
import os
import re
from typing import Optional, Tuple

try:
    import git
    _GIT_PRESENT = True
except ImportError:
    _GIT_PRESENT = False

_VERSIONFILE = os.path.join(os.path.dirname(__file__), 'versioninfo')
_FASTR_SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))


def get_base_version() -> Optional[str]:
    """
    Get the version from the top-level version file

    :return: the version
    :rtype str:
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'version'), 'r') as version_file:
            return version_file.read().strip()
    except IOError:
        return None


def get_git_info() -> Tuple[Optional[str], Optional[str]]:
    if not _GIT_PRESENT:
        return None, None

    try:
        search_path = os.path.dirname(os.path.abspath(__file__))
        repo = git.Repo(path=search_path, search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        return None, None

    git_head, git_branch = repo.head.object.name_rev.split(" ", 1)
    return git_head, git_branch


def get_saved_version() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Get cached version from file

    :return: tuple with version, head revision and branch
    """
    try:
        with open(_VERSIONFILE, 'r') as version_file:
            data = version_file.read().split()
            data = dict(x.split('=', 1) for x in data)

        return data.get('version', None), data.get('git_head', None), data.get('git_branch', None)
    except IOError:
        return None, None, None


def save_version(current_version: str, current_hg_head: str, current_hg_branch: str):
    """
    Cache the version information (useful for when installing)

    :param str current_version: version
    :param str current_hg_head: mercurial head revision
    :param str current_hg_branch: mercurial branch
    :return:
    """
    with open(_VERSIONFILE, 'w') as version_file:
        version_file.write('version={}\n'.format(current_version))
        version_file.write('git_head={}\n'.format(current_hg_head))
        version_file.write('git_branch={}\n'.format(current_hg_branch))


def clear_version():
    """
    Remove the cached version info
    """
    os.remove(_VERSIONFILE)


# Try to get version info
version = get_base_version()
git_head, git_branch = get_git_info()

# Note that we imported from a mercurial repository
from_git = git_branch is not None

# Try to get missing info from saved versioninfo
if version is None or git_head is None or git_branch is None:
    _n_version, _n_hg_head, _n_hg_branch = get_saved_version()

    version = version or _n_version
    git_head = git_head or _n_hg_head
    git_branch = git_branch or _n_hg_branch

git_head = git_head or 'unknown'
git_branch = git_branch or 'unknown'

full_version = '{}_{}_{}'.format(version, git_branch, git_head[:8])
not_master_branch = re.match(f'^tags/{version}(\^\d+)?$', git_branch) is None