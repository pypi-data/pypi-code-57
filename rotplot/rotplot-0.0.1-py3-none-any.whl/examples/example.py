# -*- coding: utf-8 -*-


import sys
sys.path.append(".")

from rotplot.rotplot import rot_3D, rot_3D_surf

from mpl_toolkits.mplot3d import Axes3D 

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['legend.fontsize'] = 10


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_axis_on()
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)

a=5
b=3.4
c = np.sqrt(a**2 - b**2)
R=a


u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(-1, 1.73, 100)
U,V = np.meshgrid(np.linspace(0, 2*np.pi, 100),np.linspace(-1.5, 1.5, 100))

Cyclide=[-c*np.cosh(V)+( (-4+a*np.cosh(V))*(-a*np.cos(U)+c*np.cosh(V)) )/( -c*np.cos(U) + a*np.cosh(V) ),
      ( b*( -4 + a*np.cosh(V) ) * np.sin(U) ) / ( -c*np.cos(U) + a* np.cosh(V)  ),
     b*np.sinh(V) - ( b*( -4 +a*np.cosh(V) )*np.sinh(V) ) / ( -c * np.cos(U) + a*np.cosh(V)  )]

Ellipse=[a * np.cos(u),  b*np.sin(u),np.zeros(len(u))]

ax.plot_surface(Cyclide[0], Cyclide[1], Cyclide[2])
ax.plot(Ellipse[0], Ellipse[1], Ellipse[2])


#Rotation :
Ellipse_rot=rot_3D(Ellipse,180,1)
Cyclide_rot=rot_3D_surf(Cyclide,180,1)
    
ax.plot_surface(Cyclide_rot[0], Cyclide_rot[1], Cyclide_rot[2])
ax.plot(Ellipse_rot[0], Ellipse_rot[1], Ellipse_rot[2])
plt.show()