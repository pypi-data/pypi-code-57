import logging
from typing import Any, Dict, List

from google.cloud import storage
from google.cloud.exceptions import NotFound

from forge_template.handler.handler import BaseHandler
from forge_template.paths import (
    JOB_BUCKET,
    JOB_FILES_PATH,
    PROJECT_BUCKET,
    PROJECT_FILES_PATH,
    SCHEDULE_BUCKET,
    SCHEDULE_FILES_PATH,
)
from forge_template.tool_info import ToolInfo
from forge_template.util import log_util


class FileTypeMetadata:
    def __init__(
        self,
        file_type_name: str,
        bucket: str,
        path: str,
        files_to_upload: List[str],
        existing_files: List[str],
        uploaded_files: List[str],
    ):
        self.file_type_name = file_type_name
        self.bucket = bucket
        self.path = path
        self.files_to_upload = files_to_upload
        self.existing_files = existing_files
        self.uploaded_files = uploaded_files


class CloudStorageHandler(BaseHandler):
    def __init__(self, config: Dict[str, Any], tool_info: ToolInfo):
        self.name = tool_info.name

        self.job_files_metadata = FileTypeMetadata(
            file_type_name="job",
            bucket=JOB_BUCKET,
            path=JOB_FILES_PATH,
            files_to_upload=[],
            existing_files=[],
            uploaded_files=[],
        )
        self.project_files_metadata = FileTypeMetadata(
            file_type_name="project",
            bucket=PROJECT_BUCKET,
            path=PROJECT_FILES_PATH,
            files_to_upload=[],
            existing_files=[],
            uploaded_files=[],
        )
        self.schedule_files_metadata = FileTypeMetadata(
            file_type_name="schedule",
            bucket=SCHEDULE_BUCKET,
            path=SCHEDULE_FILES_PATH,
            files_to_upload=[],
            existing_files=[],
            uploaded_files=[],
        )

        self.all_config_files_metadata = [
            self.job_files_metadata,
            self.project_files_metadata,
            self.schedule_files_metadata,
        ]

        self.storage_client = storage.Client()

        super().__init__(config=config, tool_info=tool_info)

    def create_preview(self) -> None:
        """
        1. Check if files (listed in paths_to_upload) already exist in GCP
        2. For each file: If it exist add its name to existing_paths
        """
        for file_type in self.all_config_files_metadata:
            self.check_files_to_upload(file_type)

    def print_preview(self) -> None:
        """
        1. Print the name of the files that will be uploaded (from paths_to_upload)
        2. If file also in existing_paths inform the user that the existing file will be overwritten
        """
        for file_type in self.all_config_files_metadata:
            self.check_files_for_preview(file_type)

    def setup(self) -> None:
        """
        Upload files from paths_to_upload. If the file is successfully uploaded add it to uploaded_paths
        """
        for file_type in self.all_config_files_metadata:
            self.upload_files_to_gcp(file_type)

    def rollback(self) -> None:
        """
        Iterate through the files in uploaded_paths and delete them from GCP
        """
        for file_type in self.all_config_files_metadata:
            logging.info(f"Rolling back all {file_type.file_type_name} config files that have benn added to GCP")
            self.delete_files_from_gcp(
                files_to_delete=file_type.uploaded_files, bucket_name=file_type.bucket, path=file_type.path
            )

    def delete_all_resources(self):
        """
        Iterate through the files in paths_to_upload and delete them if they exist
        """
        for file_type in self.all_config_files_metadata:
            self.delete_files_from_gcp(
                files_to_delete=file_type.files_to_upload, bucket_name=file_type.bucket, path=file_type.path
            )

    def list_files_in_gcp(self, bucket_name, path) -> List[str]:
        """
        List all files in a bucket under a given path

        Args:
            bucket_name:
            path: path under given bucket. Has to end with '/'
        """
        blobs = self.storage_client.list_blobs(bucket_name, prefix=path, delimiter="/")
        return [name for name in map(lambda f: f.name.replace(path, ""), blobs) if name]

    def check_files_to_upload(self, file_type: FileTypeMetadata):
        """
        Takes a file_type (job, project, schedule) and checks if the corresponding files to upload are already in GCP
        project
        """
        gcp_files = self.list_files_in_gcp(file_type.bucket, file_type.path)
        file_type.existing_files = [file for file in file_type.files_to_upload if file in gcp_files]

    @staticmethod
    def check_files_for_preview(file_type: FileTypeMetadata):
        """
        Takes a file_type (job, project, schedule) and prints the corresponding files via print_resource_to_add or (if
        it exists already via print_resource_already_exists
        """
        for file in file_type.files_to_upload:
            if file in file_type.existing_files:
                log_util.print_resource_already_exists(file, file_type.file_type_name, override=True)
            else:
                log_util.print_resource_to_add([file], file_type.file_type_name)

    def upload_files_to_gcp(self, file_type: FileTypeMetadata):
        """
        Takes a file type (job, project, schedule), uploads all corresponding files to the GCP project and adds the
        files to uploaded_files
        """
        for file in file_type.files_to_upload:
            bucket = self.storage_client.bucket(file_type.bucket)
            destination_path = file_type.path + file
            blob = bucket.blob(destination_path)
            blob.upload_from_filename(file)
            file_type.uploaded_files.append(file)
            log_util.print_message(
                f"Successfully uploaded a {file_type.file_type_name} config file to \n "
                + f"bucket: {file_type.bucket} \n "
                + f"path: {destination_path}"
            )

    def delete_files_from_gcp(self, files_to_delete, bucket_name, path):
        """
        Takes a list of files, and deletes them from GCP
        """
        bucket = self.storage_client.bucket(bucket_name)
        for file in files_to_delete:
            self.delete_file(bucket, path, file)

    @staticmethod
    def delete_file(bucket: storage.Bucket, path: str, file: str) -> None:
        try:
            bucket.blob(path + file).delete()
            logging.info(f"Successfully deleted {file} \n from bucket: {bucket.name} \n path {path}")
        except NotFound:
            logging.info(f"File {file} does not exist on \n bucket: {bucket.name} \n path {path}")
