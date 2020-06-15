from subprocess import CalledProcessError

import attr

from .utils.cmd import get_cmd, run_cmd
from .servers import get_server_from_url
from .config import conf


@attr.s
class GitRepo:
    def get_branch(self, name):
        return GitBranch(name=name)

    def get_branches(self):
        return [
            GitBranch(name=line[2:]) for line in get_cmd("git", "branch").splitlines()
        ]

    def get_current_branch(self):
        branch = [
            GitBranch(name=line[2:])
            for line in get_cmd("git", "branch").splitlines()
            if line.startswith("* ")
        ]
        assert len(branch) == 1
        return branch[0]

    def get_remote(self, name):
        return GitRemote(name)

    def get_remotes(self):
        return [GitRemote(name) for name in get_cmd("git", "remote").splitlines()]

    def get_upstream_remote(self):
        for remote in self.get_remotes():
            if remote.is_upstream():
                return remote
        return self.get_remote(conf["upstream_remote"])

    def get_origin_url(self):
        master_branch = GitBranch("master")
        origin = master_branch.get_remote()
        return origin.get_url()


@attr.s(auto_attribs=True)
class GitBranch:

    name: str

    def get_remote(self):
        try:
            remote_name = get_cmd("git", "config", f"branch.{self.name}.pushRemote")
        except CalledProcessError:
            try:
                remote_name = get_cmd("git", "config", f"branch.{self.name}.remote")
            except CalledProcessError:
                return None
        return GitRemote(name=remote_name)

    def get_merge_ref(self):
        try:
            ref = get_cmd("git", "config", f"branch.{self.name}.merge")
        except CalledProcessError:
            return None
        prefix_len = len("refs/heads/")
        return ref[prefix_len:]

    def delete(self, force=False):
        run_cmd("git", "branch", "-D" if force else "-d", self.name)

    def set_upstream_to(self, remote, reference, quiet=True):
        cmd = [
            "git",
            "branch",
            "--set-upstream-to",
            f"{remote.name}/{reference}",
            self.name,
        ]
        if quiet:
            cmd.insert(2, "-q")
        run_cmd(*cmd)

    def checkout(self, quiet=False):
        cmd = ["git", "checkout", self.name]
        if quiet:
            cmd.insert(2, "-q")
        run_cmd(*cmd)

    @classmethod
    def create_from(cls, name, reference):
        run_cmd("git", "branch", name, reference)
        return cls(name)

    @classmethod
    def create_and_checkout_from(cls, name, reference, quiet=False):
        cmd = ["git", "checkout", "-b", name, reference]
        if quiet:
            cmd.insert(2, "-q")
        run_cmd(*cmd)
        return cls(name)


@attr.s(auto_attribs=True)
class GitRemote:

    name: str

    def get_url(self):
        return get_cmd("git", "remote", "get-url", self.name)

    def prune(self):
        run_cmd("git", "remote", "prune", self.name)

    def fetch(self, reference=None, quiet=False):
        cmd = ["git", "fetch", self.name]
        if quiet:
            cmd.insert(2, "-q")
        if reference:
            cmd.append(reference)
        run_cmd(*cmd)

    def get_server_repo(self):
        return get_server_from_url(self.get_url())

    def get_default_branch(self):
        try:
            ref = get_cmd(
                "git",
                "symbolic-ref",
                f"refs/remotes/{self.name}/HEAD",
                hide_stderr=True,
            )
        except CalledProcessError:
            branch_name = "master"
        else:
            prefix_len = len(f"refs/remotes/{self.name}/")
            branch_name = ref[prefix_len:]
        return GitBranch(branch_name)

    def set_upstream(self, value=True):
        run_cmd("git", "config", f"remote.{self.name}.upstream", str(value).lower())

    def is_upstream(self, value=True):
        try:
            return get_cmd("git", "config", f"remote.{self.name}.upstream") == "true"
        except CalledProcessError:
            return False

    @classmethod
    def create(cls, name, url):
        run_cmd("git", "remote", "add", name, url)
        return cls(name)
