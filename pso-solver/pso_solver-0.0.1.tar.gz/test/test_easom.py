# Refer: https://en.wikipedia.org/wiki/Test_functions_for_optimization

import numpy as np
import matplotlib.pyplot as plt
from pso import *

set_seed(1)

lower = xlower = ylower = 0
upper = xupper = yupper = 6.28
particleList = createRandomParticleList(2, numParticles=10, lower=lower, upper=upper)

# Testing on Easom function
f = lambda x, y: -np.cos(x)*np.cos(y)*np.exp(-((x-np.pi)**2 + (y-np.pi)**2))

psoVisualize(particleList, f, xlower, xupper, ylower, yupper, c1=1, c2=1, W=0.5, numIters=25, maxFlag=False, sleepTime=0.1, density=100, accuracy=2, verbose=False)
