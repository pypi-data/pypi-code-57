from PyQt5.QtCore import QObject, pyqtSignal
from deriva.core import format_exception
from deriva.transfer import DerivaUpload
from deriva.qt import async_execute, Task


class UploadTask(QObject):
    status_update_signal = pyqtSignal(bool, str, str, object)
    progress_update_signal = pyqtSignal(int, int)

    def __init__(self, uploader, parent=None):
        super(UploadTask, self).__init__(parent)
        assert (uploader is not None and isinstance(uploader, DerivaUpload))
        self.uploader = uploader
        self.task = None

    def start(self):
        async_execute(self.task)

    def cancel(self):
        self.task.cancel()

    def set_status(self, success, status, detail, result):
        self.status_update_signal.emit(success, status, detail, result)

    def result_callback(self, success, result):
        self.set_status(success, str(status), "", result)

    def progress_callback(self, current, maximum):
        if self.task.canceled:
            return False

        self.progress_update_signal.emit(current, maximum)
        return True


class SessionQueryTask(UploadTask):
    def __init__(self, parent=None):
        super(SessionQueryTask, self).__init__(parent)

    def result_callback(self, success, result):
        self.set_status(success,
                        "Session query success" if success else "Session query failure",
                        "" if success else format_exception(result),
                        result.json() if success else None)

    def query(self):
        self.task = Task(self.uploader.catalog.get_authn_session, [], self.result_callback)
        self.start()


class ConfigUpdateTask(UploadTask):
    def __init__(self, parent=None):
        super(ConfigUpdateTask, self).__init__(parent)

    def result_callback(self, success, result):
        self.set_status(success,
                        "Configuration update success" if success else "Configuration update failure",
                        "" if success else format_exception(result),
                        result if success else None)

    def update_config(self):
        self.task = Task(self.uploader.getUpdatedConfig, [], self.result_callback)
        self.start()


class ScanDirectoryTask(UploadTask):
    def __init__(self, parent=None):
        super(ScanDirectoryTask, self).__init__(parent)

    def result_callback(self, success, result):
        self.set_status(success,
                        "Directory scan success" if success else "Directory scan failure.",
                        "" if success else format_exception(result),
                        None)

    def scan(self, path):
        self.task = Task(self.uploader.scanDirectory, [path], self.result_callback)
        self.start()


class UploadFilesTask(UploadTask):
    def __init__(self, parent=None):
        super(UploadFilesTask, self).__init__(parent)

    def result_callback(self, success, result):
        self.set_status(success,
                        "File upload success" if success else "File upload failure",
                        "" if success else format_exception(result),
                        None)

    def upload(self, status_callback=None, file_callback=None):
        self.task = Task(self.uploader.uploadFiles, [status_callback, file_callback], self.result_callback)
        self.start()
