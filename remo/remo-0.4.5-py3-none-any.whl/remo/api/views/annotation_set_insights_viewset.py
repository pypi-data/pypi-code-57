import base64
import binascii
import itertools
import zlib

from django.db.models import (
    F, Count, Case, When, FloatField, CharField, Value,
    Q)
from django.db.models.functions import Cast
from rest_framework import mixins
from rest_framework.exceptions import ParseError

from remo_app.remo.models import AnnotationSet, Tag, Class
from remo_app.remo.api.serializers import AnnotationSetInsightsSerializer
from remo_app.remo.api.viewsets import BaseNestedModelViewSet


class AnnotationSetInsightsViewSet(mixins.ListModelMixin,
                                   BaseNestedModelViewSet):
    parent_lookup = 'annotation_set'
    ordering_fields = ('name', 'total_annotation_objects', 'total_images', 'objects_per_image')
    serializer_class = AnnotationSetInsightsSerializer

    def get_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def get_queryset(self):
        annotation_set = self.get_parent_object_or_404()

        # TODO: restrict to team when it will be implemented, #272
        qs = {
            'class': Class.objects.filter(
                # We also need classes with objects/images == 0
                annotation_sets__in=[annotation_set]
            ).annotate(
                # TODO: use Count(...,filter=Q(...)) parameter when
                #  django will get upgraded to >=2.0
                # Count of annotation objects whose annotation belongs to given annotation set
                total_annotation_objects=Count(Case(When(
                    annotationobject__annotation__annotation_set=annotation_set,
                    then=1
                ))),
                # Count of annotations belongs to given annotation set
                total_images=Count(Case(When(
                    annotationobject__annotation__annotation_set=annotation_set,
                    then='annotationobject__annotation'
                ))) + Count(Case(When(
                    annotations__annotation_set=annotation_set,
                    then='annotations'
                )))
            ).annotate(
                # objects/images ratio. Also avoiding 'division by zero'
                objects_per_image=Case(
                    When(total_images=0, then=0),
                    default=F('total_annotation_objects') / F('total_images'),
                    output_field=FloatField()
                ),
                record_type=Value('class', output_field=CharField())
            ).values(
                'name', 'total_annotation_objects', 'total_images', 'objects_per_image',
                'record_type'
            ),
            # Tag name have to be unique in response
            'tag': Tag.objects.filter(
                image__annotations__annotation_set=annotation_set
            ).values('name').annotate(
                total_images=Count('name'),
                total_annotation_objects=Count('image__annotations__annotation_objects')
            ).annotate(
                # 'total_images' can't be 0 cause Tag.image is mandatory
                objects_per_image=Cast(
                    F('total_annotation_objects'), FloatField()
                ) / Cast(
                    F('total_images'), FloatField()
                ),
                record_type=Value('tag', output_field=CharField())
            )
        }

        # ('query parameter name', 'qs name')
        # query params with name started from 'z_' are come compresssed
        filters = (
            ('tags_in', 'tag'),
            ('tags_not_in', 'tag'),
            ('z_tags_in', 'tag'),
            ('z_tags_not_in', 'tag'),
            ('classes_in', 'class'),
            ('classes_not_in', 'class'),
            ('z_classes_in', 'class'),
            ('z_classes_not_in', 'class')
        )

        # Apply fields filters
        # Filter only if such parameter is present or leave it as is otherwise
        for param, qs_name in filters:
            query = self.request.query_params.get(param)
            if query is None:
                continue

            # Compressed query params
            if param.startswith('z_'):
                try:
                    query = self.uncompress_filter(query)
                except (zlib.error, binascii.Error):
                    raise ParseError()

            splitted = query.split(',')
            if param.endswith('not_in'):
                qs[qs_name] = qs[qs_name].exclude(name__in=splitted)
            else:
                qs[qs_name] = qs[qs_name].filter(name__in=splitted)

        # Filter out by record_type, if filter is present
        record_type = self.request.query_params.get('record_type')
        if record_type:
            qs = {record_type: qs[record_type]}

        data = itertools.chain.from_iterable(qs.all() for qs in qs.values())

        return list(self.order_records(data, self.request.query_params.get('ordering')))

    def order_records(self, records, param):
        """
        Apply ordering to a given records
        :param records:
        :param param: 'ordering' parameter value
        :return:
        """
        if not isinstance(param, str):
            return sorted(records, key=lambda x: x['name'], reverse=False)

        desc = param.startswith('-')
        field = param[1:] if desc else param
        if field not in self.ordering_fields:
            return records

        return sorted(records, key=lambda x: x[field], reverse=desc)

    def uncompress_filter(self, compressed_data: str) -> str:
        """
        Extract filter string from compressed query
        :param compressed_data:
        :return: uncompressed string
        """
        decoded = base64.standard_b64decode(compressed_data)
        uncompressed = zlib.decompress(decoded)  # type: bytes
        return uncompressed.decode()
