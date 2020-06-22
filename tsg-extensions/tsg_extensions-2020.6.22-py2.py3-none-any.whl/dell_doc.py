# -*- coding: UTF-8 -*-
"""
Modified Markdown syntax for generating links to Dell EMC KBs & documents.
"""
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


class DellDocExtension(Extension):
    def extendMarkdown(self, md, config):
        self.md = md
        MD_RE = r'\[\[([\w0-9_: -]+)\]\]'
        md_pattern = DellDocInlineProcessor(MD_RE)
        md_pattern.md = md
        md.inlinePatterns.register(md_pattern, 'dell_doc', 70)


class DellDocInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        if m.group(1).strip():
            html_class = 'dell-doc'
            label = m.group(1).strip()
            url, title = self.build_url(label)
            a = etree.Element('a')
            a.text = title
            a.set('href', url)
            a.set('class', html_class)
            a.set('target', '_blank')
        else:
            a = ''
        return a, m.start(0), m.end(0)

    def build_url(self, label):
        base = 'https://support.emc.com/'
        label_bits = label.split(' ')
        if label_bits[0].lower() == 'kb':
            middle = 'kb/{}'.format(label_bits[-1].strip())
            title = 'article {}'.format(label_bits[-1].strip())
        elif label_bits[-1].lower().startswith('docu'):
            middle = label_bits[-1]
            title = ' '.join(label_bits[:-1])
        else:
            raise RuntimeError('Invalid Dell Doc Link label provided: {}'.format(label))
        return '{}{}'.format(base, middle), title


def makeExtension(**kwargs):
    return DellDocExtension(**kwargs)
