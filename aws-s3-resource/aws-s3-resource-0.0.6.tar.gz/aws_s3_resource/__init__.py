import boto3

class S3:
	resource = boto3.resource('s3',region_name=os.environ['region_name'])

