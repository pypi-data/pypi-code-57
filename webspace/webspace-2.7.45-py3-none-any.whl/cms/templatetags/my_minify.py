from django.template import (Library, Node)
import json

register = Library()


class MinifySchema(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        ld = self.nodelist.render(context)
        try:
            return json.dumps(json.loads(ld))
        except Exception:
            return ''


@register.tag('minify_schema')
def minify_schema(parser, token):
    nodelist = parser.parse(('endminify_schema',))
    parser.delete_first_token()
    return MinifySchema(
        nodelist,
    )
