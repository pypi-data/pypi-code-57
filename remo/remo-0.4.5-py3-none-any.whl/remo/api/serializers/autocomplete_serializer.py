from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, SerializerMethodField

from remo_app.remo.models import Tag, Class, Task


class AutocompleteSerializer(Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"] = CharField()
        self.fields["type"] = SerializerMethodField()
        self.fields["filter"] = SerializerMethodField()

    @staticmethod
    def get_type(instance):
        type_map = {
            Tag: "tag",
            Class: "class",
            Task: "task"
        }

        return type_map.get(type(instance))

    @staticmethod
    def get_filter(instance):
        filter_map = {
            Tag: "tags",
            Class: "classes",
            Task: "tasks"
        }

        return filter_map.get(type(instance))


class AutocompleteQuerySerializer(Serializer):
    query = CharField(min_length=3)
