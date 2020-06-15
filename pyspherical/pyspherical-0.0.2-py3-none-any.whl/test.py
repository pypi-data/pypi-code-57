from pyspherical import forward_transform, inverse_transform, get_grid_sampling, spin_spherical_harmonic
from pyspherical.utils import unravel_lm, ravel_lm
import numpy as np

lmax = 20   # Maximum multipole moment.
theta, phi = get_grid_sampling(lmax)
gtheta, gphi = np.meshgrid(theta, phi)

# Set up some test data
# This test is just the SH function with spin 1, l=2, and m=0.
dat = spin_spherical_harmonic(1, 2, 0, gtheta, gphi)

# The transformations can be run with either:
#   [dat.shape == (phi.size, theta.size)] or [dat.shape == phi.shape == theta.size]

flm = forward_transform(dat, phi, theta, lmax, spin=1)
flm2 = forward_transform(dat, gphi, gtheta, lmax, spin=1)
print(np.allclose(flm2, flm))

# The flm has shape (lmax-1)**2, with indices ordered as:
#        ind = 0  1  2  3  4  5  6  7  8
#        l  = 0  1  1  1  2  2  2  2  2
#        m  = 0 -1  0  1 -2 -1  0  1  2
# l, m = ravel_lm(ind)
# ind = unravel_lm(l, m)

peak_ind = np.argmax(flm.real)
print(ravel_lm(peak_ind))
# Matches the amplitude of the peak inserted.
# (See scripts/example_1.py for a more complete example).

# Now the inverse transform:
dat2 = inverse_transform(flm, phi, theta, lmax, spin=1)
print(np.allclose(dat, dat2))
