def flatten(iterable):
    for item in iterable:
        if hasattr(item, '__iter__'):
            yield from flatten(item)
        else:
            yield item


def fold_like(flat, example):
    folded = []
    for item in example:
        if hasattr(item, '__iter__'):
            n = len(list(flatten(item)))
            folded.append(fold_like(flat[:n], item))
            flat = flat[n:]
        else:
            folded.append(flat[0])
            flat = flat[1:]
    return tuple(folded)
