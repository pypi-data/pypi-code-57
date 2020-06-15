# coding: utf-8
import numpy as np
from pyspherical import get_grid_sampling, utils, forward_transform
lmax = 100
thetas, phis = get_grid_sampling(lmax)
gtheta, gphi = np.meshgrid(thetas, phis)
res = utils.potential_spline(3.0, gtheta.flatten(), gphi.flatten(), np.pi/4, 1.3)

flm = forward_transform(res, gphi.flatten(), gtheta.flatten(), lmax=lmax)

ems = np.array([utils.ravel_lm(ii)[1] for ii in range(lmax**2)])


# alm = 18 * np.pi / ( (el + 5 / 2) * (el + 3 / 2) * (el + 1 / 2) * (el - 1 / 2) * (el - 3 / 2) ) * spin_spherical_harmonic(0, l, m, phi_c, theta_c)

import IPython; IPython.embed()
