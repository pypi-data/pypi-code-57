#%%
import time

import matplotlib.pyplot as plt
import numpy

from disba import GroupDispersion, PhaseDispersion

plt.style.use("ggplot")


# Velocity model (thickness, Vp, Vs, density)
velocity_model = numpy.array(
    [
        [10.0, 7.00, 3.50, 2.00],
        [10.0, 6.80, 3.40, 2.00],
        [10.0, 7.00, 3.50, 2.00],
        [10.0, 7.60, 3.80, 2.00],
        [10.0, 8.40, 4.20, 2.00],
        [10.0, 9.00, 4.50, 2.00],
        [10.0, 9.40, 4.70, 2.00],
        [10.0, 9.60, 4.80, 2.00],
        [10.0, 9.50, 4.75, 2.00],  # Infinite half-space
    ]
)

# Calculations are performed using periods
# Period axis must be sorted in increasing order beforehand
tmin, tmax, nt = 0.0, 3.0, 60
t = numpy.logspace(tmin, tmax, nt)

# Thomson-Haskell propagator
starttime = time.time()

pd = PhaseDispersion(*velocity_model.T)
gd = GroupDispersion(*velocity_model.T)

cps = [pd(t, i, wave="love") for i in range(4)]
cgs = [gd(t, i, wave="love") for i in range(4)]

print(f"Elapsed time: {time.time() - starttime} s")

# Initialize figure
fig = plt.figure(figsize=(16, 5), facecolor="white")
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Plot phase velocity
for cp in cps:
    ax1.semilogx(cp.period, cp.velocity, linewidth=2)
ax1.grid(True, linestyle=":")
ax1.set_xlabel("Period (s)")
ax1.set_ylabel("Phase velocity (km/s)")
ax1.set_xlim(t.min(), t.max())

# Plot group velocity
for cg in cgs:
    ax2.semilogx(cg.period, cg.velocity, linewidth=2)
ax2.grid(True, linestyle=":")
ax2.set_xlabel("Period (s)")
ax2.set_ylabel("Group velocity (km/s)")
ax2.set_xlim(t.min(), t.max())

plt.draw()
fig.show()
