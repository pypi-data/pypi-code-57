from ..workers.storage_manager import StorageManagerABC
from google.cloud import storage


class BucketStorage(StorageManagerABC):
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def write_to_file(self, uuid, result, content_type="text/plain"):
        blob = self.bucket.blob(uuid)
        blob.upload_from_string(result, content_type=content_type)
        return f"https://storage.cloud.google.com/{self.bucket_name}/{blob.name}"

    def read_from_file(self, uuid):
        blob = self.bucket.blob(uuid)
        return blob.download_as_string()
