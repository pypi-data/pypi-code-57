from django import template

register = template.Library()

# @register.filter(name='addcss')
# def addcss(value, arg):
#     css_classes = value.field.widget.attrs.get('class', '').split(' ')
#     if css_classes and arg not in css_classes:
#         css_classes = '%s %s' % (css_classes, arg)
#     return value.as_widget(attrs={'class': css_classes})

# @register.filter(name='get_key')
# def get_key(value, arg):
#     return value[arg]

@register.filter(name='get_attr')
def get_obj_attr(obj, attr_str):
    return getattr(obj, attr_str)

# @register.filter(name='get_range')
# def get_range(value):
#     return range(value)

# @register.filter(name='get_detail_url')
# def get_detail_url(models_urls, model_class):
#     return models_urls[model_class]['detail']
