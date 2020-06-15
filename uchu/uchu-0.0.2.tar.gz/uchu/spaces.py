
from pathlib import Path

import boto3
from botocore.errorfactory import ClientError

class Space:
    def __init__(self, region_name, access_key_id, secret_access_key):
        self.region_name = region_name
        self.endpoint_url = f"https://{self.region_name}.digitaloceanspaces.com"
        # Get a key from:
        # https://www.digitalocean.com/community/tutorials/how-to-create-a-digitalocean-space-and-api-key
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session = boto3.session.Session()
        self._client = self.session.client('s3', region_name=region_name,
                            endpoint_url=self.endpoint_url,
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key)

    def list_buckets(self):
        """Returns a list of bucket names."""
        return tuple(b['Name'] for b in self._client.list_buckets()['Buckets'])

    def upload_file(self, filename, bucket_name, object_name=None, metadata=None,
        extra_args=None, set_public=False):
        """Uploads file from local path at `filename` to
        `bucket_name`/`object_name` on S3.
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        """
        # Set the extra arguments.
        extra_args = extra_args if extra_args else {}
        if set_public:
            extra_args["ACL"] = "public-read"
        if metadata:
            extra_args["Metadata"] = metadata
        # Set the same path as filename if non specified.
        object_name = object_name if object_name else filename
        # Actual uploading.
        self._client.upload_file(filename, bucket_name, object_name, ExtraArgs=extra_args)
        # Check if file_exists in bucket.
        return self.file_exists(bucket_name, object_name)

    def file_exists(self, bucket_name, object_name):
        """Check if file exists in bucket."""
        try:
            self._client.head_object(Bucket=bucket_name, Key=object_name)
            return True
        except ClientError:
            return False

    def download_file(self, bucket_name, object_name, filename):
        """ Downloads the file from `bucket_name`/`object_name` from s3 to
        local path at `filename`.
        """
        self._client.download_file(bucket_name, object_name, filename)
        # Check if the file exists.
        return Path(filename).exists()

    def list_files(self, bucket_name):
        for content in dospace._client.list_objects(Bucket=bucket_name)['Contents']:
            yield content['Key']
