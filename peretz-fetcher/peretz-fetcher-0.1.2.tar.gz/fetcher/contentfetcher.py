class fetcher:
	def __init__(self, filename = '../assets/content.txt'):
		self.filename = filename

	def set_file_source(self, filename):
		self.filename = filename

	def get_content(self):
		with open(self.filename, 'r') as file:
			file_contents = file.read()
			return file_contents

if __name__ == '__main__':
	instance = fetcher()
	print(instance.get_content())
