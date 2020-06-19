from ehelply_logger.Logger import Logger

from pydantic import BaseModel
from pathlib import Path
import json

from typing import Dict

from git import Repo


class CommitAuthor(BaseModel):
    """
    Author of a commit
    """
    name: str
    email: str


class Stats(BaseModel):
    """
    File stats
    """
    insertions: int
    deletions: int
    lines: int


class TotalStats(Stats):
    """
    Overall stats
    """
    files: int


class CommitStats(BaseModel):
    """
    Stats of a commit
    """
    totals: TotalStats
    files: Dict[str, Stats]


class Commit(BaseModel):
    """
    Commit
    """
    sha: str
    message: str
    summary: str
    author: CommitAuthor
    created_at: str
    branch: str
    stats: CommitStats


class Release(BaseModel):
    """
    Release
    """
    version: str
    name: str
    commit: Commit


class ReleasesConfig(BaseModel):
    repo_path: Path
    releases_path: Path


class ReleaseDetails(BaseModel):
    name: str
    version: str


class Releaser:
    def __init__(self, config: ReleasesConfig, logger: Logger = None) -> None:
        self.config = config

        self.logger: Logger = logger
        if not self.logger:
            self.logger = Logger()

        self.releases: list = []

        self.setup()

    def setup(self):
        with open(str(self.config.releases_path)) as file:
            self.releases = json.load(file)

    def make(self, release_details: ReleaseDetails) -> bool:
        repo = Repo(str(self.config.repo_path))
        latest_commit = repo.head.commit

        stats: dict = {"totals": latest_commit.stats.total, "files": latest_commit.stats.files}

        commit_data: dict = {
            "message": latest_commit.message,
            "summary": latest_commit.summary,
            "sha": latest_commit.hexsha,
            "created_at": latest_commit.committed_datetime.isoformat(),
            "branch": latest_commit.name_rev.split(" ")[-1],
            "author": {"name": latest_commit.author.name, "email": latest_commit.author.email},
            "stats": stats
        }

        release_data: Release = Release(name=release_details.name, version=release_details.version,
                                        commit=Commit(**commit_data))

        self.releases.append(release_data.dict())

        with open(str(self.config.releases_path), 'w') as file:
            json.dump(self.releases, file)

        self.logger.info("Created new release.")
        self.logger.info(json.dumps(release_data.dict(), indent=2))

        return True
