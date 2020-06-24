import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from distutils import spawn

import micdata


class DisplayStacks():
    '''Display specific planes or an animation of multiple image stacks side-by-side'''

    def __init__(self, stack_list, titles=['sequence', 'labels'], figsize=(5)):
        self.set_stacks(stack_list)  # list of image stacks
        self.titles = titles
        self.titles.extend([''] * (len(self.stacks) - len(self.titles)))
        self.figsize = figsize
        self.fig = self.ax = self.movie = None
        self.calculate_thumbnails()

    def show_thumbnails(self):
        cols = len(self.thumbnails)
        self.fig, ax = plt.subplots(1, cols, figsize=(cols * self.figsize, self.figsize), squeeze=False)
        self.image_objects = ()
        for n in range(len(self.stacks)):
            data = np.squeeze(self.thumbnails[n])
            self.image_objects += (ax[0, n].imshow(data, cmap='gray', animated=True, vmin=0, vmax=1),)
        for i, a in enumerate(self.fig.axes):
            a.set_title(self.titles[i])
            a.axis('off')
        self.fig.tight_layout()

    def animate(self, framerate=20, duration=None):
        matplotlib.rcParams['animation.ffmpeg_path'] = spawn.find_executable('ffmpeg')
        self.calculate_thumbnails(plane=0)
        self.show_thumbnails()
        n_frames = len(self.stacks[0])
        if duration is not None:
            interval = (duration / n_frames) * 1000
        else:
            interval = 1 / framerate * 1000
        self.movie = anim.FuncAnimation(
            self.fig, self._update, frames=range(n_frames), interval=interval, blit=True)
        plt.close(self.fig)

    def calculate_thumbnails(self, plane=None, stack_operation=None, *args, **kwargs):
        self.thumbnails = []
        if plane is not None:
            # use the specified plane number
            for stack in self.stacks:
                self.thumbnails.append(stack[plane])
        elif stack_operation is not None:
            # apply a function to the stack
            for stack in self.stacks:
                self.thumbnails.append(stack_operation(stack, *args, **kwargs))
        else:
            # default is to use the center frame of each stack
            for stack in self.stacks:
                self.thumbnails.append(stack[round(stack.shape[0] / 2)])

    def set_stacks(self, stack_list):
        self.stacks = []
        for stack in stack_list:
            if isinstance(stack, micdata.Stack):
                self.stacks.append(stack.data)
            elif isinstance(stack, np.ndarray):
                self.stacks.append(stack)
            else:
                raise ValueError('Stacks must be either micdata.Stack or numpy.ndarray.')

    def _update(self, plane):
        for n in range(len(self.image_objects)):
            data = np.squeeze(self.stacks[n][plane])
            self.image_objects[n].set_array(data)
