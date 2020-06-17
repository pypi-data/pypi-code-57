import typing

from aws_cdk.aws_kms import Key, IKey
from aws_cdk.core import Construct, RemovalPolicy
from aws_cdk.aws_s3 import Bucket, BucketAccessControl, BlockPublicAccess, BucketEncryption


class GICBucket(Construct):
    def __init__(self, scope: Construct, id: str, bucket_name: str, *, encryption_key: typing.Optional[IKey] = None):
        super().__init__(scope, id)
        if not encryption_key:
            encryption_key = Key(self, f'{bucket_name}-s3-key',
                                 enable_key_rotation=True,
                                 description='Key for encryption at rest for S3',
                                 alias=f'{bucket_name}/s3')
        access_log_bucket = Bucket(self, f'{id}-access-logs',
                                   block_public_access=BlockPublicAccess.BLOCK_ALL,
                                   bucket_name=f'{bucket_name}-access-logs',
                                   versioned=False,
                                   removal_policy=RemovalPolicy.DESTROY)
        self.bucket = Bucket(self, bucket_name,
                             access_control=BucketAccessControl.PRIVATE,
                             block_public_access=BlockPublicAccess.BLOCK_ALL,
                             bucket_name=bucket_name,
                             encryption=BucketEncryption.KMS,
                             encryption_key=encryption_key,
                             versioned=True,
                             removal_policy=RemovalPolicy.DESTROY,
                             server_access_logs_bucket=access_log_bucket,
                             server_access_logs_prefix=bucket_name
                             )

    @property
    def bucket_name(self):
        return self.bucket.bucket_name
