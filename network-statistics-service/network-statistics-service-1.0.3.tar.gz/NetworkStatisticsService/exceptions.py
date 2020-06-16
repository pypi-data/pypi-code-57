class NetworkStatisticsServiceException(Exception):
	"""
	Class used to encapsulate top level exceptions.
	"""
	pass

class CommandOutputFormatException(NetworkStatisticsServiceException):
	"""
	Class used to encapsulate exceptions regarding unexpected output format from executed bash commands.
	"""
	pass

class LatencyStatisticsException(NetworkStatisticsServiceException):
	"""
	Class used to encapsulate exceptions regarding unexpected format of the ping command.
	"""
	pass

class SpeedStatisticsException(NetworkStatisticsServiceException):
	"""
	Class used to encapsulate exceptions regarding unexpected format of the speedets cli.
	"""
	pass

class DynamoDbException(NetworkStatisticsServiceException):
	"""
	Class used to encapsulate exceptions regarding DynamoDB APIs.
	"""
	pass

class CommandRunException(NetworkStatisticsServiceException):
	"""
	Class used to encapsulate exceptions regarding executing bash commands.
	"""
	pass