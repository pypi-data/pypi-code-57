from __future__ import division, print_function
from io import open
import os
import requests
import shutil
import subprocess
import tempfile
import sys
from unittest import TestCase

from codetree.handlers import charm
from codetree.handlers import CharmStoreHandler
from codetree.handlers.utils import handler_types
from codetree.handlers.exceptions import InvalidOption
from codetree import six
from codetree.six.moves.urllib.parse import urlparse

if six.PY2:
    from mock import call, patch, MagicMock
else:
    from unittest.mock import call, patch, MagicMock


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class MockedReq(object):
    """ A class to mock out a request object without actually hitting the internet.
    """

    def __init__(
        self,
        file_data=None,
        sha="5a1481850e29647059f21f8bf23f082649d3f5a9808481fe122db41f7a827765025da5e17da9e9ae522140113b2f1804",
        url=None
    ):

        self.test_file = os.path.join(TEST_DIR, "test_data", "charm.zip")
        self.headers = {"Content-Sha384": sha}
        self.url = url if url else "file://{0}".format(self.test_file)
        self.raw = None
        self.status_code = None
        self.encoding = None
        if file_data is not None:
            self._content = file_data
        else:
            self._content = six.BytesIO()
            with open(self.test_file, 'rb') as test_zip:
                shutil.copyfileobj(test_zip, self._content)
            self._content.seek(0)

    def __iter__(self):
        return self.iter_content(128)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def content(self):
        if isinstance(self._content, six.BytesIO):
            return self._content.getvalue()
        return self._content

    def iter_content(self, size=1):
        if isinstance(self._content, six.BytesIO):
            self._content.seek(0)
            for chunk in iter(lambda: self._content.read(size), b""):
                yield chunk
        else:
            str_pos = 0
            while str_pos < len(self._content):
                yield self._content[str_pos:min(str_pos + size, len(self._content))]
                str_pos += size

    def json(self):
        return {'Id': 'cs:trusty/charm'}


def mocked_get(*args, **kwargs):
    file_data = kwargs.pop("file_data", None)
    sha = kwargs.pop("sha", "5a1481850e29647059f21f8bf23f082649d3f5a9808481fe122db41f7a827765025da5e17da9e9ae522140113b2f1804")
    url = kwargs.pop("url", None)
    kwargs.pop("raw", False)
    return MockedReq(file_data=file_data, sha=sha, url=url)


