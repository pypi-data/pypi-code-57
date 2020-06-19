import csv
import io
import json
from typing import List

from remo_app.remo.models import AnnotationSet, NewAnnotation


class JSON:
    @staticmethod
    def buffer(obj):
        output = io.StringIO()
        json.dump(obj, output, indent=2, separators=(',', ': '), sort_keys=True)
        return output.getvalue()


class CSV:
    @staticmethod
    def buffer(headers: List[str], rows: List[List[str]]):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()


def export_tags_for_annotation_set(annotation_set: AnnotationSet):
    headers = ['file_name', 'tag']
    rows = []
    for obj in NewAnnotation.objects.filter(annotation_set=annotation_set).all():
        if not obj.tags:
            continue
        img, tags = obj.image, obj.tags
        rows.extend(map(lambda tag: [img.original_name, tag], tags))

    return CSV.buffer(headers, rows)

