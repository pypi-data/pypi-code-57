import math as m
import numpy as np

def E2R(Ry, Rx, Rz):
    '''Combine Euler angles to the rotation matrix (right-hand)
       
        Inputs:
            Ry, Rx, Rz : rotation angles along  y, x, z axis
                         only has Ry in the KITTI dataset
        Returns:
            3 x 3 rotation matrix

    '''
    R_yaw = np.array([[ m.cos(Ry), 0 ,m.sin(Ry)],
                      [ 0,         1 ,     0],
                      [-m.sin(Ry), 0 ,m.cos(Ry)]])
    R_pitch = np.array([[1, 0, 0],
                        [0, m.cos(Rx), -m.sin(Rx)],
                        [0, m.sin(Rx), m.cos(Rx)]])
    #R_roll = np.array([[[m.cos(Rz), -m.sin(Rz), 0],
    #                    [m.sin(Rz), m.cos(Rz), 0],
    #                    [ 0,         0 ,     1]])
    return (R_pitch.dot(R_yaw))

def project_corns(corns, intrins):
    '''
    corns: 3*8
    intrins: 3*4

    return: 8*2
    '''
    corns = np.concatenate([corns, np.ones((1,8))], axis=0)
    proj_points = np.dot(intrins, corns)
    proj_points[0,:] = proj_points[0,:]/proj_points[2,:]
    proj_points[1,:] = proj_points[1,:]/proj_points[2,:]
    proj_points = np.transpose(proj_points[:2,:])
    return proj_points