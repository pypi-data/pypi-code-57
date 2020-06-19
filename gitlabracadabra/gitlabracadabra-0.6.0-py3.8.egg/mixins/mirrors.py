#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import subprocess  # noqa: S404
from urllib.request import getproxies, proxy_bypass
try:
    from urllib import quote, urlparse  # Python 2.X
except ImportError:
    from urllib.parse import quote, urlparse  # Python 3+

from pygit2 import (
    GIT_FETCH_PRUNE,
    GitError,
    LIBGIT2_VER,
    Passthrough,
    RemoteCallbacks,
    Repository,
    UserPass,
    init_repository,
)

import gitlabracadabra.manager
import gitlabracadabra.utils

logger = logging.getLogger(__name__)


class PyGit2Callbacks(RemoteCallbacks):
    def __init__(self, use_token):
        self._use_token = use_token

    """"credentials()

    Authenticate using OAuth2 token
    """
    def credentials(self, url, username_from_url, allowed_types):
        if self._use_token:
            mgr = gitlabracadabra.manager.get_manager()
            return UserPass('oauth2', mgr.private_token)
        else:
            raise Passthrough


class MirrorsMixin(object):
    """"_process_mirrors()

    Process the mirrors param.
    """
    def _process_mirrors(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'mirrors'  # noqa: S101
        assert not skip_save  # noqa: S101

        def init_repo():
            repo_dir = gitlabracadabra.utils.gitlabracadabra_cache_dir(quote(self.web_url(), safe=''))
            if not os.path.isdir(repo_dir):
                logger.debug('[%s] Creating cache repository in %s',
                                        self._name, repo_dir)
                self._repo = init_repository(repo_dir, bare=True)
            else:
                self._repo = Repository(repo_dir)
            try:
                self._repo.remotes['gitlab']
            except KeyError:
                self._repo.remotes.create('gitlab', self.web_url(), "+refs/heads/*:refs/remotes/gitlab/heads/*")
                self._repo.remotes.add_fetch('gitlab', "+refs/tags/*:refs/remotes/gitlab/tags/*")
                self._repo.remotes.add_push('gitlab', "+refs/heads/*:refs/heads/*")
                self._repo.remotes.add_push('gitlab', "+refs/tags/*:refs/tags/*")
                self._repo.config["remote.gitlab.mirror"] = True

        def fetch_remote(name):
            url = self._repo.config['remote.{}.url'.format(name)]
            libgit2_workaround = False
            if url.startswith('https://') and LIBGIT2_VER < (0, 28, 0):
                try:
                    http_proxy = self._repo.config['http.proxy']
                except KeyError:
                    http_proxy = None
                try:
                    http_proxy = self._repo.config['remote.{}.proxy'.format(name)]
                except KeyError:
                    pass
                if http_proxy is None:  # '' being explicitly disabled
                    proxies = getproxies()
                    parsed = urlparse(url)
                    http_proxy = proxies.get(parsed.scheme) or proxies.get('any')
                    if proxy_bypass(parsed.hostname):
                        http_proxy = None
                if http_proxy:
                    libgit2_workaround = True
            if libgit2_workaround:
                # libgit2 >= 0.28 required for proper HTTP proxy support
                # https://github.com/libgit2/libgit2/pulls/4870
                # https://github.com/libgit2/libgit2/pulls/5052
                logger.warning('[%s] Using git command to fetch remote %s', self._name, name)
                subprocess.run(['git', 'fetch', '--quiet', '--prune', name], cwd=self._repo.path)  # noqa: S603,S607
            else:
                pygit2_callbacks = PyGit2Callbacks(use_token=name == 'gitlab')
                self._repo.remotes[name].fetch(refspecs=self._repo.remotes[name].fetch_refspecs,
                                               callbacks=pygit2_callbacks, prune=GIT_FETCH_PRUNE)

        def push_remote(name, refs):
            pygit2_callbacks = PyGit2Callbacks(use_token=name == 'gitlab')
            try:
                self._repo.remotes[name].push(refs, callbacks=pygit2_callbacks)
            except GitError as e:
                logger.error('[%s] Unable to push remote=%s refs=%s: %s',  # noqa: G200
                             self._name, name, ','.join(refs), e)

        def pull_mirror(url, direction, skip_ci):
            if skip_ci:
                # FIXME Ignored by libgit2/PyGit2
                # https://github.com/libgit2/libgit2/issues/5335
                self._repo.config['push.pushOption'] = 'ci.skip'
            else:
                self._repo.config['push.pushOption'] = ''
            try:
                self._repo.remotes['pull']
            except KeyError:
                self._repo.remotes.create('pull', url, "+refs/heads/*:refs/heads/*")
                self._repo.remotes.add_fetch('pull', "+refs/tags/*:refs/tags/*")
                self._repo.config["remote.pull.mirror"] = True
            fetch_remote('pull')
            for ref in self._repo.references.objects:
                if ref.name.startswith('refs/heads/'):
                    shorthand = ref.name[11:]
                    pull_commit = ref.peel().id
                    gitlab_ref = self._repo.references.get('refs/remotes/gitlab/heads/{}'.format(shorthand))
                    try:
                        gitlab_commit = gitlab_ref.peel().id
                    except AttributeError:
                        gitlab_commit = None
                    if pull_commit != gitlab_commit:
                        if dry_run:
                            logger.info('[%s] %s NOT Pushing branch %s: %s -> %s (dry-run)',
                                        self._name, url, shorthand, gitlab_commit, pull_commit)
                        else:
                            logger.info('[%s] %s Pushing branch %s: %s -> %s',
                                        self._name, url, shorthand, gitlab_commit, pull_commit)
                            push_remote('gitlab', [ref.name])
                elif ref.name.startswith('refs/tags/'):
                    shorthand = ref.name[10:]
                    pull_commit = ref.peel().id
                    gitlab_ref = self._repo.references.get('refs/remotes/gitlab/tags/{}'.format(shorthand))
                    try:
                        gitlab_commit = gitlab_ref.peel().id
                    except AttributeError:
                        gitlab_commit = None
                    if pull_commit != gitlab_commit:
                        if dry_run:
                            logger.info('[%s] %s NOT Pushing tag %s: %s -> %s (dry-run)',
                                        self._name, url, shorthand, gitlab_commit, pull_commit)
                        else:
                            logger.info('[%s] %s Pushing tag %s: %s -> %s',
                                        self._name, url, shorthand, gitlab_commit, pull_commit)
                            push_remote('gitlab', [ref.name])

        pull_mirror_count = 0
        init_repo()
        fetch_remote('gitlab')
        for mirror in param_value:
            url = mirror['url']
            direction = mirror.get('direction', 'pull')
            skip_ci = mirror.get('skip_ci', True)
            if direction == 'pull':
                if pull_mirror_count > 0:
                    logger.warning('[%s] NOT Pulling mirror: %s (Only first pull mirror is processed)',
                                   self._name, url)
                    continue
                pull_mirror(url, direction, skip_ci)
                pull_mirror_count += 1
            else:
                logger.warning('[%s] NOT Push mirror: %s (Not supported yet)',
                                self._name, url)
                continue
