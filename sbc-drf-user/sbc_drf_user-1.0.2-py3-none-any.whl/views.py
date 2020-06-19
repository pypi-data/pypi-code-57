import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer

L = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    filter_fields = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email',)
    ordering_fields = ('id', 'first_name', 'email')
    ordering = '-id'

    @action(detail=True, methods=['PUT'])
    def action_change_password(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request, 'user': user}
        )
        serializer.is_valid(True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'PUT'])
@permission_classes((AllowAny,))
def password_reset(request, *args, **kwargs):
    if request.method == 'POST':
        User.objects.generate_password_reset_key(request.data.get('email'))
    else:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
