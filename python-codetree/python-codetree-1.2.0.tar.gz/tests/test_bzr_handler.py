from __future__ import division, print_function
import os
import shutil
import subprocess
from tempfile import mkdtemp
from unittest import TestCase
import six
from six.moves.urllib.parse import urlparse
from six import StringIO

from codetree.handlers import (
    BzrSourceHandler,
    NotSameBranch
)
from .test_basic_handlers import was_called_with_cmd

if six.PY2:
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch


BzrURLs = (
    "bzr://example.com/foo/",
    "lp:debian/apt/",
    "bzr+ssh://bazaar.launchpad.net/~foo/bar/trunk/",
    "bzr+http://example.com/foo/",
    "bzr+https://example.com/foo/",
    "lp:debian/apt",
)

BzrInfoOutputs = {
    'anon': {
        'bzrinfo': """Repository branch (format: 2a)
Location:
  shared repository: http://bazaar.launchpad.net/~openstack-charmers/charms/trusty/ceph/trunk/
  repository branch: http://bazaar.launchpad.net/~openstack-charmers/charms/trusty/ceph/trunk/

Related branches:
  parent branch: http://bazaar.launchpad.net/~openstack-charmers/charms/precise/ceph/trunk/
     stacked on: /+branch-id/905249
""",
        'parent': 'http://bazaar.launchpad.net/~openstack-charmers/charms/trusty/ceph/trunk',
    },
    'auth': {
        'bzrinfo': """Repository branch (format: unnamed)
Location:
  shared repository: bzr+ssh://bazaar.launchpad.net/+branch/charms/trusty/ceph/
  repository branch: bzr+ssh://bazaar.launchpad.net/+branch/charms/trusty/ceph/

Related branches:
  parent branch: bzr+ssh://bazaar.launchpad.net/+branch/precise/ceph/trunk/
     stacked on: /+branch-id/905249
""",
        'parent': 'bzr+ssh://bazaar.launchpad.net/+branch/charms/trusty/ceph',
    },
    'local': {
        'bzrinfo': """Standalone tree (format: 2a)
Location:
  branch root: .

Related branches:
  parent branch: bzr+ssh://bazaar.launchpad.net/+branch/codetree/
""",
        'parent': 'bzr+ssh://bazaar.launchpad.net/+branch/codetree',
    },
}


def shellcmd(cmd):
    try:
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("------- output --------")
        print(e.output)
        print("-----------------------")
        raise


