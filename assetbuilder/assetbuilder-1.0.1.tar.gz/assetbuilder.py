# Copyright 2017 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
from collections import defaultdict
from collections import namedtuple
from email.utils import parsedate_tz, mktime_tz
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from wsgiref.util import application_uri
import hashlib
import io
import logging
import mimetypes
import os
import pathlib
import subprocess
import time
import uuid

import portalocker
import itsdangerous

logger = logging.getLogger(__name__)
ustr = type("")

if ustr is str:

    def getenv(environ, key, default="", enc="UTF-8"):
        return environ.get(key, default).encode("iso-8859-1").decode(enc)


else:

    def getenv(environ, key, default="", enc="UTF-8"):
        return environ.get(key, default).decode(enc)


BuildCommand = namedtuple("BuildCommand", "command chdir cwd shell env")


class MultiFileWrapper:
    def __init__(self, files, separator):
        self._files = []
        if isinstance(separator, str):
            separator = separator.encode("UTF-8")
        for ix, f in enumerate(files):
            if separator and ix > 0:
                self._files.append(io.BytesIO(separator))
            self._files.append(f)

        self._ifile = 0
        self.separator = separator

    def read(self, size):
        buf = b""
        remaining = size
        try:
            f = self._files[self._ifile]
        except IndexError:
            return b""
        while size < 0 or remaining > 0:
            chunk = f.read(remaining)
            if chunk == b"":
                self._ifile += 1
                if self._ifile == len(self._files):
                    break
                f = self._files[self._ifile]
            else:
                buf += chunk
                remaining -= len(chunk)
        return buf

    def close(self):
        for f in self._files:
            f.close()


