from humps import camelize
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


class CaseJSONRenderer(JSONRenderer):
    def render(self, data, *args, **kwargs):
        return super().render(camelize(data), *args, **kwargs)


class CaseBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, *args, **kwargs):
        return super(CaseBrowsableAPIRenderer, self).render(camelize(data), *args, **kwargs)
