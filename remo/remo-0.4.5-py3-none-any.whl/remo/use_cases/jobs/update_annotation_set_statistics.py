import logging

from django.db import connection

from remo_app.remo.models import AnnotationSetStatistics, AnnotationSet, Class
from remo_app.remo.api.constants import TaskType
from remo_app.remo.use_cases.images import count_skipped_images

logger = logging.getLogger('remo_app')


def update_all_annotation_sets_statistics():
    logger.info('Running scheduled job: update_annotation_set_statistics')

    for annotation_set in AnnotationSet.objects.raw('SELECT id FROM annotation_sets'):
        update_annotation_set_statistics(annotation_set)


def update_annotation_set_statistics(annotation_set: AnnotationSet) -> AnnotationSetStatistics:
    stats = get_or_create_annotation_set_statistics(annotation_set)

    if annotation_set.task.type == TaskType.image_classification.name:
        classes, top3_classes = collect_classes_statistics_for_image_classification(annotation_set.id)
    else:
        classes, top3_classes = collect_classes_statistics(annotation_set.id)
        stats.total_annotation_objects = count_total_annotation_objects(annotation_set.id)

    stats.top3_classes = top3_classes
    stats.classes = classes
    stats.total_classes = count_total_classes(annotation_set.id)
    stats.tags = count_tags(annotation_set.id)
    stats.total_annotated_images = count_total_annotated_images(annotation_set.id)
    stats.skipped_images = count_skipped_images(annotation_set.id)
    stats.save()
    return stats


def count_tags(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT tags.name, tags_count.count
        FROM (SELECT tag_id, COUNT(image_id) AS count
            FROM annotation_tags
            WHERE annotation_set_id = %s
            GROUP BY tag_id) AS tags_count
        JOIN tags ON tags_count.tag_id = tags.id
        """, [annotation_set_id])
        all_tags = cursor.fetchall()
    return all_tags


def count_total_annotated_images(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT COUNT(*) FROM annotations WHERE annotation_set_id = %s AND status = 1
        """, [annotation_set_id])
        count = cursor.fetchone()[0]
    return count


def count_total_annotation_objects(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT COUNT(obj.id) FROM annotation_objects obj
        JOIN annotations ann ON obj.annotation_id = ann.id
        WHERE ann.annotation_set_id = %s
        """, [annotation_set_id])
        count = cursor.fetchone()[0]
    return count


def count_class_n_objects_for_annotation_set(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT COUNT(class.id), class.name
        FROM classes class
             JOIN annotation_object_classes obj_class ON class.id = obj_class.annotation_class_id
             JOIN annotation_objects an_obj ON obj_class.annotation_object_id = an_obj.id
             JOIN annotations an ON an_obj.annotation_id = an.id
        WHERE an.annotation_set_id = %s
        GROUP BY class.id
        ORDER BY COUNT(class.id) DESC
        """, [annotation_set_id])
        all_classes = cursor.fetchall()
    return all_classes


def merge_class_statistics(filed_name, all_classes, classes):
    for count, class_name in all_classes:
        class_stat = classes.get(class_name, {})
        class_stat[filed_name] = count
        classes[class_name] = class_stat
    return classes


def count_class_n_images_for_annotation_set(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT class_counts.count, class.name
        FROM (SELECT COUNT(image_classes.annotation_class_id) AS count, image_classes.annotation_class_id
              FROM (SELECT obj_class.annotation_class_id
                    FROM annotations an
                         JOIN annotation_objects an_obj ON an.id = an_obj.annotation_id
                         JOIN annotation_object_classes obj_class ON an_obj.id = obj_class.annotation_object_id
                    WHERE an.annotation_set_id = %s
                    GROUP BY obj_class.annotation_class_id, an.image_id
                   ) AS image_classes
              GROUP BY image_classes.annotation_class_id
              ORDER BY COUNT(image_classes.annotation_class_id) DESC) AS class_counts
              JOIN classes class on class_counts.annotation_class_id = class.id
        """, [annotation_set_id])
        all_classes = cursor.fetchall()
    return all_classes


def collect_classes_statistics(annotation_set_id):
    classes = {}
    all_classes = count_class_n_objects_for_annotation_set(annotation_set_id)
    top3_classes = all_classes[:3]
    classes = merge_class_statistics('n_objs', all_classes, classes)

    all_classes = count_class_n_images_for_annotation_set(annotation_set_id)
    classes = merge_class_statistics('n_imgs', all_classes, classes)

    return classes, top3_classes


def count_total_classes(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT COUNT(id) FROM annotation_sets_classes WHERE annotationset_id = %s
        """, [annotation_set_id])
        count = cursor.fetchone()[0]
    return count


def count_class_n_images_for_image_classification_annotation_set(annotation_set_id):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT COUNT(class.id), class.name
        FROM classes class
             JOIN annotation_classes an_class ON class.id = an_class.annotation_class_id
             JOIN annotations an ON an_class.annotation_id = an.id
        WHERE an.annotation_set_id = %s
        GROUP BY class.id
        ORDER BY COUNT(class.id) DESC
        """, [annotation_set_id])
        all_classes = cursor.fetchall()
    return all_classes


def collect_classes_statistics_for_image_classification(annotation_set_id):
    classes = {}
    all_classes = count_class_n_images_for_image_classification_annotation_set(annotation_set_id)
    top3_classes = all_classes[:3]
    classes = merge_class_statistics('n_imgs', all_classes, classes)
    return classes, top3_classes


def get_or_create_annotation_set_statistics(annotation_set):
    stats = AnnotationSetStatistics.objects.filter(annotation_set=annotation_set).first()
    if stats:
        if stats.dataset is None:
            stats.dataset = annotation_set.dataset
        return stats

    stats = AnnotationSetStatistics()
    stats.annotation_set = annotation_set
    stats.dataset = annotation_set.dataset
    stats.save()
    return stats
