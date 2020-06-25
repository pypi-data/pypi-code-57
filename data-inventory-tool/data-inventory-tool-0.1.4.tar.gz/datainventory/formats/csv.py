import csv

from datainventory.core import Column


def write(f, rows):
    writer = csv.DictWriter(f, list(c.name for c in Column))
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
