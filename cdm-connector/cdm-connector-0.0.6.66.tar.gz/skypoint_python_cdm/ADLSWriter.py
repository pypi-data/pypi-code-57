from .Writer import Writer
from azure.storage.blob import BlockBlobService
import uuid
import datetime
import json
import pandas as pd
import numpy as np


class ADLSWriter(Writer):
    """
        Write dataframe/json to specified blob storage location
    """
    def __init__(self, account_name, account_key, container_name, storage_name, dataflow_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.storage_name = storage_name
        self.dataflow_name = dataflow_name

    def get_existing(self, location, snapshot_dir_name):
        """
            Create a snapshot of the file current file in the passed directory name
            and return flag along with current data
            location: dir1/dir2/dir3/filename.extension or "model.json"
            snashot_dir_name: Snapshot directory name
        """
        if location.strip() == "model.json":
            location = self.dataflow_name + "/" + location
        #print("Location:", location)
        block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
        exists = block_blob_service.exists(self.container_name, location)
        #print("Existing flag:", exists)
        if not exists:
            return (False, [''])

        proposed_lease_id_1 = str(uuid.uuid4())
        #print("Lease id:", proposed_lease_id_1)
        block_blob_service.acquire_blob_lease(self.container_name, location, lease_duration=60, proposed_lease_id=proposed_lease_id_1)
        t = datetime.datetime.now().strftime('%Y-%M-%dT%H:%M:%S.%fZ')
        file_path, filename = '/'.join(location.split('/')[:-1]), location.split('/')[-1]
        
        # copy file into snapshot folder
        old_blob_url = block_blob_service.make_blob_url(self.container_name, location)
        block_blob_service.copy_blob(self.container_name, file_path + '/' + snapshot_dir_name + '/' + filename + '@snapshot' + t, old_blob_url)
        content = json.loads(block_blob_service.get_blob_to_text(self.container_name, location, lease_id=proposed_lease_id_1).content)
        return (True, [content, proposed_lease_id_1])
    
    def write_df(self, blob_location, dataframe, number_of_partition=5):
        """
            Write dataframe to specified blob storage location
        """
        block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
        dfs = np.array_split(dataframe, number_of_partition)
        result = list()

        entity_name = blob_location.split('/')[0]
        blob_location = blob_location + "/" + entity_name
        for i in range(len(dfs)):
            dataframe = dfs[i].to_csv(index=False, header=False)
            filename = blob_location + str(i) + ".csv"
            block_blob_service.create_blob_from_text(self.container_name + "/" + self.dataflow_name, 
                                                     filename, dataframe)
            blob_url = 'https://' + self.storage_name + '.dfs.core.windows.net/' + self.container_name + '/' + self.dataflow_name + '/' + filename
            result.append((filename, blob_url))
        return result

    def write_json(self, blob_location, json_dict, lease_id=None):
        """
        write json to specified blob storage location
        """
        #print("Writing Model.json with leaseid:", lease_id)
        json_dict = json.dumps(json_dict)
        block_blob_service = BlockBlobService(
            account_name=self.account_name, account_key=self.account_key)
        block_blob_service.create_blob_from_text(self.container_name, self.dataflow_name+"/"+ blob_location, json_dict, lease_id=lease_id)
        if lease_id:
            block_blob_service.release_blob_lease(self.container_name, self.dataflow_name+"/"+ blob_location, lease_id)
        blob_url = 'https://' + self.storage_name + '.dfs.core.windows.net/' + self.container_name + '/' + self.dataflow_name + '/' + blob_location
        return blob_url
