import os
import boto3
import json
from botocore.exceptions import ClientError

secret_client = boto3.client('secretsmanager')

def get_auth_key(SECRET_NAME):
    try:
        response = secret_client.get_secret_value(
            SecretId=SECRET_NAME,
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + SECRET_NAME + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    auth_key = json.loads(response["SecretString"])
    return auth_key["BSA_API_INTERNAL_AUTH"]
