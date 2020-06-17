from __future__ import division, print_function
from unittest import TestCase

from codetree.handlers import (
    CommandFailure,
    HttpFileHandler,
    LocalHandler,
)
from codetree.handlers.basic import HandlerResult, SourceHandler
from codetree.handlers.utils import log_failure, strip_trailing_slash
from codetree import six
from codetree.six.moves.urllib.parse import urlparse
from codetree.six.moves.urllib.error import URLError
from codetree.six import StringIO

if six.PY2:
    from mock import mock_open, patch
else:
    from unittest.mock import mock_open, patch


HttpURLs = (
    "http://example.com/foo.txt",
    "https://example.com/foo.txt",
)

LocalURLs = (
    "file:///etc/hosts",
    "/etc/hosts",
    "etc/hosts",
    "../etc/hosts",
    "hosts,"
    "/etc",
)


def was_called_with_cmd(mock, cmd):
    for call_args in mock.call_args_list:
        if call_args[0][0] == cmd:
            return True
    return False


class TestHandlerResult(TestCase):
    def test_true(self):
        hr = HandlerResult(True)
        self.assertTrue(hr)

    def test_false(self):
        hr = HandlerResult(False)
        self.assertFalse(hr)

    def test_str(self):
        hr = HandlerResult(True)
        self.assertEqual("", str(hr))

        hr.dest = "dest"
        self.assertEqual("", str(hr))

        hr.dest = None
        hr.source = "source"
        self.assertEqual("", str(hr))

        hr.dest = "dest"
        self.assertEqual("dest  source", str(hr))

        hr.revision = "12"
        self.assertEqual("dest  source;revno=12", str(hr))

        hr.source = "cs:source"
        self.assertEqual("dest  cs:source-12", str(hr))

    def test_collect_location(self):
        hr = HandlerResult(True)
        hr.dest = "dest"
        hr.source = "source"
        self.assertEqual("source", hr.collect_location)

        hr.revision = "12"
        self.assertEqual("source;revno=12", hr.collect_location)

        hr.source = "cs:source"
        self.assertEqual("cs:source-12", hr.collect_location)

        # If we manually specify a charmstore revision, confirm we don't
        # append it twice to built_location.
        hr.source = "cs:source-12"
        self.assertEqual("cs:source-12", hr.collect_location)

        hr.options = {"channel": "candidate"}
        self.assertEqual("cs:source-12;channel=candidate", hr.collect_location)

        hr.source = "source"
        hr.options["overwrite"] = "true"
        del hr.options["channel"]
        self.assertEqual("source;overwrite=true,revno=12", hr.collect_location)


class TestLogHandlers(TestCase):
    @patch("codetree.handlers.utils.check_output")
    def test_log_failure_success(self, _call):
        cmd = ("echo", "hello world")
        log_failure(cmd, "Saying hello")
        assert(was_called_with_cmd(_call, cmd))

    def test_log_failure_failure(self):
        # Throws OSError
        cmd = ("/invalid/cmd", "hello world")
        self.assertFalse(log_failure(cmd, "Saying hello"))
        with self.assertRaises(CommandFailure):
            log_failure(cmd, "Failing", fatal=True)

        cmd = ("false",)
        self.assertFalse(log_failure(cmd, "Failing"))
        with self.assertRaises(CommandFailure):
            log_failure(cmd, "Failing", fatal=True)

    def test_strip_trailing_slash(self):
        value = "abc"
        self.assertEqual(value, strip_trailing_slash(value))
        self.assertEqual(value, strip_trailing_slash(value + "/"))


class TestSourceHandler(TestCase):
    def setUp(self):
        super(TestSourceHandler, self).setUp()
        self.source = "foo"
        self.sh = SourceHandler("foo")

    def test_stores_source(self):
        self.assertEqual(self.sh.source, self.source)

    def test_handles_nothing(self):
        self.assertEqual(SourceHandler.schemes, tuple())


