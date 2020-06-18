from datetime import datetime
from django.core.management.base import BaseCommand
from wagtail.core.models import Page


class Command(BaseCommand):
    help = 'Page commands : update'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)
        parser.add_argument('extra', type=str, nargs='?', default='')

    def handle(self, *args, **options):
        eval('self.' + options['action'] + '(' + options['extra'] + ')')

    def update(self):
        for page in Page.objects.all():
            page.last_published_at = datetime.now()
            page.save()
