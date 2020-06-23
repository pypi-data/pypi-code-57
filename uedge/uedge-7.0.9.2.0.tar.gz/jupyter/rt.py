from uedge import *
import numpy as np
import pickle
from matplotlib import pyplot as plt

def ray_tracing_numpy(x,y,poly,inside=None):
    #n = len(poly)
    n = 4
    if inside == None:
        inside = np.zeros(len(x),np.bool_)
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        idx = np.nonzero((y > min(p1y,p2y)) & (y <= max(p1y,p2y)) & (x <= max(p1x,p2x)))[0]
        if idx != []:
           if p1y != p2y:
               xints = (y[idx]-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
           if p1x == p2x:
               inside[idx] = ~inside[idx]
           else:
               idxx = idx[x[idx] <= xints]
               inside[idxx] = ~inside[idxx]    

        p1x,p1y = p2x,p2y
    return inside    

def ray_tracing_mult(x,y,poly):
    return [ray_tracing_numpy(xi, yi, poly) for xi,yi in zip(x,y)]

import random
random.seed('uedge')
x = np.array([random.uniform(1.4,1.5) for i in range(100)])
y = np.array([random.uniform(0.5,0.6) for i in range(100)])

x = np.linspace(1.0,2.5,100)
y = np.linspace(0.0,3.2,100)
xv,yv = np.meshgrid(x,y)
x = xv.reshape(10000)
y = yv.reshape(10000)


#res = [for i,rval in ndenumerate(com.rm[:,:,1]):
#https://www.geeksforgeeks.org/python-get-indices-of-true-values-in-a-binary-list/

from uedge import *
from case_setup import *
from uedge import hdf5
hdf5.hdf5_restore('d3d.hdf5')
bbb.exmain()


ixmin = com.nxomit
ixmax = (com.nxm-1)
iymin = 0
iymax = (com.ny-1)


im = np.zeros(len(x))
for ix in range(ixmax-ixmin+1):
        for iy in range(iymax-iymin+1):
            r0 = [com.rm[ix, iy, 1], com.rm[ix, iy, 2],
                  com.rm[ix, iy, 4], com.rm[ix, iy, 3]]
            z0 = [com.zm[ix, iy, 1], com.zm[ix, iy, 2],
                  com.zm[ix, iy, 4], com.zm[ix, iy, 3]]
            i = ray_tracing_numpy(x,y,list(zip(r0,z0)))
            b = list(filter(lambda ii: i[ii],range(len(i))))
            print(len(b))
            if len(b) > 0: 
               for jj in range(len(b)):
                  im[b[jj]] = im[b[jj]] + 1




plt.imshow(im.reshape(100,100))

plt.show()


