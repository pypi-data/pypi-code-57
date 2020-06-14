from content_fetcher import Fetcher

class Counter:
	def __init__(self, filename):
		self.fetcher = Fetcher(filename)

	def count_content(self):
		return len(self.fetcher.get_content().split())
	
	def get_fetcher(self):
		return self.fetcher

if __name__ == '__main__':
	instance = Counter('/home/peretz/dependencies/assets/content.txt')
	print(instance.count_content())