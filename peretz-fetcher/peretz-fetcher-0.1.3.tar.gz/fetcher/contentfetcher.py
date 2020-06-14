class fetcher:
	def __init__(self, filename):
		self.filename = filename

	def set_file_source(self, filename):
		self.filename = filename

	def get_content(self):
		with open(self.filename, 'r') as file:
			file_contents = file.read()
			return file_contents

if __name__ == '__main__':
	instance = fetcher('/home/peretz/dependencies/assets/content.txt')
	print(instance.get_content())
