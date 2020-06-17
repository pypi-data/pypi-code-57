import requests
from colorama import Fore

from repofinder import __LOGO__
from repofinder.config import Config
from repofinder.query import QueryBuilder
from repofinder.repository import get_repos_from_response, Repositories


def run(params_file: str):
    display_logo()
    config = Config(params_file)
    print(config)
    params = {
        "language": config.language,
        "created": config.created,
        "pushed": config.pushed,
        "stars": config.stars,
        "forks": config.forks
    }
    query = QueryBuilder(**params).build()
    response = get_response(query)
    repos = get_repos_from_response(response)
    display(repos)


def display_logo():
    print(f"{Fore.CYAN}{__LOGO__}")


def get_response(query: str) -> dict:
    try:
        return requests.get(query).json()
    except Exception as e:
        print(e)
        return {}


def display(repo_list: Repositories) -> None:
    print(f"{Fore.CYAN }Collected repos: {len(repo_list)}")
    for i, repo in enumerate(repo_list):
        print(f"{i + 1}) {repo}")
