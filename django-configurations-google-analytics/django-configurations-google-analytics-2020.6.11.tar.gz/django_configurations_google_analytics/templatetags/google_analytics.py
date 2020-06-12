from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

"""
{% load ga %}

{% ga %}
"""


@register.simple_tag
def google_analytics():
    GA_ID = getattr(settings,"GA_ID")
    html = """
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '%s');
</script>
""" % (GA_ID,GA_ID)
    return mark_safe(html)
