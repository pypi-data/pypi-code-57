import boto3
import os
import requests
from time import strftime

def upload_file_to_s3(aws_bucket,aws_region,project_id , file_has_to_upload_with_path,
                      s3_file_name_has_to_upload):
    s3 = boto3.client('s3', region_name=aws_region)
    s3.upload_file(file_has_to_upload_with_path,
               aws_bucket, '{}/Output/{}'.format(str(project_id), s3_file_name_has_to_upload))
    print("File Successfully Uploaded to S3...", s3_file_name_has_to_upload)
    
def print_data_fetch_variables(var_list):
    print("Data Fetch Variables:\n")
    for var in var_list :
        print(var)

def upload_file_to_S3_with_hook(file_has_to_upload_with_path, s3_file_name_has_to_upload, aws_bucket,connection_name):
    hook = airflow.hooks.S3_hook.S3Hook(connection_name)
    hook.load_file(file_has_to_upload_with_path, s3_file_name_has_to_upload, aws_bucket,replace=True)
    print("File Successfully Uploaded to S3...", s3_file_name_has_to_upload)
    
def upload_file_to_s3_key(bucket_name, aws_access_key_id, aws_secret_access_key, file_has_to_upload_with_path,
                      s3_file_name_with_path):
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    s3 = session.resource('s3')
    s3.Bucket(bucket_name).upload_file(file_has_to_upload_with_path, s3_file_name_with_path)
    print("File Successfully Uploaded to S3...", s3_file_name_with_path)
    
    
def call_api(api_host,api_url):
    print ("calling the user side API at: "+strftime("%Y_%m_%d_%H_%M_%S"))
    r = requests.get(api_url, headers={'Host': api_host})
    print ("user side api response status code: "+str(r.status_code))
    if r.status_code == 200:
        print ("Recommendation process completed at "+strftime("%Y_%m_%d_%H_%M_%S"))
    else:
        raise Exception('Recommendation process failed because of API call failure.')
    return r.status_code

def test_pd():
    import pandas as pd
    print(pd.__version__)    
    df = pd.read_csv("/usr/local/airflow/data/26/input/fintech_Z_Ops_raw_data.csv")
    print((df).head(2).to_markdown())
    return 1