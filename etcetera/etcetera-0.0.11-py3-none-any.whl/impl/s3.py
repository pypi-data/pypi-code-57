from ..repo import Repo
import re
try:
    import boto3
    import botocore
except ImportError:
    raise ImportError('boto3 not installed. Please re-install etcetera with s3 option: "pip install \'etcetera[s3]\'"')

def load(url, aws_access_key_id=None, aws_access_key_secret=None, endpoint_url=None, public=False):
    return S3Repo(url, aws_access_key_id, aws_access_key_secret, endpoint_url, public)


class S3Repo(Repo):

    def __init__(self, url, aws_access_key_id, aws_secret_access_key, endpoint_url, public):
        self._resource = boto3.resource(
            's3', endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
        )

        mtc = re.match(r's3://([^/]+)$', url)
        if mtc is None:
            raise ValueError('Failed to parse URL ' + url)
        self._bucket = mtc.group(1)
        self._url = url
        self._public = public

    def ls(self):
        bucket = self._resource.Bucket(self._bucket)
        for obj in bucket.objects.all():
            if obj.key.endswith('.tgz'):
                yield obj.key

    def exists(self, name):
        try:
            self._resource.Object(self._bucket, name).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            raise
        else:
            return True

    def upload(self, localfile, key):
        obj = self._resource.Object(self._bucket, key)
        obj.upload_file(Filename=localfile)
        if self._public:
            obj.Acl().put(ACL='public-read')

    def download(self, key, localfile):
        obj = self._resource.Object(self._bucket, key)
        obj.download_file(localfile)

    def __repr__(self):
        return self._url
