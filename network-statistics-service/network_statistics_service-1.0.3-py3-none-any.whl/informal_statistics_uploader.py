
class StatisticUploaderMeta(type):
	"""
	A StatisticUploader metaclass that will be used for Statistic Uploader class creation.
	"""

	def __instancecheck__(cls, instance):
		return cls.__subclasscheck__(type(instance))

	def __subclasscheck__(cls, subclass):
		return (hasattr(subclass, 'upload_statistics') and
				callable(subclass.upload_statistics) and
				hasattr(subclass, 'upload_logs') and
				callable(subclass.upload_logs))


class InformalStatisticUploaderInterface(metaclass=StatisticUploaderMeta):
	"""
	An interface which defines the required methods for the statistic uploader.

	Methods
	-------
	upload_statistics(stats_dict)
		Stub method
	upload_logs(logs_dict)
		Stub method
	"""
	def upload_statistics(self, stats_dict: dict):
		pass

	def upload_logs(self, logs_dict: dict):
		pass
    