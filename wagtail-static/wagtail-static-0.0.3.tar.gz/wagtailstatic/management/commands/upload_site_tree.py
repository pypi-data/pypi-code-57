from django.core.management.base import BaseCommand, CommandError

from wagtail.core.models import Page, Site
from wagtailstatic.s3 import upload_site_tree


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('site_name', type=str)

    def handle(self, *args, **options):
        try:
            site = Site.objects.get(site_name=options['site_name'])
            upload_site_tree(site)
        except Site.DoesNotExist():
            site_names = '\n'.join([s.site_name for s in Site.objects.all()])
            raise CommandError(f'Site not found with that name, options are: {site_names}')
        
        
        