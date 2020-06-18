from .Reader import Reader
from azure.storage.blob import BlockBlobService
from io import StringIO
import json
import pandas as pd


class ADLSPandasReader(Reader):
    """
        Read dataframe/json to specified blob storage location
    """
    def __init__(self, account_name, account_key):
        self.account_name = account_name
        self.account_key = account_key
        self.block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
    def read_df(self, locations, headers, dtypes):
        """
            Read csv files from the specified locations
        """
        dfs = pd.DataFrame()
        for blob_location in locations:
            location_list = blob_location.split('/',3)
            container_name = location_list[2].split('@')[0]
            csv_content = self.block_blob_service.get_blob_to_text(container_name, location_list[3] ).content
            df = pd.read_csv(StringIO(csv_content), names=headers,header=0 )
            dfs=dfs.append(df)
        return dfs