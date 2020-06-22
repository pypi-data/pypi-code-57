from point import Point
import math

class Line:
	coord = property(lambda self: f'(({self.a.x}, {self.a.y}), ({self.b.x}, {self.b.y}))')
	midpoint = property(lambda self: Point((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2))
	gradient = property(lambda self: (self.a.y - self.b.y) / (self.a.x - self.b.x))
	pgrad = property(lambda self: -1 / self.gradient)
	edist = property(lambda self: math.dist([self.a.x, self.a.y], [self.b.x, self.b.y]))
	mdist = property(lambda self: abs(self.a.x-self.b.x) + abs(self.a.y-self.b.y))

	def __init__(self, a, b):
		self.a = a
		self.b = b

	def lineEqn(self):
		try:
			m = self.gradient
		except ZeroDivisionError:
			return f'x = {self.a.x}'
		c = self.a.y - (m*self.a.x)
		if m == 0:
			return f'y = {c}'
		else:
			if c == 0:
				return f'y = {m}x'
			elif c > 0:
				return f'y = {m}x + {c}'
			else:
				return f'y = {m}x - {c*-1}'

	def isParallel(self, l):
		return self.gradient == l.gradient

	def isPerp(self, l):
		return self.pgrad == l.gradient