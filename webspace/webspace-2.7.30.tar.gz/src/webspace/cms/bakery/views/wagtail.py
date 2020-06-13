import logging
import os
from urllib.parse import urlparse

from django.conf import settings
from django.utils import translation
from django.core.handlers.base import BaseHandler
from django.test.client import RequestFactory
from wagtail.core.models import Page, Site

from . import BuildableDetailView
from ..models import BuildableWagtailBakeryModel

logger = logging.getLogger(__name__)

USER_AGENT_DESKTOP = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
USER_AGENT_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"


class WagtailBakeryView(BuildableDetailView):

    def __init__(self, *args, **kwargs):
        self.handler = BaseHandler()
        self.handler.load_middleware()
        self.request = None
        super().__init__(*args, **kwargs)

    def get(self, request):
        response = self.handler.get_response(request)
        return response

    def get_content(self, obj):
        response = self.get(self.request)
        if hasattr(response, 'render'):
            return response.render().content
        if hasattr(response, 'content'):
            return response.content
        raise AttributeError(
            "'%s' object has no attribute 'render' or 'content'" % response)

    def get_build_path(self, obj):
        url = self.get_url(obj)
        if url.startswith('http'):
            url_parsed = urlparse(url)
            path = url_parsed.path
            hostname = url_parsed.hostname
            if getattr(settings, 'BAKERY_MULTISITE', False):
                build_path = os.path.join(
                    settings.BUILD_DIR, hostname, path[1:])
            else:
                build_path = os.path.join(settings.BUILD_DIR, path[1:])
        else:
            build_path = os.path.join(settings.BUILD_DIR, url[1:])
        os.path.exists(build_path) or os.makedirs(build_path)
        return os.path.join(build_path, 'index.html')

    def get_url(self, obj):
        return obj.specific.url

    def get_path(self, obj):
        return obj.path

    def build_object(self, obj):
        site = Site.objects.all().first()
        logger.debug("Building %s" % obj)

        self.build_object_env(site, obj)
        self.build_object_env(site, obj, mobile=True)
        self.build_object_env(site, obj, amp=True)
        self.build_object_env(site, obj, mobile=True, amp=True)

    def build_object_env(self, site, obj, amp=False, mobile=False):
        user_agent = USER_AGENT_MOBILE if mobile else USER_AGENT_DESKTOP
        pre_url = '/amp' if amp else ''
        self.request = RequestFactory(SERVER_NAME=site.hostname).get(
            pre_url + self.get_url(obj) + '?build=true',
            HTTP_USER_AGENT=user_agent
        )
        self.set_kwargs(obj)
        path = self.get_build_path(obj)
        if mobile:
            path = path.replace('.html', '-mobile.html')
        if amp:
            path = path.replace('.html', '-amp.html')
        self.build_file(path, self.get_content(obj))
        print(path + ' : OK')

    def build_queryset(self):
        for item in self.get_queryset().all():
            url = self.get_url(item)
            if url is not None:
                self.build_object(item)

    class Meta:
        abstract = True


class AllBuildablePagesView(WagtailBakeryView):

    def get_queryset(self):
        return Page.objects.all() \
            .public() \
            .type(BuildableWagtailBakeryModel) \
            .live()
