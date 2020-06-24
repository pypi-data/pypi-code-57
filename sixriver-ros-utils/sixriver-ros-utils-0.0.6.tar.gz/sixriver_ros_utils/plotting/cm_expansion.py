#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import math

# Declare some constants
MAX_INFLATION_RADIUS = 1.6
NPOINTS = 30
INSCRIBED_RADIUS = 0.3

# Create the two functions

class StandardInflation:
    def __init__(self, radius, scalar, inscribed_radius):
        self.radius = radius
        self.scalar = scalar
        self.inscribed_radius = inscribed_radius

    def inflate(self, x):
        y = []
        for pt in x:
            y.append(self.cost(pt))
        return y

    def cost(self,pt):
        if (pt <= self.inscribed_radius):
            return 253
        if (pt <= self.radius):
            return int(253 * math.exp(-1.0 * self.scalar * (pt-self.inscribed_radius)))
        else:
            return 0
    def str(self):
        return 'IR: {}, W: {}'.format(self.radius, self.scalar)


class VoronoiInflation:
    def __init__(self, radius, scalar, inscribed_radius, vor_dist):
        self.radius = radius
        self.scalar = scalar
        self.inscribed_radius = inscribed_radius
        self.vor_dist = vor_dist
    def inflate(self, x):
        y = []
        for pt in x:
            y.append(self.cost(pt))
        return y

    def cost(self, pt):
        dO = pt - self.inscribed_radius
        dV = self.vor_dist - dO
        if (pt <= self.inscribed_radius):
            return 253
        elif (pt <= self.radius):
            return int(253 *(self.scalar / (self.scalar + dO)) * (dV / (dO + dV)) * math.pow((dO - self.radius) / self.radius, 2))
        else:
            return 0

    def str(self):
        return 'IR: {}, W: {}, VD: {}'.format(self.radius, self.scalar, self.vor_dist)

class SigmoidInflation:
    def __init__(self, radius, scalar, inscribed_radius):
        self.radius = radius
        self.scalar = scalar
        self.inscribed_radius = inscribed_radius
    def inflate(self, x):
        y = []
        for pt in x:
            y.append(self.cost(pt))
        return y

    def cost(self, pt):
        dO = pt - self.inscribed_radius
        dV = self.radius - pt

        if (pt <= self.inscribed_radius):
            return 253
        elif (pt <= self.radius):
            b = 10
            x0 = self.scalar
            x = 1.0 - (pt - self.inscribed_radius) / (self.radius - self.inscribed_radius)
            #val = 1 / (1 + math.exp(-b*(x - (1 - x0))))
            val = math.pow(1 / (1 + math.exp(-b*(x - (1 - x0)))) * x, 1-x)
            print "x: {}".format(x)
            return int(253 * val)
        else:
            return 0

    def str(self):
        return 'IR: {}, W: {}'.format(self.radius, self.scalar)


# instatiate inflators
si = StandardInflation(0.6, 2.0, INSCRIBED_RADIUS)
vi = VoronoiInflation(1.0, 2.0, INSCRIBED_RADIUS, 0.4)
vi2 = VoronoiInflation(1.0, 2, INSCRIBED_RADIUS, 0.8)
vi3 = VoronoiInflation(1.0, 2, INSCRIBED_RADIUS, 1.0)
vi4 = VoronoiInflation(1.0, 2.0, INSCRIBED_RADIUS, 1.5)
vi5 = VoronoiInflation(1.0, 2.0, INSCRIBED_RADIUS, 2.0)
sig = SigmoidInflation(1.6, 2.2, INSCRIBED_RADIUS)

x = np.linspace(0, MAX_INFLATION_RADIUS, NPOINTS)

plt.plot(x, si.inflate(x), 'k-*',
    x, vi.inflate(x), 'b-o',
    x, vi2.inflate(x), 'r-o',
    x, vi3.inflate(x), 'g-o',
    x, vi4.inflate(x), 'm-o',
    x, sig.inflate(x), 'k-o')

plt.xlabel('Distance from obstacle (m)')
plt.ylabel('Cost')
plt.legend(['Exponential inflatoin ' + si.str(),
    'Voronoi inflation ' + vi.str(),
    'Voronoi inflation ' + vi2.str(),
    'Voronoi inflation ' + vi3.str(),
    'Voronoi inflation ' + vi4.str(),
    'Sigmoid inflation ' + sig.str()
    ])

plt.show()