class BzrSourceHandlerTest(TestCase):
    def test_url_handling(self):
        for url in BzrURLs:
            assert(urlparse(url).scheme in BzrSourceHandler.schemes)

    def test_stores_source(self):
        url = BzrURLs[0]
        bh = BzrSourceHandler(url)
        self.assertEqual(bh.source, url)

    def test_nonstandard_schemes(self):
        http_url = "bzr+http://example.com/repo"
        bh = BzrSourceHandler(http_url)
        self.assertTrue(bh.source.startswith("http"))

        https_url = "bzr+https://example.com/repo"
        bh = BzrSourceHandler(https_url)
        self.assertTrue(bh.source.startswith("https"))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=[False, True])
    @patch("codetree.handlers.bzr.logging")
    @patch("codetree.handlers.bzr.os.path.exists", return_value=True)
    @patch("codetree.handlers.bzr.shutil.rmtree")
    def test_overwite(self, _rmtree, _exists, _log, _call, _output, _auth):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock(return_value=False)

        # Update the parent and try a pull but don't overwrite
        options = {"overwrite": False}
        self.assertTrue(bh.get(dest, options))
        self.assertTrue(
            was_called_with_cmd(_output, ['bzr', 'config', '-d', dest, 'parent_location={}'.format(source)]))
        _rmtree.assert_not_called()

        # don't overwrite if source = parent
        options = {"overwrite": True}
        bh.is_same_branch = MagicMock(return_value=True)
        self.assertTrue(bh.get(dest, options))
        _rmtree.assert_not_called()

        # overwrite (delete) existing when asked
        options = {"overwrite": True}
        bh.is_same_branch = MagicMock(return_value=False)
        self.assertTrue(bh.get(dest, options))
        _rmtree.assert_called_with(dest)

        bh.checkout_branch = MagicMock(return_value=False)
        self.assertFalse(bh.get(dest, options))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch("codetree.handlers.bzr.os.path.exists", return_value=False)
    def test_branches_new(self, _exists, _call, _output, _auth):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        self.assertTrue(bh.get(dest, {}))
        self.assertTrue(
            was_called_with_cmd(_output, ['bzr', 'branch', source, dest]))
        bh.checkout_branch = MagicMock(return_value=False)
        self.assertFalse(bh.get(dest, {}))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch("codetree.handlers.bzr.os.path.exists", return_value=False)
    def test_branches_new_lightweight(self, _exists, _call, _output, _auth):
        source = "lp:debian/apt"
        dest = "foo"
        bh = BzrSourceHandler(source)
        _output.return_value = ""
        options = {'lightweight': 'true'}
        self.assertTrue(bh.get(dest, options))
        self.assertTrue(
            was_called_with_cmd(
                _output, ['bzr', 'checkout', '--lightweight',
                          'lp:debian/apt', dest]))
        bh.checkout_branch = MagicMock(return_value=False)
        self.assertFalse(bh.get(dest, {}))

    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch("codetree.handlers.bzr.os.makedirs")
    def test_creates_new_dirs(self, _makedirs, _call, _output):
        source = BzrURLs[0]
        dest = "foo/bar/baz"
        bh = BzrSourceHandler(source)
        self.assertTrue(bh.get(dest, {}))
        _makedirs.assert_called_with(os.path.dirname(dest))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch("codetree.handlers.bzr.os.path.exists", return_value=True)
    def test_updates_existing(self, _exists, _call, _output, _uoutput, _auth):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock(return_value=True)
        self.assertTrue(bh.get(dest, {}))
        assert(was_called_with_cmd(_uoutput, ['bzr', 'pull', '-d', dest]))

        bh.update_branch = MagicMock(return_value=False)
        self.assertFalse(bh.get(dest, {}))

    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    def test_gets_revno(self, _call, _output, _uoutput):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock()

        revno = "1"
        options = {"revno": "1"}
        self.assertTrue(bh.get(dest, options))
        assert(was_called_with_cmd(
            _uoutput, ['bzr', 'branch', '-r', revno, source, dest]))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch('codetree.handlers.bzr.BzrSourceHandler.get_working_tree_revno', return_value='5')
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch('codetree.handlers.bzr.os.path.exists', return_value=True)
    def test_existing_revno_no_overwrite_no_match(self, _exists, _call, _output, _revno, _auth):
        source = BzrURLs[0]
        dest = "/foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock()

        revno = "1"
        options = {"revno": "1"}
        self.assertTrue(bh.get(dest, options))
        assert(was_called_with_cmd(
            _output, ['bzr', 'pull', '-r', revno, '-d', dest]))

        assert(was_called_with_cmd(
            _output, ['bzr', 'update', '-r', revno, dest]))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch('codetree.handlers.bzr.BzrSourceHandler.update_branch')
    @patch('codetree.handlers.bzr.BzrSourceHandler.get_working_tree_revno', return_value='1')
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch('codetree.handlers.bzr.os.path.exists', return_value=True)
    def test_existing_revno_no_overwrite_with_match(self, _exists, _call, _output, _revno, _update, _auth):
        source = BzrURLs[0]
        dest = "/foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock()

        revno = "1"
        options = {"revno": "1"}
        self.assertTrue(bh.get(dest, options))
        assert(was_called_with_cmd(
            _output, ['bzr', 'pull', '-r', revno, '-d', dest]))

        _update.assert_not_called()

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch('codetree.handlers.bzr.BzrSourceHandler.update_branch')
    @patch('codetree.handlers.bzr.BzrSourceHandler.get_working_tree_revno', return_value='1')
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch('codetree.handlers.bzr.os.path.exists', return_value=True)
    def test_existing_revno_with_overwrite(self, _exists, _call, _output, _update, _revno, _auth):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock()

        revno = "1"
        options = {"revno": "1", "overwrite": True}
        self.assertTrue(bh.get(dest, options))
        assert(was_called_with_cmd(
            _output, ['bzr', 'pull', '--overwrite', '-r', revno, '-d', dest]))

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch('codetree.handlers.bzr.BzrSourceHandler.update_branch')
    @patch('codetree.handlers.bzr.BzrSourceHandler.working_tree_matches_revno', return_value=True)
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch('codetree.handlers.bzr.os.path.exists', return_value=True)
    def test_existing_no_revno_with_match(self, _exists, _call, _output, _tree, _update, _auth):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock()

        options = {}
        self.assertTrue(bh.get(dest, options))
        assert(was_called_with_cmd(
            _output, ['bzr', 'pull', '-d', dest]))

        _update.assert_not_called()

    @patch("codetree.handlers.bzr.BzrSourceHandler.has_lp_auth", return_value=True)
    @patch('codetree.handlers.bzr.BzrSourceHandler.working_tree_matches_revno', return_value=False)
    @patch("codetree.handlers.utils.check_output")
    @patch("codetree.handlers.bzr.check_call", return_value=True)
    @patch('codetree.handlers.bzr.os.path.exists', return_value=True)
    def test_existing_no_revno_no_match(self, _exists, _call, _output, _tree, _auth):
        source = BzrURLs[0]
        dest = "foo"
        bh = BzrSourceHandler(source)
        bh.is_same_branch = MagicMock()

        options = {}
        self.assertTrue(bh.get(dest, options))
        assert(was_called_with_cmd(
            _output, ['bzr', 'pull', '-d', dest]))

        assert(was_called_with_cmd(
            _output, ['bzr', 'update', dest]))

    def test_same_branch(self):
        parent = mkdtemp()
        self.addCleanup(shutil.rmtree, parent)
        shellcmd("bzr init {}".format(parent))
        bh = BzrSourceHandler(parent)

        child_tmp = mkdtemp()
        self.addCleanup(shutil.rmtree, child_tmp)

        # is same
        child = os.path.join(child_tmp, "child") + "/"
        shellcmd("bzr branch {} {}".format(parent, child))
        self.assertTrue(bh.is_same_branch(child))

        # is not the same
        nonchild = os.path.join(child_tmp, "nonchild")
        shellcmd("bzr branch {} {}".format(child, nonchild))
        self.assertFalse(bh.is_same_branch(nonchild), "test: is not same")

        # is standalone
        stdalone = os.path.join(child_tmp, "stdalone")
        shellcmd("bzr init {}".format(stdalone))
        self.assertFalse(bh.is_same_branch(stdalone), "test: is standalone")

    @patch('codetree.handlers.bzr.check_output')
    def test_parent_branch(self, _check_output):
        lh = BzrSourceHandler("/some/file")
        for key in BzrInfoOutputs:
            bzr = BzrInfoOutputs[key]
            _check_output.return_value = bzr['bzrinfo']
            parent = lh.parent_branch("foo", key == 'local')
            _check_output.assert_called_with(('bzr', 'info', '-q', 'foo'), universal_newlines=True)
            self.assertEqual(parent, bzr['parent'])
            _check_output.reset_mock()

    @patch('codetree.handlers.bzr.BzrSourceHandler.parent_branch')
    @patch('codetree.handlers.bzr.BzrSourceHandler.has_lp_auth', return_value=True)
    def test_normalize_lp_branch_auth(self, _has_lp_auth, _parent_branch):
        lh = BzrSourceHandler("/some/file")
        # ~user, only replaces lp: by bzr+ssh://...
        normalized = lh.normalize_lp_branch("lp:~bob/foo")
        _parent_branch.assert_not_called()
        self.assertEqual(normalized,
                         'bzr+ssh://bazaar.launchpad.net/~bob/foo')
        # non ~user, adds +branch
        normalized = lh.normalize_lp_branch("lp:foo")
        self.assertEqual(normalized,
                         'bzr+ssh://bazaar.launchpad.net/+branch/foo')
        _parent_branch.assert_not_called()

    @patch('codetree.handlers.bzr.BzrSourceHandler.parent_branch')
    @patch('codetree.handlers.bzr.BzrSourceHandler.has_lp_auth', return_value=False)
    def test_normalize_lp_branch_anon(self, _has_lp_auth, _parent_branch):
        _parent_branch.return_value = 'http://foo/bar'
        lh = BzrSourceHandler("/some/file")
        # normalize doesn't change LP paths if it's anon LP,
        # but uses parent_branch() value
        normalized = lh.normalize_lp_branch("lp:foo")
        _parent_branch.assert_called_with("lp:foo")
        self.assertEqual(normalized, 'http://foo/bar')
