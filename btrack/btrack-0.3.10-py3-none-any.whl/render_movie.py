import os
import numpy as np
import matplotlib.pyplot as plt
from .render import _render_tracks, _check_plot_order, _draw_cube

def _render_agents(ax, agents, colors_rgb=[], order='xyz', labels=False,
                   terminii=False, lw=5., frame=None):
    """ Render the agents """
    DIMS = _check_plot_order(order)
    if frame:
        p = [[getattr(a, order[i]) for a in agents if a.t==frame] for i in range(DIMS)]
    else:
        p = [[getattr(a, order[i]) for a in agents] for i in range(DIMS)]
    ax.scatter(*p, c='lightgrey', alpha=0.9)


class RenderTrackingMovie(object):
    """ RenderTrackingMovie

    Render tracks as a movie, by slicing tracks to show comet tails.

    Args:
        tracks: the tracks
        agents: (optional) agent objects if a simulation
        volume: the tracking volume

    Properties:
        save_dir: directory to save rendered images to

    Notes:
        TODO(arl): render image data
    """

    def __init__(self, tracks, agents, volume):
        self._tracks = tracks
        self._agents = agents
        self._volume = volume
        self.cmap = plt.get_cmap('gnuplot')

        self.image_stack = None

        self.xx, self.yy = np.meshgrid(np.linspace(0,1599,800), np.linspace(0,1199,600))

    @property
    def save_dir(self):
        return self._save_dir
    @save_dir.setter
    def save_dir(self, save_dir):
        if not isinstance(save_dir, str):
            raise TypeError('Save directory must be a string.')
        if not os.path.exists(save_dir):
            raise IOError('Save directory does not exist.')
        self._save_dir = save_dir


    def _display_image(self, ax, frame):
        im = self.image_stack[frame][0:-1:2,0:-1:2]
        X =  xx
        Y =  yy
        Z =  frame*np.ones(X.shape)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=im, shade=False)


    def render(self, order='xyz', labels=True, lw=3., tail=75):
        """ Render the movie """
        DIMS = 3 #_check_plot_order(order)

        fig = plt.figure(figsize=(16,16))

        # set up fiddly plot functions
        if DIMS == 3:
            ax = fig.add_subplot(111, projection='3d')
        else:
            ax = fig.add_subplot(111)

        colors_rgb = [self.cmap(int(i)) for i in np.linspace(0,255,16)]
        p_args = {'colors_rgb':colors_rgb, 'order':order, 'labels':labels}

        for f in range(self._volume[3][0], self._volume[3][1]):
            ax.cla()

            if self.image_stack is not None:
                self._display_image(ax, f)

            # _render_agents(ax, self._agents, lw=5., **p_args)
            to_plot = [ t.trim(f, tail=tail) for t in self._tracks if t.in_frame(f) ]
            _render_agents(ax, self._agents, frame=f)
            _render_tracks(ax, to_plot, lw=lw, **p_args)


            # plot a box of the appropriate dimensions
            if DIMS == 3:
                box_dims = 'xyzt'
                this_box = [self._volume[box_dims.index(dim)] for dim in order]
                _draw_cube(ax, this_box)

            ax.set_xlabel(order[0])
            ax.set_ylabel(order[1])
            if DIMS == 3:
                ax.set_zlabel(order[2])
            else:
                ax.autoscale('tight')

            ax.view_init(30, 150.+180.*(float(f)/float(self._volume[3][1])))

            plt.title('Tracking {0:d} objects in frame {1:d}'.format(len(to_plot), f))
            plt.axis('image')
            plt.savefig(os.path.join(self.save_dir,'tracking_'+str(f)+'.png'))

        plt.show()
