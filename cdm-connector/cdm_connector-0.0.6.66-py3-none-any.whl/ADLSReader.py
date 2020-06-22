from .Reader import Reader
from azure.storage.blob import BlockBlobService
from io import StringIO
import json
import pandas as pd


class ADLSReader(Reader):
    """
        Write dataframe/json to specified blob storage location
    """
    def __init__(self, account_name, account_key, container_name, storage_name, dataflow_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.storage_name = storage_name
        self.dataflow_name = dataflow_name
    
    def read_df(self, locations, headers, dtypes):
        """
            Read csv files from the specified locations
        """
        dfs = []
        for blob_location in locations:
            blob_location = self.dataflow_name + blob_location.split(self.container_name)[1]
            block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
            csv_content = block_blob_service.get_blob_to_text(self.container_name, blob_location).content
            df = pd.read_csv(StringIO(csv_content), names=headers)
            dfs.append(df)
        return pd.concat(dfs)