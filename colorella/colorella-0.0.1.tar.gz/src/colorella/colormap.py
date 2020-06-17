# Copyright (c) 2019, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.
#
# All information contained herein is, and remains the property of Vienna
# University of Technology (TU Wien), Department of Geodesy and Geoinformation
# (GEO). The intellectual and technical concepts contained herein are
# proprietary to Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO). Dissemination of this information or
# reproduction of this material is forbidden unless prior written permission
# is obtained from Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO).

'''
Created On 2019-10-16, last modified
@author: Felix Reuß felix.reuss@geo.tuwien.ac.at
- includes functions from pytesmo package https://github.com/TUW-GEO/pytesmo

Colorella Package: Color organizing and easy to learn laboratory
The packages allows to load color maps from several sources including:
- matplotlib default colormaps (e.g viridis, plasma)
- colorcet colormaps (e.g fire, rainbow)
- cpt files
- ct files
- json
- or to create new colormaps from dictionaries or lists of colors
classmethods allow the following functions:
- save a newly or modified colormap as .cpt, .ct or .json file
- turn a colormap to greyscale (e.g. for printing in greyscale)
- reverse a colormap
- view a colormap as plot
- load or convert to gdal colortable objects
- create a list or dictionary object contaning all the colors from a colormap

'''''
import os
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
import colorcet as cc
import warnings
from colorella.conversions import cptfile2dict, ctfile2list, json2list

gdal_warning = 'No GDAL Installation found. Without gdal the following functions are not available: from_gdal, to_gdal'
try:
    from osgeo import gdal
    GDAL_INSTALLED = True
except:
    GDAL_INSTALLED = False

