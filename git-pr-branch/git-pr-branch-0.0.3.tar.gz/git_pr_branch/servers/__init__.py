from .github import GithubRepo

_SERVERS = [GithubRepo]


def get_server_from_url(url):
    for server_class in _SERVERS:
        if server_class.owns_url(url):
            return server_class.from_url(url)
    raise NotImplementedError(f"Can't handle server for URL {url}")
