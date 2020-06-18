from .github import GithubRepo
from .pagure import PagureRepo

_SERVERS = [GithubRepo, PagureRepo]


def get_server_from_url(url):
    for server_class in _SERVERS:
        if server_class.owns_url(url):
            return server_class.from_url(url)
    raise NotImplementedError(f"Can't handle server for URL {url}")
