def nospace(string):
	"""
	Remove spaces between json keys and values, and between the items
	in lists etc., from the given string

	:param string:
	:type string: str

	:return:
	:rtype: str
	"""
	
	return string.replace(": ", ':').replace(", ", ",")
