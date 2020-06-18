import numpy as np
def rect_bbox_to_polys(bbox):
    poly = np.zeros((4,2), dtype='int32')
    left_top_x, left_top_y, right_bot_x, right_bot_y = bbox[:4]
    poly[0] = [left_top_x, left_top_y]
    poly[1] = [right_bot_x, left_top_y]
    poly[2] = [right_bot_x, right_bot_y]
    poly[3] = [left_top_x, right_bot_y]
    return poly