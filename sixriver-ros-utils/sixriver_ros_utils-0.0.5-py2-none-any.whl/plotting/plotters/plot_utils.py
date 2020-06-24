#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cmx
import matplotlib.colors as mpl_colors
from tf.transformations import euler_from_quaternion
import numpy as np

class PlotUtils:
    @staticmethod
    def getColorMap(num_colors):
        '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct
        RGB color.'''
        color_norm  = mpl_colors.Normalize(vmin=0, vmax=num_colors)
        scalar_map = mpl_cmx.ScalarMappable(norm=color_norm, cmap='hsv')
        def map_index_to_rgb_color(index):
            return scalar_map.to_rgba(index)
        return map_index_to_rgb_color
    @staticmethod
    def getMarkerStyle(num):
        markers = []
        for m in Line2D.markers:
            try:
                if len(m) == 1 and m != ' ':
                    markers.append(m)
            except TypeError:
                pass

        styles = markers + [
            r'$\lambda$',
            r'$\bowtie$',
            r'$\circlearrowleft$',
            r'$\clubsuit$',
            r'$\checkmark$']

        return styles[num % len(styles)]
    @staticmethod
    def getLineStyle(num):
        linestyles = ['-', '--', ':']
        return linestyles[num % len(linestyles)]
    @staticmethod
    def runningMean(x, num_samples):
        return np.convolve(x, np.ones((num_samples,))/num_samples)[(num_samples - 1):]



class ConversionUtils:
    @staticmethod
    def quat2Yaw(quat):
        orientation_list = [quat.x, quat.y, quat.z, quat.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        return yaw
    @staticmethod
    def clampAngle(angle):
        while (angle >= np.pi):
            angle -= np.pi
        while (angle < -np.pi):
            angle += np.pi
        return angle
