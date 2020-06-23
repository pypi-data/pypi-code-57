import sys
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal


def async_execute(task):
    QThreadPool.globalInstance().start(task)


class TaskSignal(QObject):
    callback = pyqtSignal(bool, object)

    def __init__(self, callback, parent=None):
        super(TaskSignal, self).__init__(parent)
        self.callback.connect(callback)


class Task(QRunnable):

    INSTANCES = []

    def __init__(self, method, args, callback):
        super(Task, self).__init__()

        self.method = method
        self.args = args
        self.canceled = False
        self.signal = None
        self.callback = callback
        self.setAutoDelete(True)

        Task.INSTANCES.append(self)

    def cancel(self):
        self.canceled = True

    def signal_success(self, result):
        self.signal.callback.emit(True, result)

    def signal_failure(self, result):
        self.signal.callback.emit(False, result)

    def signal_canceled(self):
        self.signal.callback.emit(False, "Task canceled.")

    def run(self):
        try:
            self.signal = TaskSignal(self.callback)
            if self.canceled:
                self.signal_canceled()
                return
            result = self.method(*self.args)
            if self.canceled:
                self.signal_canceled()
                return
            self.signal_success(result)
        except:
            (etype, value, traceback) = sys.exc_info()
            if self.canceled:
                self.signal_canceled()
                return
            self.signal_failure(str(value))
        finally:
            self.cleanup()

    def cleanup(self):
        if self.signal is not None:
            self.signal.deleteLater()
        try:
            Task.INSTANCES.remove(self)
        except ValueError:
            return

    @staticmethod
    def shutdown_all():
        for task in Task.INSTANCES:
            task.cancel()
        Task.INSTANCES = []
