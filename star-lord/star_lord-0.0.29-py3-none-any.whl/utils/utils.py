# Django
from django.db.models import ManyToManyField
from django.db import connection
from django.apps import apps

# Project
from ..amqp.job import JobClient


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_new_fields(model):
    table_name = model._meta.db_table
    current_fields = [i.name for i in model._meta.fields]

    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name "
                       "FROM INFORMATION_SCHEMA.COLUMNS "
                       "WHERE TABLE_NAME = %s", [table_name])
        db_fields = [i['column_name'] for i in dictfetchall(cursor)]

    return set(current_fields) - set(db_fields)


def pick(keys, dict_data):
    return {key: dict_data[key] for key in keys if dict_data.get(key)}


def get_changed_models():
    models = apps.get_models()
    models = [model for model in models if hasattr(model, 'main_service_name')]
    models = [
        model for model in models
        if get_new_fields(model) and 'id' not in get_new_fields(model)
    ]
    return models


def refresh_models(models):
    [JobClient().call(model.main_service_name) for model in models]


def model_sync(data, model):
    fields = [field.get_attname() for field in model._meta.fields]
    m2m_fields = [
        field.get_attname() for field in model._meta.get_fields()
        if field.__class__ is ManyToManyField
    ]

    for item in data:
        defaults = pick(fields, item)

        model.objects.update_or_create(id=item['id'], defaults=defaults)
        if m2m_fields:
            instance = model.objects.get(id=item['id'])

            for field in m2m_fields:
                getattr(instance, field).set(item[field])
