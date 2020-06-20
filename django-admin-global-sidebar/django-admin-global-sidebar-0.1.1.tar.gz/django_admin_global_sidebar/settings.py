from django.conf import settings


DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS = getattr(settings, "DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS", [])
DJANGO_ADMIN_GLOBAL_SIDEBAR_COLLAPSED_FLAG_COOKIE_NAME = getattr(settings, "DJANGO_ADMIN_GLOBAL_SIDEBAR_COLLAPSED_FLAG_COOKIE_NAME", "django-admin-global-sidebar-collapsed-flag")

