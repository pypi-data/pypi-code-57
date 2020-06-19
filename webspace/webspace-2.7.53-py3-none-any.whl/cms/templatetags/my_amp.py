from lxml import etree
import requests
from django.conf import settings
from django import template
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException

from webspace.cms import constants
from webspace.cms.amp.utils import amp_mode_active
from webspace.cms.amp.mixins import AmpMixin

register = template.Library()

SIZES_IMG = {
    's-icon x0-5': 10,
    's-icon x1': 20,
    's-icon x1-5': 30,
    's-icon x2': 40,
    's-icon x3': 60,
    's-icon x6': 120,
}

AMP_SCRIPTS = {
    'carousel': "<script async custom-element='amp-carousel' src='https://cdn.ampproject.org/v0/amp-carousel-0.2.js'></script>",
    'iframe': "<script async custom-element='amp-iframe' src='https://cdn.ampproject.org/v0/amp-iframe-0.1.js'></script>"
}


class AMPImage(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def get_match(self, classname):
        for key, value in SIZES_IMG.items():
            if key in classname:
                return key
        return False

    def render(self, context):
        if amp_mode_active():
            html = self.nodelist.render(context)
            tree = etree.XML(html)
            classname = tree.get('class')
            layout = tree.get('data-layout', 'responsive')
            width = tree.get('data-width', '500')
            height = tree.get('data-height', '500')

            match = None
            if classname:
                match = self.get_match(classname)

            # Check icons or custom
            if match:
                tree.set('layout', layout)
                tree.set('width', str(SIZES_IMG[match]))
                tree.set('height', str(SIZES_IMG[match]))
            else:
                tree.set('layout', layout)
                if width and height:
                    tree.set('width', width)
                    tree.set('height', height)

            # Check lazy
            lazy_src = tree.get('data-src')
            if lazy_src:
                tree.set('src', lazy_src)
                tree.set('data-src', '')

            #  Replacement HTML
            ret = etree.tostring(tree).decode()
            ret = ret.replace('<img ', '<amp-img ')
            ret = ret.replace('/>', '></amp-img>')
            return ret
        return self.nodelist.render(context)


@register.tag('amp_img')
def amp_img(parser, token):
    nodelist = parser.parse(('endamp_img',))
    parser.delete_first_token()
    return AMPImage(nodelist=nodelist)


class AMPStyles(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        if amp_mode_active():
            html = self.nodelist.render(context)
            tree = etree.XML(html)
            href = tree.get('href')
            request = context['request']
            http = 'https://' if request.is_secure() else 'http://'
            host = request.get_host()
            if host == 'localhost':
                host += ':8080'
            url = http + host + href
            response = requests.get(url)
            css = response.content.decode().replace('\n', '').replace('!important', '')
            ret = "<style amp-custom>%s</style>" % css
            return ret
        return self.nodelist.render(context)


@register.tag('amp_styles')
def amp_styles(parser, token):
    nodelist = parser.parse(('endamp_styles',))
    parser.delete_first_token()
    return AMPStyles(nodelist=nodelist)


@register.inclusion_tag('%s/templatetags/content-safe.html' % constants.BLOCK_TEMPLATES_PATH, takes_context=True)
def amp_scripts(context):
    scripts = []
    page = context['page']
    for block in page.body:
        if hasattr(block.block, 'amp_scripts'):
            for script in block.block.amp_scripts:
                if script not in scripts:
                    if block.block_type == 'cards' and script == 'carousel':
                        if block.value['carousel']:
                            scripts.append(script)
                    if block.block_type == 'media_text' and script == 'iframe':
                        for media in block.value['media']:
                            if media.block_type == 'embed':
                                scripts.append(script)
                    else:
                        scripts.append(script)
    html = ''
    for script in scripts:
        html += AMP_SCRIPTS[script]
    return {
        'content': html
    }


@register.inclusion_tag('%s/templatetags/content-safe.html' % constants.BLOCK_TEMPLATES_PATH, takes_context=True)
def amp_canonical(context):
    page = context['page']
    if isinstance(page, AmpMixin):
        return {
            'content': "<link rel='amphtml' href='https://%s" % context[
                'request'].get_host() + "/amp%s'>" % context[
                'request'].path.replace('?build=true', '')
        }
    return None


@register.filter
def amp_embed(url):
    try:
        embed = get_embed(url)
        tree = etree.XML(embed.html.replace('allowfullscreen', ''))
        tree.set('layout', 'responsive')
        tree.set('sandbox', 'allow-scripts allow-same-origin allow-presentation')

        #  Replacement HTML
        ret = etree.tostring(tree).decode()
        ret = ret.replace('<iframe ', '<amp-iframe ')
        ret = ret.replace('/>', '></amp-iframe>')

        return ret
    except EmbedException:
        # Cannot find embed
        pass
