from django import template
from django.template.defaultfilters import register
from django.template.loader import render_to_string

from cookie_alert.app_settings import cookie_alert_settings


class CookieAlertNode(template.Node):

    def __init__(self, template_name):
        if not template_name:
            self.template_name = 'cookie_alert/footer.html'
        else:
            self.template_name = template.Variable(template_name)

    def render(self, context):
        request = context['request']
        if 'cookies_confirmed' in request.COOKIES:
            return ''  # do nothing

        try:
            self.template_name = self.template_name.resolve(context)
        except Exception:
            pass

        template_context = {
            'with_analysis_choice': cookie_alert_settings.WITH_ANALYSIS_CHOICE,
        }
        return render_to_string(template_name=self.template_name,
                                context=template_context, request=request)


@register.tag(name='render_cookie_alert')
def do_render_cookie_alert(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, template_name = token.split_contents()
    except ValueError:
        template_name = None

    return CookieAlertNode(template_name=template_name)
