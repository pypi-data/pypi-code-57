from ..workers.storage_manager import StorageManagerABC
from google.cloud import storage


class BucketStorage(StorageManagerABC):
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def write_to_file(self, uuid, result):
        blob = self.bucket.blob(uuid)
        blob.upload_from_string(result)
        return f"https://storage.cloud.google.com/{self.bucket_name}/{blob.name}"
