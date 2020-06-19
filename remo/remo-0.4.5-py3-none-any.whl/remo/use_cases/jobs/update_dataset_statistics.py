import json
import logging

from django.db.models import Sum
from django.db import connection

from remo_app.remo.models import Dataset, DatasetStatistics

logger = logging.getLogger('remo_app')


def update_dataset_statistics(dataset: Dataset):
    dataset.quantity = dataset.images.count()
    dataset.size_in_bytes = dataset.images.aggregate(size=Sum('size'))['size'] or 0
    dataset.save()

    stats = get_or_create_dataset_statistics(dataset)
    top3_classes = get_top3_classes(dataset.id)
    total_classes = get_total_classes(dataset.id)
    stats.statistics = {'top3_classes': top3_classes, 'total_classes': total_classes}
    stats.save()


def update_all_datasets_statistics():
    logger.info('Running scheduled job: update_all_datasets_statistics')

    for dataset in Dataset.objects.all():
        update_dataset_statistics(dataset)


def get_or_create_dataset_statistics(dataset):
    stats = DatasetStatistics.objects.filter(dataset=dataset).first()
    if stats:
        return stats

    stats = DatasetStatistics()
    stats.dataset = dataset
    stats.save()
    return stats


def get_top3_classes(dataset_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT top3_classes FROM annotation_set_statistics WHERE dataset_id = %s
        """, [dataset_id])
        top3_classes = cursor.fetchall()

    classes = {}
    for row in top3_classes:
        if isinstance(row, tuple):
            row = row[0]
        if row is None:
            continue
        if isinstance(row, str):
            row = json.loads(row)

        for count, name in row:
            classes[name] = max(count, classes.get(name, 0))

    return [
        {'name': cls[0], 'count': cls[1]}
        for cls in sorted(classes.items(), reverse=True, key=lambda x: x[1])[:3]
    ]


def get_total_classes(dataset_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT classes FROM annotation_set_statistics WHERE dataset_id = %s
        """, [dataset_id])
        classes = cursor.fetchall()

    unique_classes = set()
    for row in classes:
        if type(row) == tuple:
            row = row[0]
        if type(row) == str:
            row = json.loads(row)
        for name in row.keys():
            unique_classes.add(name)

    return len(unique_classes)
