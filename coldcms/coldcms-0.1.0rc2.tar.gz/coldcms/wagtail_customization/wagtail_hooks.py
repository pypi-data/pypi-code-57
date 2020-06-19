from coldcms.wagtail_customization.admin_views import generate_statics
from django.urls import path, reverse
from django.utils.translation import ugettext_lazy as _
from wagtail.admin import widgets as wagtailadmin_widgets
from wagtail.core import hooks


@hooks.register("register_admin_urls")
def hook_generate_statics():
    return [
        path(
            "generate_statics/<int:page_id>/",
            generate_statics,
            name="generate_statics",
        )
    ]


@hooks.register("register_page_listing_more_buttons")
def register_button_regenerate_statics(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.Button(
        _("Re-build page"),
        reverse("generate_statics", kwargs={"page_id": page.pk}),
        priority=60,
    )
