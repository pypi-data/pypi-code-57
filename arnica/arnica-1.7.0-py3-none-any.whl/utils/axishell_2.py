""" axishell module
to create x-axisymmetric shells for scientific computations
"""

import numpy as np
from arnica.utils.shell import Shell

class AxiShell(Shell):
    #pylint: disable=too-many-instance-attributes
    r"""\
    *Base class for x-axisymmetric computationnal shells*

    AxiShell class is based on Shell class, inheriting of Shell methods.
    At initialization, the shell is builded an an x-axisymmetric shell.

    Some attributes are based on **u** and **v**, defined as the curvilinear\
    longitudinal (x/r) abscissa and curvilinear azimutal (theta) abscissa\
    respectively.

    ::
                      (x_n, r_n)
                _____X_____
         ___----     |     ----___     Cylindrical system
        \            |            /    Example longi/u <=> r
         \           |           /
          \          |          /      r - longi/u
           \         |         /       ^
            \        | (x_0, r_0)      |
             \      _X_      /         |
              \__---   ---__/          X-----> theta - azi/v
                                      x

              ................
          ...                 ..       Cylindrical system
        ..                     .       Example longi/u <=> x/r
        .                      .
        .      ................         r
        .     .                         ^
         .     ...................      |
         ..                             |
            ......................      X-----> x
                          <--      theta - azi/v
                     x/r - longi/u

    :param n_azi: Number of azimuthal shell points
    :type n_azi: int
    :param n_longi: Number of longitudinal shell points
    :type n_longi: int
    :param angle: Range angle of the axicylindrical geometry
    :type angle: float
    :param ctrl_pts_x: Array of dim (n,) of x-coordinates of the points defining the spline
    :param ctrl_pts_r: Array of dim (n,) of r-coordinates of the points defining the spline

    Optionals arguments :
    :param angle_min: Minimum angle of the shell
    :type angle_min: float

    Public attributes :

        - **shape** - Shape of the shell : (n_azi, n_longi)
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
        - **_du**
        - **_dv**
        - **_abs_curv**
        - **_dwu**
        - **_dwv**
        - **_surf**

    """

    def __init__(self, n_azi, n_longi, angle, ctrl_pts_x, ctrl_pts_r, angle_min=None):
        #pylint: disable=too-many-arguments
        """
        *Initialize an AxiShell object*
        """

        Shell.__init__(self, n_azi, n_longi)

        self.ctrl_pts_x = ctrl_pts_x
        self.ctrl_pts_r = ctrl_pts_r
        self.angle = angle
        self.angle_min = angle_min

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
        shell_crest = self._compute_shell_crest(self.ctrl_pts_x, self.ctrl_pts_r)

        # Compute radius matrix of shape (n_azi, n_longi)
        self._rad = np.tile(shell_crest[1], (self.shape[0], 1))

        # Compute theta matrix of shape (n_azi, n_longi)
        rot_angle = 0
        if self.angle_min is not None:
            rot_angle = 0.5 * self.angle + self.angle_min
        min_theta = (rot_angle - 0.5 * self.angle) * np.pi / 180
        max_theta = (rot_angle + 0.5 * self.angle) * np.pi / 180
        self._theta = np.transpose(np.tile(np.linspace(min_theta,
                                                       max_theta,
                                                       num=self.shape[0]),
                                           (self.shape[1], 1)))

        # Compute xyz matrix of shape (n_azi, n_longi, 3)
        tmp_x = np.tile(shell_crest[0], (self.shape[0], 1))
        tmp_y = self._rad * np.cos(self._theta)
        tmp_z = self._rad * np.sin(self._theta)
        self._xyz = np.stack((tmp_x, tmp_y, tmp_z), axis=-1)

        # Compute x,y,z,r-normal matrix of shape (n_azi, n_longi)
        xr_nml_1d = self._compute_shellcrest_nml(shell_crest)
        self._n_r = np.tile(xr_nml_1d[1], (self.shape[0], 1))
        self._n_x = np.tile(xr_nml_1d[0], (self.shape[0], 1))
        self._n_y = self._n_r * np.cos(self._theta)
        self._n_z = self._n_r * np.sin(self._theta)

        # Compute du,dv matrix of shape(n_azi, n_longi)
        self._du = np.pad(np.sqrt(np.diff(self._xyz[:, :, 0], axis=1) ** 2
                                  + np.diff(self._rad, axis=1) ** 2),
                          ((0, 0), (1, 0)),
                          'edge')
        self._dv = self._rad * np.pad(np.diff(self._theta, axis=0),
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
