import math

class Vector:
	x = 0
	y = 0
	coord = property(lambda self: f'({self.x}, {self.y})')
	length = property(lambda self: math.sqrt(self.x**2 + self.y**2))
	asList = property(lambda self: [self.x, self.y])

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def term(self, v, w):
		bc = -(v.x * w.y) / v.y + w.x
		b = ((self.x) - (v.x * self.y) / v.y) / bc
		ac = v.x
		a = ((self.x) - (w.x * b)) / ac
		return (a, b)

	def smult(self, s):
		return Vector(self.x * s, self.y * s)

	def vadd(self, v):
		return Vector(self.x + v.x, self.y + v.y)

	def vsub(self, v):
		return Vector(self.x - v.x, self.y - v.y)

	def dprod(self, v):
		return self.x * v.x + self.y * v.y

	def angle(self, v):
		t = self.dprod(v)/(self.length()*v.length())
		t = math.acos(t)
		return math.degrees(t)

	def scom(self, v):
		return (self.dprod(v))/v.length()

class VectorConstants:
	unitx = Vector(1, 0)
	unity = Vector(0, 1)