# Refer: https://en.wikipedia.org/wiki/Test_functions_for_optimization

import numpy as np
import matplotlib.pyplot as plt
from pso import *

set_seed(4)

lower = xlower = ylower = -4
upper = xupper = yupper = 4
particleList = createRandomParticleList(2, numParticles=10, lower=lower, upper=upper)

# Testing on Himmelblau's function
# This function has 4 global minima, which minimum is computed by PSO depends on the initialization.
# seed = 1 gives minimum (-2.81, 3.13)
# seed = 2 gives minimum (-3, 2)
# seed = 3 gives mimimum (3.58, -1.85)
# seed = 4 gives mimimum (3, 2)
f = lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2

psoVisualize(particleList, f, xlower, xupper, ylower, yupper, c1=1, c2=1, W=0.5, numIters=50, maxFlag=False, sleepTime=0.1, density=1000, accuracy=2, verbose=False)
