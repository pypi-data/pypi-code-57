import os

def try_mkdir(dir):
	"""If dir does not exist, make it"""

	if os.path.isdir(dir):
		return None

	print(f"Making directory: {dir}")
	os.mkdir(dir)

np_minmax = lambda x: [x.min(), x.max()]
