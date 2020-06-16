import functools

def indent(val, amount=2):
    if not val:
        return val
    space = " "*amount
    return val.strip().replace("\n", "\n"+space)

def tabulate(heading, rows, display_transforms=None, totals=None, sortby=None):
    total_row = []
    if totals:
        for i, aggregate in enumerate(totals):
            if not aggregate:
                total_row.append('')
                continue

            total_row.append(aggregate(r[i] for r in rows))

    if 'key' in sortby:
        sortby = [sortby]
    for term in sortby:
        rows.sort(key=term['key'], reverse=term.get('reverse', False))

    text_totals = transform_row(total_row, display_transforms)
    text_rows = [transform_row(r, display_transforms) for r in rows]
    col_sizes = autosize([heading]+text_rows+[text_totals])
    print_row(heading, col_sizes)
    print_spacer(col_sizes)
    for r in text_rows:
        print_row(r, col_sizes)

    if totals:
        print_spacer(col_sizes)
        print_row(text_totals, col_sizes)

def transform_row(row, transforms):
    text_row = []
    for i, col in enumerate(row):
        transform = (transforms[i] if transforms else None) or str
        text_row.append(transform(col))

    return text_row

def print_row(row, col_sizes):
    for i, col in enumerate(row):
        print(col.ljust(col_sizes[i]), end="")
    print("")

def print_spacer(col_sizes):
    spacer = []
    for c in col_sizes:
        spacer.append("-"*(c-1))
    print_row(spacer, col_sizes)

def autosize(rows):
    sizes = []
    for r in rows:
        col_count = len(r) - len(sizes)
        if col_count > 0:
            sizes.extend([0]*col_count)

        for i, col in enumerate(r):
            col = str(col)
            if len(col) >= sizes[i]:
                sizes[i] = len(col)+1

    return sizes

def humanize_size(size):
    if not size:
        return ''

    size_format = '{:.2f} {}'
    for unit in ['B', 'KiB', 'MiB']:
        if size < 1024:
            return size_format.format(size, unit)

        size = size / 1024

    return size_format.format(size, "GiB")

def humanize_datetime(datetime):
    if not datetime:
        return ''

    return datetime.date().isoformat() + " " + datetime.strftime('%X')

def memoize(key=None):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def cacheable(*args):
            # reduce arguments using cache key callable
            cache_args = key(args) if key else args

            cache_key = '|'.join([str(a) for a in cache_args])
            if cache_key in cache:
                return cache[cache_key]

            result = func(*args)
            cache[cache_key] = result
            return result

        return cacheable

    return decorator
