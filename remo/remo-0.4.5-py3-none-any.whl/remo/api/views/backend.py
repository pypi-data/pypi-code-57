from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email')
        try:
            user = UserModel._default_manager.get(email=email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
