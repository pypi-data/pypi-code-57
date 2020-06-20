import matplotlib.projections as proj

from matplotlib.animation import FuncAnimation, writers
from matplotlib import pyplot as plt
from tqdm import tqdm

import math
import numpy as np
from viseng.utils import *
from viseng.function import Function, AnimatedFunction, FillBetween, AnimatedFunctional
from viseng.annotations import TextBox
from viseng.patches import AnimatedPatch

def load_writer(writer_name, message=""):

	try:
		writer = writers[writer_name]

	except RuntimeError as e:
		print(f"Runtime Error: {e}")
		if message != "": print(message)
		return None

	return writer

class AnimTiming(dict):
	"""Object for handling animation timing.
	Dictionary of 'id' : [time start: time end]"""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class FuncAxis(plt.Axes):
	"""Axis for visualising functions"""
	name = "FuncAxis"

	def __init__(self, *args, **kwargs):

		fig = self.figure
		self.fps = fig.fps
		self.anim_timings = fig.anim_timings

		self.functions = [] # list of Function objects
		self.other_objects = [] # list of Patch objects to iterate through (such as fill_between)

		self.animate = fig.animate
		self.anim = None # anim object

		super().__init__(rect=args[1], fig=fig, **kwargs) # initialise regular axis

		# defaults, modified by functions entered
		self.set_xlim(0, 1)
		self.set_ylim(0, 1)

		self.id_counter = 0

	def extend_limits(self, x=None, y=None):
		"""For all given x and y values, extend axis limits to incorporate those values"""
		items = [ [x, self.get_xlim(), self.set_xlim], [y, self.get_ylim(), self.set_ylim] ]

		for data, lims, set in items:
			if data is None: pass
			lower = min(*lims, *data)
			upper = max(*lims, *data)
			set(lower, upper)

	def new_id(self):
		self.id_counter +=1
		return self.id_counter - 1

	def add_func(self, function, timings=None, is_functional=False, **kwargs):
		"""Add new function to axis.

		if timings provided, array of [start, end]. Otherwise, assumed to be entire animation [start, end]"""

		func_id = self.new_id()

		if "animate" not in kwargs: kwargs["animate"] = self.animate # animate attribute, default to axis flag
		animate = kwargs["animate"]
		if animate:
			timings = self.anim_timings["fig"] if timings is None else timings
			self.anim_timings[func_id] = timings

			if not is_functional:
				if "x_samples" not in kwargs: kwargs["x_samples"] = int(math.ceil((timings[1] - timings[0]) * self.fps))
				func = AnimatedFunction(func=function, id=func_id, **kwargs)

			else:
				if "t_samples" not in kwargs: kwargs["t_samples"] = int(math.ceil((timings[1] - timings[0]) * self.fps))
				func = AnimatedFunctional(func=function, id=func_id, **kwargs)

		else:
			func = Function(function, id=func_id, **kwargs)
		self.functions.append(func)

		# Update axis bounds
		self.extend_limits(x=np_minmax(func.x), y=np_minmax(func(func.x)))

		return func

	def static_plot(self):
		for f in self.functions:
			f.plot, = self.plot(f.x, f(f.x), **f.plt_kw)

	def update_anim(self):
		for f in self.functions:
			f.set_plot(self.plot([], [], **f.plt_kw)[0])

		all_objects = [o for o in [*self.functions, *self.other_objects]]
		all_iters = [iter(o) for o in all_objects]

		for t in np.arange(0, self.figure.time, 1/self.figure.fps):
			for n, o in enumerate(all_iters):
				t_start, t_end = self.anim_timings[all_objects[n].id]
				if t_start <= t < t_end:
					try: next(o)
					except StopIteration: pass

			yield None

		# for plots in zip_longest(*self.functions, *self.others):
		# 	yield None	# yield at end of every frame to wait for next drawing

	def animated_plot(self):
		update = self.update_anim()
		def anim(i):
			"""Render next frame"""
			try: next(update)
			except StopIteration: return None

		return anim

	def render(self, *args, **kwargs):
		if self.animate: return self.animated_plot()
		else: self.static_plot()

	def fill_between(self, func1, func2, timings=None, **kwargs):
		obj_id = self.new_id()
		animate = self.animate if "animate" not in kwargs else kwargs['animate'] # animate attribute, default to axis flag
		if animate:
			self.anim_timings[obj_id] = self.anim_timings["fig"] if timings is None else timings
			fill = FillBetween(self, func1, func2, animate=animate, obj_id=obj_id, **kwargs)
			self.other_objects.append(fill)

	def add_text(self, s, x, y, **text_kwargs):
		text_id = self.new_id()
		text = TextBox(self, s, x, y, text_id=text_id, **text_kwargs)
		self.anim_timings[text_id] = self.anim_timings["fig"]  # timings from main figure
		self.other_objects.append(text)

	def add_patch(self, patch_type, *patch_args, animate_kwargs = None, timings=None, **patch_kwargs):
		patch_id = self.new_id()
		self.anim_timings[patch_id] = self.anim_timings["fig"] if timings is None else timings
		# get number of frames of sequence (take off one to deal with rounding errors, ensures all clip is in time
		n_frames = int((self.anim_timings[patch_id][1] - self.anim_timings[patch_id][0]) * self.fps) - 1

		patch = AnimatedPatch(patch_type, *patch_args, animate_kwargs=animate_kwargs, n_frames=n_frames,
							  patch_id = patch_id, **patch_kwargs)
		self.other_objects.append(patch)
		super().add_patch(patch.patch)  # add patch to axes

		self.extend_limits(*patch.get_bounds())  # update bounds for frame=0

