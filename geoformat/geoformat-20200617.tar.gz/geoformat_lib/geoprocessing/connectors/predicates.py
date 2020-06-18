from geoformat_lib.geoprocessing.connectors.operations import segment_to_bbox

# predicate return :
# - a boolean for geometries confrontation
# - or an information about position between a geometry in relation to another

# Return BOOLEAN
# Point vs
# point_intersects_point
# point_intersects_segment
# point_intersects_bbox
#
# segment vs
# segment_intersects_bbox
# segment_intersects_segment
#
# bbox vs
# bbox_intersects_bbox

# Return POSITION
# point_position_segment
# ccw_or_cw_segments


def point_intersects_point(point_a, point_b):
    """
    Return True if point_a and point_b have sames coordinates
    """
    return point_a[0] == point_b[0] and point_a[1] == point_b[1]


def point_intersects_segment(point, segment):
    """
    Test if point intersects a segment
    """
    if point_position_segment(point, segment) == 'ON':
        return True
    else:
        return False


def point_intersects_bbox(point, bbox):
    """
    This function send a boolean (true or false) that indicate if a given point intersect a given bbox

        Input:
            point
            bbox

        Output:
            True or False(boolean)
    """

    (point_x, point_y) = point
    (bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max) = bbox

    return point_x >= bbox_x_min and point_x <= bbox_x_max and point_y >= bbox_y_min and point_y <= bbox_y_max


def segment_intersects_segment(segment_a, segment_b):
    """"
    function that return True if two given segment intersects or False if not

    :param
    :segment_a: first segment to compare with second segment (segment_b)
    :segment_b: second segment to compare with first segment (segment_a)
    :return: True if intersects / False if not intersects
    """
    (point_a_1, point_a_2) = segment_a
    (point_b_1, point_b_2) = segment_b
    segment_a_1 = (point_a_2, point_b_1)
    segment_a_2 = (point_a_2, point_b_2)
    segment_b_1 = (point_b_2, point_a_1)
    segment_b_2 = (point_b_2, point_a_2)

    (pt_a_x, pt_a_y) = segment_a[0]
    (pt_b_x, pt_b_y) = segment_a[1]
    (pt_c_x, pt_c_y) = segment_a_1[1]

    a = (pt_b_x - pt_a_x) * (pt_c_y - pt_a_y)
    b = (pt_b_y - pt_a_y) * (pt_c_x - pt_a_x)
    if a > b:
        ccw_segment_a_1 = 'CCW'
    elif a < b:
        ccw_segment_a_1 = 'CW'
    else:
        ccw_segment_a_1 = False

    (pt_c_x, pt_c_y) = segment_a_2[1]

    a = (pt_b_x - pt_a_x) * (pt_c_y - pt_a_y)
    b = (pt_b_y - pt_a_y) * (pt_c_x - pt_a_x)
    if a > b:
        ccw_segment_a_2 = 'CCW'
    elif a < b:
        ccw_segment_a_2 = 'CW'
    else:
        ccw_segment_a_2 = False

    (pt_a_x, pt_a_y) = segment_b[0]
    (pt_b_x, pt_b_y) = segment_b[1]
    (pt_c_x, pt_c_y) = segment_b_1[1]

    a = (pt_b_x - pt_a_x) * (pt_c_y - pt_a_y)
    b = (pt_b_y - pt_a_y) * (pt_c_x - pt_a_x)
    if a > b:
        ccw_segment_b_1 = 'CCW'
    elif a < b:
        ccw_segment_b_1 = 'CW'
    else:
        ccw_segment_b_1 = False

    (pt_c_x, pt_c_y) = segment_b_2[1]

    a = (pt_b_x - pt_a_x) * (pt_c_y - pt_a_y)
    b = (pt_b_y - pt_a_y) * (pt_c_x - pt_a_x)
    if a > b:
        ccw_segment_b_2 = 'CCW'
    elif a < b:
        ccw_segment_b_2 = 'CW'
    else:
        ccw_segment_b_2 = False

    # If segments are parallels
    if ccw_segment_a_1 is False and ccw_segment_a_2 is False and ccw_segment_b_1 is False and ccw_segment_b_2 is False:
        segment_a_bbox = segment_to_bbox(segment_a)
        segment_b_bbox = segment_to_bbox(segment_b)
        return bbox_intersects_bbox(segment_a_bbox, segment_b_bbox)
    else:
        if ccw_segment_a_1 != ccw_segment_a_2:
            if ccw_segment_b_1 != ccw_segment_b_2:
                return True
        return False


