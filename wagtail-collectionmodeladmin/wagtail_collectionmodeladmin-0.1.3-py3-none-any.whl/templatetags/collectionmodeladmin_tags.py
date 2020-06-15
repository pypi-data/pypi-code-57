from django.template import Library

register = Library()


@register.filter(name='get_app_name')
def get_app_name(d):
    return d._meta.app_label


@register.filter(name='get_model_name')
def get_model_name(d):
    return d._meta.model_name


@register.simple_tag
def setvar(val=None):
    return val