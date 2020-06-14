from fetcher import fetcher

class counter:
	def __init__(self, filename):
		self.fetcher = fetcher(filename)

	def count_content(self):
		return len(self.fetcher.get_content().split())

	def get_content(self):
		return fetcher.get_content()

if __name__ == '__main__':
	instance = counter('/home/peretz/dependencies/assets/content.txt')
	print(instance.count_content())