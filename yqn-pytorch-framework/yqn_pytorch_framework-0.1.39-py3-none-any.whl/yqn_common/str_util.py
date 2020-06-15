# -*- coding:utf-8 -*-
import re


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def capitalize(name):
    return name.capitalize()


def clear_unified(s):
    s = re.sub("：", ":", re.sub("（", "(", re.sub("）", ")", re.sub("；", ";", re.sub("＆", "&", str(s))))))
    return s


def clear_number(s):
    return re.sub("[123456789]{1}", "0", s)


def is_str(s):
    return type(s) == str


def to_lowercase(s):
    return str.lower(s)


def to_uppercase(s):
    return str.upper(s)


def ends_with(s, suffix, ignore_case=False):
    """
    suffix: str, list, or tuple
    """
    if is_str(suffix):
        suffix = [suffix]
    suffix = list(suffix)
    if ignore_case:
        for idx, suf in enumerate(suffix):
            suffix[idx] = to_lowercase(suf)
        s = to_lowercase(s)
    suffix = tuple(suffix)
    return s.endswith(suffix)


def starts_with(s, prefix, ignore_case=False):
    """
    prefix: str, list, or tuple
    """
    if is_str(prefix):
        prefix = [prefix]
    prefix = list(prefix)
    if ignore_case:
        for idx, pre in enumerate(prefix):
            prefix[idx] = to_lowercase(pre)
        s = to_lowercase(s)
    prefix = tuple(prefix)
    return s.startswith(prefix)


def is_line_cross(line_1, line_2, ratio=0.9):
    if line_1[1] <= line_2[0] or line_1[0] >= line_2[1]:
        return False
    elif line_2[0] <= line_1[0] <= line_1[1] <= line_2[1] or line_1[0] <= line_2[0] <= line_2[1] <= line_1[1]:
        return True
    else:
        long_line = [min(line_1[0], line_2[0]), max(line_1[1], line_2[1])]
        short_line = [max(line_1[0], line_2[0]), min(line_1[1], line_2[1])]
        the_ratio = (short_line[1] - short_line[0]) / (long_line[1] - long_line[0])
        if the_ratio >= ratio:
            return True
        else:
            return False


def text_blocks_sort(data, ratio=0.5):
    """
    :param data: [{'v_5-13': [1570, 1212, 1682, 1254]}, {'v_5-14': [1810, 1104, 1928, 1141]}, ...]
    :param ratio
    :return:
    """
    texts_blocks_sorted = []

    line_values_sorted_array = []
    line_index = []
    values_already = []
    for a in range(len(data)):
        a_info = data[a]
        a_index = list(a_info.keys())[0]
        a_points = list(a_info.values())[0]

        line_in_values_array = []
        line_in_values_index = []
        if a_index not in values_already:
            line_in_values_array.append({str(a_points[0]): a_info})
            line_in_values_index.append(a_points[0])
            values_already.append(a_index)
            for b in range(len(data)):
                b_info = data[b]
                b_index = list(b_info.keys())[0]
                b_points = list(b_info.values())[0]

                if a != b and b_index not in values_already and is_line_cross([a_points[1], a_points[3]],
                                                                              [b_points[1], b_points[3]], ratio):
                    line_in_values_array.append({str(b_points[0]): b_info})
                    line_in_values_index.append(b_points[0])
                    values_already.append(b_index)

            line_sorted_index = sorted(line_in_values_index, reverse=False)
            line_in_values_sorted = []
            for tmp_index in line_sorted_index:
                for tmp_v in line_in_values_array:
                    tmp_v_index = list(tmp_v.keys())[0]
                    if tmp_v_index == str(tmp_index):
                        line_in_values_sorted.append(list(tmp_v.values())[0])
                        line_in_values_array.remove(tmp_v)
                    else:
                        continue
            line_values_sorted_array.append({str(a_points[1]): line_in_values_sorted})
            line_index.append(a_points[1])
        else:
            continue

    sorted_index = sorted(line_index)
    for t_index in sorted_index:
        for t_v in line_values_sorted_array:
            t_v_index = list(t_v.keys())[0]
            if t_v_index == str(t_index):
                texts_blocks_sorted.append(list(t_v.values())[0])
                line_values_sorted_array.remove(t_v)
            else:
                continue

    return texts_blocks_sorted


def is_contain_by_iou(text, cell, ratio=0.5):
    width1 = abs(text[2] - text[0])
    height1 = abs(text[1] - text[3])
    width2 = abs(cell[2] - cell[0])
    height2 = abs(cell[1] - cell[3])
    x_max = max(text[0], text[2], cell[0], cell[2])
    y_max = max(text[1], text[3], cell[1], cell[3])
    x_min = min(text[0], text[2], cell[0], cell[2])
    y_min = min(text[1], text[3], cell[1], cell[3])
    iou_width = x_min + width1 + width2 - x_max
    iou_height = y_min + height1 + height2 - y_max
    if iou_width <= 0 or iou_height <= 0:
        return False
    else:
        iou_area = iou_width * iou_height  # 交集的面积
        box1_area = width1 * height1
        iou_ratio_new = iou_area / box1_area
        if iou_ratio_new > ratio:
            return True
        else:
            return False
