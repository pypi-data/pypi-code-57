# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import

import pytest
from heptapod.testhelpers import LocalRepoWrapper
from mercurial import pycompat

from .utils import common_config

parametrize = pytest.mark.parametrize


def make_repo(tmpdir, config):
    full_config = common_config()
    full_config.update(config)
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'), config=full_config)
    return wrapper.repo.ui


def test_multiple_heads_allow(tmpdir):
    ui = make_repo(tmpdir,
                   config=dict(heptapod={'allow-multiple-heads': 'yes'},
                               experimental={'single-head-per-branch': 'no'},
                               ))
    assert not ui.configbool(b'experimental', b'single-head-per-branch')


def test_bookmarks_allow(tmpdir):
    ui = make_repo(tmpdir,
                   config=dict(heptapod={'allow-bookmarks': 'yes'},
                               ))
    assert not ui.configbool(b'experimental', b'single-head-per-branch')
    assert ui.configbool(b'experimental',
                         b'hg-git.bookmarks-on-named-branches')


def test_auto_publish_nothing(tmpdir):
    ui = make_repo(tmpdir,
                   config=dict(
                       heptapod={'auto-publish': 'nothing'},
                       experimental={'topic.publish-bare-branch': 'yes'},
                   ))
    assert not ui.configbool(b'experimental', b'topic.publish-bare-branch')


def test_auto_publish_all(tmpdir):
    ui = make_repo(tmpdir,
                   config=dict(
                       heptapod={'auto-publish': 'all'},
                       phases={'publish': 'no'},
                   ))
    assert ui.configbool(b'phases', b'publish')


@parametrize('key',
             [('experimental', 'single-head-per-branch'),
              ('experimental', 'hg-git.bookmarks-on-named-branches'),
              ('experimental', 'topic.publish-bare-branch'),
              ('phases', 'publish'),
              ])
@parametrize('value', [True, False])
def test_lower_level_config_untouched(tmpdir, key, value):
    """This case is the default config in Heptapod normal conditions."""
    section, item = key
    ui = make_repo(tmpdir, config={section: {item: value}})
    assert ui.configbool(pycompat.sysbytes(section),
                         pycompat.sysbytes(item)) == value
