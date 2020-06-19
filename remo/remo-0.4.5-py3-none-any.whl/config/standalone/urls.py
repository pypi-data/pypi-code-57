# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views import defaults as default_views

from remo_app.remo.api.views.local_files import LocalFiles
from remo_app.remo.api.views.medial_files import MediaFiles
from remo_app.remo.api.views.settings import Settings
from remo_app.remo.api.views.version import Version
from remo_app.remo.use_cases.running_mode import is_remo_local

urlpatterns = [
    url(r'^settings/?$', csrf_exempt(Settings.as_view()), name='settings'),
    url(r'^version/?$', csrf_exempt(Version.as_view()), name='version'),
    url(r'^api/', include('remo_app.remo.api.urls')),
    url(r'^api/v1/ui/', include('remo_app.remo.api.v1.ui.urls')),
    url(r'^api/v1/sdk/', include('remo_app.remo.api.v1.sdk.urls')),
    url(r'^docs/', include('remo_app.remo.docs.urls')),
    # Paste project urls here
]

if is_remo_local():
    urlpatterns += [
        url(r'^%s/.*$' % settings.LOCAL_FILES.lstrip('/'), csrf_exempt(LocalFiles.as_view()), name='local-files'),
        url(r'^%s.*$' % settings.MEDIA_URL.lstrip('/'), csrf_exempt(MediaFiles.as_view()), name='media-files'),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
        # PROFILER_ON: uncomment
        # url(r'^silk/', include('silk.urls', namespace='silk')),
    ]

urlpatterns += [
    url(r'^', TemplateView.as_view(template_name='base.html'), name='home'),
]
