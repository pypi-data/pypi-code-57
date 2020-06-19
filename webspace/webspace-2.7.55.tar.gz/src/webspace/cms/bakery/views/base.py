from __future__ import unicode_literals
import six
import sys
import gzip
import mimetypes
from fs import path
from django.apps import apps
from django.conf import settings
from django.utils.encoding import smart_text
from .. import DEFAULT_GZIP_CONTENT_TYPES
from django.test.client import RequestFactory


class BuildableMixin(object):
    fs_name = apps.get_app_config("cms").filesystem_name
    fs = apps.get_app_config("cms").filesystem

    def create_request(self, path):
        return RequestFactory().get(path)

    def get_content(self):
        return self.get(self.request).render().content

    def prep_directory(self, target_dir):
        dirname = path.dirname(target_dir)
        if dirname:
            dirname = path.join(settings.BUILD_DIR, dirname)
            if not self.fs.exists(dirname):
                self.fs.makedirs(dirname)

    def build_file(self, path, html):
        if self.is_gzippable(path):
            self.gzip_file(path, html)
        else:
            self.write_file(path, html)

    def write_file(self, target_path, html):
        with self.fs.open(smart_text(target_path), 'wb') as outfile:
            outfile.write(six.binary_type(html))
            outfile.close()

    def is_gzippable(self, path):
        if not getattr(settings, 'BAKERY_GZIP', False):
            return False
        whitelist = getattr(
            settings,
            'GZIP_CONTENT_TYPES',
            DEFAULT_GZIP_CONTENT_TYPES
        )
        return mimetypes.guess_type(path)[0] in whitelist

    def gzip_file(self, target_path, html):
        data_buffer = six.BytesIO()
        kwargs = dict(
            filename=path.basename(target_path),
            mode='wb',
            fileobj=data_buffer
        )
        if float(sys.version[:3]) >= 2.7:
            kwargs['mtime'] = 0
        with gzip.GzipFile(**kwargs) as f:
            f.write(six.binary_type(html))

        with self.fs.open(smart_text(target_path), 'wb') as outfile:
            outfile.write(data_buffer.getvalue())
            outfile.close()
