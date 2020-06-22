#  © Copyright IBM Corporation 2020.

from github import Github


class GitClient:

    def __init__(self, host, auth):
        self.client = Github(
            base_url="https://{hostname}/api/v3".format(hostname=host),
            login_or_token=auth)

    def get_repos(self, repo_id=None, repo_name=None):
        if repo_name is not None:
            self.client.get_repo(repo_name)
        else:
            self.client.get_repo(repo_id)

    def get_smth(self):
        self.client.get_rate_limit()
