from pathlib import Path
from tempfile import TemporaryDirectory
import os

from .file import File
from .queue import Queue


class FilesystemRoot:

    @classmethod
    def default_directory(self):
        env_var = os.environ.get('BUSY_ROOT')
        return Path(env_var if env_var else Path.home() / '.busy')

    def __init__(self, path=None):
        if path:
            self._path = Path(path) if isinstance(path, str) else path
            assert isinstance(self._path, Path) and self._path.is_dir()
        else:
            self._path = self.default_directory()
            if not self._path.is_dir():
                self._path.mkdir()
        self._files = {}
        self._queues = {}

    def get_queue(self, key=None):
        key = key or Queue.default_key
        if key not in self._queues:
            queueclass = Queue.subclass(key)
            queuefile = File(self._path / f'{key}.txt')
            self._files[key] = queuefile
            self._queues[key] = queueclass(self)
            self._queues[key].add(*queuefile.read(queueclass.itemclass))
        return self._queues[key]

    def save(self):
        while self._queues:
            key, queue = self._queues.popitem()
            if queue.changed:
                items = queue.all()
                self._files[key].save(*items)
