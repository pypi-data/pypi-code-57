from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap

from .views import robots
from .cms.amp import urls as wagtail_amp_urls

urlpatterns = [
    url(r'^robots\.txt$', robots),
    url(r'^sitemap\.xml$', sitemap),
    url(r'^admin_W3cJ32mq63V45CLvmjNbsqSJ32mq63V45CL/', admin.site.urls),
    url(r'^wagtail_WSQtYMxmgLV9iIn6VE3An1VxpH9aoOUeg/', include(wagtailadmin_urls)),
    url(r"^amp/", include(wagtail_amp_urls)),
    url(r"^", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = '.views.error_404'
