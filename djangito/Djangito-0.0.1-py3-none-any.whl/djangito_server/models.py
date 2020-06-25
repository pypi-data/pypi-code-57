# Commented all this out on June 22 2020
'''
# MONKEY PATCHES ADMIN URLS TO OIDC SERVER
# cf https://stackoverflow.com/questions/6779265/how-can-i-not-use-djangos-admin-login-view
from functools import update_wrapper
# from django.conf import settings
from django.views.generic.base import RedirectView

# DJANGITO_DOMAIN_NAME = settings.DJANGITO_DOMAIN_NAME
def _get_urls(self):
    from django.urls import include, path, re_path
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level,
    # and django.contrib.contenttypes.views imports ContentType.
    from django.contrib.contenttypes import views as contenttype_views

    def wrap(view, cacheable=False):
        def wrapper(*args, **kwargs):
            return self.admin_view(view, cacheable)(*args, **kwargs)

        wrapper.admin_site = self
        return update_wrapper(wrapper, view)

    # Admin-site-wide views.
    urlpatterns = [
        path('', wrap(self.index), name='index'),
        path('login/', self.login, name='login'),
        path('logout/', wrap(self.logout), name='logout'),
        path('password_change/', wrap(self.password_change, cacheable=True), name='password_change'),
        # path('password_change2/',
        #      RedirectView.as_view(url=f'{DJANGITO_DOMAIN_NAME}/admin/password_change/', permanent=False, query_string=True),
        #      name='password_change'),
        # path(
        #     'password_change/done/',
        #     wrap(self.password_change_done, cacheable=True),
        #     name='password_change_done',
        # ),
        path('password_change/done/',
             RedirectView.as_view(url='http://127.0.0.1:8001/admin/password_change/done/', permanent=False, query_string=True),
             name='password_change_done'),
        path('jsi18n/', wrap(self.i18n_javascript, cacheable=True),
             name='jsi18n'),
        path(
            'r/<int:content_type_id>/<path:object_id>/',
            wrap(contenttype_views.shortcut),
            name='view_on_site',
        ),
    ]

    # Add in each model's views, and create a list of valid URLS for the
    # app_index
    valid_app_labels = []
    for model, model_admin in self._registry.items():
        # noinspection PyProtectedMember,PyProtectedMember
        urlpatterns += [
            path('%s/%s/' % (model._meta.app_label, model._meta.model_name),
                 include(model_admin.urls)),
        ]
        # noinspection PyProtectedMember
        if model._meta.app_label not in valid_app_labels:
            # noinspection PyProtectedMember
            valid_app_labels.append(model._meta.app_label)

    # If there were ModelAdmins registered, we should have a list of app
    # labels for which we need to allow access to the app_index view,
    if valid_app_labels:
        regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
        urlpatterns += [
            re_path(regex, wrap(self.app_index), name='app_list'),
        ]
    return urlpatterns



import django.contrib.admin.sites
django.contrib.admin.sites.AdminSite.get_urls = _get_urls
'''