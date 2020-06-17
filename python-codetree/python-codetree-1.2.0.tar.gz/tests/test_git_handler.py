from __future__ import division, print_function
from io import open
import os
import shutil
import subprocess
from tempfile import mkdtemp
from unittest import TestCase

from codetree.handlers import (
    GitSourceHandler,
    NotABranch,
    NotSameBranch,
    InvalidOption
)
from codetree.six.moves.urllib.parse import urlparse
from codetree import six


class TestGitSourceHandler(TestCase):
    def setUp(self):
        self._gitdir = mkdtemp('', 'git')
        subprocess.check_call(('git', '-C', self._gitdir, 'init', '-q'))
        with open(os.path.join(self._gitdir, 'file'), 'w') as f:
            f.write(six.u('tag A'))
        subprocess.check_call(('git', '-C', self._gitdir, 'add', 'file'))
        subprocess.check_call(('git', '-C', self._gitdir, 'commit', '-q', '-m', 'tag A'))
        subprocess.check_call(('git', '-C', self._gitdir, 'tag', '-a', '-m', 'A', 'A'))
        subprocess.check_call(('git', '-C', self._gitdir, 'checkout', '-q', '-b', 'branch-B'))
        with open(os.path.join(self._gitdir, 'file'), 'w') as f:
            f.write(six.u('branch B'))
        subprocess.check_call(('git', '-C', self._gitdir, 'commit', '-q', '-a', '-m', 'branch B'))

        # Do an orphan checkout here to test the behaviour of the --single-branch behaviour.
        subprocess.check_call(('git', '-C', self._gitdir, 'checkout', '--orphan', 'branch-single'))
        subprocess.check_call(('git', '-C', self._gitdir, 'rm', '-rf', '.'))
        with open(os.path.join(self._gitdir, 'file'), 'w') as f:
            f.write(six.u('single branch'))
        subprocess.check_call(('git', '-C', self._gitdir, 'add', 'file'))
        subprocess.check_call(('git', '-C', self._gitdir, 'commit', '-q', '-m', 'tag single branch'))

        subprocess.check_call(('git', '-C', self._gitdir, 'checkout', '-q', 'master'))
        with open(os.path.join(self._gitdir, 'file'), 'w') as f:
            f.write(six.u('revision'))
        subprocess.check_call(('git', '-C', self._gitdir, 'commit', '-q', '-a', '-m', 'revision'))
        self._revision = subprocess.check_output(('git', '-C', self._gitdir, 'rev-parse', 'HEAD')).strip()
        with open(os.path.join(self._gitdir, 'file'), 'w') as f:
            f.write(six.u('HEAD'))
        subprocess.check_call(('git', '-C', self._gitdir, 'commit', '-q', '-a', '-m', 'HEAD'))

    @property
    def git_resource_prefix(self):
        return "file://{}".format(os.path.abspath(self._gitdir))

    def tearDown(self):
        shutil.rmtree(self._gitdir)

    def test_url_handling(self):
        urls = (
            'git://github.com/juju/juju',
            'git+ssh://git@github.com:juju/juju',
            'git+http://github.com/juju/juju',
            'git+https://github.com/juju/juju',
        )
        for url in urls:
            self.assertIn(urlparse(url).scheme, GitSourceHandler.schemes)

    def test_get_no_options(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {})
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('HEAD', c)
        finally:
            shutil.rmtree(d)

    def test_get_tag(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'revno': 'A'})
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('tag A', c)
        finally:
            shutil.rmtree(d)

    def test_get_branch(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            ret = gh.get(wd, {'branch': 'branch-B'})
            self.assertTrue(ret.success)
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('branch B', c)
            # Get with branch another time to validate the idempotency
            ret = gh.get(wd, {'branch': 'branch-B'})
            self.assertTrue(ret.success)
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('branch B', c)
        finally:
            shutil.rmtree(d)

    def test_get_revision(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'revno': self._revision})
            rev = subprocess.check_output(gh._git_cmd(wd, 'rev-parse', 'HEAD'))
            self.assertEqual(self._revision, rev.strip())
        finally:
            shutil.rmtree(d)

    def test_get_revision_depth_1(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'revno': self._revision, 'depth': 1})
            rev_count = subprocess.check_output(gh._git_cmd(wd, 'rev-list', '--count', '--all'), universal_newlines=True)
            self.assertEqual('1', rev_count.strip())
        finally:
            shutil.rmtree(d)

    def test_get_revision_depth_1_str(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'revno': self._revision, 'depth': "1"})
            rev_count = subprocess.check_output(gh._git_cmd(wd, 'rev-list', '--count', '--all'), universal_newlines=True)
            self.assertEqual('1', rev_count.strip())
        finally:
            shutil.rmtree(d)

    def test_get_revision_depth_is_int(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            with self.assertRaises(ValueError):
                gh.get(wd, {'revno': self._revision, 'depth': "invalid"})
        finally:
            shutil.rmtree(d)

    def test_get_specific_branch(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'branch': 'branch-B'})
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('branch B', c)
        finally:
            shutil.rmtree(d)

    def test_get_branch_and_revno(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            with self.assertRaises(InvalidOption):
                gh.get(wd, {'revno': self._revision, 'branch': 'branch-B'})
        finally:
            shutil.rmtree(d)

    def test_get_branch_with_depth(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'branch': 'branch-B', 'depth': '1'})
            with open(os.path.join(wd, 'file')) as f:
                c = f.read()
                self.assertEqual('branch B', c)
            rev_count = subprocess.check_output(gh._git_cmd(wd, 'rev-list', '--count', '--all'), universal_newlines=True)
            self.assertEqual('1', rev_count.strip())
        finally:
            shutil.rmtree(d)

    def test_get_single_branch(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {'branch': 'branch-single'})
            with open(os.path.join(wd, 'file')) as f:
                c = f.read()
                self.assertEqual('single branch', c)
                result = subprocess.call(gh._git_cmd(wd, 'checkout', 'branch-B'))
                self.assertEqual(1, result)
        finally:
            shutil.rmtree(d)

    def test_directory_exists(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            os.mkdir(wd)
            with self.assertRaises(NotABranch):
                gh.get(wd, {})
        finally:
            shutil.rmtree(d)

    def test_directory_exists_with_same_origin(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        olddir = os.getcwd()
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            os.mkdir(wd)
            os.chdir(wd)
            subprocess.check_call(('git', 'init', '-q'))
            subprocess.check_call(('git', 'remote', 'add', 'origin', '{}/.git'.format(self.git_resource_prefix)))
            os.chdir(olddir)
            gh.get(wd, {})
            with open(os.path.join(wd, 'file')) as f:
                c = f.read()
                self.assertEqual('HEAD', c)
        finally:
            os.chdir(olddir)
            shutil.rmtree(d)

    def test_directory_exists_with_different_origin(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        olddir = os.getcwd()
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            os.mkdir(wd)
            os.chdir(wd)
            subprocess.check_call(('git', 'init', '-q'))
            subprocess.check_call(('git', 'remote', 'add', 'origin', 'git://notlocalhost/.git'))
            os.chdir(olddir)
            with self.assertRaises(NotSameBranch):
                gh.get(wd, {})
        finally:
            os.chdir(olddir)
            shutil.rmtree(d)

    def test_overwrite(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        olddir = os.getcwd()
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            os.mkdir(wd)
            os.chdir(wd)
            subprocess.check_call(('git', 'init', '-q'))
            subprocess.check_call(('git', 'remote', 'add', 'origin', 'git://notlocalhost/.git'))
            os.chdir(olddir)
            gh.get(wd, {"overwrite": True})
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('HEAD', c)
        finally:
            os.chdir(olddir)
            shutil.rmtree(d)

    def test_new_commit(self):
        gh = GitSourceHandler("{}/.git".format(self.git_resource_prefix))
        d = mkdtemp('', 'git-handler')
        try:
            wd = os.path.join(d, 'test')
            gh.get(wd, {})
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('HEAD', c)
            with open(os.path.join(self._gitdir, 'file'), 'w') as f:
                f.write(six.u('modified'))
            subprocess.check_call(('git', '-C', self._gitdir, 'commit', '-q', '-a', '-m', 'modified'), universal_newlines=True)
            gh.get(wd, {})
            with open(os.path.join(wd, 'file'), "r") as f:
                c = f.read().strip()
            self.assertEqual('modified', c)
        finally:
            shutil.rmtree(d)
