from django.conf.urls import url
from django.utils.translation import ugettext_lazy

from . import views

urlpatterns = [
    url(r'^my/unnamed/untranslated_example$',
        views.unnamed_untranslated_exampleview),
    url(ugettext_lazy(r'^my/unnamed/translated_example$'),
        views.unnamed_translated_exampleview),
    url(r'^my/named/untranslated_example$',
        views.named_untranslated_exampleview,
        name="ievv_i18n_url_testapp_untranslated_exampleview"),
    url(ugettext_lazy(r'^my/named/translated_example$'),
        views.named_translated_exampleview,
        name="ievv_i18n_url_testapp_translated_exampleview"),
]
