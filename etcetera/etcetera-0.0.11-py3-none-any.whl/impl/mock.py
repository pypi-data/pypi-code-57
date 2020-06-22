from ..repo import Repo
import re


def load(url):
    return MockRepo(url)


class MockRepo(Repo):

    def __init__(self, url=None):
        self._url = url or 'mock'
        self.repo = {}

    def ls(self):
        return self.repo.keys()

    def exists(self, name):
        return name in self.repo

    def upload(self, localfile, key):
        with open(localfile, 'rb') as f:
            self.repo[key] = f.read()

    def download(self, key, localfile):
        data = self.repo[key]
        with open(localfile, 'wb') as f:
            f.write(self.repo[key])

    def __repr__(self):
        return self._url
