from django.core.management.base import BaseCommand, CommandError
from wagtail.core.models import Page
from wagtailstatic.local_files import (
    clean_unused_dirs, create_static_file, destroy_all_static_files)


class Command(BaseCommand):
    def handle(self, *args, **options):
        destroy_all_static_files()
        for page in Page.objects.all().specific():
            if getattr(page, 'is_static', False):
                self.stdout.write(f'Creating staticfile for: {page.title}')
                create_static_file(page)
        clean_unused_dirs()
