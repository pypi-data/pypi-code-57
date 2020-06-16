import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal
from NetworkStatisticsService.informal_statistics_uploader import InformalStatisticUploaderInterface
from NetworkStatisticsService.exceptions import DynamoDbException


class DynamoDBStatisticsUploader(InformalStatisticUploaderInterface):
	""" 
	A class used to upload to DynamoDB Tables.

	...

	Attributes
	----------
	aws_profile : str
		The AWS profile from the credential files to use (default 'default')
	aws_region : str
		The AWS region where the DynamoDB tables reside
	stats_table : str
		The name of the table where your statistics should be uplaoded
	logs_table : str
		The name of the table where error logs should be uplaoded

	Methods
	-------
	upload_statistics(stats_dict)
		Uploads statistics to DynamoDB
	upload_logs(logs_dict)
		Upload error logs to DynamoDB
	"""
	def __init__(self, aws_config):
		"""
		Parameters
		----------
		aws_config : DynamoDBConfig
			DynamoDB Config object
		"""

		super().__init__()
		self.__aws_region = aws_config.aws_region
		self.__aws_profile = aws_config.aws_profile
		self.__stats_table = aws_config.stats_table
		self.__logs_table = aws_config.logs_table
	
	def upload_statistics(self, stats_dict: dict):
		"""Uploads statistics to DynamoDB.

		If the upload fails, this method invokes upload_logs.

		Parameters
		----------
		stats_dict : dict
			Dictionary containing the statistics; must have the 'Timestamp' key
		"""

		session = boto3.Session(profile_name=self.__aws_profile)
		dynamodb_client = session.resource('dynamodb', region_name=self.__aws_region)
		table = dynamodb_client.Table(self.__stats_table)
		stats_dict = json.loads(json.dumps(stats_dict), parse_float=Decimal)
		
		try:
			table.put_item(Item=stats_dict)
		except ClientError as ce:
			error_log = {"Error": ce, "Timestamp": stats_dict["Timestamp"]}
			self.upload_logs(error_log)

	def upload_logs(self, logs_dict: dict):
		"""Upload error logs to DynamoDB.

		Parameters
		----------
		logs_dict : dict
			Dictionary containing the error; must have the 'Timestamp' key

		Raises
		------
		DynamoDbException
			If upload of error dictionary fails.
		"""

		session = boto3.Session(profile_name=self.__aws_profile)
		dynamodb_client = session.resource('dynamodb', region_name=self.__aws_region)
		table = dynamodb_client.Table(self.__logs_table)
		stats_dict = json.loads(json.dumps(stats_dict), parse_float=Decimal)
		
		try:
			table.put_item(Item=stats_dict)
		except ClientError as ce:
			raise DynamoDbException("Failed to upload logs to DynamoDB: " + ce)
