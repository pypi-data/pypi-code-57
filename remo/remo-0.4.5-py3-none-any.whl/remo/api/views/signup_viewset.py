import json
import re

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import AllowAny

from remo_app.remo.api.serializers import UserSignupSerializer


class SignupViewSet(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        origin = request.headers.get('Origin', '')
        if not re.match('^https://.*remo.ai$', origin):
            return Response()

        data = json.loads(request.body)
        serializer = UserSignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED, headers={'Access-Control-Allow-Origin': origin})
