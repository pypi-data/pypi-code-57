# -*- coding: utf-8 -*-


import numpy as np

def rot_3D_surf(surf3D,angle,nR):
    '''
    Fonction that rotate a three-dimensional surface by an user-defined angle, and around an axis. 
    surf3D : Equation of the surface 
    nR = 0 Rotation around the x axis
    nR = 1 Rotation around the y axis
    nR = 2 Rotation around the z axis     
    '''
    theta = np.radians(angle)
    c=np.cos(theta)
    s=np.sin(theta)
    RX = np.array( ((1,0,0),(0,c,-s),(0,s, c) ))
    RY=np.array( ((c,0,s),(0,1,0),(-s,0, c) ))
    RZ=np.array( ((c,-s,0),(s,c,0),(0,0, 1) ))
    matrot=[RX,RY,RZ]

    surf_ROT=np.zeros(np.shape(surf3D))

    for j in np.arange(0,np.shape(surf3D)[2]):
        surf_rot_fun=[surf3D[0][j],surf3D[1][j],surf3D[2][j]]
        surf_rot_fun2=np.zeros(np.shape(surf_rot_fun))
        surf_rot_fun3=np.zeros(3)
        for i in np.arange(0,np.shape(surf3D)[1]):
            surf_rot_fun3=[surf_rot_fun[0][i],surf_rot_fun[1][i],surf_rot_fun[2][i]]
            surf_rot_fun2[:,i]=np.dot(surf_rot_fun3,matrot[nR])
        surf_ROT[0][j] = surf_rot_fun2[0]
        surf_ROT[1][j] = surf_rot_fun2[1]
        surf_ROT[2][j] = surf_rot_fun2[2]
    return surf_ROT

def rot_3D(surf,angle,nR):
    '''
    Fonction that rotate a two-dimensional surface (like an ellipse in space) by an user-defined angle, and around a given axis. 
    surf : Equation of the 3D curve 
    nR = 0 Rotation around the x axis
    nR = 1 Rotation around the y axis
    nR = 2 Rotation around the z axis     
    '''
    theta = np.radians(angle)
    c=np.cos(theta)
    s=np.sin(theta)
    RX = np.array( ((1,0,0),(0,c,-s),(0,s, c) ))
    RY=np.array( ((c,0,s),(0,1,0),(-s,0, c) ))
    RZ=np.array( ((c,-s,0),(s,c,0),(0,0, 1) ))
    matrot=[RX,RY,RZ]


    surf_ROT=np.zeros(np.shape(surf))

    for i in np.arange(0,np.shape(surf)[1]):
        surf_fun=[surf[0][i],surf[1][i],surf[2][i]]
        surf_ROT[:,i]=np.dot(surf_fun,matrot[nR])
    return surf_ROT