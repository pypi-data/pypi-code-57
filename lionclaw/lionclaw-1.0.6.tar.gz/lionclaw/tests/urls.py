# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from wagtail.admin import urls as admin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as documents_urls
from lionclaw import urls as lionclaw_urls
from lionclaw.contrib.productrequests import urls as request_urls

urlpatterns = [
    url(r'^admin/', include(admin_urls)),
    url(r'^documents/', include(documents_urls)),

    url(r'', include(lionclaw_urls)),
    url(r'', include(request_urls)),
    url(r'', include(wagtail_urls)),


]
