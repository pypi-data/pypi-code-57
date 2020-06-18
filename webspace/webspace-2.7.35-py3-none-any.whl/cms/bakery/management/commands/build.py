# Env
import os
import sys
import six

# Files
import gzip
import mimetypes
from ... import DEFAULT_GZIP_CONTENT_TYPES

# Filesystem
from fs import path
from fs import copy
from django.utils.encoding import smart_text

# Pooling
import multiprocessing
from multiprocessing.pool import ThreadPool

# Django tricks
from django.apps import apps
from django.conf import settings
from django.urls import get_callable
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Bake out a site as flat files in the build directory'
    build_unconfig_msg = "Build directory unconfigured. Set BUILD_DIR in settings.py or provide it with --build-dir"
    views_unconfig_msg = "Bakery views unconfigured. Set BAKERY_VIEWS in settings.py or provide a list as arguments."
    # regex to match against for gzipping. CSS, JS, JSON, HTML, etc.
    gzip_file_match = getattr(
        settings,
        'GZIP_CONTENT_TYPES',
        DEFAULT_GZIP_CONTENT_TYPES
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start Bakery build'))
        self.set_options(*args, **options)
        self.init_build_dir()
        self.build_views()
        self.stdout.write(self.style.SUCCESS('Build finished'))

    def set_options(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        if not hasattr(settings, 'BUILD_DIR'):
            raise CommandError(self.build_unconfig_msg)
        self.build_dir = settings.BUILD_DIR
        self.build_dir = smart_text(self.build_dir)
        self.static_root = smart_text(settings.STATIC_ROOT)
        self.media_root = smart_text(settings.MEDIA_ROOT)
        self.app = apps.get_app_config("bakery")
        self.fs = self.app.filesystem
        self.fs_name = self.app.filesystem_name
        if not self.fs.exists(self.build_dir):
            self.fs.makedirs(self.build_dir)
        if not hasattr(settings, 'BAKERY_VIEWS'):
            raise CommandError(self.views_unconfig_msg)
        self.view_list = settings.BAKERY_VIEWS

    def init_build_dir(self):
        self.stdout.write(self.style.SUCCESS("Initializing %s" % self.build_dir))
        if self.fs.exists(self.build_dir):
            self.fs.removetree(self.build_dir)
        self.fs.makedirs(self.build_dir)

    def get_view_instance(self, view):
        return view()

    def build_views(self):
        for view_str in self.view_list:
            self.stdout.write("Building %s" % view_str)
            view = get_callable(view_str)
            self.get_view_instance(view).build_method()

    def copytree_and_gzip(self, source_dir, target_dir):
        build_list = []
        for (dirpath, dirnames, filenames) in os.walk(source_dir):
            for f in filenames:
                source_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(dirpath, source_dir)
                target_path = os.path.join(target_dir, rel_path, f)
                build_list.append((source_path, target_path))
        if not getattr(self, 'pooling', False):
            [self.copyfile_and_gzip(*u) for u in build_list]
        else:
            cpu_count = multiprocessing.cpu_count()
            logger.debug("Pooling build on {} CPUs".format(cpu_count))
            pool = ThreadPool(processes=cpu_count)
            pool.map(self.pooled_copyfile_and_gzip, build_list)

    def pooled_copyfile_and_gzip(self, payload):
        self.copyfile_and_gzip(*payload)

    def copyfile_and_gzip(self, source_path, target_path):
        target_dir = path.dirname(target_path)
        if not self.fs.exists(target_dir):
            try:
                self.fs.makedirs(target_dir)
            except OSError:
                pass
        guess = mimetypes.guess_type(source_path)
        content_type = guess[0]
        encoding = guess[1]

        if content_type not in self.gzip_file_match:
            copy.copy_file("osfs:///", smart_text(source_path), self.fs, smart_text(target_path))
        elif encoding == 'gzip':
            copy.copy_file("osfs:///", smart_text(source_path), self.fs, smart_text(target_path))
        else:
            with open(source_path, 'rb') as source_file:
                data_buffer = six.BytesIO()
                kwargs = dict(
                    filename=path.basename(target_path),
                    mode='wb',
                    fileobj=data_buffer
                )
                if float(sys.version[:3]) >= 2.7:
                    kwargs['mtime'] = 0
                with gzip.GzipFile(**kwargs) as f:
                    f.write(six.binary_type(source_file.read()))
                with self.fs.open(smart_text(target_path), 'wb') as outfile:
                    outfile.write(data_buffer.getvalue())
                    outfile.close()
