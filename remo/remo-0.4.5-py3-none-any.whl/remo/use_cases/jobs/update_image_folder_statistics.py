import logging

from django.db.models import Count

from remo_app.remo.models import Class, ImageFolder, ImageFolderStatistics, Image, DatasetImage

logger = logging.getLogger('remo_app')


def delete_orphan_images():
    logger.info('Running scheduled job: delete_orphan_images')

    for obj in Image.objects.all():
        exists = DatasetImage.objects.filter(image_object=obj).first()
        if not exists:
            obj.delete()


def update_image_folder_statistics():
    logger.info('Running scheduled job: update_image_folder_statistics')

    for image_folder in ImageFolder.objects.all():
        stats = get_or_create_image_folder_statistics(image_folder)
        top3_classes = get_top3_classes(image_folder)
        total_classes = get_total_classes(image_folder)
        stats.statistics = {'top3_classes': top3_classes, 'total_classes': total_classes}
        stats.save()


def get_or_create_image_folder_statistics(image_folder):
    stats = ImageFolderStatistics.objects.filter(image_folder=image_folder).first()
    if stats:
        return stats

    stats = ImageFolderStatistics()
    stats.image_folder = image_folder
    stats.save()
    return stats


def get_top3_classes(instance):
    # We are using UNION here
    # Django generates OUTER JOINs if we simply use filter and
    # annotate in single query. In this case some records miss
    # if some class assignes to a dataset which participate in two
    # annotation sets belong to different task types

    qs1 = Class.objects.filter(
        annotations__image__folder=instance
    ).values('id', 'name').annotate(count=Count('name'))
    qs2 = Class.objects.filter(
        annotationobject__annotation__image__folder=instance
    ).values('id', 'name').annotate(count=Count('name'))
    qs = qs1.union(qs2, all=True)

    classes = {}
    for i in qs.all():
        count = classes.get(i['name'], 0)
        classes[i['name']] = i['count'] + count

    return [
        {'name': cls[0], 'count': cls[1]}
        for cls in sorted(classes.items(), reverse=True, key=lambda x: x[1])[:3]
    ]


def get_total_classes(instance):
    qs1 = Class.objects.filter(
        annotations__image__folder=instance
    )
    qs2 = Class.objects.filter(
        annotationobject__annotation__image__folder=instance
    )
    qs = qs1 | qs2

    return qs.distinct().count()
