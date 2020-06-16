import logging, time, uuid, string, math, os
from azure.storage.file import FileService
from datetime import datetime

def human_readable_size(size, decimal_places=2):
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"

class Client(): # pylint: disable=too-few-public-methods
    """simple client to access and execute basic operations on the Board Shared Storage"""

    def __init__(self, sas_uri):
        # split sas uri to get token and account
        self.azure_token = sas_uri[sas_uri.find("bss?")+4:]
        self.azure_account = sas_uri[8:sas_uri.find(".file")]
        self.azure_share = "bss"
        self.azfs = FileService(                     # create file service to access board extractions
            account_name=self.azure_account,
            sas_token=self.azure_token,
            socket_timeout=10
        )

    def list_directories_and_files(self,azure_dir=None):
        """List all files and directories in a Board Shared Storage path
        if no path specified, runs at root level"""
        return self.azfs.list_directories_and_files(self.azure_share,azure_dir)

    def delete_file(self,azure_file,azure_dir=None):
        """Delete a file from the Board Shared Storage"""
        self.azfs.delete_file(self.azure_share,azure_dir,azure_file)

    def download_file(self,azure_file,local_path,azure_dir=None,):
        """Download a file from the Board Shared Storage
        If content is set to true, return the full content and not just reference to the file"""
        self.azfs.get_file_to_path(self.azure_share,azure_dir,azure_file,local_path)

    def upload_file(self,azure_file,local_path,azure_dir=None):
        self.azfs.create_file_from_path(self.azure_share,azure_dir,azure_file,local_path)

    def get_file_size(self,azure_file,azure_dir,readable = True):
        """return size in bytes of a file on the Board Shared Storage
        if readable set to True, return in a human readable format (e.g. 10GiB)"""
        fileinfo = self.azfs.get_file_properties(self.azure_share,azure_dir,azure_file)
        if readable:
            return human_readable_size(fileinfo.properties.content_length)
        else:
            return fileinfo.properties.content_length
