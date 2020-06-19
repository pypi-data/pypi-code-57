def assertEqual(actual, expected):
    if actual != expected:
        print('ERROR: got {}, expected {}'.format(actual, expected))


def filter_range(img_idx: int, limit: int, size: int):
    if img_idx is None:
        return size - limit, size

    half = int(limit / 2)
    left_exp = img_idx - half
    right_exp = img_idx + limit - half

    if left_exp < 0:
        rest = -left_exp
        left_exp = 0
        right_exp += rest
    elif right_exp > size:
        rest = right_exp - size
        right_exp = size
        left_exp -= rest

    if right_exp - left_exp < limit:
        print('additional')
        right_exp += 1

    return left_exp, right_exp


def test_filter_range():
    assertEqual(filter_range(None, 5, 9), (4, 9))
    assertEqual(filter_range(3, 5, 9), (1, 6))

    assertEqual(filter_range(1, 5, 9), (0, 5))
    assertEqual(filter_range(0, 10, 20), (0, 10))
    assertEqual(filter_range(None, 10, 20), (10, 20))

    assertEqual(filter_range(1, 6, 9), (0, 6))
    assertEqual(filter_range(1, 7, 9), (0, 7))
    assertEqual(filter_range(1, 8, 9), (0, 8))
    assertEqual(filter_range(4, 3, 9), (3, 6))

    assertEqual(filter_range(None, 3, 10), (7, 10))
    assertEqual(filter_range(0, 3, 10), (0, 3))
    assertEqual(filter_range(1, 3, 10), (0, 3))
    assertEqual(filter_range(2, 3, 10), (1, 4))
    assertEqual(filter_range(3, 3, 10), (2, 5))
    assertEqual(filter_range(4, 3, 10), (3, 6))
    assertEqual(filter_range(5, 3, 10), (4, 7))
    assertEqual(filter_range(6, 3, 10), (5, 8))
    assertEqual(filter_range(7, 3, 10), (6, 9))
    assertEqual(filter_range(8, 3, 10), (7, 10))
    assertEqual(filter_range(9, 3, 10), (7, 10))
    assertEqual(filter_range(10, 3, 10), (7, 10))

    assertEqual(filter_range(None, 6, 10), (4, 10))
    assertEqual(filter_range(0, 6, 10), (0, 6))
    assertEqual(filter_range(1, 6, 10), (0, 6))
    assertEqual(filter_range(2, 6, 10), (0, 6))
    assertEqual(filter_range(3, 6, 10), (0, 6))  # ?
    assertEqual(filter_range(4, 6, 10), (1, 7))
    assertEqual(filter_range(5, 6, 10), (2, 8))
    assertEqual(filter_range(6, 6, 10), (3, 9))
    assertEqual(filter_range(7, 6, 10), (4, 10))
    assertEqual(filter_range(8, 6, 10), (4, 10))
    assertEqual(filter_range(9, 6, 10), (4, 10))


if __name__ == '__main__':
    test_filter_range()
