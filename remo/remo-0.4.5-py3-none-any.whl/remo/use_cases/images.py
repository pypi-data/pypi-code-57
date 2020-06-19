from django.db import connection


def count_skipped_images(annotation_set_id):
    return count_annotated_images(annotation_set_id, status=0)


def count_annotated_images(annotation_set_id, status=1):
    """
    Counts annotated images
    :param annotation_set_id:
    :param status: 0 - skipped, 1 - annotated
    :return: count
    """
    query = """
            SELECT COUNT("new_annotations"."id") as count
            FROM "new_annotations"
            WHERE ("new_annotations"."annotation_set_id" = {annotation_set_id}
                    AND "new_annotations"."status" = {status})
            """.format(
        annotation_set_id=annotation_set_id,
        status=status
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return count
