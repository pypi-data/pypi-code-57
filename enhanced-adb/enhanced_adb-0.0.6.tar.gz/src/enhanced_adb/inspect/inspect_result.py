import os


class InspectResult:

    def __init__(self, path):
        self._path = path
        self._package = ''
        self._label = ''
        self._version = ''
        self._version_code = ''
        self._permissions = []
        self._compile_config = {}
        self._properties = {}
        self._manifest = None

        import hashlib
        block_size = 65536
        hasher = hashlib.sha1()
        with open(path, 'rb') as file:
            buf = file.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(block_size)
        self._file_hash = hasher.hexdigest()

    @property
    def packpage(self):
        return self._package

    @packpage.setter
    def package(self, value):
        self._package = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def version_code(self):
        return self._version_code

    @version_code.setter
    def version_code(self, value):
        self._version_code = value

    def add_permission(self, permission):
        self._permissions.append(permission)

    def set_compile_setting(self, compile, sdk, target):
        self._compile_config = {'compileSdkVersion': compile, 'sdkVersion': sdk, 'targetSdkVersion': target}

    @property
    def compile_config(self):
        return self._compile_config

    @property
    def path(self):
        return self._path

    @property
    def permissions(self):
        return self._permissions

    @property
    def file_hash(self):
        return self._file_hash

    def add_properties(self, filename, text):
        self._properties[filename] = text

    @property
    def properties(self):
        return self._properties

    @property
    def manifest(self):
        return self.manifest

    @manifest.getter
    def manifest(self):
        return self._manifest

    @manifest.setter
    def manifest(self, value):
        self._manifest = value
