import cv2
import numpy as np
def debug_polys(np_image_or_path, polys, BNMode=True, color=255, thickness=1, save_image_path=None):
    if isinstance(np_image_or_path, np.ndarray):
        np_image = np_image_or_path
    else:
        np_image = cv2.imread(np_image_or_path, 1)

        
    if polys is None or len(polys)==0: return np_image
    if BNMode:
        zeros_img = np.zeros(np_image.shape[:2])
    else:
        zeros_img = np_image.copy()
    for poly in polys:
        draw = cv2.polylines(zeros_img, [poly.astype('int32')], True, color, thickness)
        center = np.average(poly, axis=0).astype('int32')
        draw = cv2.line(draw, tuple(center), tuple(poly[1].astype('int32')), color, thickness)

    if save_image_path:
        cv2.imwrite(save_image_path, draw)
    return draw