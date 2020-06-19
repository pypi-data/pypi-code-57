from datetime import datetime

from remo_app.remo.api.constants import TaskType, AnnotationStatus, AnnotationSetType
from .db import conn, is_sqlite_db
from peewee import Model, AutoField, ForeignKeyField, CharField, IntegerField, BigIntegerField, BooleanField, \
    DateTimeField, \
    TextField, ManyToManyField

if is_sqlite_db():
    from playhouse.sqlite_ext import JSONField
else:
    from playhouse.postgres_ext import JSONField


class BaseModel(Model):
    class Meta:
        database = conn


class License(BaseModel):
    class Meta:
        table_name = 'licenses'

    id = AutoField()
    name = CharField(max_length=50)
    description = TextField(null=True)


class Image(BaseModel):
    class Meta:
        table_name = 'images'

    id = AutoField()
    image = CharField(max_length=1000, null=True)
    local_image = CharField(max_length=1000, null=True)
    thumbnail = CharField(max_length=1000, null=True)
    view = CharField(max_length=1000, null=True)
    preview = CharField(max_length=1000, null=True)
    size = BigIntegerField(default=0)  # File size in bytes
    width = IntegerField(default=0)
    height = IntegerField(default=0)


class Dataset(BaseModel):
    class Meta:
        table_name = 'datasets'

    id = AutoField()
    name = CharField(max_length=255)
    is_archived = BooleanField(default=False)
    # user = ForeignKeyField(settings.AUTH_USER_MODEL, null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    license = ForeignKeyField(License, null=True)
    is_public = BooleanField(default=False)
    # users_shared = ManyToManyField(settings.AUTH_USER_MODEL, backref='users_shared')
    # images = models.ManyToManyField(Image, through='DatasetImage', backref='datasets')
    size_in_bytes = BigIntegerField(default=0)
    quantity = BigIntegerField(default=0)


class DatasetImage(BaseModel):
    class Meta:
        table_name = 'dataset_images'

    id = AutoField()
    dataset = ForeignKeyField(Dataset, backref='dataset_images', on_delete='CASCADE')
    image_object = ForeignKeyField(Image, on_delete='CASCADE')
    number_in_dataset = IntegerField(default=0)
    original_name = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.now)

    # folder = models.ForeignKey(
    #     'ImageFolder',
    #     on_delete=models.CASCADE,
    #     backref='contents',
    #     null=True
    # )


class AnnotationSet(BaseModel):
    class Meta:
        table_name = 'annotation_sets'

    id = AutoField()
    name = CharField(max_length=255)
    updated_at = DateTimeField(default=datetime.now)
    released_at = DateTimeField(null=True)
    last_annotated_date = DateTimeField(null=True)
    type = CharField(max_length=20, choices=AnnotationSetType.choices())
    # task = ForeignKeyField(Task, null=True, backref='annotation_sets')
    # user = ForeignKeyField(settings.AUTH_USER_MODEL, null=True, backref='annotation_sets')
    dataset = ForeignKeyField(Dataset, backref='annotation_sets')

    # classes = ManyToManyField(Class, backref='annotation_sets')


class NewAnnotation(BaseModel):
    id = AutoField()
    dataset = ForeignKeyField(Dataset, backref='new_annotations')
    image = ForeignKeyField(DatasetImage, backref='new_annotations')
    annotation_set = ForeignKeyField(AnnotationSet, backref='new_annotations')
    classes = JSONField(null=True)
    tags = JSONField(null=True)
    task = CharField(max_length=255, choices=TaskType.choices())
    data = JSONField(null=True)
    status = IntegerField(choices=AnnotationStatus.choices(), default=AnnotationStatus.not_annotated.value)

    class Meta:
        indexes = (
            (('image', 'annotation_set'), True),
        )
        table_name = 'new_annotations'


class pewee_Table(BaseModel):
    id = AutoField()
    name = CharField()
    license_id = IntegerField()


class pewee_AnnotationStats(BaseModel):
    id = AutoField()
    annotation_set_id = IntegerField()
    classes = CharField()
    tags = CharField()
    top3_classes = CharField()
    total_classes = IntegerField()
    total_annotated_images = IntegerField()
    total_annotation_objects = IntegerField()
    dataset_id = IntegerField()


class pewee_AnnotationSets(BaseModel):
    id = AutoField()
    name = CharField()
    dataset_id = IntegerField()
    task_id = IntegerField()
    user_id = IntegerField()
    ann_stats = ForeignKeyField(AnnotationStats)


class pewee_Annotation(BaseModel):
    id = AutoField()
    # MC: Some of them are actually binary json but
    # BinaryJSONField() is not recognized in the package
    classes = CharField()
    tags = CharField()
    task = CharField()
    data = CharField()
    annotation_set_id = IntegerField()
    dataset_id = IntegerField()
    image_id = IntegerField()
    annotation_sets = ForeignKeyField(pewee_AnnotationSets)
