import cv2
import numpy as np
import .detbbox as detbbox

def draw_bbox(img, bbox, color=(0,255,255), width=2, xywh=False):
    assert(len(bbox)==4)
    if xywh:
        bbox = detbbox.xywh2xyxy(bbox)
    bbox = [int(ii) for ii in bbox]
    cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2],bbox[3]), color, )
    return img

def draw_3dbbox(img, corns_2d, width=2, color=None):
    '''
    corns_2d: 2*8 or 1*16: [x1,y1, x2,y2,..., x8,y8]
    '''
    corns_2d = np.array(corns_2d, dtype=np.int)
    corns_2d = corns_2d.reshape(2, 8)
    if color is None:
        cont_color = (255,0,0)
        front_color = (0,255,0)
        rear_color = (0,0,255)
    else:
        cont_color = front_color = rear_color = color
    
    cv2.drawContours(img, [corns_2d[:4]], -1, cont_color, 1)
    cv2.drawContours(img, [corns_2d[4:]], -1, cont_color, 1)
    for i in range(2):
        cv2.line(img, (corns_2d[i][0], corns_2d[i][1]), (corns_2d[i+4][0], corns_2d[i+4][1]), front_color, 2)
    for i in range(2,4):
        cv2.line(img, (corns_2d[i][0], corns_2d[i][1]), (corns_2d[i+4][0], corns_2d[i+4][1]), rear_color, 2)

    return img

def get_bev_img(points, res=0.1, xrange=(-40, 40), zrange=(0, 70), hrange=(-2, 1), hist_scale=(0, 255)):
    '''
    points: shape (-1, 4) -- [x,y,z,s]; x->forward, y->left, z->up
    res: resolution of distance

    '''
    assert(points.shape[1]==4)
    # lidar coord different from camera coord
    points_x, points_y, points_z = [points[:, 0], points[:, 1], points[:, 2]]
    
    # filter points
    f_filt = np.logical_and(points_x > zrange[0], points_x < zrange[1]) # return mask
    s_filt = np.logical_and(points_y > xrange[0], points_y < xrange[1])
    filt_points = np.logical_and(f_filt, s_filt) # return mask
    indices = np.argwhere(filt_points).flatten()
    points_x = points_x[indices]
    points_y = points_y[indices]
    points_z = points_z[indices]
    
    u_img = (-points_y / res).astype(np.int32)
    v_img = (points_x / res).astype(np.int32)
    u_img -= int(np.floor(xrange[0]) / res) 
    v_img = (int(np.floor(zrange[1]) / res)-v_img) # set bottom as 0m
    
    pixel_value = np.clip(a=points_z, a_max=hrange[1], a_min=hrange[0])

    def scale_hist(a, dtype=np.uint8):
        height = hrange[1] - hrange[0]
        hist_range = hist_scale[1] - hist_scale[0]
        return ((hrange[1]-a) / height * hist_range + hist_scale[0]).astype(dtype)
    
    pixel_value = scale_hist(pixel_value)

    u_max = 1 + int((xrange[1] - xrange[0]) / res)
    v_max = 1 + int((zrange[1] - zrange[0]) / res)
    img = np.ones([v_max, u_max], dtype=np.uint8)*255
    img[v_img, u_img] = pixel_value
    img = np.reshape(img, (v_max, u_max, 1))
    img = np.concatenate([img, img, img], axis=-1)
    return img

def draw_3dbox_on_bev(bev_img, g_corners, res=0.1, xrange=(-40, 40), zrange=(0, 70), cont_color=(0,0,255)):
    assert(g_corners.shape==(3,8))
    corners_bev_xz = np.transpose(g_corners)[..., [0,2]]
    corners_bev_xz[..., 0] = (corners_bev_xz[..., 0]-xrange[0])/res
    corners_bev_xz[..., 1] = (zrange[1]-corners_bev_xz[..., 1])/res
    corners_bev_xz = corners_bev_xz.astype(np.int)
    cv2.drawContours(bev_img, [corners_bev_xz], -1, cont_color, 1)
    return bev_img

def get_bev_with_3dbbox(points, g_corners, res=0.1, xrange=(-40, 40), zrange=(0, 70), hrange=(-2, 1), hist_scale=(0, 255), cont_color=(0,0,255)):
    bev_img = get_bev_img(points, res, xrange, zrange, hrange, hist_scale)
    bev_img = draw_3dbox_on_bev(bev_img, g_corners, res, xrange, zrange, hrange, hist_scale, cont_color)
    return bev_img