class TestCharmStoreHandler(TestCase):
    def setUp(self):
        charm._have_charm_tools = lambda: False
        self.cs = CharmStoreHandler('cs:trusty/charm')
        self.get_url = "{}/{}/archive".format(self.cs.base_url, 'trusty/charm')
        self.tdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tdir)

    def test_url_handling(self):
        urls = (
            'cs:trusty/auditd',
            'cs:trusty/auditd-0'
        )
        for url in urls:
            self.assertIn(urlparse(url).scheme, CharmStoreHandler.schemes)

        assert 'cs' in list(handler_types().keys())

    def test_metadata(self):
        dest = os.path.join(self.tdir, 'test_download')
        os.mkdir(dest, 0o0755)
        self.cs.charmstore_url = 'cs:trusty/test-auditd-1'

        self.assertEqual(None, self.cs._get_url(dest))

        self.cs._set_url(dest)
        self.assertEqual('cs:trusty/test-auditd-1;channel=stable', self.cs._get_url(dest))

    @patch("codetree.handlers.charm.logging.error")
    @patch("codetree.handlers.charm.logging.info")
    @patch("codetree.handlers.charm.requests.get")
    def test_download(self, _get, _logging_info, _logging_error):
        dest = os.path.join(self.tdir, 'test_download')
        _get.return_value = mocked_get()

        assert self.cs.get(dest, {})
        assert _get.call_count == 2
        expected_request_args = [call('{}/trusty/charm/meta/id?channel=stable'.format(self.cs.base_url)),
                                 call('{}/trusty/charm/archive'.format(self.cs.base_url))]
        assert _get.call_args_list == expected_request_args
        expected_logging = [call("Downloading {} from charm store to {}".format(self.cs.source, dest)),
                            call("{} charm retrieved from {}".format(dest, self.cs.charmstore_url))]
        self.assertEqual(_logging_info.call_args_list, expected_logging)
        _get.reset_mock()
        _logging_info.reset_mock()

        # check only, no update needed
        assert self.cs.get(dest, {})
        assert _get.call_count == 1
        expected_request_args = [call('{}/trusty/charm/meta/id?channel=stable'.format(self.cs.base_url))]
        assert _get.call_args_list == expected_request_args
        expected_logging = [call("{} is up to date from url {}, skipping.".format(dest, self.cs.charmstore_url))]
        assert _logging_info.call_args_list == expected_logging
        _get.reset_mock()
        _logging_info.reset_mock()

        # Edit the metadata forcing a re-download
        self.cs.charmstore_url += 'test'
        self.cs._set_url(dest)
        assert self.cs.get(dest, {})
        assert _get.call_count == 2
        expected_request_args = [call('{}/trusty/charm/meta/id?channel=stable'.format(self.cs.base_url)),
                                 call('{}/trusty/charm/archive'.format(self.cs.base_url))]
        assert _get.call_args_list == expected_request_args
        expected_logging = [call("Downloading {} from charm store to {}".format(self.cs.source, dest)),
                            call("{} charm retrieved from {}".format(dest, self.cs.charmstore_url))]
        assert _logging_info.call_args_list == expected_logging
        _get.reset_mock()
        _logging_info.reset_mock()

        # Trick it into thinking it's a git repo, `get()` should refuse to
        # update and log an error.
        os.remove(os.path.join(dest, self.cs.metadata_filename))
        with open(os.path.join(dest, '.git'), 'w') as git:
            git.write(six.u('This is a git repo'))
        # Confirm we return False which will be considered an error.
        self.assertFalse(self.cs.get(dest, {}))
        self.assertEqual(_get.call_count, 1)
        expected_request_args = [call('{}/trusty/charm/meta/id?channel=stable'.format(self.cs.base_url))]
        assert _get.call_args_list == expected_request_args
        expected_logging = [call("Failed to update {} to {} because it looks like a bzr or git branch, and the "
                                 "'overwrite' option wasn't set".format(dest, self.cs.charmstore_url))]
        assert _logging_error.call_args_list == expected_logging

    @patch("codetree.handlers.charm.logging.info")
    @patch("codetree.handlers.charm.requests.get")
    def test_download_with_overwrite(self, _get, _logging):
        dest = os.path.join(self.tdir, 'test_overwrite')
        _get.return_value = mocked_get()

        assert self.cs.get(dest, {'overwrite': True})
        _get.assert_called_with(self.get_url)
        expected_logging = [call("Downloading {} from charm store to {}".format(self.cs.source, dest)),
                            call("{} charm retrieved from trusty/charm".format(dest))]
        self.assertEqual(_logging.call_args_list, expected_logging)
        _logging.reset_mock()

        # Now let's trick it into thinking it's a git repo
        with open(os.path.join(dest, '.git'), 'w') as git:
            git.write(six.u('This is a git repo'))

        # Second run should overwrite (redownload) even though it's a git branch
        assert self.cs.get(dest, {'overwrite': True})
        _get.assert_called_with(self.get_url)

        expected_logging = [call("Downloading {} from charm store to {}".format(self.cs.source, dest)),
                            call("{} charm retrieved from {}".format(dest, self.cs.charmstore_url))]
        assert _logging.call_args_list == expected_logging

    @patch("codetree.handlers.charm.logging.info")
    @patch("codetree.handlers.charm.requests.get")
    def test_download_from_channel(self, _get, _logging):
        dest = os.path.join(self.tdir, 'test_download')
        _get.return_value = mocked_get()

        assert self.cs.get(dest, {'channel': 'edge'})
        assert _get.call_count == 2
        expected_request_args = [call('{}/trusty/charm/meta/id?channel=edge'.format(self.cs.base_url)),
                                 call('{}/trusty/charm/archive'.format(self.cs.base_url))]
        assert _get.call_args_list == expected_request_args
        expected_logging = [call("Downloading {} from charm store to {}".format(self.cs.source, dest)),
                            call("{} charm retrieved from {}".format(dest, self.cs.charmstore_url))]
        assert _logging.call_args_list == expected_logging
        _get.reset_mock()
        _logging.reset_mock()

        # Second run should re-download as we have no way of knowing if the upstream is the same as on disk
        self.assertRaises(InvalidOption, self.cs.get, dest, {'channel': 'fakechannel'})
        _get.reset_mock()
        _logging.reset_mock()

    @patch("codetree.handlers.charm.requests.get")
    def test_failed_sha(self, _get):
        dest = os.path.join(self.tdir, 'test_failed_sha')
        _get.return_value = mocked_get(sha='toosmallforasha')

        with self.assertRaises(requests.HTTPError):
            self.cs.get(dest, {})

    @patch("codetree.handlers.charm.requests.get")
    def test_download_invalid_zip(self, _get):
        dest = os.path.join(self.tdir, 'test_invalid_zip')

        test_sha = '0291dbcaaa51039c59ae631f106d95791fb8c74815fee44f3f31fea7f9f30d001e24d038e90ed632d1d71a6f4082ad5c'
        mock_file_data = six.BytesIO(six.ensure_binary("not a valid zip"))
        _get.return_value = mocked_get(file_data=mock_file_data, sha=test_sha)

        with self.assertRaises(subprocess.CalledProcessError):
            self.cs.get(dest, {})


