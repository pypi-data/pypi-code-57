from itertools import chain
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Iterable
from typing import Sequence
from typing import Set


def fetch_dicts(cursor) -> Iterable[Dict]:
    """
    Return an iterable over db-api cursor rows. Each row is returned as a
    dict.
    """
    keys = [item[0] for item in cursor.description]
    row: Sequence
    for row in iter(cursor.fetchone, None):
        yield dict(zip(keys, row))


def group_and_aggregate(items: Iterable[Dict[str, Any]], **groups: Sequence):
    """
    Aggregate and nest joined records in query results.

    Example:

        >>> import pprint
        >>> data = [
        ...     {'id': 1, 'name': 'fred', 'email': 'fred@example.org'},
        ...     {'id': 1, 'name': 'jim', 'email': 'jim@example.org'},
        ...     {'id': 2, 'name': 'sheila', 'email': 'sheila@example.org'},
        ... ]
        >>> pprint.pprint(list(group_and_aggregate(data, people=('email', 'name'))))
        [{'id': 1,
          'people': [{'email': 'fred@example.org', 'name': 'fred'},
                     {'email': 'jim@example.org', 'name': 'jim'}]},
          {'id': 2, 'people': [{'email': 'sheila@example.org', 'name': 'sheila'}]}]
    """

    DEFAULT = ""
    items = iter(items)
    peek = next(items, None)
    if peek is None:
        return
    group_items: List[Tuple[str, Set[str]]] = [
        (k, set(v)) for k, v in groups.items()
    ]
    allgroupkeys = {colname for k, v in group_items for colname in v}
    group_items = [
        (DEFAULT, {k for k in peek if k not in allgroupkeys})
    ] + group_items
    items = chain([peek], items)

    lastrow = None
    record: Dict[Any, Any] = {}
    row: Dict[Any, Any]
    for row in items:
        current = record
        is_new = False
        for groupname, groupkeys in group_items:
            group = {k: row[k] for k in groupkeys}
            is_new = (
                is_new
                or lastrow is None
                or any(lastrow[k] != v for k, v in group.items())
            )
            if is_new:
                if groupname is DEFAULT and record:
                    yield record[DEFAULT][0]
                    current = record = {}
                current.setdefault(groupname, []).append(group)
            current = current[groupname][-1]

        lastrow = row

    if record:
        yield record[DEFAULT][0]


if __name__ == "__main__":
    data = [
        {"id": 1, "name": "fred", "email": "fred@example.org"},
        {"id": 1, "name": "jim", "email": "jim@example.org"},
        {"id": 2, "name": "sheila", "email": "sheila@example.org"},
    ]
    import pprint

    pprint.pprint(list(group_and_aggregate(data, people=("email", "name"),)))
