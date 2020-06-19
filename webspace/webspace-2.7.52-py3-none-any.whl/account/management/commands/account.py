from django.core.management.base import BaseCommand
from ...utils import get_test_account


class Command(BaseCommand):
    help = 'Account commands : test'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)
        parser.add_argument('extra', type=str, nargs='?', default='')

    def handle(self, *args, **options):
        eval('self.' + options['action'] + '(' + options['extra'] + ')')
        get_test_account()
