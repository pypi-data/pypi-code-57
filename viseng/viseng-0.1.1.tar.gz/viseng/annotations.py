from matplotlib import pyplot as plt
from matplotlib.text import Text

class TextBox(Text):

	def __init__(self, ax, s="Text", x=0, y=0, strings = None, text_id=None, **text_kwargs):
		"""
		:param ax:
		:param s:
		:param x:
		:param y:
		:param strings: list of strings, used for animating text
		:param text_kwargs:
		"""
		super().__init__(x=x, y=y, **text_kwargs)

		self.id = text_id
		self.strings = strings
		self.c = 0 # counter
		ax.add_artist(self)

	def __iter__(self):
		if self.strings is None:
			raise ValueError("Text cannot be made animated - no strings given")

		return self

	def __next__(self):
		if self.c >= len(self): raise StopIteration

		self.set_text(self.strings[self.c])

		self.c += 1

	def __len__(self):
		"""Length if animated, in number of provided strings"""
		return len(self.strings)