import matplotlib
matplotlib.use("Agg")

import os

from matplotlib import pylab as p

gshow=True

def plot(fn="fit.png",show=True,**aa):
    p.savefig(fn,**aa)

    print("saving",fn,show,gshow)
    if show and gshow:
        print("showing")
        os.system("display "+fn+"&")


def plot_line_colored(x,y,t,w=None,color=None,cmap=None):
    import numpy as np
    from matplotlib.collections import LineCollection

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be numlines x points per line x 2 (x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    extra={}
    if w is None: extra['linewidths']=w

    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    lc = LineCollection(segments, cmap=p.get_cmap(cmap),
        **extra
        #norm=p.Normalize(0, 10)
        )
    lc.set_array(t)
    lc.set_linewidth(w)

    if color is not None:
        lc.set_color(color)

    p.gca().add_collection(lc)
