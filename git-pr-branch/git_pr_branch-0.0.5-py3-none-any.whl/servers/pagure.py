import attr

from git_pr_branch.config import conf
from .base import ServerRepo, PullRequest


class PagurePR(PullRequest):
    @classmethod
    def from_server(cls, repo, data):
        url = f"{repo.api_url}/pull-request/{data['id']}"
        html_url = f"{repo.html_url}/pull-request/{data['id']}"
        head_username = data["repo_from"]["user"]["name"]
        head_repo = PagureRepo(
            username=head_username,
            namespace=data["repo_from"]["namespace"],
            reponame=data["repo_from"]["name"],
        )
        return cls(
            number=data["id"],
            url=url,
            title=data["title"],
            state=data["status"],
            html_url=html_url,
            head_fullname=data["repo_from"]["fullname"],
            head_username=head_username,
            head_branch=data["branch_from"],
            head_commit=data["commit_stop"],
            head_git_url=head_repo.git_url,
            username=data["user"]["name"],
            repo=repo,
        )


@attr.s
class PagureRepo(ServerRepo):

    namespace = attr.ib(default=None)
    _clone_url_prefixes = (
        "ssh://git@pagure.io/",
        "git@pagure.io:",
        "https://pagure.io/",
    )
    _pr_class = PagurePR

    @classmethod
    def from_path(cls, path):
        parts = path.split("/")
        repo = parts[-1]
        if repo.endswith(".git"):
            repo = repo[: -len(".git")]
        if parts[0] == "forks":
            parts.pop(0)
            username = parts.pop(0)
        else:
            username = None
        if len(parts) == 2:
            namespace = parts[0]
        else:
            namespace = None
        return cls(username=username, reponame=repo, namespace=namespace)

    @property
    def fullname(self):
        parts = [self.reponame]
        if self.namespace is not None:
            parts.insert(0, self.namespace)
        if self.username is not None:
            parts[:0] = ["forks", self.username]
        return "/".join(parts)

    @property
    def api_url(self):
        return f"https://pagure.io/api/0/{self.fullname}"

    @property
    def html_url(self):
        return f"https://pagure.io/{self.fullname}"

    @property
    def git_url(self):
        return f"ssh://git@pagure.io/{self.fullname}.git"

    def call_api(self, url):
        if conf["pagure_token"]:
            headers = {"Authorization": f"token {conf['pagure_token']}"}
        else:
            headers = None
        return super().call_api(url, headers=headers)

    def _get_pull_ref(self, fork_repo, remote_ref):
        return (fork_repo.username, remote_ref)

    def _get_pulls(self, pull_ref):
        response = self.call_api(f"/pull-requests?status=All&author={pull_ref[0]}")
        return [pr for pr in response["requests"] if pr["branch_from"] == pull_ref[1]]

    def _get_pull(self, number):
        return self.call_api(f"/pull-request/{number}")
