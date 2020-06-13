from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException

from django import template

register = template.Library()


def ico(icon, theme):
    if theme == 'space':
        return icon['space']
    return icon['light']


def ico_astro(icons, level):
    return icons['astro_level_%s' % level]


def ico_get(icons, key):
    return icons[key]


@register.filter(is_safe=False)
def plur(value, arg='s'):
    if ',' not in arg:
        arg = ',' + arg
    bits = arg.split(',')
    if len(bits) > 2:
        return ''
    singular_suffix, plural_suffix = bits[:2]
    try:
        return singular_suffix if float(value) <= 1 else plural_suffix
    except ValueError:  # Invalid string that's not a number.
        pass
    except TypeError:  # Value isn't a string or a number; maybe it's a list?
        try:
            return singular_suffix if len(value) <= 1 else plural_suffix
        except TypeError:  # len() of unsized object.
            pass
    return ''


def embed(url):
    try:
        embed = get_embed(url)
        ret = embed.html.replace('width="480"', '')
        ret = ret.replace('height="270"', '')
        ret = ret.replace('src=', 'class="lazy" data-src=')
        return ret
    except EmbedException:
        # Cannot find embed
        pass


def strfix(value):
    return value.replace('\n', '')


register.filter('ico', ico)
register.filter('ico_astro', ico_astro)
register.filter('ico_get', ico_get)
register.filter('plur', plur)
register.filter('embed', embed)
register.filter('strfix', strfix)
