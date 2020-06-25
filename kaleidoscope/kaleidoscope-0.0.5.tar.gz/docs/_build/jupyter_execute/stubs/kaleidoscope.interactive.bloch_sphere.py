import numpy as np
from matplotlib.colors import LinearSegmentedColormap, rgb2hex
from kaleidoscope.interactive import bloch_sphere

cm = LinearSegmentedColormap.from_list('graypurple', ["#999999", "#AA00FF"])

pointsx = [[0, -np.sin(th), np.cos(th)] for th in np.linspace(0, np.pi/2, 20)]
pointsz = [[np.sin(th), -np.cos(th), 0] for th in np.linspace(0, 3*np.pi/4, 30)]

points = pointsx + pointsz

points_alpha = [np.linspace(0.8, 1, len(points))]

points_color = [[rgb2hex(cm(kk)) for kk in np.linspace(-1,1,len(points))]]

vectors_color = ["#777777", "#AA00FF"]

bloch_sphere(points=points,
             vectors=[[0, 0, 1], [1/np.sqrt(2), 1/np.sqrt(2), 0]],
             vectors_color=vectors_color,
             points_alpha=points_alpha,
             points_color=points_color,
             as_widget=True)