#%%
# %matplotlib qt
import os
import time

import matplotlib.pyplot as plt
import numpy

from disba import ThomsonHaskell

os.sys.path.append("../")

plt.style.use("ggplot")


# Velocity model (Vp, Vs, density, thickness)
# Comparison with results from CPIS:
# http://www.eas.slu.edu/eqc/eqc_cps/TUTORIAL/LessonA/index.html
thickness = numpy.array([5.0, 23.0, 8.0, 0])
vs = numpy.array([2, 3.6, 3.8, 3.3])
vp = vs * 1.73
rho = vp * 0.32 + 0.77
velocity_model = numpy.c_[vp, vs, rho, thickness]

# Frequency axis
# Calculations are performed using frequencies, but we want to
# calculate dispersion functions at regularly spaced periods
# nt is the number of period samples
tmin, tmax, nt = 0.0, 1.0, 60
t = numpy.logspace(tmin, tmax, nt)

# Thomson-Haskell propagator
starttime = time.time()
th = ThomsonHaskell(velocity_model)
cp0 = th(t, 0, velocity_type="phase")
cp1 = th(t, 1, velocity_type="phase")
cp2 = th(t, 2, velocity_type="phase")
cp3 = th(t, 3, velocity_type="phase")
cg0 = th(t, 0, velocity_type="group")
cg1 = th(t, 1, velocity_type="group")
cg2 = th(t, 2, velocity_type="group")
cg3 = th(t, 3, velocity_type="group")
print(time.time() - starttime)

# Initialize figure
fig = plt.figure(figsize=(16, 5), facecolor="white")
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# Plot phase velocity (frequency)
for cp in [cp0, cp1, cp2, cp3]:
    ax1.semilogx(cp.period, cp.velocity, linewidth=2)
ax1.grid(True, linestyle=":")
ax1.set_xlabel("Period (s)")
ax1.set_ylabel("Phase velocity (m/s)")
ax1.set_xlim(t.min(), t.max())

# Plot group velocity (period)
for cg in [cg0, cg1, cg2, cg3]:
    ax2.semilogx(cg.period, cg.velocity, linewidth=2)
ax2.grid(True, linestyle=":")
ax2.set_xlabel("Period (s)")
ax2.set_ylabel("Group velocity (m/s)")
ax2.set_xlim(t.min(), t.max())

plt.draw()
fig.show()

# %%
