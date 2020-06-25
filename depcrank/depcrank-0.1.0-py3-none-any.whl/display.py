"""
FIXME: insert program metadata
"""

import operator


def _sort_data(input_data):
    return sorted(input_data.items(), key=operator.itemgetter(1),
        reverse=True)


def find_top_ranks(input_data, ranks, exclude=None):
    # FIXME: give equal weight to same score
    if '-' in ranks:
        start, end = ranks.split('-')
    else:
        start = 0
        end = ranks

    if exclude:
        for package in exclude:
            if package in input_data:
                input_data.pop(package)

    sorted_data = _sort_data(input_data)

    result = []
    for i in range(int(start) - 1, int(end)):
        result.append((i + 1, sorted_data[i][0], sorted_data[i][1]))

    return result


def find_single_rank(input_data, package, exclude=None):
    # FIXME: give equal weight to same score
    if exclude:
        for package in exclude:
            if package in input_data:
                input_data.pop(package)

    sorted_data = _sort_data(input_data)

    for i in range(len(sorted_data)):
        if sorted_data[i][0] == package:
            return (i + 1, sorted_data[i][1])

    return None
