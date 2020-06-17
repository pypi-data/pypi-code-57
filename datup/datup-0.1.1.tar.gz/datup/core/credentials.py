import boto3
import s3fs

''' 
The Credential class must be instantiaded for use the aws secret id and access key for 
working with AWS S3 Buckets. This class must be called through Datup class
'''
class Credentials:
    def __init__(
        self,
        aws_access_key_id,
        aws_secret_access_key,
        datalake,
        prefix_s3,
        local_path,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.datalake = datalake
        self.aws_credentials_s3fs = s3fs.core.S3FileSystem(anon=False, key=aws_access_key_id, secret=aws_secret_access_key)
        self.aws_credentials_s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.aws_client_s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.prefix_s3 = prefix_s3 
        self.local_path = local_path
