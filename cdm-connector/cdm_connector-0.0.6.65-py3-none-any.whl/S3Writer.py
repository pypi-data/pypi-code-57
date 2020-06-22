from azure.storage.blob import BlockBlobService
import uuid
import datetime
import json
import pandas as pd
import numpy as np
import boto3
import botocore
from .Writer import Writer


class S3Writer(Writer):
    """
        Write dataframe/json to specified blob storage location
    """
    def __init__(self, access_key, secret_access_key, region_name,encryption, bucket_name, dataflow_name):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.encryption= encryption
        self.dataflow_name = dataflow_name

    def get_existing(self, location, snapshot_dir_name):
        """
                 a snapshot of the file current file in the passed directory name
            and return flag along with current data
            location: dir1/dir2/dir3/filename.extension or "model.json"
            snashot_dir_name: Snapshot directory name            
        """
        copy_source={}

        if location.strip() == "model.json":
            location = self.dataflow_name + "/" + location
        # print("Location:", location)
        s3=boto3.resource('s3',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_access_key,region_name=self.region_name)
        

        try:
            s3.Object(self.bucket_name, location).load()
            # print('inside try')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # print('error 404')
                return (False, [''])
            else:
                raise
            
        #print("Existing flag:", exists)
        proposed_lease_id_1 = str(uuid.uuid4())

        copy_source['Bucket']=self.bucket_name
        copy_source['Key']=location
        # print('copy_source',copy_source)

        #print("Lease id:", proposed_lease_id_  1)
        t = datetime.datetime.now().strftime('%Y-%M-%dT%H:%M:%S.%fZ')
        file_path, filename = '/'.join(location.split('/')[:-1]), location.split('/')[-1]
        
        x=self.bucket_name, file_path + '/' + snapshot_dir_name + '/' + filename + '@snapshot' + t
        # print('x',x)
        # copy file into snapshot folder. Encrypted bucket will be copied with the encryption specified
        if self.encryption == '':
            s3.meta.client.copy(copy_source, self.bucket_name, file_path + '/' + snapshot_dir_name + '/' + filename + '@snapshot' + t)
            # print('inside encrpytion if')
        else:
            encrytion_value={"SSE-S3":"AES256","SSE-KMS": "aws:kms","SSE-C": "aws:c" , "AES256": "AES256"}
            s3.meta.client.copy(copy_source, self.bucket_name, file_path + '/' + snapshot_dir_name + '/' + filename + '@snapshot' + t,ExtraArgs={'ServerSideEncryption':encrytion_value[self.encryption]})

        obj = s3.Object(self.bucket_name, location)
        content = json.loads(obj.get()['Body'].read())

        return (True, [content, proposed_lease_id_1])
    
    def write_df(self, s3_location, dataframe, number_of_partition=5):
        """
            Write dataframe to specified blob storage location
        """
        s3 = boto3.client('s3',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_access_key,region_name=self.region_name)
        dfs = np.array_split(dataframe, number_of_partition)
        result = list()

        entity_name = s3_location.split('/')[0]
        s3_location = s3_location + "/" + entity_name
        for i in range(len(dfs)):
            dataframe = dfs[i].to_csv(index=False, header=False)
            filename = s3_location + str(i) + ".csv"
            if self.encryption=="":
                s3.put_object(Bucket=self.bucket_name,Key=self.dataflow_name + '/' + filename, Body=dataframe)
            else:
                encrytion_value={"SSE-S3":"AES256","SSE-KMS": "aws:kms","SSE-C": "aws:c" , "AES256": "AES256"}
                KEY = os.urandom(32)
                s3.put_object(Bucket=self.bucket_name,Key=self.dataflow_name + '/' + filename, Body=dataframe,SSECustomerKey=Key,SSECustomerAlgorithm=encrytion_value[str(self.encryption)])
            
            s3_url='https://' + self.bucket_name + '.s3.' + self.region_name + '.amazonaws.com/' + self.dataflow_name + '/' + filename
            result.append((filename, s3_url))
        return result

    def write_json(self, s3_location, json_dict, lease_id=None):
        """
        write json to specified blob storage location
        """
        #print("Writing Model.json with leaseid:", lease_id)
        json_dict = json.dumps(json_dict)
        s3 = boto3.client('s3',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_access_key,region_name=self.region_name)

        if self.encryption=="":
            s3.put_object(Bucket=self.bucket_name,Key=self.dataflow_name + '/' + s3_location, Body=json_dict)
        else:
            encrytion_value={"SSE-S3":"AES256","SSE-KMS": "aws:kms","SSE-C": "aws:c" , "AES256": "AES256"}
            KEY = os.urandom(32)
            s3.put_object(Bucket=self.bucket_name,Key=self.dataflow_name + '/' + s3_location, Body=json_dict,SSECustomerKey=Key,SSECustomerAlgorithm=encrytion_value[str(self.encryption)])

        s3_url='https://' + self.bucket_name + '.s3.' + self.region_name + '.amazonaws.com/' + self.dataflow_name + '/' + s3_location
        return s3_url