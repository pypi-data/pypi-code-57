from django.core.management.base import BaseCommand
from ...models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Account commands : test'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)
        parser.add_argument('extra', type=str, nargs='?', default='')

    def handle(self, *args, **options):
        eval('self.' + options['action'] + '(' + options['extra'] + ')')

    def test(self):
        user = User.objects.create(
            username='test',
            first_name='Firstname',
            last_name='Lastname',
            email='test@test.test',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.save()
        user.set_password('password')
        for group in Group.objects.all():
            user.groups.add(group)
        user.save()
