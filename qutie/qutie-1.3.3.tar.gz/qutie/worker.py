"""A convenient worker thread class.

## Example Usage

```python
def calculate(worker):
    for i in range(100):
        # Emit custom events.
        worker.emit('progress', i, 100)
        worker.emit('message', "All ok...")

worker = ui.Worker(target=calculate)
# Assign custom event callbacks.
worker.progress = lambda step, max: print(f"progress: {step}/{max}")
worker.message = lambda msg: print(f"message: {msg}")
worker.start()
```

For more information on the underlying Qt5 object see [QObject](https://doc.qt.io/qt-5/qobject.html).
"""

import copy
import logging
import threading
import traceback

from .qt import QtCore
from .qt import bind

from .object import Object

__all__ = ['Worker', 'StopRequest']

class StopRequest(Exception):
    """Raise to stop worker execution."""

@bind(QtCore.QObject)
class Worker(Object):
    """Worker thread class using python `threading`."""

    def __init__(self, *, target=None, started=None, finished=None, failed=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.started = started
        self.finished = finished
        self.failed = failed
        self.__lock = threading.RLock()
        self.__thread = None
        self.__stop_requested = False
        self.__values = {}

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    @property
    def started(self):
        return self.__started

    @started.setter
    def started(self, value):
        self.__started = value

    @property
    def finished(self):
        return self.__finished

    @finished.setter
    def finished(self, value):
        self.__finished = value

    @property
    def failed(self):
        """Event triggered if exception is thrown from worker thread. Provides
        arguments exception _e_ and traceback _tb_.

        >>> worker.failed = lambda e, tb: ...
        """
        return self.__failed

    @failed.setter
    def failed(self, value):
        self.__failed = value

    def set(self, key, value):
        """Set thread safe copy of value."""
        self.__set(key, value)

    def __set(self, key, value):
        with self.__lock:
            self.__values[key] = copy.deepcopy(value)

    def get(self, key, default=None):
        """Return thread safe copy of value."""
        return self.__get(key, default)

    def __get(self, key, default=None):
        with self.__lock:
            return copy.deepcopy(self.__values.get(key, default))

    def keys(self):
        """Return keys of available thread safe values."""
        return self.__keys()

    def __keys(self):
        with self.__lock:
            return tuple(self.__values.keys())

    def start(self):
        """Start worker thread."""
        self.__start()

    def __start(self):
        with self.__lock:
            if not self.__thread:
                self.__thread = threading.Thread(target=self.__run)
            self.__stop_requested = False
            self.__thread.start()

    def stop(self):
        """Stop worker. This will only work when using properties `stopping`
        or `running` in `target`.
        """
        self.__stop()

    def __stop(self):
        self.__stop_requested = True

    def join(self):
        """Join thread, blocking until finished."""
        self.__join()

    def __join(self):
        try:
            self.__thread.join()
        except AttributeError:
            pass

    @property
    def stopping(self):
        """Return `True` when stopping."""
        return self.__stop_requested

    @property
    def running(self):
        """Return `True` while not stopping."""
        return not self.__stop_requested

    @property
    def alive(self):
        """Return `True` while worker thread is alive."""
        with self.__lock:
            if self.__thread:
                return self.__thread.is_alive()
        return False

    def __run(self):
        self.emit('started')
        try:
            if self.target is None:
                self.run()
            else:
                self.target(self)
        except StopRequest:
            pass
        except Exception as e:
            tb = traceback.format_exc()
            logging.error("%s %s: %s", self, type(e).__name__, e)
            self.emit('failed', e, tb)
        finally:
            with self.__lock:
                self.__stop_requested = False
                self.__thread = None
                self.emit('finished')

    def run(self):
        pass
