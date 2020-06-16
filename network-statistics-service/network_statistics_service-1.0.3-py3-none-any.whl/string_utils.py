class StringUtils(object):
	""" 
	A class used to hold various util mthods for working with strings.

	...

	Methods
	-------
	remove_empty_strings_from_string_list(string_list)
		returns a new list without the empty strings
	"""

	@staticmethod
	def remove_empty_strings_from_string_list(string_list):
		"""Removes empty strings from a list.

		Parameters
		----------
		string_list : [str]
			A list of strings
		"""

		return list(filter(None, string_list))
