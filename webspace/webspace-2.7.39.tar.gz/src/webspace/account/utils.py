from .models import User
from django.contrib.auth.models import Group


def get_test_account():
    user, created = User.objects.get_or_create(
        username='test',
        first_name='Elon',
        last_name='Musk',
        email='test@test.test',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    if created:
        user.save()
        user.set_password('password')
        for group in Group.objects.all():
            user.groups.add(group)
        user.save()
    return user
