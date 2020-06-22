import os

def xywh2xyxy(bbox):
    assert(len(bbox)==4)
    return [bbox[0]-(bbox[2]-1)/2, bbox[1]-(bbox[3]-1)/2, bbox[0]+(bbox[2]-1)/2, bbox[1]+(bbox[3]-1)/2]

def xyxy2xywh(bbox):
    assert(len(bbox)==4)
    return [(bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2, bbox[2]-bbox[0]+1, bbox[3]-bbox[1]+1]


#----------------------3D BBox-----------------#

def ry_matrix(ry):
    RY = np.asarray([[+np.cos(ry), 0, +np.sin(ry)],
                    [          0, 1,          0],
                    [-np.sin(ry), 0, +np.cos(ry)]])
    return RY

def local_corners(dims, ry):
    '''
    dims: h, w, l
    ry: rad; 0->right, 90->forward, 180->left
    return: shape(3*8)
    '''
    assert(len(dims)==3)
    h, w, l = dims
    cood_x = [l/2, l/2, -l/2, -l/2, l/2, l/2, -l/2, -l/2]
    cood_y = [0,0,0,0,-h,-h,-h,-h]
    cood_z = [w/2, -w/2, -w/2, w/2, w/2, -w/2, -w/2, w/2]
    corners = np.asarray([cood_x, cood_y, cood_z]) # 3*8

    RY = ry_matrix(ry)
    corners = np.dot(RY, corners)
    return corners

def global_corners(dims, ry, locat):
    '''
    dims: h, w, l
    ry: rad; 0->right, 90->forward, 180->left
    locat: 
    return: shape(3*8)
    '''
    locat = np.array(locat).reshape(3,1)
    local_corns = local_corners(dims, ry)
    global_corns = local_corns + locat
    return global_corns

def projcted_3d_corns(global_corns, P2):
    global_corners = np.concatenate([transed_corners, np.ones((1,8))], axis=0)
    proj_points = np.dot(P2, global_corners)
    proj_points[0,:] = proj_points[0,:]/proj_points[2,:];
    proj_points[1,:] = proj_points[1,:]/proj_points[2,:];
    proj_points = np.transpose(proj_points[:2,:])
    return proj_points

def projcted_3d_corns(dims, ry, locat, P2):
    global_corns = global_corners(dims, ry, locat)
    global_corns = np.concatenate([global_corns, np.ones((1,8))], axis=0)
    proj_points = np.dot(P2, global_corns)
    proj_points[0,:] = proj_points[0,:]/proj_points[2,:]
    proj_points[1,:] = proj_points[1,:]/proj_points[2,:]
    proj_points = np.transpose(proj_points[:2,:])
    return proj_points

