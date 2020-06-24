import os
from typing import Union
from google.oauth2.service_account import Credentials

from siametrics.deepmap.dataset import DatasetDiscoveryService
from .util import default_key_path


class DeepmapClient:
    __default_project_id = 'siametrics-deepmap-dp'

    def __init__(self, key_path: Union[str, None] = None, project_id: Union[str, None] = None):
        self.__key_path = key_path or default_key_path
        self.project_id = project_id or DeepmapClient.__default_project_id

        if not os.path.exists(self.__key_path):
            self.__key_path = None

        self.__g_cred = None
        if self.__key_path:
            self.__g_cred = Credentials.from_service_account_file(self.__key_path)

        self.__discovery = DatasetDiscoveryService(self.__g_cred, self.project_id)

    def get_dataset(self, name: str):
        return self.__discovery.get_dataset(name)

    def list_datasets(self):
        return self.__discovery.list_datasets()
