# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import MapStoreResource

import re
import base64
import logging

logger = logging.getLogger(__name__)


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    id = serializers.ReadOnlyField()

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        try:
            return value.blob
        # try:
        #     return json.loads(value)
        except Exception:
            return value


class JSONArraySerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    id = serializers.ReadOnlyField()

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        if value:
            attributes = []
            for _a in list(value.all()):
                data = ''
                if re.match(r'b\'(.*)\'', _a.value):
                    data = re.match(r'b\'(.*)\'', _a.value).groups()[0]
                attributes.append({
                    "name": _a.name,
                    "type": _a.type,
                    "label": _a.label,
                    "value": base64.b64decode(data).decode('utf8')
                })
        else:
            attributes = []
        return attributes


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'username', 'email', 'is_staff')


class MapStoreResourceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source='user.username',
                                 read_only=True)

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(MapStoreResourceSerializer, self).__init__(*args, **kwargs)

        _full = self.context['request'].query_params.get('full')
        if _full:
            self.fields['data'] = JSONSerializerField(read_only=False)
            self.fields['attributes'] = JSONArraySerializerField(read_only=False)

    class Meta:
        model = MapStoreResource
        fields = ('id', 'user', 'name', 'creation_date', 'last_update')