class TestLocalHandler(TestCase):
    def test_url_handling(self):
        for local_url in LocalURLs:
            assert(urlparse(local_url).scheme in LocalHandler.schemes)

    @patch("codetree.handlers.basic.fileutils.mkdir")
    def test_creates_directory(self, _mkdir):
        lh = LocalHandler("@")
        self.assertTrue(lh.get("foo", {}))
        _mkdir.assert_called_with('foo', overwrite=False)

    @patch("codetree.handlers.basic.fileutils.copy")
    def test_copies_files_dirs(self, _copy):
        lh = LocalHandler("/some/file")
        options = {"method": "copy"}
        self.assertTrue(lh.get("/foo", options))
        _copy.assert_called_with("/some/file", "/foo")

    @patch("codetree.handlers.basic.fileutils.rsync")
    def test_rsyncs_files_dirs(self, _rsync):
        lh = LocalHandler("/some/file")
        options = {"method": "rsync"}
        self.assertTrue(lh.get("/foo", options))
        _rsync.assert_called_with("/some/file", "/foo")

    @patch("subprocess.check_output")
    @patch("os.path.isdir")
    def test_rsync_call_args(self, _is_dir, _check_output):
        _is_dir.return_value = True
        lh = LocalHandler("/some/file")
        options = {"method": "rsync"}
        self.assertTrue(lh.get("/foo", options))
        _check_output.assert_called_with(["rsync", "-rpl", "--delete", "/some/file/", "/foo"])

        lh = LocalHandler("/some/file")
        options = {"method": "copy"}
        self.assertTrue(lh.get("/foo", options))
        _check_output.assert_called_with(["rsync", "-rpl", "/some/file/", "/foo"])

    @patch("codetree.handlers.basic.fileutils.link")
    def test_links_files_dirs(self, _link):
        lh = LocalHandler("/some/file")
        # symbolic link
        options = {"method": "link"}
        self.assertTrue(lh.get("foo", options))
        _link.assert_called_with("/some/file", "foo", overwrite=True)
        # hard link
        options = {"method": "hardlink"}
        self.assertTrue(lh.get("foo", options))
        _link.assert_called_with("/some/file", "foo", symbolic=False)

    @patch("codetree.handlers.basic.fileutils.rsync")
    def test_rsync_is_default(self, _rsync):
        lh = LocalHandler("/some/file")
        self.assertTrue(lh.get("foo", {}))
        _rsync.assert_called_with("/some/file", "foo")


class TestHttpFileHandler(TestCase):
    def test_url_handling(self):
        for http_url in HttpURLs:
            assert(urlparse(http_url).scheme in HttpFileHandler.schemes)

    @patch('codetree.handlers.basic.os.unlink')
    @patch('codetree.handlers.basic.os.path.exists')
    @patch('codetree.handlers.basic.urlopen')
    def test_gets_file(self, _urlopen, _exists, _unlink):
        destfile = "foo"

        _urlopen.return_value = StringIO("words words")
        hh = HttpFileHandler(HttpURLs[0])

        # New file
        _open = mock_open()
        _exists.return_value = False
        with patch('codetree.handlers.basic.open', _open, create=True):
            self.assertTrue(hh.get(destfile, {}))
        self.assertFalse(_unlink.called)
        _open.assert_called_with(destfile, "wb")
        _urlopen.assert_called_with(HttpURLs[0])

    @patch('codetree.handlers.basic.os.unlink')
    @patch('codetree.handlers.basic.os.path.exists')
    @patch('codetree.handlers.basic.urlopen')
    def test_gets_file_no_overwrite(self, _urlopen, _exists, _unlink):
        destfile = "foo"

        _urlopen.return_value = StringIO("words words")
        hh = HttpFileHandler(HttpURLs[0])

        # Existing file
        _open = mock_open()
        _exists.return_value = True
        with patch('codetree.handlers.open', _open, create=True):
            self.assertTrue(hh.get(destfile, {}))
        self.assertFalse(_unlink.called)
        self.assertFalse(_open.called)
        self.assertFalse(_urlopen.called)

    @patch('codetree.handlers.basic.os.unlink')
    @patch('codetree.handlers.basic.os.path.exists')
    @patch('codetree.handlers.basic.urlopen')
    def test_gets_file_with_overwite(self, _urlopen, _exists, _unlink):
        destfile = "foo"

        _urlopen.return_value = StringIO("words words")
        hh = HttpFileHandler(HttpURLs[0])

        # Overwrite existing file
        _open = mock_open()
        _exists.return_value = True
        with patch('codetree.handlers.basic.open', _open, create=True):
            self.assertTrue(hh.get(destfile, options={"overwrite": True}))
        _unlink.assert_called_with(destfile)
        _open.assert_called_with(destfile, "wb")
        _urlopen.assert_called_with(HttpURLs[0])

    @patch('codetree.handlers.basic.os.unlink')
    @patch('codetree.handlers.basic.os.path.exists')
    @patch('codetree.handlers.basic.urlopen')
    def test_gets_file_bad_url(self, _urlopen, _exists, _unlink):
        destfile = "foo"

        _urlopen.return_value = StringIO("words words")
        hh = HttpFileHandler(HttpURLs[0])

        # Broken source
        _open = mock_open()
        _exists.return_value = False
        _urlopen.side_effect = URLError('failed')
        with patch('codetree.handlers.open', _open, create=True):
            self.assertFalse(hh.get(destfile, {}))
