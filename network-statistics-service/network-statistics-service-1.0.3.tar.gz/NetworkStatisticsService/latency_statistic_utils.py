from NetworkStatisticsService.exceptions import CommandOutputFormatException, LatencyStatisticsException

class LatencyStatisticUtils(object):
	""" 
	A class used to extract latency statistics from ping command output

	...

	Methods
	-------
	extract_latency_statistics_from_command_output(statistics_rows)
		returns statistics dictionary or raises an error
	"""

	@staticmethod
	def __get_packet_loss_from_command_output(packet_loss_row):
		"""Extracts packet loss information from ping output row containing it.

		Parameters
		----------
		packet_loss_row : str
			The row from the ping command output containing the packet loss percentage

		Raises
		------
		CommandOutputFormatException
			If the row has unexpected format.
		"""

		stats = {}
		try:
			packet_loss_comma_split = packet_loss_row.split(",")
			for info in packet_loss_comma_split:
				if "packet loss" in info:
					stats['Loss'] = float(info.strip().split()[0][:-1])
					return stats
			raise CommandOutputFormatException("Could not find packet loss information in latency statistics.")
		except (ValueError) as error:
			raise CommandOutputFormatException("Ping command output for the packet loss row was not of expected format.\nUnderlaying error: " + str(error))

	@staticmethod
	def __get_ping_statistics_from_command_output(min_avg_max_row):
		"""Extracts latency statistics from ping command output row containing it.

		Parameters
		----------
		min_avg_max_row : str
			The row from the ping command output containing the network stats

		Raises
		------
		CommandOutputFormatException
			If the row has unexpected format.
		"""

		if min_avg_max_row is None:
			return {}
			
		try:
			elems = min_avg_max_row.split("=")
			keys = elems[0].strip().split()[-1].split("/")
			values = elems[1].strip().split()[0].split("/")
			stats = {}
			for index, key in enumerate(keys):
				stats[key.capitalize()] = float(values[index])
			return stats
		except IndexError as ie:
			raise CommandOutputFormatException("Ping command output for the packe loss row was not of expected format.\nUnderlaying error: " + str(ie))

	@staticmethod
	def extract_latency_statistics_from_command_output(statistics_rows):
		"""Extracts latency statistics from ping command output rows.

		Parameters
		----------
		statistics_rows : [str]
			The rows from the ping command output containing the network stats

		Raises
		------
		LatencyStatisticsException
			If any of the rows has unexpected format
		"""

		try:
			if "www.google.com" in statistics_rows[0]:
				packet_loss_row = statistics_rows[1]
				min_avg_max_row = None
			else:
				packet_loss_row, min_avg_max_row = statistics_rows[0], statistics_rows[1]
			loss_stats = LatencyStatisticUtils.__get_packet_loss_from_command_output(packet_loss_row)
			ping_stats = LatencyStatisticUtils.__get_ping_statistics_from_command_output(min_avg_max_row)
			return {**loss_stats, **ping_stats}
		except IndexError as ie:
			raise LatencyStatisticsException("Accessing the two statistic rows failed.\nUnderlying error: " + str(ie))
		except CommandOutputFormatException as cofe:
			raise LatencyStatisticsException("An error occured when processing the latency statistics.\nUnderlying error: " + str(cofe))
