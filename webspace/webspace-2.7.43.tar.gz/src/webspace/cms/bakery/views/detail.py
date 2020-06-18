import os
from fs import path
from .base import BuildableMixin
from django.conf import settings
from django.views.generic import DetailView
from django.core.exceptions import ImproperlyConfigured


class BuildableDetailView(DetailView, BuildableMixin):

    @property
    def build_method(self):
        return self.build_queryset

    def get_url(self, obj):
        if not hasattr(obj, 'get_absolute_url') or not obj.get_absolute_url():
            raise ImproperlyConfigured("No URL configured. You must either \
set a ``get_absolute_url`` method on the %s model or override the %s view's \
``get_url`` method" % (obj.__class__.__name__, self.__class__.__name__))
        return obj.get_absolute_url()

    def get_build_path(self, obj):
        target_path = path.join(settings.BUILD_DIR, self.get_url(obj).lstrip('/'))
        if not self.fs.exists(target_path):
            self.fs.makedirs(target_path)
        return path.join(target_path, 'index.html')

    def set_kwargs(self, obj):
        slug_field = self.get_slug_field()
        self.kwargs = {
            'pk': getattr(obj, 'pk', None),
            slug_field: getattr(obj, slug_field, None),
            # Also alias the slug_field to the key `slug`
            # so it can work for people who just toss that in
            'slug': getattr(obj, slug_field, None),
        }

    def build_object(self, obj):
        self.request = self.create_request(self.get_url(obj))
        self.set_kwargs(obj)
        target_path = self.get_build_path(obj)
        self.build_file(target_path, self.get_content())

    def build_queryset(self):
        [self.build_object(o) for o in self.get_queryset().all()]

    def unbuild_object(self, obj):
        target_path = os.path.split(self.get_build_path(obj))[0]
        if self.fs.exists(target_path):
            self.fs.removetree(target_path)