class TestCharmStoreHandlerUsingCharm(TestCase):
    def setUp(self):
        charm._have_charm_tools = lambda: True
        self.cs = CharmStoreHandler('cs:trusty/charm')
        self.tdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tdir)

    @patch("codetree.handlers.charm.logging.info")
    @patch("codetree.handlers.charm.subprocess.check_output")
    def test_download(self, _check_output, _logging):
        dest = os.path.join(self.tdir, 'test_download')

        def simulate_charm(cmd, *args, **kwargs):
            if cmd[1] == 'show':
                return '{"id": {"Id": "cs:trusty/charm-10"}}'
            elif cmd[1] == 'pull':
                os.makedirs(cmd[5])

        _check_output.side_effect = simulate_charm

        assert self.cs.get(dest, {})
        assert _check_output.call_count == 2
        expected_request_args = [
            call(['charm', 'show', '--format=json', '--channel', 'stable', 'cs:trusty/charm', 'id'], stderr=subprocess.STDOUT, universal_newlines=True),
            call(['charm', 'pull', '--channel', 'stable', 'cs:trusty/charm-10', dest], stderr=subprocess.STDOUT, universal_newlines=True)]
        self.assertEqual(_check_output.call_args_list, expected_request_args)
        expected_logging = [call("Downloading cs:trusty/charm-10 from charm store to {}".format(dest)),
                            call("{} charm retrieved from {}".format(dest, self.cs.charmstore_url))]
        self.assertEqual(_logging.call_args_list, expected_logging)

    @patch("codetree.handlers.charm.logging.info")
    @patch("codetree.handlers.charm.subprocess.check_output")
    def test_charm_error(self, _check_output, _logging):
        dest = os.path.join(self.tdir, 'test_download')

        def simulate_charm(cmd, *args, **kwargs):
            if cmd[1] == 'show':
                return '{"id": {"Id": "cs:trusty/charm-10"}}'
            elif cmd[1] == 'pull':
                raise subprocess.CalledProcessError(1, cmd, 'test error output')

        _check_output.side_effect = simulate_charm

        with self.assertRaises(charm.CharmClientError) as context:
            self.cs.get(dest, {})
        self.assertEqual(str(context.exception), 'test error output')
