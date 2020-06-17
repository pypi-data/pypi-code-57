from django import template
from django.conf import settings

register = template.Library()

debconf = {
    'LOCAL_CURRENCY': settings.DEBCONF_LOCAL_CURRENCY,
}

@register.simple_tag
def debconf_setting(key):
    return debconf[key]


# These colors were taken by picking the lightest colors from
# https://en.wikipedia.org/wiki/Web_colors#X11_color_names then shuffling the
# list
colors = [
    ('#FFE4E1', 'MistyRose'),
    ('#F0FFF0', 'Honeydew'),
    ('#00FFFF', 'Cyan'),
    ('#E0FFFF', 'LightCyan'),
    ('#00FF00', 'Lime'),
    ('#D2B48C', 'Tan'),
    ('#FFD700', 'Gold'),
    ('#D3D3D3', 'LightGray'),
    ('#B0C4DE', 'LightSteelBlue'),
    ('#E6E6FA', 'Lavender'),
    ('#00BFFF', 'DeepSkyBlue'),
    ('#F5DEB3', 'Wheat'),
    ('#90EE90', 'LightGreen'),
    ('#FFB6C1', 'LightPink'),
    ('#FFA07A', 'LightSalmon'),
    ('#AFEEEE', 'PaleTurquoise'),
    ('#DDA0DD', 'Plum'),
    ('#FFFFE0', 'LightYellow'),
    ('#F0E68C', 'Khaki'),
]


@register.simple_tag
def debconf_track_color(track):
    if track:
        return colors[track.id % len(colors)][0]
