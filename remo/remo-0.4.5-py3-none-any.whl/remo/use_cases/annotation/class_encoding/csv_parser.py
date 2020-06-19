import csv
import os

from .class_encoding import CustomClassEncoding


def parse_csv_class_encoding(path: str) -> CustomClassEncoding:
    _, ext = os.path.splitext(path)
    if ext != '.csv':
        return None

    with open(path, 'r') as f:
        return parse_csv_class_encoding_file(f)


def parse_csv_class_encoding_file(file):
    classes = {}
    csv_file = csv.reader(file, delimiter=',')
    for row in csv_file:
        if len(row) >= 2:
            label = str(row[0]).strip()
            class_name = str(row[1]).strip()
            classes[label] = class_name
    return CustomClassEncoding(classes)


def parse_raw_csv_class_encoding(rows):
    classes = {}
    for row in rows:
        row = row.split(',')
        if len(row) >= 2:
            label = str(row[0]).strip()
            class_name = str(row[1]).strip()
            classes[label] = class_name
    return CustomClassEncoding(classes)
