import threading

from .. import SingletonMetaClass, UserConfig

from . import connect_to_driver, recurse_find_file, Version


class ApkFile:

    def __init__(self, project, path):

        dic = path(0)
        name = path(1)

        self._name = name
        self._version = Version.get_version(name)

    def __str__(self):
        return "{}-{}".format(self._name, self._version)


class Project:
    def __init__(self, repo, cfg):
        self._id = cfg['id']
        self._channels = {}
        for ch in cfg['channels']:
            ch_list = [ApkFile(self, path) for path in repo.get_files("{}/{}".format(cfg['dir'], ch))]
            self._channels[ch] = ch_list

    def __str__(self):
        r = "Project [{}]:".format(self._id)

        for k, l in self._channels.items():
            r += "\n  Channel {}({}):".format(k, len(l))
            for item in l:
                r += "\n    {}".format(item)

        return r


class Repo(object):
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._conn, self._driver = connect_to_driver()
        self._root = None
        self._projects = []
        self._refresh()

    def _refresh(self):
        cfg = UserConfig()
        self._root = cfg.get('repo_root_file')
        self._projects = [Project(self, i['project']) for i in cfg.get('repo_cfg')]

    def get_files(self, path):
        return recurse_find_file(self._conn, self._driver, "{}/{}".format(self._root, path))

    @property
    def projects(self):
        return self._projects

    def download(self):
        with open("a.apk", 'wb') as f:
            self._conn.retrieveFile(self._driver, "Products Versions/QBlock/Google/apk/blockpuzzle-v1.6.2-release_2.apk", f)

    def ls(self):
        download_thread = threading.Thread(target=self.download())
        download_thread.start()
        download_thread.join()
