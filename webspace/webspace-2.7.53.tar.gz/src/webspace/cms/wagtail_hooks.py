import re
from wagtail.admin.rich_text.converters import html_to_contentstate
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler, KEEP_WHITESPACE, WHITESPACE_RE
)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from webspace.cms.bakery import urls as urls_bakery

NOTHING_RE = re.compile('a^')


@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    feature_name = 'mark'
    type_ = 'MARK'
    tag = 'mark'

    control = {
        'type': type_,
        'label': '☆',
        'description': 'Mark',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append('mark')


class PreformattedTextElementHandler(BlockElementHandler):
    """
    BlockElementHandler that preserves all whitespace.
    """

    def handle_starttag(self, name, attrs, state, contentstate):
        super().handle_starttag(name, attrs, state, contentstate)
        # Keep all whitespace while rendering this block
        html_to_contentstate.WHITESPACE_RE = NOTHING_RE
        state.leading_whitespace = KEEP_WHITESPACE

    def handle_endtag(self, name, state, contentstate):
        # Reset whitespace handling to normal behaviour
        html_to_contentstate.WHITESPACE_RE = WHITESPACE_RE
        super().handle_endtag(name, state, contentstate)


@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    feature_name = 'code-block'
    feature_type = 'code-block'
    control = {
        'type': feature_type,
        'label': '{}',
        'description': 'Code',
    }
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'pre': PreformattedTextElementHandler(feature_type),
        },
        'to_database_format': {
            'block_map': {
                feature_type: {
                    'element': 'pre',
                    'props': {'class': 'code'},
                },
            },
        },
    })
    features.default_features.append(feature_name)


#  Bakery


class BakeryItem(MenuItem):
    """
    Registers wagtail-cache in wagtail admin for superusers.
    """

    def is_shown(self, request):
        return request.user.is_superuser


@hooks.register('register_admin_urls')
def register_admin_urls():
    """
    Registers wagtail-cache urls in the wagtail admin.
    """
    return [
        path('bakery/', include((urls_bakery, 'bakery'), namespace='bakery')),
    ]


@hooks.register('register_settings_menu_item')
def register_cache_menu():
    """
    Registers wagtail-cache settings panel in the wagtail admin.
    """
    return BakeryItem(
        _('Bakery'),
        reverse('bakery:index'),
        classnames='icon icon-cog')
