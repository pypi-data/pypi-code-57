""" axishell module
to create x-axisymmetric shells for scientific computations
"""

import numpy as np
from arnica.utils.shell import Shell

class CartShell(Shell):
    #pylint: disable=too-many-instance-attributes
    r"""\
    *Base class for cartesian computationnal shells*

    CartShell class is based on Shell class, inheriting of Shell methods.
    At initialization, the shell is builded an an cartesian shell parallel to z.

    Some attributes are based on **u** and **v**, defined as the curvilinear\
    longitudinal (x/y) abscissa and curvilinear transversal (z) abscissa\
    respectively.

    ::
                   (x_n, y_n)
          ________X________
          |       |       |            Cartesian system
          |       |       |            Example longi/u <=> x
          |       |       |
          |       |       |            x - longi/u
          |    <----->    |            ^
          |       |       |            |
          |       |       |            |
          |       |       |            O-----> z - transvers/v
          |_______X_______|           y
                   (x_0, y_0)

    :param n_transvers: Number of azimuthal shell points
    :type n_transvers: int
    :param n_longi: Number of longitudinal shell points
    :type n_longi: int
    :param z_range: Extrusion range in transvers direction
    :type z_range: float
    :param ctrl_pts_x: Array of dim (n,) of x-coordinates of the points defining the spline
    :param ctrl_pts_y: Array of dim (n,) of y-coordinates of the points defining the spline

    Optionals arguments :
    :param z_min: Minimum transversal value of the shell
    :type z_min: float

    Public attributes :

        - **shape** - Shape of the shell : (n_transvers, n_longi)
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

    def __init__(self,
                 n_trans,
                 n_longi,
                 z_range,
                 ctrl_pts_x,
                 ctrl_pts_y,
                 z_min=None):
        #pylint: disable=too-many-arguments
        """
        *Initialize a CartShell object*
        """

        Shell.__init__(self, n_trans, n_longi)

        self.ctrl_pts_x = ctrl_pts_x
        self.ctrl_pts_y = ctrl_pts_y
        self.z_range = z_range
        self.z_min = z_min

        self._build_shell()

    def _build_shell(self):
        #pylint: disable=arguments-differ
        """
        *Build shell from geometric features*

            - Construct a spline used as base for extrusion\
              from control points : tck
            - Discretise the spline : shell_crest
            - Compute normal vectors for the 1D shell_crest
            - Compute r,n_x,n_r-components for 2D shell
            - Compute theta-components for 2D shell
            - Compute xyz,n_y,n_z-components for 2D shell
        """

        # Construct Shell Crest
        shell_crest = self._compute_shell_crest(self.ctrl_pts_x, self.ctrl_pts_y)

        # Compute xyz matrix of shape (n_transvers, n_longi, 3)
        tmp_x = np.tile(shell_crest[0], (self.shape[0], 1))
        tmp_y = np.tile(shell_crest[1], (self.shape[0], 1))

        trans_z = 0.
        if self.z_min is not None:
            trans_z = 0.5 * self.z_range + self.z_min
        min_z = trans_z - 0.5 * self.z_range
        max_z = trans_z + 0.5 * self.z_range
        tmp_z = np.transpose(np.tile(np.linspace(min_z,
                                                 max_z,
                                                 num=self.shape[0]),
                                     (self.shape[1], 1)))
        self._xyz = np.stack((tmp_x, tmp_y, tmp_z), axis=-1)

        # Compute radius and azimuth matrix of shape (n_transvers, n_longi)
        self._rad = np.sqrt(np.take(self._xyz, 1, -1) ** 2
                            + np.take(self._xyz, 2, -1) ** 2)
        self._theta = np.arctan2(np.take(self._xyz, 2, -1),
                                 np.take(self._xyz, 1, -1))

        # Compute x,y,z,r-normal matrix of shape (n_transvers, n_longi)
        xy_nml_1d = self._compute_shellcrest_nml(shell_crest)
        self._n_x = np.tile(xy_nml_1d[0], (self.shape[0], 1))
        self._n_y = np.tile(xy_nml_1d[1], (self.shape[0], 1))
        self._n_z = np.zeros(self.shape)
        self._n_r = self._n_y * np.cos(self._theta)

        # Compute du,dv matrix of shape (n_transvers, n_longi)
        self._du = np.pad(np.sqrt(np.diff(self._xyz[:, :, 0], axis=1) ** 2
                                  + np.diff(self._xyz[:, :, 1], axis=1) ** 2),
                          ((0, 0), (1, 0)),
                          'edge')
        self._dv = np.pad(np.diff(self._xyz[:, :, 2], axis=0),
                          ((1, 0), (0, 0)),
                          'edge')
        # Compute abs_curv array of shape (n_longi,)
        self._abs_curv = np.cumsum(np.take(self._du, 0, 0)) - self._du[0, 0]

        # Compute weight intervals in u and v directions array of shape (n_transvers, n_longi)
        self._dwu = self._du.copy()
        self._dwu[:, (0, -1)] /= 2
        self._dwv = self._dv.copy()
        self._dwv[(0, -1), :] /= 2

        # Compute surface nodoes array of shape (n_transvers, n_longi)
        self._surf = np.multiply(self._dwu, self._dwv)
