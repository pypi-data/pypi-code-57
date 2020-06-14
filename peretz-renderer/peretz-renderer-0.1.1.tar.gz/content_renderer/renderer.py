from content_counter import Counter

class Renderer:
	def __init__(self, filename):
		self.counter = Counter(filename)

	def render_content(self):
		return self.counter.get_fetcher().get_content()

if __name__ == '__main__':
	instance = Renderer('/home/peretz/dependencies/assets/content.txt')
	print(instance.render_content())