def extent_bbox(bbox, extent):
    """
    Realize ratio enlargement or reduction of a given bbox

    :param bbox: input bbox
    :param extent:  size of enlargement (positive) or reduction (negative)
    :return: enlarge or reduce bbox
    """
    (x_min, y_min, x_max, y_max) = bbox
    x_min = x_min - extent
    y_min = y_min - extent
    x_max = x_max + extent
    y_max = y_max + extent

    return x_min, y_min, x_max, y_max


def bbox_union(bbox_a, bbox_b):
    """
    realize union between two given bbox

    :param bbox_a: first bbox
    :param bbox_b: second bbox
    :return: unioned bbox
    """
    (x_min_a, y_min_a, x_max_a, y_max_a) = bbox_a
    (x_min_b, y_min_b, x_max_b, y_max_b) = bbox_b

    return min(x_min_a, x_min_b), min(y_min_a, y_min_b), max(x_max_a, x_max_b), max(y_max_a, y_max_b)