def segment_intersects_bbox(segment, bbox):
    """
        Output :
            result (boolean) : True or False
    """
    point_start = segment[0]
    point_end = segment[1]
    (x_min, y_min, x_max, y_max) = bbox

    segment_bbox = segment_to_bbox(segment)
    # the bbox of segment and bbox must intersects
    if bbox_intersects_bbox(segment_bbox, bbox):
        # if begin or end point of segment is on bbox
        if point_intersects_bbox(point_start, bbox) or point_intersects_bbox(point_end, bbox):
            return True
        # if segment bbox intersect other bbox so segment intersect bbox :)
        else:
            segment_est = ((x_min, y_min), (x_min, y_max))
            segment_north = ((x_min, y_max), (x_max, y_max))
            segment_west = ((x_max, y_max), (x_max, y_min))
            segment_south = ((x_max, y_min), (x_min, y_min))
            # Each segment is test while result is true
            segments_list = (segment_est, segment_north, segment_west, segment_south)
            for segment_in_list in segments_list:
                if segment_intersects_segment(segment_in_list, segment):
                    return True
            return False
    else:
        return False



def bbox_intersects_bbox(bbox_a, bbox_b):
    """
    This function return a Truth Value Testing (True False) that qualifies the rectangle intersection


    True : bbox intersects
    False : bbox doesn't intersects

    The algorithm is inspired from : http://stackoverflow.com/questions/13390333/two-rectangles-intersection
                                    IA  : https://web.archive.org/web/*/http://stackoverflow.com/questions/13390333/two-rectangles-intersection

        Input :
            bbox_a : first boundary box
            bbox_b : second boundary box

        Output :
            result (boolean) : True or False

    """
    (x_min_a, y_min_a, x_max_a, y_max_a) = bbox_a
    (x_min_b, y_min_b, x_max_b, y_max_b) = bbox_b

    return x_min_a <= x_max_b and x_max_a >= x_min_b and y_min_a <= y_max_b and y_max_a >= y_min_b


def ccw_or_cw_segments(segment_a, segment_b, precision=None):
    """
    Return orientation for two consecutive segments. The second coordinate in segment A must be the same
    that the first segment B coordinate.
    This orientation is given in relation to a north-south-east-west oriented axis.

    This function is inspired from  : https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation

    :param:
    :segment_a: (list/tuple) first segment (last point must be same that second segment (segment_b))
    :segment_b: (list/tuple) second segment (first point must be same that first segment (segment_a))
    :return: - 'CCW': counter clock wise
             - 'CW': clock wise
             - 'NEITHER' : same direction
    """
    if segment_a[1][0] == segment_b[0][0] and segment_a[1][1] == segment_b[0][1]:
        (pt_a_x, pt_a_y) = segment_a[0]
        (pt_b_x, pt_b_y) = segment_a[1]
        (pt_c_x, pt_c_y) = segment_b[1]

        slope_a = (pt_b_x - pt_a_x) * (pt_c_y - pt_a_y)
        slope_b = (pt_b_y - pt_a_y) * (pt_c_x - pt_a_x)

        if slope_a == slope_b:
            return 'NEITHER'  # |
        elif slope_a > slope_b:
            return 'CCW'  # ↺
        else:
            return 'CW'  # ↻


def point_position_segment(point, segment, precision=None):
    """
    Return position of point regarding a segment
    :param:
    :point: point that we position
    :segment: segment that
    :return: - 'LEFT'
             - 'RIGHT'
             - 'ON'
             - 'NEITHER'
    """
    segment_b = (segment[1], point)
    orientation = ccw_or_cw_segments(segment, segment_b)
    if orientation in {"CW", 'CCW'}:
        if orientation == 'CCW':
            return 'LEFT'
        else:
            return 'RIGHT'
    else:
        seg_bbox = segment_to_bbox(segment)
        if point_intersects_bbox(point, seg_bbox):
            return 'ON'
        else:
            return 'NEITHER'
