# Copyright 2019 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Helpers for automatic tests.

These allow both high level operation on testing repos, and lower level
calls and introspections, making it possible to test more exhaustively inner
code paths that with `.t` tests, which are really functional tests.
"""
import os
from mercurial import (
    cmdutil,
    commands,
    hg,
    node,
    phases,
    ui as uimod,
)
import random
import time

# re-exports for stability
NULL_REVISION = node.nullrev
NULL_ID = node.nullid


def as_bytes(s):
    """Whether s is a path, an str, or bytes, return a bytes representation.

    Explicitely, the conversion to bytes is done in UTF-8, so that it cannot
    fail.

    If that doesn't suit your case, just encode your string or path
    before hand as needed.
    """
    if s is None:
        return None
    if isinstance(s, bytes):
        return s
    return str(s).encode('utf-8')


def make_ui(base_ui, config=None):
    # let's make sure we aren't polluted by surrounding settings
    os.environ['HGRCPATH'] = ''
    if base_ui is None:
        ui = uimod.ui.load()
    else:
        ui = base_ui.copy()

    # with load(), ui.environ is encoding.environ, with copy() it's not copied
    # we need the environ to be unique for each test to avoid side effects.
    # Also, on Python 2, encoding.environ is os.environ, leading to even
    # worse side effects.
    ui.environ = dict(ui.environ)

    # we want the most obscure calls to ui output methods to be executed
    # in tests. With the default settings, ui.note() early returns for example
    # meaning that only its arguments are tested, not what it does of them.
    ui.setconfig(b'ui', b'debug', b'yes')

    if config is not None:
        for section_name, section in config.items():
            for item_name, item_value in section.items():
                ui.setconfig(as_bytes(section_name),
                             as_bytes(item_name),
                             as_bytes(item_value),
                             source=b'tests')
    return ui


class LocalRepoWrapper(object):
    """Facilities for handling Mercurial repositories.

    As the name suggests, this is a wrapper class that embeds an
    instance of :class:`mercurial.localrepo.localrepo` as :attr:`repo`.

    It provides helper methods for initialization and content creation or
    mutation, both in the working directory and in changesets.

    For convenience, these high level methods accept both unicode and bytes
    strings. The path objects used by pytest can be used readily where
    a path is expected. There is one notable exception to this:
    the generic :meth:`command` which is designed to forward its arguments
    to the underlying Mercurial command directly.

    All return values that are from Mercurial are untouched, hence strings
    would be bytes.

    All conversions to bytes are done with the UTF-8 codec. If that doesn't
    suit your case, simply encode your strings before hand.
    Running unmodified tests based on this helpers on a non UTF-8 filesystem
    is not supported at this point, but it could be done, we are open to
    suggestions.
    """

    def __init__(self, repo):
        self.repo = repo

    @classmethod
    def init(cls, path, base_ui=None, config=None):
        path = as_bytes(str(path))
        init = cmdutil.findcmd(b'init', commands.table)[1][0]
        ui = make_ui(base_ui, config)
        init(ui, dest=path)
        return cls(hg.repository(ui, path))

    @classmethod
    def load(cls, path, base_ui=None, config=None):
        ui = make_ui(base_ui, config=config)
        return cls(hg.repository(ui, as_bytes(path)))

    @classmethod
    def share_from_path(cls, src_path, dest_path,
                        ui=None, base_ui=None, config=None,
                        **share_opts):
        """Create a new repo as the `share` command would do.

        :param ui: if specified, will be copied and used for the new repo
                   creation through ``share``
        :param config: only if ``ui`` is not specified, will be used to
                       create a new ``ui`` instance
        :param base_ui: only if ``ui`` is not specified, will be used to
                       create a new :class:`ui` instance
        :param share_opts: passed directly to :func:`hg.share()`
        :return: wrapper for the new repo
        """
        if ui is None:
            ui = make_ui(base_ui, config=config)
        else:
            # TODO not enough for environ independence
            ui = ui.copy()

        # the 'share' command defined by the 'share' extension, is just a thin
        # wrapper around `hg.share()`, which furthermore returns a repo object.
        return cls(hg.share(ui, as_bytes(src_path), dest=as_bytes(dest_path),
                            **share_opts))

    def share(self, dest_path, **share_opts):
        return self.share_from_path(self.repo.root, dest_path,
                                    ui=self.repo.ui, **share_opts)

    def command(self, name, *args, **kwargs):
        cmd = cmdutil.findcmd(as_bytes(name), commands.table)[1][0]
        repo = self.repo
        return cmd(repo.ui, repo, *args, **kwargs)

    def write_commit(self, rpath,
                     content=None, message=None,
                     return_ctx=True,
                     parent=None,
                     branch=None,
                     user=None,
                     utc_timestamp=None,
                     topic=None):
        """Write content at rpath and commit in one call.

        This is meant to allow fast and efficient preparation of
        testing repositories. To do so, it goes a bit lower level
        than the actual commit command, so is not suitable to test specific
        commit options, especially if through extensions.

        This leaves the working directoy updated at the new commit.

        :param rpath: relative path from repository root. If existing,
                      will be overwritten by `content`
        :param content: what's to be written in ``rpath``.
                        If not specified, will be replaced by random content.
        :param message: message commit. If not specified, defaults to
                        ``content``
        :param parent: binary node id or :class:`changectx` instance.
                       If specified, the repository is
                       updated to it first. Useful to produce branching
                       histories. This is single valued, because the purpose
                       of this method is not to produce merge commits.
        :param user: full user name and email, as in ``ui.username`` config
                     option. Can be :class:`str` or :class:`bytes`
        :param utc_timestamp: seconds since Epoch UTC. Good enough for
                              tests without ambiguity. Can be float (only
                              seconds will be kept). Defaults to
                              ``time.time()``
        :param return_ctx: if ``True``, returns a :class:`changectx` instance
                           and a binary node id otherwise, which can be more
                           straightforward and faster in some cases.
        :returns: :class:`changectx` instance or binary node id for the
                  generated commit, according to ``return_ctx``.
        """
        repo = self.repo
        path = os.path.join(repo.root, as_bytes(rpath))
        if parent is not None:
            if isinstance(parent, bytes):
                self.update_bin(parent)
            else:
                self.update(parent.hex())

        if content is None:
            content = "random: {}\n\nparent: {}\n".format(
                random.random(),
                node.hex(repo.dirstate.p1()))
        content = as_bytes(content)

        if message is None:
            message = content

        if branch is not None:
            self.repo.dirstate.setbranch(as_bytes(branch))

        if topic is not None:
            self.command(b'topics', as_bytes(topic))

        with open(path, 'wb') as fobj:
            fobj.write(content)

        if utc_timestamp is None:
            utc_timestamp = time.time()

        def commitfun(ui, repo, message, match, opts):
            return self.repo.commit(message,
                                    as_bytes(user),
                                    (int(utc_timestamp), 0),
                                    match=match,
                                    editor=False,
                                    extra=None)
        new_node = cmdutil.commit(repo.ui, repo, commitfun, (path, ),
                                  {b'addremove': True,
                                   b'message': as_bytes(message),
                                   })
        return repo[new_node] if return_ctx else new_node

    def update_bin(self, bin_node, **opts):
        """Update to a revision specified by its node in binary form.

        This is separated in order to avoid ambiguities
        """
        # maybe we'll do something lower level later
        self.update(node.hex(bin_node), **opts)

    def update(self, rev, hidden=False):
        repo = self.repo.unfiltered() if hidden else self.repo
        cmdutil.findcmd(b'update', commands.table)[1][0](repo.ui, repo,
                                                         as_bytes(rev))

    def set_phase(self, phase_name, revs, force=True):
        repo = self.repo
        opts = dict(force=force, rev=[as_bytes(r) for r in revs])
        phase_name_bytes = as_bytes(phase_name)
        opts.update((phn.decode(), phn == phase_name_bytes)
                    for phn in phases.cmdphasenames)
        cmdutil.findcmd(b'phase', commands.table)[1][0](repo.ui, repo, **opts)

    def prune(self, revs, successors=(), bookmarks=()):
        # the prune command expects to get all these arguments (it relies
        # on the CLI defaults but doesn't have any at the function call level).
        # They are unconditionally concatened to lists, hence must be lists.
        # (as of Mercurial 5.3.1)
        if isinstance(revs, (bytes, str)):
            revs = [revs]
        return self.command('prune',
                            rev=[as_bytes(r) for r in revs],
                            new=[],  # deprecated yet expected
                            # TODO py3 convert these two to bytes as needed:
                            successor=list(successors),
                            bookmark=list(bookmarks))
