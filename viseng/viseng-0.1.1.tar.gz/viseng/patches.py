from matplotlib import patches
import numpy as np

### ATTRIBUTE MAP
### for each patch, a dict of attribute, and the required function to change that attribute
ATTRIBUTE_MAP = {
	"Circle" : dict( xy = "set_center", radius = "set_radius")

}

class AnimatedPatch():
	"""Object for animating the input patch."""

	def __init__(self, patch_type, *patch_args, patch_id=0, animate_kwargs = None, n_frames=0, **patch_kwargs):
		"""
		:param patch_type: string corresponding to type of patch.
		:param animate_kwargs: dict of patch_attr : numpy array of values
		:param patch_kwargs: kwargs to be passed to patch
		"""

		assert patch_type in dir(patches), f"Patch '{patch_type}' not found in patches."

		self.patch_type = patch_type
		self.patch = getattr(patches, patch_type)(*patch_args, **patch_kwargs)

		self.animate_kwargs = animate_kwargs
		if self.animate_kwargs is not None:
			self.animate = True
			self.length = n_frames
		else:
			self.animate = False
			self.length = 0

		self.id = patch_id
		self.n_frames = n_frames
		self.c = 0

	def __len__(self):
		return self.length

	def __iter__(self):
		return self

	def __next__(self):
		if self.animate_kwargs is None: return None
		if self.c > len(self): raise StopIteration

		for attr, arr in self.animate_kwargs.items():

			frame = int(np.ceil((self.c / self.n_frames) * (len(arr) - 1))) # get relevant frame sample of this array (sample at axis fps)
			val = arr[frame]

			setter = getattr(self.patch, ATTRIBUTE_MAP[self.patch_type][attr]) # function to set value
			setter(val)

		self.c += 1

	def get_bounds(self):
		"""Get all x_bounds, y_bounds for patch"""
		patch = self.patch
		if self.patch_type == "Circle":
			x, y = patch._center
			r = patch.get_radius()
			if not self.animate:
				return [[x - r, x + r], [y - r, y + r]]
			else:
				x, y = (x,y) if "xy" not in self.animate_kwargs else np.swapaxes(self.animate_kwargs["xy"], 0, 1)
				r = r if "radius" not in self.animate_kwargs else self.animate_kwargs["radius"]
				return [ [(x - r).min(), (x + r).max()], [(y-r).min(), (y+r).max()] ]


def animate_patch(obj, *args, **kwargs):

	pass #