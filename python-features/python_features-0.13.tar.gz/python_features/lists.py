def top(ls):
    try:
        return ls[-1]
    except IndexError:
        return None


def last(ls, i):
    try:
        return ls[i-1] if len(ls) > 1 else None
    except IndexError:
        return None
