from typing import Any
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List

from datainventory.core import Column
from datainventory.core import Manifest
from datainventory.iterate import iterrows


def render(manifest: Manifest, cols: List[Column] = None) -> str:
    rows = iterrows(manifest)
    rows = asciirows(rows)
    cols = cols or list(Column)
    hs = 1 if Column.id in cols else 0  # hierarchical cols start
    he = cols.index(Column.property)    # hierarchical cols end
    hsize = 1                           # hierarchical column size
    bsize = 3                           # border size
    sizes = dict(
        [(c, len(c.name)) for c in cols[:hs]] +
        [(c, 1) for c in cols[hs:he]] +
        [(c, len(c.name)) for c in cols[he:]]
    )
    rows = list(rows)
    for row in rows:
        for i, col in enumerate(cols):
            val = '' if row[col] is None else str(row[col])
            if col == Column.id:
                sizes[col] = 2
            elif i < he:
                size = (hsize + bsize) * (he - hs - i) + sizes[Column.property]
                if size < len(val):
                    sizes[Column.property] += len(val) - size
            elif sizes[col] < len(val):
                sizes[col] = len(val)

    line = []
    for col in cols:
        size = sizes[col]
        line.append(col.name[:size].ljust(size))
    lines = [line]

    depth = 0
    for row in rows:
        if Column.id in cols:
            line = [row[Column.id][:2] if row[Column.id] else '  ']
        else:
            line = []

        for i, col in enumerate(cols[hs:he + 1]):
            val = row[col] or ''
            if val:
                depth = i
                break
        else:
            val = ''
            if Column.base in cols:
                if Column.id in cols:
                    depth = cols.index(Column.base) - 1
                else:
                    depth = cols.index(Column.base)
            elif depth < he - hs:
                depth += 1
            else:
                depth = 0

        line += [' ' * hsize] * depth
        size = (hsize + bsize) * (he - hs - depth) + sizes[Column.property]
        line += [val.ljust(size)]

        for col in cols[he + 1:]:
            val = '' if row[col] is None else str(row[col])
            size = sizes[col]
            line.append(val.ljust(size))

        lines.append(line)

    lines = [' | '.join(line) for line in lines]
    lines = [l.rstrip() for l in lines]
    return '\n'.join(lines)


def asciirows(rows: Iterable[Dict[Column, Any]]) -> Iterator[Dict[Column, Any]]:
    for row in rows:
        if Column.access in row and row[Column.access]:
            row[Column.access] = row[Column.access].name

        if Column.level in row and row[Column.level]:
            row[Column.level] = row[Column.level].value

        if Column.ref in row and isinstance(row[Column.ref], list):
            row[Column.ref] = ', '.join(row[Column.ref])

        yield row
