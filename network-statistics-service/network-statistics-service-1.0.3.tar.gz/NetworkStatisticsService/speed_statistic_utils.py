from NetworkStatisticsService.exceptions import SpeedStatisticsException

class SpeedStatisticUtils(object):
	""" 
	A class used to extract speed statistics from speedteest command output

	...

	Methods
	-------
	extract_speed_statistics_from_command_output(statistics_rows)
		returns statistics dictionary or raises an error
	"""

	@staticmethod
	def extract_speed_statistics_from_command_output(statistics_rows):
		"""Extracts speed statistics from speedtest command output rows.

		Parameters
		----------
		statistics_rows : [str]
			The rows from the speedtest command output containing the network stats

		Raises
		------
		SpeedStatisticsException
			If any of the rows has unexpected format
		"""

		try: 
			stats = {}
			for row in statistics_rows:
				elems = row.split(":")
				stats[elems[0]] = float(elems[1].strip().split()[0].strip())
			return stats
		except IndexError as ie:
			raise SpeedStatisticsException("An error occured when processing the speed statistics.\nUnderlying error: " + str(ie))
