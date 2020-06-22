from . import S3
from .s3_object import S3Object
from botocore.client import ClientError
import uuid
import os
import boto3

class S3Bucket(S3):
    
    @staticmethod
    def create_name(bucket_prefix, num_random_chars=6):
        
        if num_random_chars < NumberRandomCharsException.min_num_chars or \
           num_random_chars > NumberRandomCharsException.max_num_chars:
            
            raise NumberRandomCharsException
        
        bucket_name = ''.join([bucket_prefix, '-', str(uuid.uuid4()).replace('-', '')[:num_random_chars]])
        
        if len(bucket_name) < NumberCharsBucketNameException.min_num_chars or \
           len(bucket_name) > NumberCharsBucketNameException.max_num_chars:
            
            raise NumberCharsBucketNameException(bucket_name, len(bucket_name))
        
        return bucket_name
    
    @classmethod
    def create(cls, bucket_name):
        
        # Take the region from the config file
        session = boto3.session.Session()
        region = session.region_name

        # Create the bucket
        cls.resource.create_bucket(Bucket=bucket_name,
                          CreateBucketConfiguration={'LocationConstraint': region})
    
    @classmethod
    def create_with_random_name_suffix(cls, bucket_name, num_random_chars=6):
        while True:
            try:
                response = cls.create(bucket_name)
            except ClientError as e:
                if e.response['Error']['Code'] == 'BucketAlreadyExists':
                    bucket_name = cls.create_name(bucket_name)
                else:
                    raise e
            else:
                return bucket_name
    
    @classmethod
    def delete(cls, bucket_name):
        return cls.resource.Bucket(bucket_name).delete()
    
    @classmethod
    def list_all(cls, as_generator):
        buckets = cls.resource.buckets.all()
        
        if as_generator:
            return buckets
        
        return list(buckets)
    
    @classmethod
    def list_all_names(cls, as_generator):
        buckets = cls.list_all(as_generator=True)
        buckets_names = (bucket.name for bucket in buckets)
        
        if as_generator:
            return buckets_names 
        
        return list(buckets_names)
    
    @classmethod
    def is_available(cls, bucket_name):
        bucket = cls.resource.Bucket(bucket_name)
        return bucket in cls.resource.buckets.all()
    
    @classmethod
    def num_buckets(cls):
        return cls.list_all(False)

    @classmethod
    def download(cls, bucket_name, folder_name):
        # Create the root folder
        os.makedirs(folder_name)
        bucket = cls.resource.Bucket(bucket_name)

        # A set contains all created folders
        created_folders = set()

        for my_bucket_object in bucket.objects.all():

            # Folder or file path
            path = os.path.join(folder_name, my_bucket_object.key)

            # If the object name end with special character "/", it will definitely be a folder 
            if my_bucket_object.key.endswith('/'):

                # Continue if folder already created
                if my_bucket_object.key in created_folders:
                    continue

                # Create the folder tree and add it to the created set
                os.makedirs(path)
                created_folders.add(my_bucket_object.key)

            # Download the object if it is a file
            else:
                file_dict = {
                'file_path': path
                }

                S3Object.download(bucket_name, my_bucket_object.key, file_dict)

