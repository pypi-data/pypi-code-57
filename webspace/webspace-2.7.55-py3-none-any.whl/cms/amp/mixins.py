import os.path

from .utils import amp_mode_active


class AmpMixin:

    @property
    def amp_template(self):
        name, ext = os.path.splitext(super().get_template({}))
        return name + '_amp' + ext

    def get_template(self, request):
        if amp_mode_active():
            return self.amp_template
        return super().get_template(request)

    def get_url(self, request=None, current_site=None):
        urls = super().get_url(request, current_site)
        if amp_mode_active():
            urls = urls.replace('/amp', '')
            return '/amp%s' % urls
        return urls
