#%%
import time

import matplotlib.pyplot as plt
import numpy
from pysurf96 import surf96

plt.style.use("ggplot")


# Velocity model (Vp, Vs, density, thickness in km)
velocity_model = numpy.array(
    [
        [7.00, 3.50, 2.00, 10.0],
        [6.80, 3.40, 2.00, 10.0],
        [7.00, 3.50, 2.00, 10.0],
        [7.60, 3.80, 2.00, 10.0],
        [8.40, 4.20, 2.00, 10.0],
        [9.00, 4.50, 2.00, 10.0],
        [9.40, 4.70, 2.00, 10.0],
        [9.60, 4.80, 2.00, 10.0],
        [9.50, 4.75, 2.00, 10.0],  # Infinite half-space
    ]
)
vp, vs, rho, d = velocity_model.T

# Calculations are performed using periods
# Period axis must be sorted in increasing order beforehand
tmin, tmax, nt = 0.0, 3.0, 60
t = numpy.logspace(tmin, tmax, nt)

# Thomson-Haskell propagator
# %timeit surf96(d, vp, vs, rho, t, "rayleigh", 1, "phase", True)

starttime = time.time()

cps = [surf96(d, vp, vs, rho, t, "rayleigh", i + 1, "phase", True) for i in range(4)]
cgs = [surf96(d, vp, vs, rho, t, "rayleigh", i + 1, "group", True) for i in range(4)]

print(f"Elapsed time: {time.time() - starttime} s")

# Initialize figure
fig = plt.figure(figsize=(16, 5), facecolor="white")
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Plot phase velocity
for cp in cps:
    idx = cp > 0.0
    ax1.semilogx(t[idx], cp[idx], linewidth=2)
ax1.grid(True, linestyle=":")
ax1.set_xlabel("Period (s)")
ax1.set_ylabel("Phase velocity (km/s)")
ax1.set_xlim(t.min(), t.max())

# Plot group velocity
for cg in cgs:
    idx = cg > 0.0
    ax2.semilogx(t[idx], cg[idx], linewidth=2)
ax2.grid(True, linestyle=":")
ax2.set_xlabel("Period (s)")
ax2.set_ylabel("Group velocity (km/s)")
ax2.set_xlim(t.min(), t.max())

plt.draw()
fig.show()
