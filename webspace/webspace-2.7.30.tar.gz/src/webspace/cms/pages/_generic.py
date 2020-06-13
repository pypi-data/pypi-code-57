from django.db import models
from django.utils.functional import cached_property
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.conf import settings
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.admin.edit_handlers import FieldPanel
from ..bakery.models import BuildableWagtailBakeryModel
from ..amp.mixins import AmpMixin
from ..amp.utils import amp_mode_active
from .. import constants
from ..blocks import \
    MediaText, \
    Text, \
    Svg, \
    Image, \
    Cards, \
    ButtonBlock, \
    FirstContent, \
    GridInfo, \
    MediasLine, \
    TimeLine, \
    Buttons, \
    Calendly, \
    Articles, \
    Embed, \
    HowTo, \
    FAQPage
from ...loader import get_model


Menu = get_model('cms', 'Menu')
IconSnippet = get_model('cms', 'IconSnippet')


class AGenericPage(Page):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="SEO - Image",
    )

    theme = models.CharField(
        choices=constants.THEME_CHOICES,
        default=constants.THEME_SPACE,
        max_length=100
    )

    breadcrumb = models.BooleanField(
        default=True,
        verbose_name="Public pour Google",
        help_text="Ajoute la page dans le sitemap et génère un schéma Breadcrumb",
    )

    header_menus = StreamField([
        ('menu', SnippetChooserBlock(Menu, required=False)),
    ], blank=True)

    header_buttons = StreamField([
        ('button', ButtonBlock())
    ], blank=True)

    schemas = StreamField([
        ('how_to', HowTo()),
        ('faq_page', FAQPage()),
    ], blank=True)

    body = StreamField([
        ('first_content', FirstContent()),
        ('svg', Svg()),
        ('image', Image()),
        ('text', Text()),
        ('cards', Cards()),
        ('media_text', MediaText()),
        ('grid_info', GridInfo()),
        ('medias_line', MediasLine()),
        ('timeline', TimeLine()),
        ('buttons', Buttons()),
        ('calendly', Calendly()),
        ('articles', Articles()),
        ('embed', Embed()),
    ], blank=True)

    footer = StreamField([
        ('menu', SnippetChooserBlock(Menu, required=False)),
    ], blank=True)

    content_panels = [
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
        ], "Google Search"),
        MultiFieldPanel([
            ImageChooserPanel('feed_image'),
            FieldPanel('breadcrumb'),
        ], "SEO - DATA"),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('theme'),
        StreamFieldPanel('header_menus'),
        StreamFieldPanel('header_buttons'),
        StreamFieldPanel('footer'),
    ]

    subpage_types = [
        'cms.ContentPage',
        'cms.DocumentPage',
    ]

    class Meta:
        abstract = True
        app_label = 'cms'

    def get_context(self, request, *args, **kwargs):
        context = super(AGenericPage, self).get_context(request)
        context['env'] = settings.TYPENV
        context['icons'] = {}
        DEFAULT_LINK = '/static/webspace/img/svg/default.svg'
        for icon in IconSnippet.objects.all():
            context['icons'][icon.key] = {
                'space': icon.space.url if icon.space else DEFAULT_LINK,
                'light': icon.light.url if icon.light else DEFAULT_LINK,
            }
        return context

    @cached_property
    def get_breadcrumbs(self):
        #  FIXME: filter by `breadcrumb` seem not to be possible with wagtail Page
        ret = []
        items = self.get_children().type(AGenericPage).specific().live()
        for item in items:
            if item.breadcrumb:
                ret.append(item)
        return ret

    def serve(self, request, *args, **kwargs):
        is_building = request.GET.get('build', False)
        request.is_preview = getattr(request, 'is_preview', False)

        if settings.DEBUG or request.is_preview or is_building or not isinstance(self,
                                                                                 BuildableWagtailBakeryModel):
            return TemplateResponse(
                request,
                self.get_template(request, *args, **kwargs),
                self.get_context(request, *args, **kwargs)
            )
        else:
            return self.render_baked_file(
                request,
                settings.TEMPLATE_PATH + "/build" + self.get_url()
            )

    def get_sitemap_urls(self, request=None):
        if not self.breadcrumb:
            return []
        return super().get_sitemap_urls(request)

    def get_url_parts(self, *args, **kwargs):
        urls = super().get_url_parts(*args, **kwargs)
        if isinstance(self, AmpMixin) and amp_mode_active():
            return (urls[0], urls[1], '/amp' + urls[2])
        return urls

    def render_baked_file(self, request, path_file):
        index = 'index.html' if request.user_agent.is_pc else 'index-mobile.html'
        if amp_mode_active():
            index = index.replace('.html', '-amp.html')
            path_file = path_file.replace('/amp', '')
        with open(path_file + index, "rb") as fd:
            compressed = fd.read()
            response = HttpResponse(compressed)
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = str(len(compressed))
            return response
