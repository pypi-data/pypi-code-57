from urllib.parse import urlparse

import attr
import click
import requests

from git_pr_branch.config import conf, ConfigurationException


@attr.s(auto_attribs=True)
class APIError(Exception):
    message: str


@attr.s(auto_attribs=True)
class PullRequest:
    number: int
    url: str
    title: str
    state: str
    html_url: str
    head_fullname: str
    head_username: str
    head_branch: str
    head_commit: str
    head_git_url: str
    username: str
    repo: object = attr.ib()

    @classmethod
    def from_server(cls, repo, data):
        raise NotImplementedError()

    def get_reviews(self):
        return []


@attr.s
class ServerRepo:

    username = attr.ib(factory=str)
    reponame = attr.ib(factory=str)
    _cache_pulls = attr.ib(init=False, factory=dict)
    _clone_url_prefixes = None
    _config_requires = None
    _pr_class = PullRequest

    def __attrs_post_init__(self):
        for required in self._config_requires or []:
            if not conf.get(required):
                raise ConfigurationException(
                    f"You must set {required} in the configuration"
                )

    @classmethod
    def owns_url(cls, url):
        for prefix in cls._clone_url_prefixes or []:
            if url.startswith(prefix):
                return True
        return False

    @classmethod
    def from_url(cls, url):
        if url.startswith("https://"):
            path = urlparse(url).path[1:]
        else:
            path = url.split(":", 1)[1]
        return cls.from_path(path)

    @classmethod
    def from_path(cls, path):
        raise NotImplementedError()

    @property
    def fullname(self):
        raise NotImplementedError()

    @property
    def api_url(self):
        raise NotImplementedError()

    @property
    def html_url(self):
        raise NotImplementedError()

    @property
    def git_url(self):
        raise NotImplementedError()

    def call_api(self, url, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        url = f"{self.api_url}/{url}"

        if conf["verbose"]:
            click.secho(f"GET {url}", fg="bright_blue")

        response = requests.get(url, **kwargs)
        if not response.ok:
            raise APIError(response.text)
        return response.json()

    def get_pulls(self, branch):
        remote = branch.get_remote()
        remote_ref = branch.get_merge_ref()
        if remote is None or remote_ref is None:
            return []
        fork_repo = remote.get_server_repo()
        pull_ref = self._get_pull_ref(fork_repo, remote_ref)
        if pull_ref not in self._cache_pulls:
            pulls = self._get_pulls(pull_ref)
            self._cache_pulls[pull_ref] = [
                self._pr_class.from_server(self, pr) for pr in pulls
            ]
        return self._cache_pulls[pull_ref]
        # return [
        #     pr for pr in self._cache_pulls[pull_ref] if pr.head_branch == remote_ref
        # ]

    def _get_pull_ref(self, fork_repo, remote_ref):
        raise NotImplementedError()

    def _get_pulls(self, pull_ref):
        raise NotImplementedError()

    def get_pull(self, number):
        pr = self._get_pull(number)
        return self._pr_class.from_server(self, pr)

    def _get_pull(self, number):
        raise NotImplementedError()
