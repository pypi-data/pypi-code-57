from lxml import etree
import requests
from django.conf import settings
from django import template

from .. import constants
from ..amp.utils import amp_mode_active
from ..amp.mixins import AmpMixin

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

    def __init__(self, nodelist, layout='responsive', size=None):
        self.nodelist = nodelist
        self.layout = layout.replace('\'', '') if layout else layout
        self.size = size.replace('\'', '') if size else size
        self.classname = ''

    @property
    def width(self):
        return self.size.split('x')[0] if self.size else None

    @property
    def height(self):
        return self.size.split('x')[1] if self.size else None

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
            match = self.get_match(classname)

            # Check icons or custom
            if match:
                tree.set('layout', self.layout)
                tree.set('width', str(SIZES_IMG[match]))
                tree.set('height', str(SIZES_IMG[match]))
            else:
                tree.set('layout', self.layout)
                if self.size:
                    tree.set('width', self.width)
                    tree.set('height', self.height)

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
    tokens = token.split_contents()
    return AMPImage(
        nodelist=nodelist,
        layout=tokens[1] if len(tokens) > 1 else 'responsive',
        size=tokens[2] if len(tokens) > 2 else None,
    )


@register.inclusion_tag('%s/templatetags/content-safe.html' % constants.BLOCK_TEMPLATES_PATH, takes_context=True)
def amp_custom(context):
    request = context['request']
    http = 'https://' if request.is_secure == 'local' else 'http://'
    path_url = "/static/dist/css/cmsamp%s.css" % settings.VERSION
    url = http + request.get_host() + path_url
    response = requests.get(url)
    return {
        'content': response.content.decode().replace('\n', '').replace('!important', '')
    }


@register.inclusion_tag('%s/templatetags/content-safe.html' % constants.BLOCK_TEMPLATES_PATH, takes_context=True)
def amp_scripts(context):
    scripts = []
    page = context['page']
    for block in page.body:
        if hasattr(block.block, 'amp_scripts'):
            for script in block.block.amp_scripts:
                if script not in scripts:
                    if script == 'carousel':
                        if block.value['carousel']:
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
    from wagtail.embeds.embeds import get_embed
    from wagtail.embeds.exceptions import EmbedException
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
