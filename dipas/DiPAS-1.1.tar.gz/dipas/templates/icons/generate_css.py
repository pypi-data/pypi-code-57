import base64
import glob
import os.path
import re


colors = {
    'blue': {'fill': '#0000a0', 'border': '#000064'},
    'red':  {'fill': '#a00000', 'border': '#640000'},
    'grey': {'fill': '#a0a0a0', 'border': '#646464'},
}
color_shifter = {'hkicker', 'vkicker', 'quadrupole', 'sextupole', 'rbend', 'sbend'}
img_url_template = '--icon-{keyword}{color}: url(data:image/svg+xml;base64,{base64});'

css = []
for f_name in glob.glob('*.svg'):
    with open(f_name) as fh:
        svg = fh.read()
    name, suffix = os.path.splitext(f_name)
    if name in color_shifter:
        for c_name, color in colors.items():
            new = svg.replace(colors['blue']['fill'], color['fill']).replace(colors['blue']['border'], color['border'])
            new = re.sub(r' {2,}', ' ', new.replace('\n', ''))
            css.append(img_url_template.format(
                keyword=name, color=f'-{c_name}',
                base64=base64.encodebytes(new.encode('utf-8')).decode('utf-8').replace('\n', '')))
    else:
        css.append(img_url_template.format(
            keyword=name, color='',
            base64=base64.encodebytes(svg.encode('utf-8')).decode('utf-8').replace('\n', '')))
css.append('--icon-placeholder: var(--icon-drift);')

print('\n'.join(css))
