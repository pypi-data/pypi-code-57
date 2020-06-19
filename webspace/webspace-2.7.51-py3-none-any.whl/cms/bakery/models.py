from django.db import models
from django.conf import settings
from django.template.response import TemplateResponse
from django.http import HttpResponse


class BuildableModel(models.Model):
    detail_views = []

    def _get_view(self, name):
        from django.urls import get_callable
        return get_callable(name)

    def _build_related(self):
        pass

    def _build_extra(self):
        pass

    def _unbuild_extra(self):
        pass

    def build(self):
        for detail_view in self.detail_views:
            view = self._get_view(detail_view)
            view().build_object(self)
        self._build_extra()
        self._build_related()

    def unbuild(self):
        for detail_view in self.detail_views:
            view = self._get_view(detail_view)
            view().unbuild_object(self)
        self._unbuild_extra()
        # _build_related again to kill the object from RSS etc.
        self._build_related()

    def get_absolute_url(self):
        pass

    class Meta:
        abstract = True


class BuildableWagtailBakeryModel(BuildableModel):
    detail_views = ['.views.wagtail.AllBuildablePagesView']

    def serve(self, request, *args, **kwargs):
        is_building = request.GET.get('build', False)
        request.is_preview = getattr(request, 'is_preview', False)

        #  Remove settings.DEBUG if you want to test static page

        if settings.DEBUG or request.is_preview or is_building:
            return TemplateResponse(
                request,
                self.get_template(request, *args, **kwargs),
                self.get_context(request, *args, **kwargs)
            )
        else:
            index = 'index.html' if request.user_agent.is_pc else 'index-mobile.html'
            with open(settings.TEMPLATE_PATH + "/build" + self.get_url() + index, "rb") as fd:
                compressed = fd.read()
                response = HttpResponse(compressed)
                response['Content-Encoding'] = 'gzip'
                response['Content-Length'] = str(len(compressed))
                return response

    class Meta:
        abstract = True
