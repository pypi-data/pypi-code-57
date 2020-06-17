from dataclasses import dataclass
from typing import List


@dataclass
class Repository:
    name: str
    url: str

    def __str__(self):
        return f"{self.name} --> {self.url}"


Repositories = List[Repository]


def get_repos_from_response(response: dict) -> Repositories:
    raw_repos = response.get("items", []) or []

    repos = []
    for raw_repo in raw_repos:
        repos.append(
            Repository(
                name=raw_repo["name"],
                url=raw_repo["html_url"]
            )
        )

    return repos