proj.register_projection(FuncAxis)

class FuncFig(plt.Figure):
	"""Used to generate custom axes"""

	def __init__(self, *args, animate=False, fps=30, time = 5, **kwargs):
		super().__init__(*args, **kwargs)
		self.animate = animate
		self.fps = fps
		self.time = time
		self.n_frames = fps * time

		self.anim_timings = AnimTiming(fig = [0, time])

	def add_subplot(self, *args, **kwargs):
		"""Add FuncAxis as subplot"""
		return super(FuncFig, self).add_subplot(*args, **kwargs, projection="FuncAxis")

	def render(self):

		funcs = [ax.render() for ax in self.axes]

		def anim(i):
			[f(i) for f in funcs]

		self.anim = FuncAnimation(fig=self, func=anim, frames=self.n_frames, interval = 1000//self.fps) # attribute func animation to permanent object

	def save(self, *args, **kwargs):

		if self.animate:
			self.saveanim(*args, **kwargs)

		else:
			super().savefig(*args, **kwargs)

	def saveanim(self, title="unnamed", fmt="mp4", out_dir = "outputs"):

		# writer = writers["xxx"]
		if fmt == "gif":
			writer = load_writer("imagemagick",
								 message="imagemagick not found on system. Required for gifs - check installed and try again")

		elif fmt == "mp4":
			writer = load_writer("ffmpeg")

		else:
			print(f"Format '{fmt}' not currently supported. Only 'mp4', 'gif' accepted.")
			return None

		w = writer(fps = self.fps, bitrate = 1500)

		dir_path = os.path.dirname(os.path.realpath(__file__)) # directory of viseng

		try_mkdir(os.path.join(dir_path, out_dir))

		with tqdm(total = self.n_frames) as save_progress:
			self.anim.save(os.path.join(dir_path, out_dir, f"{title}.{fmt}"), writer=w,
						   progress_callback = lambda x,i: save_progress.update())

	def extend(self, left=0, right=1, bottom=0, top=1):
		"""Extend subplot. By default, full size"""
		self.subplots_adjust(left=left, right=right, bottom=bottom, top=top)