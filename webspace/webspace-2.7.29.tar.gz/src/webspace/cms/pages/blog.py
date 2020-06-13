from datetime import date
import re
import readtime
from lxml import etree

from django.shortcuts import render
from django.db import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse

from wagtail.documents.models import Document
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.core.url_routing import RouteResult
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase

from ..blocks.entries.text import Text
from ..bakery.models import BuildableWagtailBakeryModel
from .. import constants
from ..amp.mixins import AmpMixin

from ...loader import get_model

GenericPage = get_model('cms', 'GenericPage')


class ABlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')

    class Meta:
        app_label = 'cms'
        abstract = True


class ABlogPage(AmpMixin, BuildableWagtailBakeryModel, GenericPage):
    template = '%s/blog_page.html' % constants.PAGES_TEMPLATES_PATH
    author = models.ForeignKey(
        settings.WAGTAIL_BLOG_AUTHOR_PAGE,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    svg_cover = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension : 1920x1080'
    )
    svg_bg_desktop = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    svg_bg_mobile = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    tags = ClusterTaggableManager(through='BlogPageTag', blank=True)
    date = models.DateTimeField("Date publication + tri", default=date.today)
    date_updated = models.DateTimeField("Date mise à jour", default=None, null=True, blank=True)
    intro = models.CharField(default='', max_length=500, blank=True)
    intro_page = fields.RichTextField(default='', blank=True, features=settings.RICH_TEXT_FEATURES)
    h1 = models.CharField(default='', max_length=200, blank=True)
    related_blogs = StreamField([
        ('article', blocks.PageChooserBlock(required=False, target_model='cms.BlogPage')),
    ], blank=True)

    promote_panels = GenericPage.promote_panels + [
        StreamFieldPanel('schemas'),
    ]
    content_panels = [
                         FieldPanel('author'),
                         FieldPanel('date'),
                         FieldPanel('date_updated'),
                         FieldPanel('tags'),
                         DocumentChooserPanel('svg_cover'),
                         FieldPanel('intro'),
                         DocumentChooserPanel('svg_bg_desktop'),
                         DocumentChooserPanel('svg_bg_mobile'),
                         FieldPanel('h1'),
                         FieldPanel('intro_page'),
                         StreamFieldPanel('related_blogs'),
                     ] + GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'

    @property
    def blog_index(self):
        return self.get_ancestors().type(ABlogIndexPage).last()

    @property
    def read_time(self):
        rgx = re.compile(r'<.*?>')
        words = ""
        for block in self.body:
            if isinstance(block.block, Text):
                text = block.value['text']['value'].source
                words += " " + rgx.sub('', text)
        return readtime.of_text(words)

    def get_absolute_url(self):
        return self.full_url

    def get_context(self, request, *args, **kwargs):
        context = super(ABlogPage, self).get_context(request)
        html = render(
            request,
            self.get_template(request, *args, **kwargs),
            context
        )
        tree = etree.HTML(html.content)
        summary = []
        for node in tree.xpath('//h2|//h3|//h4|//h5'):
            if node.attrib.get('id'):
                if node.tag == 'h2':
                    summary.append({
                        'content': node.text,
                        'link': node.attrib.get('id'),
                        'h3': []
                    })
                if node.tag == 'h3':
                    summary[-1]['h3'].append({
                        'content': node.text,
                        'link': node.attrib.get('id'),
                        'h4': []
                    })
                if node.tag == 'h4':
                    summary[-1]['h3'][-1]['h4'].append({
                        'content': node.text,
                        'link': node.attrib.get('id'),
                    })
        context['summary'] = summary
        return context


class ABlogIndexPage(AmpMixin, BuildableWagtailBakeryModel, GenericPage):
    template = '%s/blog_index_page.html' % constants.PAGES_TEMPLATES_PATH
    svg_bg_desktop = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    svg_bg_mobile = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    h1 = models.CharField(default='', max_length=200, blank=True)
    first_text = fields.RichTextField(default='', blank=True, features=settings.RICH_TEXT_FEATURES)

    content_panels = [
                         DocumentChooserPanel('svg_bg_desktop'),
                         DocumentChooserPanel('svg_bg_mobile'),
                         FieldPanel('h1'),
                         FieldPanel('first_text'),
                     ] + Page.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'

    def route(self, request, path_components):
        if path_components:
            if path_components[0] == 'tags':
                tag_slug = path_components[1]
                try:
                    tag = Tag.objects.get(slug__iexact=tag_slug)
                except Tag.DoesNotExist:
                    raise Http404
                if self.live:
                    return RouteResult(self, kwargs={"tag": tag})
                raise Http404
            else:
                path_components[0] = path_components[0][:50]
        return super(ABlogIndexPage, self).route(request, path_components)

    @property
    def blogs(self):
        blogs = ABlogPage.objects.live().descendant_of(self)
        blogs = blogs.order_by('-date')
        return blogs

    def get_context(self, request, tag=None):
        blogs = self.blogs
        if tag:
            blogs = blogs.filter(tags__slug=tag)
        page = request.GET.get('page')
        paginator = Paginator(blogs,
                              getattr(settings, 'WAGTAIL_BLOG_POSTS_PER_PAGE', 10))
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        context = super(ABlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        context['tags'] = Tag.objects.all()
        context['current_tag'] = tag
        return context

    def serve(self, request, *args, **kwargs):
        if 'tag' not in kwargs:
            return super(ABlogIndexPage, self).serve(request)

        #  Serve tag pages
        is_building = request.GET.get('build', False)
        request.is_preview = getattr(request, 'is_preview', False)
        if settings.DEBUG or request.is_preview or is_building:
            return TemplateResponse(
                request,
                self.get_template(request),
                self.get_context(request)
            )
        else:
            return self.render_baked_file(
                request,
                settings.TEMPLATE_PATH + "/build" + self.get_url() + 'tags/' + kwargs['tag'].slug + '/'
            )
