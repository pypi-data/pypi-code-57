# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Interaction with Git repos.

It is not expected that the rise of the HGitaly project would remove
all interesting things to do with Git.
"""
from __future__ import absolute_import

from dulwich.protocol import ZERO_SHA
from dulwich.repo import check_ref_format
from hggit.git_handler import GitHandler
from heptapod import (
    util,
)
from heptapod.gitlab.hooks import (
    PreReceive,
    PostReceive,
)
from heptapod.gitlab.prune_reasons import (
    HeadPruneReason,
    TopicPublished,
    AllHeadsBookmarked,
    BranchClosed,
    BookmarkRemoved,
    WildHeadResolved,
)
from hgext3rd.evolve import headchecking
from mercurial.i18n import _
from mercurial.node import hex
from mercurial import (
    error,
    hg,
    phases,
    pycompat,
)
import re
import traceback

from . import obsutil

GIT_BRANCH_REF_PREFIX = b'refs/heads/'


class MultipleDescendants(LookupError):
    pass


class InvalidRef(ValueError):
    pass


class InvalidGitLabBranch(ValueError):
    pass


def git_branch_ref(branch):
    return GIT_BRANCH_REF_PREFIX + branch


def git_branch_from_ref(ref):
    """Return git branch name from a ref name.

    Examples::

      >>> pycompat.sysstr(git_branch_from_ref(b'refs/heads/some/branch'))
      'some/branch'
      >>> git_branch_from_ref(b'refs/tags/1.0.1') is None
      True


    Special case for robustness::

      >>> git_branch_from_ref(None) is None
      True
    """

    if ref is None or not ref.startswith(GIT_BRANCH_REF_PREFIX):
        return None
    return ref[len(GIT_BRANCH_REF_PREFIX):]


TOPIC_REF_PREFIX = git_branch_ref(b'topic/')

NAMED_BRANCH_REF_PREFIX = git_branch_ref(b'branch/')


def ref_is_topic(ref):
    return ref.startswith(TOPIC_REF_PREFIX)


def ref_is_named_branch(ref):
    return ref.startswith(NAMED_BRANCH_REF_PREFIX)


def parse_git_branch_ref(ref):
    """Parse a Git branch ref for named branch and topic information

    Return ``None`` if ``ref`` is not a Git branch. This is considered
    to be a normal case::

      >>> parse_git_branch_ref(b"refs/tags/v1.2.3") is None
      True

    Example with a topical GitLab branch::

      >>> parsed = parse_git_branch_ref(b"refs/heads/topic/default/thetop")
      >>> parsed == (b'default', b'thetop')
      True

    For named branches, the returned topic is ``None``. Checking for `None`
    is the normal way for downstream code to know if this is a topic or not::

      >>> parsed = parse_git_branch_ref(b"refs/heads/branch/default")
      >>> parsed == (b'default', None)
      True

    Special case: forward slashes are considered part of the named branch::

      >>> parsed = parse_git_branch_ref(b"refs/heads/branch/ze/branch")
      >>> parsed == (b'ze/branch', None)
      True

      >>> try:
      ...     _ = parse_git_branch_ref(b"refs/heads/topic/invalid")
      ... except InvalidRef as exc:
      ...     print(pycompat.sysstr(exc.args[0]))
      ... else:
      ...     print("Expected InvalidRef exception not raised")
      refs/heads/topic/invalid
    """
    git_branch = git_branch_from_ref(ref)
    if git_branch is None:
        return None
    try:
        return parse_gitlab_branch(git_branch)
    except InvalidGitLabBranch:
        raise InvalidRef(ref)


def parse_gitlab_branch(git_branch):

    topic_prefix = b'topic/'
    if git_branch.startswith(topic_prefix):
        res = tuple(git_branch.split(b'/', 1)[1].rsplit(b'/', 1))
        if len(res) != 2:
            raise InvalidGitLabBranch(git_branch)
        return res

    named_branch_prefix = b'branch/'
    if git_branch.startswith(named_branch_prefix):
        return git_branch[len(named_branch_prefix):], None


class GitRefChange(object):
    """Represent a change to be performed in a target Git repo.

    Public attributes:

    - :attr:`ref`: Git ref name
    - :attr:`before`, :attr:`after`: Git SHAs

    These will be complemented with a system of options, e.g., to specify that
    a topic change actually comes with publication, leading to a deferred
    removal of the corresponding Git branch once all appropriate treatments are
    done, whether this removal is performed from here or by GitLab.
    """

    def __init__(self, ref, before, after):
        self.ref = ref
        self.before = before
        self.after = after

    def is_creation(self):
        return self.before == ZERO_SHA and self.after != ZERO_SHA


class HeptapodGitHandler(GitHandler):

    def __init__(self, *args, **kwargs):
        super(HeptapodGitHandler, self).__init__(*args, **kwargs)

        main_repo = hg.sharedreposource(self.repo)
        if main_repo is None:
            main_repo = self.repo

        self.gitdir = re.sub(br'\.hg$', b'', main_repo.root) + b'.git'
        self.unfiltered_repo = self.repo.unfiltered()

    def heptapod_gate_bookmarks(self, repo, allow, changes):
        """First handling of bookmark changes (refuse or not), return deleted.

        :param repo: passed explicitely because filtering may differ from
                     :attr:`repo`.
        :return: iterable of deleted bookmarks
        """
        if not changes:
            return ()

        ui = repo.ui
        deleted = []
        ui.note(b"HeptapodGitHandler bookmark changes=%r" % changes)
        new_bookmarks = []

        for name, change in changes.items():
            if change[0] is None:
                new_bookmarks.append(name)
            elif change[1] is None:
                deleted.append(name)

        if new_bookmarks and not allow:
            raise error.Abort(_(
                b"Creating bookmarks is forbidden by default in Heptapod "
                b"(got these new ones: %s). "
                b"See https://heptapod.net/pages/faq.html#bookmarks to "
                b"learn why and how to partially lift "
                b"that restriction" % util.format_bytes_list(new_bookmarks)))
        for new_bm_name, (_ign, new_bm_node) in pycompat.iteritems(changes):
            new_bm_ctx = repo[new_bm_node]
            new_bm_topic = new_bm_ctx.topic()
            if new_bm_topic:
                raise error.Abort(_(
                    b"Creating or updating bookmarks on topic "
                    b"changesets is forbidden"),
                    hint=b"topic '%s' and bookmark '%s' for changeset %s" % (
                        new_bm_topic, new_bm_name, new_bm_ctx.hex()))
        return deleted

    def get_exportable(self):
        """Heptapod version, including named branches and topics.

        This rewraps :meth:`GitHandler.get_exportable` to add named branches
        and topics to the returned Git refs
        """
        git_refs = super(HeptapodGitHandler, self).get_exportable()
        logprefix = b'HeptapodGitHandler.get_exportable '
        repo = self.repo.filtered(b'served')
        ui = repo.ui

        # "exporting" the ZERO_SHA will mean by convention a request to prune
        # the corresponding heads -- only a request, we can't really decide
        # at this stage.
        # The value is a dict mapping refs to reasons (instances of
        # `HeadPruneReason` or simple strings if it needs to be refined later)
        to_prune = git_refs[ZERO_SHA] = {}

        txn = repo.currenttransaction()
        allow_bookmarks = ui.configbool(b'experimental',
                                        b'hg-git.bookmarks-on-named-branches')
        bm_changes = txn.changes.get(b'bookmarks') if txn is not None else None
        deleted_bms = self.heptapod_gate_bookmarks(
            repo, allow_bookmarks, bm_changes)

        to_prune.update((bm, BookmarkRemoved()) for bm in deleted_bms)
        all_bookmarks = self.repo._bookmarks
        # currently, self_filter_for_bookmarks() only does some renaming,
        # and doesn't discard any, so this is actually just equivalent to
        # hgshas of all bookmarks, but that may change in future hg-git
        hgshas_with_bookmark_git_ref = {
            hex(all_bookmarks[bm])
            for _, bm in self._filter_for_bookmarks(all_bookmarks)}
        for branch, hg_nodes in repo.branchmap().iteritems():
            gb = self.git_branch_for_branchmap_branch(branch)
            revs = [repo[n].rev() for n in hg_nodes]
            ctxs = [repo[r]
                    for r in headchecking._filter_obsolete_heads(repo, revs)]

            if ui.configbool(b'experimental',
                             b'hg-git.prune-newly-closed-branches', True):
                ctxs = [c for c in ctxs if not c.closesbranch()]
                if not ctxs:
                    ui.note(logprefix,
                            b"All heads of branch '%s' are closed" % branch)
                    to_prune[gb] = 'closed'  # will be refined later on

            hg_shas = {c.hex() for c in ctxs}
            # We ignore bookmarked changesets because:
            # - we don't want them in the 'wild' namespace
            # - no other Git ref would be relevant for them
            hg_shas.difference_update(hgshas_with_bookmark_git_ref)
            if not hg_shas:
                if hg_nodes and allow_bookmarks:
                    # after removal of bookmarks, but not before,
                    # there is no hg head on this named branch:
                    # schedule potential removal. We don't want to do
                    # this if bookmarks aren't explicitely allowed because
                    # this must be a side effect, potentially disturbing, of
                    # an implicit bookmark move
                    to_prune[gb] = AllHeadsBookmarked()
                ui.note(logprefix,
                        b"Branch '%s' has no visible"
                        b"non-bookmarked head" % branch)
                continue

            if 1 < len(hg_shas):
                ui.note(logprefix, b"Multiple heads for branch '%s': %r" % (
                    branch, util.format_bytes_list(hg_shas)))
                for hg_sha in hg_shas:
                    git_refs[hg_sha].heads.add(
                        git_branch_ref(b'wild/' + hg_sha))
                gca = self.multiple_heads_choose(hg_shas, branch)
                if gca is None:
                    # giving up in order to avoid confusing situations
                    continue
                gca_sha = self.repo[gca].hex()
                ui.note(logprefix,
                        b"Chose %s out of multiple heads %s "
                        b"for forwarding branch %r" % (
                            gca_sha, util.format_bytes_list(hg_shas), branch))
                hg_shas = [gca_sha]
            hg_sha = hg_shas.pop()
            gb = self.git_branch_for_branchmap_branch(branch)
            git_refs[hg_sha].heads.add(git_branch_ref(gb))
        return git_refs

    def published_topic_latest_hg_sha(self, topic, ctx, log_before_ctx=None):
        """Rewrapping of `latest_topic_descendant` returning hg sha.
        """
        ui = self.repo.ui
        try:
            after_ctx = self.latest_topic_descendant(topic, ctx)
        except MultipleDescendants:
            msg = (b"Found several descendants in topic '%s' of the "
                   b"newly published '%s'. Can't have GitLab add them "
                   b"to any related merge request. ") % (topic, ctx)
            ui.warn(msg)
            ui.status(msg)
            # since successor is public, chances to detect merge are good
            return ctx.hex()

        if after_ctx is None:
            ui.warn(b"HeptapodGitHandler.published_topic_latest_hg_sha "
                    b"inspecting public changeset '%s' for topic '%s' gave "
                    b"inconsistent result: it's not in the expected topic. "
                    b"This will trigger immediate pruning of the "
                    b"topic Git branch" % (ctx, topic))
            return None

        ui.note(b'HeptapodGitHandler.published_topic_latest_hg_sha',
                b"updating published '%s' from '%s' to '%s'" % (
                    topic,
                    log_before_ctx if log_before_ctx is not None else ctx,
                    after_ctx))
        return after_ctx.hex()

    def prune_topic_with_sha(self, reason_cls, branch, topic, hg_sha):
        """Generate a `reason_cls` instance with the Git sha for `hg_sha`
        """
        git_sha = self.map_git_get(hg_sha)
        if git_sha is None:
            # TODO when we won't convert to Git any more, not
            # saying anything to GitLab won't be an option.
            self.repo.ui.warn(
                b"Analysis of topic '%s' for branch '%s' "
                b"that becomes invisible in this transaction "
                b"to report its latest change to GitLab "
                b"found Mercurial changeset %s that has no known "
                b"Git counterpart. Giving up on reporting "
                b"that topic/branch combination to GitLab." % (
                    topic, branch, hg_sha))
            return None
        else:
            return reason_cls(git_sha)

    def analyse_vanished_topic(self, branch, topic, before_sha,
                               log_info):
        """Compute revision to send GitLab as new topic branch head.

        This method does not access the Git repository.

        :param before_sha: Mercurial SHA for the current Git head of the topic
                           GitLab branch. Can be ``None`` if the Git head is
                           actually unknown to Mercurial.
        :param log_info: dict of useful information for logs that we must
                         restrain not to use for other purposes in this method
                         (typically some Git context).
                         Has to be given with bytes keys because
                         `b'%(key)s' % d` looks for b`key` in `d`
        :return: Mercurial SHA, or ``None`` to trigger pruning.
        """
        logprefix = b'HeptapodGitHandler.topic_new_hg_sha '
        ui = self.repo.ui
        initial_import = ui.configbool(b"heptapod", b"initial-import")
        try:
            # TODO case where before_sha is None. same error treatment?
            before_ctx = self.unfiltered_repo[before_sha]
        except error.RepoLookupError:
            log_info[b'before_sha'] = before_sha
            ui.warn(logprefix, b"Git '%(ref)s' "
                    b"(gitsha=%(before_git_sha)s, hgsha=%(before_sha)s) not "
                    b"found in the Mercurial repo (should be due to "
                    b"some half-rollbacked previous transaction), pruning "
                    b"as the topic does not seem "
                    b"to be visible anymore" % log_info)
            return HeadPruneReason()

        if before_ctx.phase() == phases.public:
            latest_sha = self.published_topic_latest_hg_sha(topic, before_ctx)
            if latest_sha is None:
                # this is a corruption: resolving the Git branch for the topic
                # actually gives us a changeset that does not bear that topic!
                # This is what happened in heptapod#265.
                # In that case, we return it unchanged. The changeset
                # surely is an ancestor of the current named branch head
                # GitLab's MR detection should thus work.
                latest_sha = before_sha
            return self.prune_topic_with_sha(
                TopicPublished, branch, topic, latest_sha)
        try:
            succctx = obsutil.latest_unique_successor(before_ctx)
        except error.Abort as exc:
            if initial_import:
                # we don't want to break an initial import because
                # of an exceptional phase divergence, let's keep it unchanged
                # TODO UPSTREAM evolve gives us a message in str instead
                # of the standard bytes for error.Abort
                ui.warn(logprefix + pycompat.sysbytes(exc.args[0]))
                return HeadPruneReason()
            else:
                raise

        if succctx is None:
            ui.note(logprefix,
                    b"scheduling prune of %(ref)s "
                    b"(obsolete, no successor)" % log_info)
            return HeadPruneReason()

        succ_phase = succctx.phase()
        if succ_phase == phases.public:
            latest_sha = None
            if not initial_import:
                latest_sha = self.published_topic_latest_hg_sha(
                    topic, succctx, log_before_ctx=before_ctx)
            if latest_sha is None:
                return HeadPruneReason()
            return self.prune_topic_with_sha(
                TopicPublished, branch, topic, latest_sha)

        elif succ_phase == phases.draft:
            # let's go over some reasons why there's no visible branch/topic
            # head and the former one is obsolete with a draft successor
            succ_brtop = (succctx.branch(), succctx.topic())
            before_brtop = (before_ctx.branch(), before_ctx.topic())
            if succ_brtop != before_brtop:
                log_info.update({b'before': before_ctx.hex(),
                                 b'succ': succctx.hex()})
                ui.note(logprefix,
                        b"pruning '%(ref)s' (hgsha %(before)s), "
                        b"as its successor %(succ)s "
                        b"is on another branch or topic" % log_info)
                # TODO we may want to refine that one
                return HeadPruneReason()

        return HeadPruneReason()

    def generate_prune_changes(self, to_prune, existing):
        """Generate those pruning Git changes that really have to be done.

        :return: a complete list of `HeadPruneReason` instances and
                 a `dict` mapping Git refs to the corresponding
                 :class:`GitRefChange` instances.

        In a further version, we may get rid of the :class:`GitRefChange`
        instances. For now, they would help adding the prune reason logic
        to the GitLab side with minimal disruption.

        This method does not use the Git repo, only the :meth:`map_hg_get`
        """
        changes = {}
        prune_reasons = {}
        prune_previously_closed_branches = self.repo.ui.configbool(
            b'experimental', b'hg-git.prune-previously-closed-branches')
        for gitlab_branch, reason in pycompat.iteritems(to_prune):
            ref = git_branch_ref(gitlab_branch)
            before_sha = existing.get(ref)
            if before_sha is None:
                continue
            if reason == 'closed':
                reason = self.analyse_closed_branch(
                    gitlab_branch, before_sha,
                    prune_previously_closed=prune_previously_closed_branches)
                if reason is None:
                    continue
            changes[ref] = GitRefChange(ref, before_sha, ZERO_SHA)
            prune_reasons[gitlab_branch] = reason
        return prune_reasons, changes

    def analyse_closed_branch(self, gitlab_branch, before_sha,
                              prune_previously_closed=True):
        """Decide whether to prune and provide details.

        :return: `None` to avoid pruning, or a :class:`HeadPruneReason` with
                 all expected details.
        """
        hg_branch = parse_gitlab_branch(gitlab_branch)[0]
        if prune_previously_closed:
            return BranchClosed()

        before_hg_sha = self.map_hg_get(before_sha)

        # In cases we can't find the Mercurial changeset for the latest known
        # Git changeset, we can't really know if the closing is new,
        # but being unknown to Mercurial, it certainly has to be pruned.
        if before_hg_sha is None:
            self.repo.ui.warn(
                b"Pruning closed branch '%s' previous Git sha has no "
                b"known Mercurial counterpart." % gitlab_branch
            )
            return BranchClosed()

        try:
            before_ctx = self.repo[before_hg_sha]
        except error.RepoLookupError:
            self.repo.ui.warn(
                b"Pruning closed branch '%s', whose "
                b"latest Git commit %r corresponds to the unknown "
                b"%s hg sha" % (gitlab_branch, before_sha, before_hg_sha))
            return BranchClosed()

        if before_ctx.closesbranch() and not prune_previously_closed:
            return None

        return self.prune_closed_branch(hg_branch)

    def prune_closed_branch(self, branch):
        """Generate a `BranchClosed` instance with the wished details.

        See :class:`BranchClosed` for description of the expected details.
        """
        repo = self.repo
        txn = repo.currenttransaction()
        info = []
        for new_closing_rev in self.repo.revs(
                b'%d: and branch(%s) and closed()',
                txn.changes[b'origrepolen'], branch):
            ctx = repo[new_closing_rev]
            parents = []
            for parent_ctx in ctx.parents():
                git_sha = self.map_git_get(parent_ctx.hex())
                if git_sha is not None:
                    parents.append(git_sha)
            info.append((self.map_git_get(ctx.hex()), parents))
        return BranchClosed(info)

    def analyze_vanished_refs(self, existing, exportable):
        """Decide what to do of existing Git refs that aren't in exportable.

        All will have to be pruned on the GitLab side, this methods tells
        why.

        :return: dict mapping refs to :class:`HeadPruneReason` instances
        """
        to_prune = {}
        exported_refs = {ref for heads_tags in exportable.values()
                         for ref in heads_tags}
        for ref, before_git_sha in pycompat.iteritems(existing):
            if ref in exported_refs:
                continue

            gitlab_branch = git_branch_from_ref(ref)
            if gitlab_branch is None:
                continue

            if ref.startswith(b'refs/heads/wild/'):
                to_prune[gitlab_branch] = WildHeadResolved(before_git_sha)
            try:
                branch_topic = parse_gitlab_branch(gitlab_branch)
            except InvalidGitLabBranch:
                self.repo.ui.warn(b"Git mirror repo has a bogus branch "
                                  b"ref '%s' "
                                  b"that's not among the exportable ones. "
                                  b"Ignoring it." % ref)
                continue
            if branch_topic is not None and branch_topic[1]:
                branch, topic = branch_topic
                before_hg_sha = self.map_hg_get(before_git_sha)
                prune_reason = self.analyse_vanished_topic(
                    branch, topic, before_hg_sha,
                    log_info={b'ref': ref, b'before_git_sha': before_git_sha},
                )
                if prune_reason is not None:
                    to_prune[gitlab_branch] = prune_reason

        return to_prune

    def compare_exportable(self, existing, exportable):
        """Analyse the exportable refs to produce Git changes

        :param exportable: a mapping from Git refs to Mercurial SHAs
        :param existing: a mapping of existing Git refs in the target repo
                         to Git SHAs
        :returns: a mapping from Git refs to :class:`GitRefChange` objects
        """
        # HEAD is the source of truth for GitLab default branch
        default_git_branch = git_branch_from_ref(
            self.git.refs.get_symrefs().get(b'HEAD'))
        to_prune = exportable.pop(ZERO_SHA, {})
        to_prune.update(self.analyze_vanished_refs(existing, exportable))
        to_prune.pop(default_git_branch, None)

        prune_reasons, changes = self.generate_prune_changes(to_prune,
                                                             existing)

        for hg_sha, refs in pycompat.iteritems(exportable):
            for ref in refs.heads:
                after_sha = self.map_git_get(hg_sha)
                before_sha = existing.get(ref, ZERO_SHA)
                if after_sha and after_sha != before_sha:
                    changes[ref] = GitRefChange(ref, before_sha, after_sha)

        if self.is_wiki():
            # GitLab wikis are much hardwired onto 'master' in a Git repo
            on_default = changes.get(git_branch_ref(b'branch/default'))
            if on_default is not None:
                master = git_branch_ref(b'master')
                changes[master] = GitRefChange(
                    master, on_default.before, on_default.after)

        return prune_reasons, changes

    def is_wiki(self):
        """Tell whether self.repo is the storage for a GitLab wiki"""
        return (self.repo.ui.environ.get(b'GL_REPOSITORY', b'')
                .startswith(b'wiki-'))

    def heptapod_notify_gitlab(self, hook, prune_reasons, changes,
                               allow_error=False):
        if not changes and not prune_reasons:
            return

        ui = self.repo.ui

        converted_changes = {ref: (ch.before, ch.after)
                             for ref, ch in pycompat.iteritems(changes)}

        # a verbose log line that will help with issues such as heptapod#278
        ui.note(pycompat.sysbytes(
            "heptapod_notify_gitlab firing hook %r "
            "for changes %r" % (hook, (prune_reasons, converted_changes))))
        try:
            code, out, err = hook((prune_reasons, converted_changes))
        except Exception as exc:
            ui.error(pycompat.sysbytes(
                "GitLab update error (%s): %r\n%s" % (
                    hook, exc, traceback.format_exc())))
            if allow_error:
                # that's an error in py-heptapod, could be a network failure
                # once we call the internal API directly, for instance
                return
            else:
                raise

        if code != 0:
            # bytes conversion for hg ui methods and exceptions
            err = pycompat.sysbytes(err)
            ui.error(b"Got code %s while sending GitLab '%s' "
                     b"hook details=%s" % (
                         pycompat.sysbytes(repr(code)), hook, err))
            quiet = ui.quiet
            ui.quiet = False
            ui.status(b"GitLab update error: '%s'. Because of this, some "
                      b"changes won't be visible in the web interface" % err)
            ui.quiet = quiet
            if not allow_error:
                raise error.Abort(err.strip())

        # useful messages such as motd, merge requests links etc.
        quiet = ui.quiet
        ui.quiet = False
        # out is already given as bytes, that was the point of much
        # of the py3 conversion for the Hook class
        ui.status(out)
        ui.quiet = quiet

    def heptapod_apply_changes(self, prune_reasons, changes):
        self.heptapod_notify_gitlab(PreReceive(self.repo),
                                    prune_reasons, changes)
        git_refs = self.git.refs

        # Right after repo creation, HEAD is typically initialized
        # as refs/heads/master, which doesn't exist,
        # and probably won't after our push. If we don't correct it
        # quickly, something on the GitLab side, even
        # before post-receive treatment actually begins will set it to
        # a random value - we don't want it to select topics if possible
        # and if it has, we want that to change.
        default_branch_ref = self.git.refs.get_symrefs().get(b'HEAD')
        update_default_branch = (default_branch_ref not in git_refs
                                 or ref_is_topic(default_branch_ref))
        new_named_branch_refs = []
        for change in pycompat.itervalues(changes):
            if change.after == ZERO_SHA:
                del git_refs[change.ref]
            else:
                git_refs[change.ref] = change.after
            if change.is_creation() and ref_is_named_branch(change.ref):
                new_named_branch_refs.append(change.ref)

        if update_default_branch and new_named_branch_refs:
            branch_default = git_branch_ref(b'branch/default')
            if branch_default in new_named_branch_refs:
                new_head = branch_default
            else:
                new_head = new_named_branch_refs[0]
            self.repo.ui.note(b"Setting Git HEAD to %s" % new_head)
            git_refs.set_symbolic_ref(b'HEAD', new_head)

        def post_receive(txn):
            self.heptapod_notify_gitlab(PostReceive(self.repo),
                                        prune_reasons, changes)

        txn = self.repo.currenttransaction()
        if txn is None:
            post_receive(None)
        else:
            txn.addpostclose(b'heptapod_git_sync', post_receive)

    def export_commits(self):
        try:
            self.export_git_objects()
            self.update_references()
        finally:
            self.save_map(self.map_file)

    def update_references(self):
        """Update or create refs in the target Git repo for Mercurial changes.

        This fires or schedules all appropriate notifications (GitLab hooks)
        """
        existing = self.git.refs.as_dict()
        changes = self.heptapod_compare_tags(existing)
        prune_reasons, compared = self.compare_exportable(
            existing, self.get_exportable())
        changes.update(compared)
        self.heptapod_apply_changes(prune_reasons, changes)

    def heptapod_compare_tags(self, existing):
        """This is derived from export_hg_tags() for two-phase application.

        Instead of immediate application to the Git repo, we emit
        a dict of `GitRefChange` instances, suitable for application between
        pre- and post-receive.
        """
        changes = {}
        for tag, sha in pycompat.iteritems(self.repo.tags()):
            if self.repo.tagtype(tag) in (b'global', b'git'):
                tag = tag.replace(b' ', b'_')
                target = self.map_git_get(hex(sha))
                if target is not None:
                    tag_refname = b'refs/tags/' + tag
                    if check_ref_format(tag_refname):
                        before_sha = existing.get(tag_refname, ZERO_SHA)
                        if before_sha != target:
                            changes[tag_refname] = GitRefChange(
                                tag_refname, before_sha, target)
                    else:
                        self.repo.ui.warn(
                            b"Skipping export of Mercurial tag '%s' because "
                            b"it has invalid name as a git refname.\n" % tag)
                else:
                    self.repo.ui.warn(
                        b"Skipping export of tag '%s' because it "
                        b"has no matching git revision.\n" % tag)
        return changes

    def multiple_heads_choose(self, hg_shas, branchmap_branch):
        """Choose among multiple heads to forward the given branch

        The branch is given in branchmap format, i.e., `branch:topic` or
        `branch`.

        Return None if nothing satisfying has been found.

        Currently, we arbitrarily take the one with the highest revision
        number (hence the most recently added to *this* repository).
        The advantage is that the given branch will never disappear
        (confusing to users, and leading to some blocking situations,
        such as heptapod#101).

        This is consistent with what Mercurial does for label-adressing,
        and shouldn't be a problem for Heptapod, since we force-push to
        Git all the time
        """
        if self.repo.ui.configbool(b'unit-tests',
                                   b'hg-git.multiple-heads-dont-choose'):
            return

        revs = self.repo.revs(b'max(%ls)', hg_shas)
        if len(revs) != 1:
            return None
        return revs.first()

    def git_branch_for_branchmap_branch(self, topbranch):
        """return Git branch name for hg branch names in branchmap()

        Does in particular the needed sanitizations to make it acceptable
        for a Git branch.

        :param topbranch: can be either a named branch name or follow the
                          branch:topic convention, as returned by branchmap()
        """
        topbranch = topbranch.replace(b' ', b'_')
        if b':' in topbranch:
            branch, topic = topbranch.split(b':', 1)
            if b'/' in topic:
                msg = b"Invalid character '/' in topic name %r. " % topic
                if self.ui.configbool(b'experimental',
                                      b'hg-git.accept-slash-in-topic-name'):
                    msg += (b"Replacing with '-'. Rename before publishing or "
                            b"you'll get serious problems.")
                    topic = topic.replace(b'/', b'-')
                    self.ui.status(msg)
                    self.ui.warn(msg)
                else:
                    self.ui.status(msg)
                    raise error.Abort(msg)

            return b'/'.join((b'topic', branch, topic))
        return b'branch/' + topbranch

    def latest_topic_descendant(self, topic, ctx):
        """Return the latest public descendent of ctx in a given topic.

        Although this is not meaningful in regular Mercurial usage,
        it's necessary because we need GitLab to understand what happened to
        a Merge Request on a published topic, and that's not possible if
        its branch vanished.

        This checks that there is one public head of the topic.
        Otherwise the push should be refused as inconsistent.

        The changeset of ctx is assumed *not* to be filtered (aka, obsolete)
        (all current callers already have obsolescence information around).
        If it does not belong to the topic, `None` gets returned.
        """
        revs = self.repo.revs("heads(extra(topic, %s) and descendants(%d))",
                              topic, ctx.rev())
        if len(revs) > 1:
            raise MultipleDescendants(topic, ctx)
        rev = revs.first()
        if rev is None:
            return None
        return self.repo[rev]
