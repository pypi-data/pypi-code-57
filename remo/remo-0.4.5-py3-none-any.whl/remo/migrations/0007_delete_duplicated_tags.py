import django
from django.db import migrations

from remo_app.remo.use_cases.annotation import update_new_annotation


def delete_duplicated_tags(apps, schema_editor):
    tag_model = apps.get_model('remo', 'Tag')
    tags = {}
    for tag in tag_model.objects.all():
        name = tag.name.lower()
        ids = tags.get(name, [])
        ids.append(tag.id)
        tags[name] = ids

    # check for duplicates
    change_id = {}
    ids_to_be_deleted = []
    for ids in tags.values():
        if len(ids) > 1:
            id = ids[0]
            ids = ids[1:]
            change_id[id] = ids
            ids_to_be_deleted.extend(ids)

    # update tag ids
    annotation_tag_model = apps.get_model('remo', 'AnnotationTags')
    annotation_tags_to_delete = []
    for id, changes in change_id.items():
        for old in changes:
            for annotation_tag in annotation_tag_model.objects.filter(tag_id=old).all():
                # ('annotation', 'tag') should be unique
                if annotation_tag_model.objects.filter(annotation=annotation_tag.annotation, tag_id=id).exists():
                    annotation_tags_to_delete.append(annotation_tag.id)
                else:
                    annotation_tag.tag_id = id
                    annotation_tag.save()

    for id in annotation_tags_to_delete:
        annotation_tag = annotation_tag_model.objects.filter(id=id)
        annotation_tag.delete()

    # delete duplicates
    for id in ids_to_be_deleted:
        tag = tag_model.objects.get(id=id)
        tag.delete()

    # rename tags
    for tag in tag_model.objects.all():
        tag.name = tag.name.lower()
        tag.save()

    # update tags in new annotations
    annotation_model = apps.get_model('remo', 'Annotation')
    for annotation in annotation_model.objects.all():
        update_new_annotation(annotation)


class Migration(migrations.Migration):

    dependencies = [
        ('remo', '0006_auto_20200501_1444'),
    ]

    operations = [
        migrations.RunPython(delete_duplicated_tags),
    ]