class AssetBuilder(object):
    """
    AssetBuilder objects hold information on managed asset files, their
    dependencies and file modification times. They allow applications to
    generate URLs for static asset files, serve the asset files via WSGI
    and trigger rebuilds when the asset files are no longer up to date.

    :param baseurl: base url for serving assets.
                    this must correspond to the URL the AssetBuilder WSGI
                    application is mounted on.
                    If only the path section is given, a fully qualified
                    URL will be generated from the WSGI environ when
                    generating asset urls with AssetBuilder.urlfor.
    :param directory: directory to search for asset files
    :param depdirs: list of directories to search for asset dependencies
    """

    def __init__(
        self, baseurl, directory, depdirs=None, autobuild=False, secret=None
    ):

        if not baseurl.endswith("/"):
            baseurl += "/"

        #: Base URL for generating asset URLs, eg 'https://example.org/'
        self.baseurl = baseurl

        self.depdirs = [pathlib.Path(d) for d in (depdirs or [directory])]
        self.directory = pathlib.Path(directory).resolve()
        self.autobuild = autobuild

        #: Mapping of asset virtual paths to asset Path
        self.served = {}

        #: Mapping of asset virtual paths to dependencies
        self.dependencies = {}
        self.dependencies_cache = {}

        #: Mapping of asset virtual paths to a set of files to exclude
        #: from the dependency list
        self.negative_deps = defaultdict(set)

        #: Mapping of tags to asset virtual paths
        self.tags = {}

        #: Mapping of asset virtual paths to (mtime, cachebuster querystring)
        self.cachebusters = {}

        #: Mapping of asset virtual paths to BuildCommand objects
        self.build_commands = {}

        #: List of files which are considered dependencies for *all* assets
        self.global_deps = []

        #: Mapping of dependency files to last updated times
        self.dependency_mtimes = {}

        #: Set of asset virtual paths which have never successfully been built
        #: Membership of this set prevents the assetbuilder from retrying
        #: the build command (which otherwise would run on every request,
        #: potentially causing signifant server load).
        self.unbuildable = set()

        # Cache (baseurl, *tags, separator) -> URL (only used when
        # autobuild is off)
        self.cached_urls = {}

        self.default_build_command = None
        self.rebuild_all_command = None
        if secret:
            self.secret = secret
        else:
            hwaddr = uuid.getnode()
            if hwaddr != uuid.getnode():
                raise AssertionError("Couldn't generate a stable secret!")
            self.secret = hwaddr.to_bytes(6, "big")
        self.serializer = itsdangerous.URLSafeSerializer(self.secret)

    def set_default_build_command(
        self, command, chdir=False, cwd=None, env=None, shell=True
    ):
        """
        Set a build command to be used for all assets that do have a
        build command configured.
        """
        self.default_build_command = BuildCommand(
            command, chdir, cwd, shell, env
        )

    def set_rebuild_all_command(self, command, cwd=None, env=None, shell=True):
        """
        Configure a command to rebuild all assets in one go (eg "make all").
        If this is left unset, each registered asset file will be rebuilt
        individually.
        """
        self.rebuild_all_command = BuildCommand(
            command, False, cwd, shell, env
        )

    def add_path(
        self,
        tag,
        p,
        deps=[],
        command=None,
        chdir=False,
        cwd=None,
        env=None,
        shell=True,
    ):
        """
        Add a path to a managed asset file.

        :param tag: a tag for this asset, that can later be used to retrieve
                    groups of related assets. For example if your application
                    has a shopping cart page, then the assets required for this
                    page might be tagged 'cart-js' and 'cart-css'.

        :param p: The filesystem path to the asset file

        :param deps: A list of dependency file specs to be monitored for
                     changes. Example:
                     ``deps=['includes/*.js', '!includes/jquery.js']``

        :param command: a build command specific to this asset file.

        :param chdir: if True, change directory to the asset file's directory
                      when building (only applies if the ``command`` argument
                      is supplied)

        :param cwd: path to a directory in which ``command`` should be
                    run (only applies if the ``command`` argument is supplied)

        :param env: mapping of environment variables to be passed to
                   ``command``

        :param shell: If True (the default), run ``command`` through the shell.
                      If False, execute ``command`` directly.

        """
        p = p.lstrip("/")

        def generate_deps():
            inc_globs = (d for d in deps if not d.startswith("!"))
            exc_globs = (d[1:] for d in deps if d.startswith("!"))

            def expand_globs(globs):
                return {
                    f
                    for pattern in globs
                    for d in self.depdirs
                    for f in d.glob(pattern)
                }

            return expand_globs(self.global_deps) | (
                expand_globs(inc_globs) - expand_globs(exc_globs)
            )

        self.served[p] = self.directory.joinpath(p)
        self.dependencies[p] = generate_deps

        self.tags.setdefault(tag, []).append(p)
        path = pathlib.Path(self.directory) / p
        try:
            relpath = path.relative_to(os.getcwd())
        except ValueError:
            relpath = path
        cmd_args = {"abspath": path, "path": relpath, "dir": path.parent}
        if command is not None:
            command = command.format(**cmd_args)
            self.build_commands[p] = BuildCommand(
                command=command, chdir=chdir, cwd=cwd, env=env, shell=shell
            )
        else:
            self.build_commands[p] = self.default_build_command._replace(
                command=self.default_build_command.command.format(**cmd_args)
            )

    def add_paths(
        self,
        tag,
        paths,
        deps=[],
        command=None,
        chdir=False,
        cwd=None,
        env=None,
        shell=True,
    ):
        """
        Add paths to multiple asset files.

        :param paths: a list or other iterable of string paths

        Other arguments are the same as for :meth:`~assetbuilder.AssetBuilder.add_path`.
        """
        for p in paths:
            self.add_path(tag, p, deps, command, chdir, cwd, env, shell)

    def add_global_dep(self, dep):
        """
        Add a dependency that will be checked for all asset files
        """
        self.global_deps.append(dep)

    def update_cachebuster(self, *assetfiles):
        self.cachebusters[assetfiles] = self.calculate_cachebuster(*assetfiles)

    def urlfor(self, assetfile, baseurl):
        return baseurl + assetfile + "?" + self.get_cachebuster(assetfile)

    def urls(self, *tags: str, environ=None):
        """
        Generate URLs for asset files with the given tag. If ``environ`` is
        supplied and no :attr:`baseurl` has been configured,
        use this to generate absolute URLs.

        :param tag: a string tag, as previously configured through
                    :meth:`add_path`.

        :param environ: (optional) a WSGI environ dict, used to generate
                        absolute URLs in the absence of
                        :attr:`baseurl`
        """
        if environ is not None and "://" not in self.baseurl:
            baseurl = (
                application_uri(environ).rstrip("/")
                + "/"
                + self.baseurl.lstrip("/")
            )
        else:
            baseurl = self.baseurl
        for tag in tags:
            for af in self.tags[tag]:
                yield self.urlfor(af, baseurl)

    def url(self, *tags, environ=None, separator="\n"):
        """
        Generate a single URL for a dynamically generated file of all assets
        with the given tag.

        :param *tags: tags, as previously configured through
                      :meth:`add_path`.

        :param environ: (optional) a WSGI environ dict, used to generate
                        absolute URLs in the absence of
                        :attr:`baseurl`
        """
        if environ is not None and "://" not in self.baseurl:
            baseurl = (
                application_uri(environ).rstrip("/")
                + "/"
                + self.baseurl.lstrip("/")
            )
        else:
            baseurl = self.baseurl
        if not self.autobuild:
            try:
                return self.cached_urls[(baseurl, tags, separator)]
            except KeyError:
                pass

        assetfiles = [af for t in tags for af in self.tags[t]]
        signed_paths = self.serializer.dumps((assetfiles, separator))
        url = (
            baseurl
            + "@@/"
            + signed_paths
            + "/"
            + self.get_cachebuster(*assetfiles)
        )
        self.cached_urls[(baseurl, tags, separator)] = url
        return url

    def paths(self, tag):
        return (self.served[virtual] for virtual in self.tags[tag])

    def cat(
        self, *tags: str, separator="\n", encoding="UTF-8"
    ) -> Iterator[str]:
        """
        Iterate over the content of all asset files with the given tags
        """
        for tag in tags:
            first = True
            eof = "" if encoding else b""
            for virtual in self.tags[tag]:
                if self.autobuild:
                    self.ensure_up_to_date(virtual)
                if not first:
                    yield separator
                path = self.served[virtual]
                with path.open("r", encoding=encoding) as f:
                    yield from iter(lambda: f.read(8192), eof)
                first = False

    def inline(self, *tags: str, separator="\n", encoding="UTF-8") -> str:
        return "".join(self.cat(*tags, separator=separator, encoding=encoding))

    cats = inline

    def rebuild_all(self, clean=False):
        """
        Trigger a rebuild of all asset files.

        :param clean: If ``True``, unlink asset files before
                      rebuilding (ie this will DELETE the file).

        If the ``rebuild_all_command`` property is set, this will be used to
        build all assets in a single step. Otherwise the build command for each
        registered asset will be called in turn.

        This method also clears the ``unbuildable`` set, causing previously
        unbuilt assets to be retried.
        """
        logger.debug("Getting build lock before rebuilding all")
        with portalocker.Lock(".assetbuilder.lock"):
            self.unbuildable.clear()
            if clean:
                for assetfile, path in self.served.items():
                    logger.info("Unlinking %r", str(path))
                    try:
                        os.unlink(str(path))
                    except OSError:
                        pass

            if self.rebuild_all_command:
                self._run_build_command(self.rebuild_all_command)
            else:
                for assetfile, path in self.served.items():
                    self.ensure_up_to_date(assetfile, lock=False)

    def ensure_up_to_date(self, assetfile, lock=None):
        """
        Ensures that the given assetfile is up to date.
        """
        logger.debug("%s: checking is up to date", str(assetfile))

        if assetfile in self.unbuildable:
            logger.debug("%s: is marked as unbuildable", str(assetfile))
            return

        if lock:
            logger.debug("Getting build lock for %r", assetfile)
            with portalocker.Lock(".assetbuilder.lock"):
                self.ensure_up_to_date(assetfile, False)
                return

        if assetfile in self.unbuildable:
            return
        path = self.served[assetfile]
        if not path.exists():
            self._make(assetfile)
            if not path.exists():
                logger.warning(
                    "Tried to build %r, "
                    "but no file was created!\n"
                    "    build_command is %r",
                    path,
                    self.build_commands[assetfile],
                )

                self.unbuildable.add(assetfile)
            self.update_cachebuster(assetfile)
            return

        asset_mtime = path.stat().st_mtime
        try:
            deps = self.dependencies_cache[assetfile]
        except KeyError:
            deps = self.dependencies[assetfile]()
            self.dependencies_cache[assetfile] = deps
        deps = deps - self.negative_deps[assetfile]

        updated_deps = [d for d in deps if d.stat().st_mtime > asset_mtime]
        if updated_deps:
            logger.info(
                "%s: rebuilding (changed files: %r)",
                str(path),
                [str(d) for d in updated_deps],
            )
            success = self._make(assetfile)
            if success and path.stat().st_mtime == asset_mtime:
                logger.info(
                    "%s: file was not updated after rebuilding", str(path)
                )
                logger.debug(
                    "%s: removing files from dependency list: %r",
                    str(path),
                    [str(d) for d in updated_deps],
                )
                self.negative_deps[assetfile].update(updated_deps)
        else:
            logger.debug("%s has no updated dependencies", str(path))

        self.update_cachebusters()

    def update_cachebusters(self):
        """
        Check all cachebusters and update any that are out of date
        """
        for assetfile, path in self.served.items():
            try:
                mtime, _ = self.cachebusters[assetfile]
            except KeyError:
                mtime = 0
            try:
                if mtime < path.stat().st_mtime:
                    self.update_cachebuster(assetfile)
            except FileNotFoundError:
                pass

    def _make(self, assetfile):
        path = self.served[assetfile]
        build_command = self.build_commands[assetfile]
        return self._run_build_command(build_command, path)

    def _run_build_command(self, build_command, relpath=None):
        if relpath and build_command.chdir:
            cwd = str(relpath.parent)
        else:
            cwd = build_command.cwd or os.getcwd()

        logger.debug("Calling %r in %r", build_command.command, cwd)
        returncode = subprocess.call(
            [build_command.command],
            shell=build_command.shell,
            cwd=cwd,
            env=build_command.env,
        )
        if returncode != 0:
            logger.error(
                "Command %r exited with status %r " "(cwd=%s; env=%r)",
                build_command.command,
                returncode,
                cwd,
                build_command.env,
            )
            return False
        return True

    def get_cachebuster(self, *assetfiles):
        for assetfile in assetfiles:
            if self.autobuild:
                self.ensure_up_to_date(assetfile)
        if assetfiles not in self.cachebusters:
            self.update_cachebuster(*assetfiles)
        return self.cachebusters.get(assetfiles, [0, ""])[1]

    def calculate_cachebuster(self, *assetfiles):
        latest_mtime = 0
        h = hashlib.sha1()
        for assetfile in assetfiles:
            try:
                mtime = self.served[assetfile].stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
                with self.served[assetfile].open("rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if chunk == b"":
                            break
                        h.update(chunk)
            except OSError:
                pass

        return latest_mtime, h.hexdigest()[:8]

    def __call__(self, environ, start_response):

        path = getenv(environ, "PATH_INFO").lstrip("/")
        qs = getenv(environ, "QUERY_STRING", "")
        if path.strip("/") == "update" and self.autobuild:
            self.rebuild_all(clean=(qs.lower() == "clean"))
            start_response("204 no content", [])
            return []

        if path.startswith("@@/"):
            remaining, cachebuster = path[3:].split("/", 1)
            requested_paths, separator = self.serializer.loads(remaining)
        else:
            requested_paths = [path]
            separator = ""
            cachebuster = qs

        paths = []
        ab_served = True
        for path in requested_paths:
            p = None
            if path in self.served:
                p = self.served[path]
                if self.autobuild:
                    self.ensure_up_to_date(path)
            else:
                ab_served = False
                try:
                    p = self.directory.joinpath(path).resolve()
                    if not p.is_file():
                        p = None
                except OSError:
                    p = None

            if p is None:
                start_response(
                    "404 not found", [("Content-Type", "text/plain")]
                )
                return [b"not found."]
            paths.append(p)

        cachebuster_valid = (
            ab_served
            and cachebuster
            and cachebuster == self.get_cachebuster(*requested_paths)
        )

        return serve_static_files(
            paths, separator, cachebuster_valid, environ, start_response
        )


def serve_static_files(
    paths: List[pathlib.Path],
    separator: bytes,
    cachebuster_valid: bool,
    environ: Dict[str, Any],
    start_response: Callable,
    bufsize: int = 8192,
):
    """
    Serve the concatenated static files located at ``paths``.
    """

    mod_since = getenv(environ, "HTTP_IF_MODIFIED_SINCE")
    if mod_since:
        try:
            mod_since = mktime_tz(parsedate_tz(mod_since))
        except (TypeError, OverflowError):
            start_response("400 bad request", [("Content-Type", "text/plain")])
            return ["invalid if-modified-since value"]

    try:
        stats = [path.stat() for path in paths]
    except OSError:
        logger.debug("Could not stat a file in %r", str(paths))
        start_response("404 not found", [("Content-Type", "text/plain")])
        return [b"not found."]

    last_modified = max(s.st_mtime for s in stats)
    if mod_since and last_modified <= mod_since:
        start_response("304 not modified", [])
        return []

    ct = mimetypes.guess_type(str(paths[0]))[0] or "application/octet-stream"

    total_length = sum(s.st_size for s in stats) + (len(paths) - 1) * len(
        separator
    )
    files = []
    try:
        for path in paths:
            files.append(path.open("rb"))
    except IOError:
        for f in files:
            f.close()
        start_response("403 forbidden", [("Content-Type", "text/plain")])
        return ["access denied."]

    headers = [
        ("Content-Type", ct),
        ("Content-Length", str(total_length)),
        ("Date", format_date(time.gmtime())),
        ("Last-Modified", format_date(time.gmtime(last_modified))),
        ("Expires", "Wed, 20 Jan 2038 00:00:00 GMT"),
    ]
    if cachebuster_valid:
        headers.append(
            ("Cache-Control", "immutable, max-age=700000000, public")
        )

    if len(paths) == 1:
        fileob = files[0]
    else:
        fileob = MultiFileWrapper(files, separator)

    file_wrapper = environ.get("wsgi.file_wrapper")
    if False and file_wrapper is not None:

        def content_iterator(f=fileob, bufsize=bufsize):
            return file_wrapper(f, bufsize)

    else:

        def content_iterator(f=fileob, bufsize=bufsize):
            try:
                while True:
                    c = f.read(bufsize)
                    if c == b"":
                        break
                    yield c
            finally:
                f.close()

    start_response("200 OK", headers)
    return content_iterator()


def format_date(utctimetuple):
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
        ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[utctimetuple[6]],
        utctimetuple[2],
        (
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        )[utctimetuple[1] - 1],
        utctimetuple[0],
        utctimetuple[3],
        utctimetuple[4],
        utctimetuple[5],
    )
