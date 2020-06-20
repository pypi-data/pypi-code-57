"""Introduces the Function class, a class which represents a mathematical function,
which can be plotted as an animation, or visualised as a graph"""

import numpy as np
from matplotlib.collections import PolyCollection


plot_defaults = {
	"lw" : 3,
	"color" : "black",
}

def add_point_to_line(l, x, y):
	"""Add (x,y) point to pyplot line2d"""
	l.set_xdata(np.concatenate([l._x, [x]]))
	l.set_ydata(np.concatenate([l._y, [y]]))

def add_points_to_line(l, xs, ys):
	"""Add points to pyplot line2d"""
	l.set_xdata(np.concatenate([l._x, xs]))
	l.set_ydata(np.concatenate([l._y, ys]))

class Function:

	def __init__(self, func, xrange=None, animate=False, id=0, **plt_kw):

		self.id = id
		self.func = func

		if xrange is None: xrange = np.arange(0, 1, 0.05)

		self.x = xrange
		self.plot = None # Line2D object

		self.plt_kw = plot_defaults.copy()
		# replace default plot keywords with any given
		for kw, val in plt_kw.items():
			self.plt_kw[kw] = val

	def set_plot(self, plot):
		self.plot = plot

	def __call__(self, *args, **kwargs):
		return self.func(*args, **kwargs)

class XSampler():
	"""Used to sample a numpy xrange in order to effectively provide smooth animations"""
	def __init__(self, x0=0, x1=1, n_samples=10, sample="linear"):
		self.x = np.linspace(x0, x1, n_samples)

class AnimatedFunction(Function):
	"""Subclass of function, used to produce animations"""

	def __init__(self, x0=0, x1=1, x_samples=10, sampling="linear", sample_per_it = 1, **kwargs):
		"""
		:param sample_data: tuple of (x_start, x_end, n_samples)
		:param sampling:
		:param kwargs:
		"""
		super().__init__(**kwargs)
		self.x = XSampler(x0, x1, x_samples * sample_per_it, sampling).x

		self.sample_per_it = sample_per_it
		self.c = 0 # counter

	def set_plot(self, plot):
		"""Take Line2D object, save to function"""
		# For animating, mark every param needs to be stored separately to render through animation
		if plot._markevery is not None:
			self.markevery = np.array(plot._markevery)
			plot._markevery = []
		else:
			self.markevery = None

		return super().set_plot(plot)

	def __iter__(self): return self

	def __next__(self):
		xs, ys = [], []
		for n in range(self.sample_per_it):
			if self.c >= len(self):
				add_points_to_line(self.plot, xs, ys) # add points so far
				raise StopIteration

			if self.markevery is not None:
				self.plot._markevery = self.markevery[self.markevery < self.c] # update markevery

			x = self.x[self.c]
			y = self(x)

			xs.append(self.x[self.c])
			ys.append(y)

			self.c += 1

		add_points_to_line(self.plot, xs, ys)

	def __len__(self): return len(self.x)

class AnimatedFunctional(Function):
	"""A univariable function f(x), which changes with t. """

	def __init__(self, func,  t0=0, t1=1, t_samples=10, t_sampling="linear", x0=0, x1=1, x_samples = 100, xrange=None, *args, **kwargs):

		if xrange is None:
			xrange = XSampler(x0, x1, x_samples).x

		self.t = XSampler(t0, t1, t_samples, t_sampling).x
		self.functional = func

		self.c = 0
		super().__init__(lambda x: func(x, t=t0), xrange=xrange, *args, **kwargs)

	def __next__(self):
		if self.c >= len(self): raise StopIteration
		t = self.t[self.c]
		self.func = lambda x: self.functional(x, t=t)

		self.plot.set_xdata(self.x)
		self.plot.set_ydata(self.func(self.x))

		self.c += 1

	def __iter__(self): return self
	def __len__(self): return len(self.t)

class FillBetween(PolyCollection):
	"""Fills between two functions. Can be animated."""

	def __init__(self, ax, func1, func2, animate=False, obj_id=0, **fill_kwargs):
		self.ax = ax
		self.id = obj_id
		self.func1, self.func2 = func1, func2
		self.animate = animate
		if not np.array_equal(func1.x, func2.x):
			print("Func1.x and func2.x do not match for fill_between. Using func1.x")

		self.x = x = func1.x

		if not animate:
			ax.fill_between(x, func1(x), func2(x), **fill_kwargs)

		self.fill_kwargs = fill_kwargs
		self.c = 0 # counter

	def get_animated(self):
		return self.animate

	def __len__(self):
		return len(self.x) - 1 # only go to penultimate x val

	def __iter__(self): return self

	def __next__(self):

		if self.c >= len(self): raise StopIteration

		x0, x1 = self.x[self.c:self.c+2]
		x1+=(x1-x0)*0.5 # padding to prevent whitespace
		f1, f2 = self.func1, self.func2
		verts = np.array([[[x, f(x)] for x, f in [[x0, f1], [x0, f2], [x1, f2], [x1, f1] ]]])

		collection = PolyCollection(verts, **self.fill_kwargs)
		self.ax.add_collection(collection, autolim=False)

		self.c += 1