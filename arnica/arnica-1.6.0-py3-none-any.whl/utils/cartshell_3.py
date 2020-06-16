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
    At initialization, the shell is builded an an cartesian shell.

    Some attributes are based on **u** and **v**, defined as the curvilinear
    longitudinal (u) abscissa and curvilinear transversal (v) abscissa
    respectively.

    The shell is set using three corners (assuming they are othogonal)

    ::
          X umax
          ________________
          |              |            Cartesian system
          |              |            Example longi/u <=> x  and v <==> z
          |              |            zero. (0, 0, 0)
          |              |            umax. (1, 0, 0)
          |              |            vmax. (0, 0, 1)
          |              |            x - longi/u
          |              |            ^
          |              |            |
          |              |            |
          |              |            O-----> z - transvers/v
          |______________| X vmax     y
          X zero.

    :param n_transvers: Number of azimuthal shell points
    :type n_transvers: int
    :param n_longi: Number of longitudinal shell points
    :type n_longi: int
    :param z_range: Extrusion range in transvers direction
    :type z_range: float
    :param zero: Array of dim (3) lower left corner of shell
    :param umax: Array of dim (3) corner of shell for umax
    :param vmax: Array of dim (3) corner of shell for vmax

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
                 zero,
                 umax,
                 vmax,
                 ):
        #pylint: disable=too-many-arguments
        """
        *Initialize a CartShell object*
        """

        Shell.__init__(self, n_trans, n_longi)
        self._build_shell(
            np.array(zero),
            np.array(umax),
            np.array(vmax))

    def _build_shell(self, zero, umax, vmax):
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

        vec_u = umax-zero
        vec_v = vmax-zero

        norm = np.cross(vec_u, vec_v)
        norm /= np.linalg.norm(norm)

        u_range = np.linspace(0., 1., num=self.shape[0])
        v_range = np.linspace(0., 1., num=self.shape[1])
        d_u = np.linalg.norm(vec_u)/(self.shape[0]-1)
        d_v = np.linalg.norm(vec_v)/(self.shape[1]-1)

        v_coor, u_coor = np.meshgrid(v_range, u_range)
        u_coor = vec_u[np.newaxis, np.newaxis, :]*u_coor[:, :, np.newaxis]
        v_coor = vec_v[np.newaxis, np.newaxis, :]*v_coor[:, :, np.newaxis]
        tmp_x = (
            zero[np.newaxis, np.newaxis, 0]
            + u_coor[:, :, 0] + v_coor[:, :, 0])
        tmp_y = (
            zero[np.newaxis, np.newaxis, 1]
            + u_coor[:, :, 1] + v_coor[:, :, 1])
        tmp_z = (
            zero[np.newaxis, np.newaxis, 2]
            + u_coor[:, :, 2] + v_coor[:, :, 2])

        self._xyz = np.stack((tmp_x, tmp_y, tmp_z), axis=-1)

        # Compute radius and azimuth matrix of shape (n_transvers, n_longi)
        self._rad = np.sqrt(
            np.take(self._xyz, 1, -1) ** 2
            + np.take(self._xyz, 2, -1) ** 2)
        self._theta = np.arctan2(
            np.take(self._xyz, 2, -1),
            np.take(self._xyz, 1, -1))

        # Compute x,y,z,r-normal matrix of shape (n_transvers, n_longi)
        self._n_x = np.full(self.shape, norm[0])
        self._n_y = np.full(self.shape, norm[1])
        self._n_z = np.full(self.shape, norm[2])
        self._n_r = self._n_y * np.cos(self._theta)

        self._du = np.full(self.shape, d_u)
        self._dv = np.full(self.shape, d_v)

        # Compute abs_curv array of shape (n_longi,)
        self._abs_curv = np.cumsum(np.take(self._du, 0, 0)) - self._du[0, 0]

        # Compute weight intervals in u and v directions array of shape (n_transvers, n_longi)
        self._dwu = self._du.copy()
        self._dwu[:, (0, -1)] /= 2
        self._dwv = self._dv.copy()
        self._dwv[(0, -1), :] /= 2

        # Compute surface nodoes array of shape (n_transvers, n_longi)
        self._surf = np.multiply(self._dwu, self._dwv)

