import os

from cnvrg.modules.storage.base_storage import BaseStorage
from cnvrg.modules.cnvrg_files import CnvrgFiles
from typing import Dict
from azure.storage.blob import BlockBlobService


class AzureStorage(BaseStorage):
    def __init__(self, element: CnvrgFiles, working_dir: str, storage_resp: Dict):
        super().__init__(element, working_dir, storage_resp.get("sts"))

        try:
            os.remove(self.sts_local_file)
        except Exception:
            pass

        del storage_resp["sts"]

        props = self.decrypt_dict(storage_resp, keys=["container", "storage_access_key", "storage_account_name", "container"])
        account_name = props["storage_account_name"]
        accout_key = props["storage_access_key"]
        container = props["container"]

        self.access_key = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(account_name, accout_key)
        self.accout_key = accout_key
        self.container_name = container
        self.account_name = account_name
        self.service = self._get_service()

    def upload_single_file(self, file, target):
        try:
            self.service.create_blob_from_path(self.container_name, target, file)
        except Exception as e:
            print(e)

    def download_single_file(self, file, target):
        pass

    def _get_service(self):
        return BlockBlobService(account_name=self.account_name, account_key=self.accout_key)