class ColorMap:
    """create a colormap object compatible with matplotlib
        """

    def __init__(self, arg):
        """
        Constructor of colormap class.

        Parameters
        ----------
        arg : str
            defining the input for the colormap, can be one of the following: mpl:Name to load a matplotlib colormap, cc:Name to load a Colorcet colormap, clName to load a Colorella Colormap from json file
        """
        self.arg = arg

        if isinstance(self.arg, col.LinearSegmentedColormap) or isinstance(self.arg, col.ListedColormap):
            self._mpl_cm = self.arg
        elif isinstance(self.arg, str):
            pkg_name, cm_name = arg.split(':')
            if pkg_name == "mpl":
                if cm_name not in plt.colormaps():
                    raise ValueError('Input provided {0} is not a Matplotlib Colormap'.format(
                cm_name))
                self._mpl_cm = cm.get_cmap(cm_name)
            elif pkg_name == "cl":
                cm_filepath = os.path.join(os.path.dirname(__file__), "colormaps", cm_name + ".json")
                name, colors, gradient = json2list(cm_filepath)
                if not gradient:
                    self._mpl_cm = col.ListedColormap(colors=colors, name=name)
                else:
                    self._mpl_cm = col.LinearSegmentedColormap(segmentdata=colors, name=name)
            elif pkg_name == 'cc':
                if cm_name not in cc.cm:
                    raise ValueError('Input provided {0} is not a Colorcet Colormap'.format(
                        cm_name))
                self._mpl_cm = cc.cm[cm_name]

        else:
            txt = "Input provided {0} is not recognised".format(
                self.arg)
            txt += "\n Use mpl:*name* for Matplotlib Colormaps, cc:*name* for Colorcet Colormaps and cl:*name* to open a" \
                   " Colormap from the Colormap directory"

            raise ValueError(txt)

    @property
    def name(self):
        """
        Returns attribute name

        Returns
        ---------
        attribute name
        """
        return self._mpl_cm.name

    @classmethod
    def from_file(cls, filepath, name=None, gradient=True):
        """
        Function to open colormap objects from .cpt, .ct, .json files

        Parameters:
        ----------
        filepath: str
            path and filename of the colormap to be opened
        name: str, optional
            name of the Colormap

        Returns
        ---------
        ColorMap object
        """

        mpl_cm = None
        extension = os.path.splitext(filepath)[1]
        if '.cpt' == extension:
            filename, cpt_list, cpt_dict = cptfile2dict(filepath)
            name = name if name is not None else filename
            if not gradient:
                mpl_cm = col.ListedColormap(name=name, colors=cpt_list)
            else:
                mpl_cm = col.LinearSegmentedColormap(name=name, segmentdata=cpt_dict)
        elif '.ct' == extension:
            filename, gdal_list = ctfile2list(filepath)
            name = name if name is not None else filename
            if not gradient:
                mpl_cm = col.ListedColormap(name=name, colors=gdal_list)
            else:
                mpl_cm = col.LinearSegmentedColormap.from_list(name=name, colors=gdal_list)
        elif '.json' == extension:
            filename, colors, gradient = json2list(filepath)
            name = name if name is not None else filename
            if not gradient:
                mpl_cm = col.ListedColormap(colors,  name=name)
            else:
                mpl_cm = col.LinearSegmentedColormap(name=name, segmentdata=colors)

        else:
            raise ValueError('File extensions is not recognized, supported file extensions are: .cpt, .ct, .json')

        return cls(mpl_cm)

    @classmethod
    def from_cptfile(cls, filepath, gradient=True):
        """
        Create a LinearSegmented Colormap from a .cpt file

        Parameters
        ----------
        filepath: str
            absolute filepath including filename and extension of the cpt file

        Returns
        -------
        ColorMap object (LinearSegmented Colormap object)
        """
        name, cpt_list, cpt_dict = cptfile2dict(filepath)
        if not gradient:
            return cls.from_list(cpt_list, name=name, gradient=False)
        else:
            return cls.from_dict(cpt_dict, name=name)


    @classmethod
    def from_ctfile(cls, filepath, gradient=True):
        """
        Create a Listed Colormap from a gdal .ct file

        Parameters
        ----------
        filepath: str
            absolute filepath including filename and extension of the ct file

        Returns
        -------
        ColorMap object (Listed Colormap object)
        """
        name, gdal_list = ctfile2list(filepath)
        if not gradient:
            return cls.from_list(gdal_list, name=name, gradient=False)
        else:
            return cls.from_list(gdal_list, name=name, gradient=True)


    @classmethod
    def from_jsonfile(cls, filepath):
        """
        Creates a LinearSegmented Colormap from a .json file

        Parameters
        ----------
        filepath: str
            absolute filepath including filename and extension of the json file

        Returns
        -------
        ColorMap object (LinearSegmented or Listed Colormap object)
        """
        name, colors, gradient = json2list(filepath)
        if not gradient:
            return cls.from_list(colors, name=name, gradient=gradient)
        else:
            return cls.from_dict(colors, name=name)


    @classmethod
    def from_gdal(cls, ct):
        """
        Converts a gdal Colortable to a matplotlib colormap

        Parameters
        ----------
        ct: gdal colortable object
            gdal colortable object from which a ColorMap shall be created

        Returns
        -------
        ColorMap object (Listed Colormap object)

        """
        if GDAL_INSTALLED:
            mpl_arr = [[ct.GetColorEntry[x][0] / 255.0, ct.GetColorEntry[x][1] / 255.0,
                        ct.GetColorEntry[x][0] / 255.0] for x in ct.GetCount()]
            return cls.from_list(mpl_arr)
        else:
            warnings.warn(gdal_warning)
            return None

    @classmethod
    def from_dict(cls, cdict, name='default'):
        """
        Create color map from linear mapping segments
        Parameters:
        ----------
        cdict: dictionary
            cdict argument is a dictionary with a red, green and blue
               entries. Each entry should be a list of *x*, *y0*, *y1* tuples,
               forming rows in a table. Entries for alpha are optional.
                example from matplotlib:
                suppose you want red to increase from 0 to 1 over
               the bottom half, green to do the same over the middle half,
               and blue over the top half.  Then you would use::

                   cdict = {'red':   [(0.0,  0.0, 0.0),
                                      (0.5,  1.0, 1.0),
                                      (1.0,  1.0, 1.0)],

                            'green': [(0.0,  0.0, 0.0),
                                      (0.25, 0.0, 0.0),
                                      (0.75, 1.0, 1.0),
                                      (1.0,  1.0, 1.0)],

                            'blue':  [(0.0,  0.0, 0.0),
                                      (0.5,  0.0, 0.0),
                                      (1.0,  1.0, 1.0)]}

               Each row in the table for a given color is a sequence of
               *x*, *y0*, *y1* tuples.  In each sequence, *x* must increase
               monotonically from 0 to 1.  For any input value *z* falling
               between *x[i]* and *x[i+1]*, the output value of a given color
               will be linearly interpolated between *y1[i]* and *y0[i+1]*::

                   row i:   x  y0  y1
                                  /
                                 /
                   row i+1: x  y0  y1

               Hence y0 in the first row and y1 in the last row are never used.

        name: str
            name of the Colormap
        Returns
        ---------
        ColorMap object (LinearSegmented Colormap object)
        """
        mpl_cm = col.LinearSegmentedColormap(name=name, segmentdata=cdict)
        return cls(mpl_cm)

    @classmethod
    def from_list(cls, clist, name='default', gradient=False):
        """
        Make a linear segmented colormap with *name* from a sequence
        of *colors* which evenly transitions from colors[0] at val=0
        to colors[-1] at val=1.
        Alternatively, a list of (value, color) tuples can be given
        to divide

        Parameters
        ----------
        clist: list
            list of colors given as RGBA tuples
        name: str
            name of the Colormap
        gradient: bool
            if False a Listed Colormap is created, if True a LinearSegmented Colormap is created

        Returns
        -------
        ColorMap object (LinearSegmented or Listed Colormap object)
        """
        if not gradient:
            mpl_cm = col.ListedColormap(name=name, colors=clist)
        else:
            mpl_cm = col.LinearSegmentedColormap.from_list(name=name, colors=clist)
        return cls(mpl_cm)

    def convert2greyscale(self, weights=1, inplace=True):
        """
        Return a grayscale version of the given colormap. Luminanance values are calculated using a dot  product of a weight array and the color array of the object

        Parameters
        ----------
        weights: int
            weights used to convert RGB values to luminance, default =1
        inplace: bool
            if True the original object is replaced, if False a new ColorMap object is returned

        Returns
        -------
        ColorMap object if inpalce = False

        """
        colors = self._mpl_cm(np.arange(self._mpl_cm.N))

        if weights == 1:
            RGB_weights = [0.2126, 0.7152, 0.0722]
            luminance = np.dot(colors[:, :3], RGB_weights)
        elif weights == 2:
            RGB_weights = [0.299, 0.587, 0.114]
            luminance = np.dot(colors[:, :3], RGB_weights)
        elif weights == 3:
            RGB_weights = [0.299, 0.587, 0.114]
            luminance = np.sqrt(np.dot(colors[:, :3] ** 2, RGB_weights))
        else:
            warnings.warn('Argument weight only supports values between 1 and 3')

        colors[:, :3] = luminance[:, np.newaxis]
        mpl_cm = col.LinearSegmentedColormap.from_list(self._mpl_cm.name +'_grey', colors, self._mpl_cm.N)

        if inplace:
            self._mpl_cm = mpl_cm
            return self
        else:
            return ColorMap(mpl_cm)

    def show(self):
        """
        Shows the colormap as a colorbar in a plot
        """
        colors = self._mpl_cm(np.arange(self._mpl_cm.N))
        plt.imshow([colors], extent=[0, 10, 0, 1])
        plt.axis('off')
        plt.show()

    def reverse(self, inplace=True):
        """
        Reverses a colormap, a.k.a returns the containing colors in reverse direction. Class type remains the same

        Parameters
        ----------
        inplace: bool
            if True the original object is replaced, if False a new ColorMap object is returned

        Returns
        -------
        ColorMap object if inplace = False
        """

        if isinstance(self._mpl_cm, col.ListedColormap):
            mpl_cm = col.ListedColormap(self._mpl_cm.colors[::-1])

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            reverse = []
            keys = []

            for key in self._mpl_cm._segmentdata:
                keys.append(key)
                channel = self._mpl_cm._segmentdata[key]
                data = []

                for c in channel:
                    data.append((1 - c[0], c[2], c[1]))
                reverse.append(sorted(data))

            revdict = dict(zip(keys, reverse))
            mpl_cm = mpl.colors.LinearSegmentedColormap(segmentdata=revdict, name=self._mpl_cm.name + '_reversed')

        if inplace:
            self._mpl_cm = mpl_cm
            return self._mpl_cm
        else:
            return ColorMap(mpl_cm)

    def to_matplotlib(self):
        """
        Returns the matplotlib colormap object

        Returns
        -------
        matplotlib colormap object

        """
        return self._mpl_cm

    def to_dict(self):
        """
        Creates a dictionary of colors from a colormap object

        Returns
        -------
        dict object

        """
        if isinstance(self._mpl_cm, col.ListedColormap):
            col_list = self._mpl_cm._lut
            red = []
            green = []
            blue = []
            alpha = []

            for i in range(len(col_list)):
                red.append(col_list[i][0])
                green.append(col_list[i][1])
                blue.append(col_list[i][2])
                alpha.append(col_list[i][3])
            col_dct = {'R': red, 'G': green, 'B': blue, 'A': alpha}
            return col_dct

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return self._mpl_cm._segmentdata

    def to_list(self):
        """
        Creates a list of colors from a colormap object

        Returns
        -------
        List object
        """
        if isinstance(self._mpl_cm, col.ListedColormap):
            return self._mpl_cm.colors

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            dic_list = []
            for key, value in self._mpl_cm._segmentdata.items():
                temp = [key, value]
                dic_list.append(temp)
            return  dic_list

    def to_gradient(self, inplace=True):
        """
        Converts a listed Colormap to a Linear Segmented Colormap

        Parameters
        ----------
        outname: str, optional
            filename if the colormap is saved
        inplace: bool
            if True the original object is replaced, if False a new ColorMap object is returned

        Returns
        -------
        ColorMap object is inplace = False
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            warnings.warn("Colormap is already a Segmented Colormap. Listed Colormap required")
            return self
        else:
            mpl_cm = col.LinearSegmentedColormap.from_list(name=self._mpl_cm.name+'_gradient', colors=self._mpl_cm.colors)

        if inplace:
            self._mpl_cm = mpl_cm
            return self
        else:
            return ColorMap(mpl_cm)

    def to_gdal(self, accelerate=1):
        """
        Converts a ColorMap object to a gdal colortable object

        Parameters
        ----------
        accelerate: int
            scale factor applied to Colors

        Returns
        -------
        Gdal color table object
        """
        if GDAL_INSTALLED:
            gdal_ct = gdal.ColorTable()
            if isinstance(self._mpl_cm, col.ListedColormap):
                mpl_ct = self._mpl_cm.colors

                for i in range(0, len(mpl_ct), accelerate):
                    gdal_ct.SetColorEntry(int(i / accelerate), tuple(np.rint(np.multiply(mpl_ct[i], 256)).astype(np.byte)) + (0,))
                for i in range(256 // accelerate, 256):
                    gdal_ct.SetColorEntry(i, tuple((255, 255, 255)) + (0,))
            elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
                mpl_ct = (self._mpl_cm(np.linspace(0., 1., 255))[:, :3] * 255).astype(int)
                for i in range(0, mpl_ct.shape[0], accelerate):
                    gdal_ct.SetColorEntry(int(i / accelerate),
                                          tuple(np.rint(np.multiply(mpl_ct[i], 256)).astype(np.byte)) + (0,))
                for i in range(256 // accelerate, 256):
                    gdal_ct.SetColorEntry(i, tuple((255, 255, 255)) + (0,))
            return gdal_ct
        else:
            warnings.warn(gdal_warning)
            return None

    def save_as_cpt(self, outpath=None, **kwargs):
        """
        Saves a acolormap.object as a .cpt file

        Parameters
        ----------
        outname: str, optional
            outname for the file
        keyword arguments: int
            Vmin, Vmax, N (Number of colorsteps)
        """
        if outpath is None:
            outpath = os.path.join(self.dirpath, self._mpl_cm.name+'.cpt')

        vmin=0
        vmax=1
        N=255
        #create string for upper, lower colors
        b = np.array(kwargs.get("B", self._mpl_cm(0.)))
        f = np.array(kwargs.get("F", self._mpl_cm(1.)))
        na = np.array(kwargs.get("N", (0, 0, 0))).astype(float)
        ext = (np.c_[b[:3], f[:3], na[:3]].T * 255).astype(int)
        # Creating footer
        extstr = "B {:3d} {:3d} {:3d}\nF {:3d} {:3d} {:3d}\nN {:3d} {:3d} {:3d}"
        footer = extstr.format(*list(ext.flatten()))
        # create colormap
        colors = (self._mpl_cm(np.linspace(0., 1., N))[:, :3] * 255).astype(int)
        vals = np.linspace(vmin, vmax, N)
        col_arr = np.c_[vals[:-1], colors[:-1], vals[1:], colors[1:]]

        fmt = "%e %3d %3d %3d %e %3d %3d %3d"

        np.savetxt(outpath, col_arr, fmt=fmt,
                   header="# COLOR_MODEL = RGB",
                   footer=footer, comments="")

    def save_as_ct(self, outpath=None):
        """
        Saves a colormap.object as a gdal .ct file

        Parameters
        ----------
        outname: str, optional
            outname for the file
        """
        if outpath is None:
            outpath = os.path.join(self.dirpath, self._mpl_cm.name+'.cpt')

        arr = np.zeros((255, 3), dtype=int)

        if isinstance(self._mpl_cm, col.ListedColormap):
            for i in range(len(self._mpl_cm.colors)):
                arr[i, :] = [int(self._mpl_cm.colors[i][0] * 255), int(self._mpl_cm.colors[i][1] * 255),
                                          int(self._mpl_cm.colors[i][2] * 255)]
        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            colors = (self._mpl_cm(np.linspace(0., 1., 255))[:, :3] * 255).astype(int)
            for i in range(len(colors)):
                arr[i, :] = [int(colors[i][0]), int(colors[i][1]), int(colors[i][2])]

        fmt = "%3d %3d %3d"
        np.savetxt(outpath, arr, fmt=fmt)

    def save_as_json(self, outpath=None):
        """
        Saves a colormap.object as a gdal .ct file

        Parameters
        ----------
        outname: str, optional
            outname for the file
        """
        if outpath is None:
            outpath = os.path.join(self.dirpath, self._mpl_cm.name+'.json')

        cmap_dict = {}
        cmap_dict["ColorSpace"] = "RGB"
        cmap_dict['Name'] = self._mpl_cm.name
        rgb_points = []
        if isinstance(self._mpl_cm, col.ListedColormap):
            for i in range(len(self._mpl_cm.colors)):
                rgb_points.append((self._mpl_cm.colors[i][0], self._mpl_cm.colors[i][1],
                                          self._mpl_cm.colors[i][2]))
            cmap_dict["Type"] = "Listed"
        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            segmnetdata = self._mpl_cm._segmentdata
            rgb_points = [segmnetdata]
            cmap_dict["Type"] = "Segmented"
        cmap_dict['RGBPoints'] = rgb_points
        cmap_list = []
        cmap_list.append(cmap_dict)

        with open(outpath, 'w') as file:
            file.write(json.dumps(cmap_list))

    def __len__(self):
        """
        Returns number of colors in the colormap
        - for Segmented Colormap: Number of Segments
        - for Listed Colormap: total number of colors
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return len(self._mpl_cm._segmentdata.get('red'))
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return self._mpl_cm.N

    def __getitem__(self, item):
        """
        Returns the xth color of the colormap
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return {'red':self._mpl_cm._segmentdata.get('red')[item], 'green':self._mpl_cm._segmentdata.get('green')[item], 'blue': self._mpl_cm._segmentdata.get('blue')[item], 'alpha': self._mpl_cm._segmentdata.get('alpha')[item]}
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return self._mpl_cm.colors[item]

    def __str__(self):
        """
        Returns a string containing the RGB values of the colormap
        - for Segmented Colormap: Start and end color
        - for a Listed Colormap: all colors
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return str(self._mpl_cm._segmentdata.values())
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return str(self._mpl_cm.colors[0]+self._mpl_cm.colors[-1])