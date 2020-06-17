"""
shell module implemented as parent for CartShell and AxiShell classes
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
from scipy import interpolate, spatial
import matplotlib.pyplot as plt
from arnica.utils import nparray2xmf

MAX_SPLINE_ORDER = 3
SPLINE_SMOOTHNESS = 0

AXIS_NAMES = ['time', 'v', 'u']

class Shell():
    #pylint: disable=too-many-instance-attributes
    """
    *Parent class for computationnal shells*

    :param n_axe_1: Number of x/longitudinal shell points
    :type n_axe_1: int
    :param n_axe_1: Number of y/azimuthal shell points
    :type n_axe_1: int

    Public attributes :

        - **shape** - Shape of the shell : (n_axe_1, n_axe_2)
        - **width_matrix** - Dict containing thickness matrices of shape 'shape'
        - **matrix** - Dict containing fields of shape 'shape' - To deprecate

    Private attributes :

        - **_xyz**
        - **_rad**
        - **_theta**
        - **_n_x**
        - **_n_r**
        - **_n_y**
        - **_n_z**
        - **_du**
        - **_dv**
        - **_abs_curv**
        - **_dwu**
        - **_dwv**
        - **_surf**

    """

    def __init__(self, n_axe_1, n_axe_2):
        """
        *Initialize a Shell object*
        """

        self.shape = (n_axe_1, n_axe_2)
        self.axis_names = AXIS_NAMES

        self._xyz = np.empty((*self.shape, 3))
        self._rad = np.empty(self.shape)
        self._theta = np.empty(self.shape)
        self._n_x = np.empty(self.shape)
        self._n_r = np.empty(self.shape)
        self._n_y = np.empty(self.shape)
        self._n_z = np.empty(self.shape)
        self._du = np.empty(self.shape)
        self._dv = np.empty(self.shape)
        self._abs_curv = np.empty(self.shape[0])
        self._dwu = np.empty(self.shape)
        self._dwv = np.empty(self.shape)
        self._surf = np.empty(self.shape)

        u_range = np.linspace(0., 1., num=self.shape[0])
        v_range = np.linspace(0., 1., num=self.shape[1])
        self._u_adim = np.ones(self.shape) * u_range[:, np.newaxis]
        self._v_adim = np.ones(self.shape) * v_range[np.newaxis,:]

        self.width_matrix = {}

    @property
    def xyz(self):
        """
        *Getter method for xyz matrix of shape (self.shape, 3)*
        """
        return self._xyz

    @property
    def rad(self):
        """
        *Getter method for rad matrix of shape (self.shape,)*
        """
        return self._rad

    @property
    def theta(self):
        """
        *Getter method for theta matrix of shape (self.shape,)*
        """
        return self._theta

    @property
    def n_x(self):
        """
        *Getter method for x-normal matrix of shape (self.shape,)*
        """
        return self._n_x

    @property
    def n_r(self):
        """
        *Getter method for r-normal matrix of shape (self.shape,)*
        """
        return self._n_r

    @property
    def n_y(self):
        """
        *Getter method for y-normal matrix of shape (self.shape,)*
        """
        return self._n_y

    @property
    def n_z(self):
        """
        *Getter method for z-normal matrix of shape (self.shape,)*
        """
        return self._n_z

    @property
    def du(self):
        #pylint: disable=invalid-name
        """
        *Getter method for u-direction spacing matrix of shape (self.shape,)*
        """
        return self._du

    @property
    def dv(self):
        #pylint: disable=invalid-name
        """
        *Getter method for v-direction spacing matrix of shape (self.shape,)*
        """
        return self._dv

    @property
    def u_adim(self):
        #pylint: disable=invalid-name
        """
        *Getter method for u-direction non dimentional matrix of shape (self.shape,)*
        """
        return self._u_adim

    @property
    def v_adim(self):
        #pylint: disable=invalid-name
        """
        *Getter method for v-direction non dimentional matrix of shape (self.shape,)*
        """
        return self._v_adim

    @property
    def abs_curv(self):
        """
        *Getter method for central curvilinear abscissa array of shape (self.shape[1],)*
        """
        return self._abs_curv

    @property
    def dwu(self):
        #pylint: disable=invalid-name
        """
        *Getter method for weighted u-direction spacing matrix of shape (self.shape,)*
        """
        return self._dwu

    @property
    def dwv(self):
        #pylint: disable=invalid-name
        """
        *Getter method for weighted v-direction spacing matrix of shape (self.shape,)*
        """
        return self._dwv

    @property
    def surf(self):
        #pylint: disable=invalid-name
        """
        *Getter method for weighted surface matrix of shape (self.shape,)*
        """
        return self._surf

    def dump_shell(self, name='shell'):
        """
        *Dump shell geometrical properties into hdf file*

        Optional :
        :param name: Name of the file to dump. Default 'shell'
        :type name: str
        """
        xmdf = nparray2xmf.NpArray2Xmf("./" + name + ".h5")
        xmdf.create_grid(np.take(self._xyz, 0, axis=-1),
                         np.take(self._xyz, 1, axis=-1),
                         np.take(self._xyz, 2, axis=-1))
        xmdf.add_field(self._rad, 'r')
        xmdf.add_field(self._theta, 'theta')
        xmdf.add_field(self._n_x, 'n_x')
        xmdf.add_field(self._n_y, 'n_y')
        xmdf.add_field(self._n_z, 'n_z')
        xmdf.add_field(self._n_r, 'n_r')
        xmdf.add_field(self._du, 'du')
        xmdf.add_field(self._dv, 'dv')
        xmdf.add_field(self._u_adim, 'u_adim')
        xmdf.add_field(self._v_adim, 'v_adim')
        xmdf.add_field(self._dwu, 'dwu')
        xmdf.add_field(self._dwv, 'dwv')
        xmdf.add_field(self._surf, 'surf')

        xmdf.dump()

    def add_curviwidth(self, label, points):
        """
        *Add a 2D width matrix of shell shape extruded from points spline*

        The witdh matrix is iso-shape[0]

        :param label: Label of the width matrix
        :type label: str
        :param points: Tuple (dim n) of tuple (dim 2) of float coordinates\

        Optional :
        :param replace: If True, overwrite matrix.
                        If False, addition matrix to possible previous one.
                        Default True
        :type replace: bool
        """

        (x_tuple, y_tuple) = tuple(zip(*points))

        # Extend Bounds
        xlist = [0] + list(x_tuple) + [1]
        ylist = [y_tuple[0]] + list(y_tuple) + [y_tuple[-1]]
        # Generate continuous fictive spline
        f_int = interpolate.interp1d(xlist, ylist)
        # Generate discretise spline
        xnew = np.linspace(0, 1, num=self.shape[1])
        ynew = f_int(xnew)

        if label not in self.width_matrix:
            self.width_matrix[label] = np.zeros(self.shape)

        # Extrude azimuthally
        self.width_matrix[label] += np.tile(ynew, (self.shape[0], 1))

    def set_mask_on_shell(self, point_cloud, tol):
        """
        *Create a mask on the shell from a point cloud*

        The mask value is 0 for shell points located near cloud points.
        Otherwise the mask value is 1.

        :param point_cloud: Array of dim (n,3) of coordinates of points.
        :type point_cloud: numpy array
        :param tol: Tolerance of proximity
        :type tol: int
        """

        # Create a KDTree from cloud points
        kdtree = spatial.KDTree(point_cloud)
        # Compute distances between cloud points and
        # the closest neighbor from the 2D shell points.
        dists, _ = kdtree.query(self.xyz, k=1)
        # Mask takes 1 if the distance is below tolerance.
        mask = np.where(dists.reshape(self.shape) > tol,
                        1.,
                        0.)

        return mask

    def bake_millefeuille(self, width_matrix_label, n_layers, shift=0.0):
        """
        *Create a millefeuille-like shell.

        Extrude a 2D shell in the normal direction up
        pointwise height given by "width_matrix_label" matrix.

        :param width_matrix_label: Label of the width matrix
        :type width_matrix_label: str
        :param n_layers: Number of layer for extrusion
        :type n_layers: int
        :param shift: Additional depth (optional)
        :type shift: float

        :returns:

            - **cake** - A dict() containing shell data :

                - *xyz* - np.array of dim (self.shape, n_layers, 3)
                - *dz*  - np.array of dim (self.shape, n_layers)

        "Bon appetit!"
        """

        cake = {}
        cake["xyz"] = np.empty((self.shape[0],
                                self.shape[1],
                                n_layers,
                                3))
        cake["dz"] = np.empty((self.shape[0],
                               self.shape[1],
                               n_layers))

        for j, n_j in enumerate((self._n_x, self._n_y, self._n_z)):
            for i in range(n_layers):
                cake["xyz"][:, :, i, j] = (np.take(self._xyz, j, -1)
                                           + (1.0 * i / n_layers
                                              * self.width_matrix[width_matrix_label]
                                              + shift)
                                           * n_j)

        for i in range(n_layers):
            cake["dz"][:, :, i] = abs(self.width_matrix[width_matrix_label] / n_layers)
        cake["dz"][:, :, 0] /= 2
        cake["dz"][:, :, -1] /= 2

        return cake

    def average_on_shell_over_dirs(self, variable, directions, scale=True):
        """
        *Performs an integration (average) over one or multiple directions*

        :param variable: A np.array to be averaged of dim (n_time, n_v, n_u)\
        :param directions: A list() of directions on which the average process\
                           is to be performed.\
                           Contains keywords from ['time','v','u'].

        :returns:

            - **averaged_variable** - A np.array of averaged data on given directions.
            - **min_variable** - A np.array of min data on given directions.
            - **max_variable** - A np.array of max data on given directions.
        """

        dirs = self.axis_names.copy()
        if scale:
            averaged_variable = np.multiply(variable, self.surf)
        else:
            averaged_variable = variable

        if (len(directions) > 0 and
                all(dir_ in dirs for dir_ in directions)):
            for dir_ in directions:
                index = dirs.index(dir_)
                averaged_variable = np.mean(averaged_variable, axis=index)
                dirs.pop(index)

        else:
            mess = 'Averaging directions do not conform to criteria\n'
            mess += 'It should be a list containing one of or all items\n'
            for axis in self.axis_names:
                mess += axis + ', '
            raise ValueError(mess)

        return averaged_variable

    def plot(self, savefile=None):
        """
        *Plot 2D curve of the Shell*

        Optional :
        :param savefile: If None, the figure is plot.
                         If string, the figure is saved into files
        """

        plt.plot(self.xyz[0, :, 0], self.xyz[0, :, 1])
        plt.title("Shell")
        plt.xlabel("x")
        plt.ylabel("y")

        if savefile is None:
            plt.show()
        else:
            plt.savefig(savefile)

    def _compute_shell_crest(self, ctrl_pts_1, ctrl_pts_2):
        """
        *Build the shell crest of shape (2, self.shape[1]) and respecting controle points*
        """

        # Build crest
        spline_order = min(len(ctrl_pts_1) - 1, MAX_SPLINE_ORDER)
        # Generate continuous spline from control points.
        tck, _ = interpolate.splprep([ctrl_pts_1,
                                      ctrl_pts_2],
                                     s=SPLINE_SMOOTHNESS,
                                     k=spline_order)
        unew = np.linspace(0, 1, num=self.shape[1])
        # Generate discrete spline
        # Numpy Array of dim (2, self.shape[1]) [x,r] / [x,y]
        shell_crest = np.asarray(interpolate.splev(unew, tck))

        return shell_crest

    def _compute_shellcrest_nml(self, shell_crest):
        #pylint: disable=no-self-use
        """
        *Private methold returning shell crest normals*

            - AxiShell -> x,r-normal
            - CartShell -> x,y-normal
        """
        nml_vect = np.roll(np.diff(shell_crest), 1, axis=0)
        nml_vect /= np.linalg.norm(nml_vect, axis=0)
        nml_vect[0, :] *= -1
        nml_vect = np.pad(nml_vect, ((0, 0), (0, 1)), mode='edge')
        return nml_vect
