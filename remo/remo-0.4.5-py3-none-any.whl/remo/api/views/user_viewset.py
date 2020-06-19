from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from remo_app.remo.api.serializers import UserInfoSerializer


class UserViewSet(GenericAPIView):
    serializer_class = UserInfoSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)
