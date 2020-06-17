from typing import Union, Iterable

import backoff
from google.cloud.storage import Client as GoogleStorageClient, Blob

from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY


class Client(GoogleStorageClient):
    def __init__(self, project=None, credentials=None, _http=None):
        super().__init__(project=project, credentials=credentials, _http=_http)

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def list_blobs(self, bucket_name: str, prefix: Union[str, None] = None) -> Iterable[Blob]:
        bucket = self.get_bucket(bucket_name)
        return bucket.list_blobs(prefix=prefix)
