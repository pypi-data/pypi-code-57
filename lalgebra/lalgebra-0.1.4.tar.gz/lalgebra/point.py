class Point:
	x = 0
	y = 0
	coord = property(lambda self: f'({self.x}, {self.y})')
	asList = property(lambda self: [self.x, self.y])

	def __init__(self, x, y):
		self.x = x
		self.y = y