import factory
from rest_framework.authtoken.models import Token

from .models import User


class RegistrationFactory(factory.DictFactory):
    email = factory.Faker('email')
    password = 'z57^6EhdqMw&'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class UserFactory(factory.DjangoModelFactory, RegistrationFactory):
    class Meta:
        model = User

    is_superuser = False
    is_staff = False
    is_active = True

    @factory.post_generation
    def generate_auth_token(self, create, extracted, **kwargs):
        if create is True:
            Token.objects.get_or_create(user=self)


class StaffUserFactory(UserFactory):
    is_staff = True
    is_active = True


class AdminUserFactory(UserFactory):
    email = factory.Sequence(lambda n: 'admin{0}@example.com'.format(n))
    is_superuser = True
    is_staff = True
