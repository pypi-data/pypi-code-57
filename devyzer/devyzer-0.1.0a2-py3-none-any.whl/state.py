import os
import pathlib
import uuid
from uuid import uuid4

from devyzer.constants import DEFAULT_CONFIG_NAME
from devyzer.utils.cli import load_json_from_file


class SessionState(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    session_id = uuid4().hex
    mac_ip = hex(uuid.getnode())

    active_project = None

    # the status of the session if it is paused or running
    status = None

    @property
    def current_folder(self):
        return str(pathlib.Path(os.getcwd()).relative_to(pathlib.Path.home()))

    @property
    def current_configurations(self):

        project_config_path = os.getcwd() + "/" + DEFAULT_CONFIG_NAME

        if not os.path.isfile(project_config_path):
            return None
        try:
            configuration = load_json_from_file(project_config_path)
        except:
            configuration = None
        return configuration
