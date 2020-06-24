#
#   All template tags provided by the PSU Base plugin are registered in this file.
#   For browse-ability, all processing happens outside this file.
#

from django.conf import settings
from django import template
from psu_base.classes.Log import Log
from psu_base.services import utility_service, auth_service
from psu_base.templatetags.tag_processing import supporting_functions as support, html_generating, static_content
from psu_base.classes.User import User
from psu_base.classes.DynamicRole import DynamicRole
from django.urls import reverse

register = template.Library()
log = Log()


# # # # # # # # # # # # # # # # # # #
# UTILITY CATEGORY
# # # # # # # # # # # # # # # # # # #


@register.simple_tag(takes_context=True)
def absolute_url(context, *args, **kwargs):
    if args:
        reverse_args = args[1:] if len(args) > 1 else None
        return f"{context['absolute_root_url']}{reverse(args[0], args=reverse_args)}"
    else:
        return context['absolute_root_url']


@register.simple_tag
def log_to_session(*args):
    utility_service.append_session_log(' - '.join([str(x) for x in args if x]))
    return ''


@register.simple_tag()
def flash_variable(*args, **kwargs):
    var = kwargs.get('var', args[0] if args else None)
    alt = kwargs.get('alt', args[1] if args and len(args) >= 2 else None)
    return utility_service.get_flash_variable(var, alt)


@register.simple_tag()
def app_code():
    return utility_service.get_app_code()


@register.simple_tag()
def app_name():
    return utility_service.get_app_name()


@register.simple_tag()
def app_version():
    return utility_service.get_app_version()


@register.simple_tag()
def psu_version():
    return utility_service.get_setting('PSU_BASE_VERSION')


@register.simple_tag(takes_context=True)
def setting_value(context, *args, **kwargs):
    return utility_service.get_setting(args[1])


@register.simple_tag(takes_context=True)
def set_var(context, *args, **kwargs):
    log.trace(args)
    context[args[0]] = args[1]
    return ''


@register.simple_tag(takes_context=True)
def decode(context, *args):
    """
    Given an ID, return it's label from a dict of options.
    Optional third argument is a default value

    Ex:  {% decode department_code department_options %}
         {% decode 'CS' department_options %}
         {% decode 'N$^&' department_options 'Invalid Department' %}
    """
    value = args[1].get(args[0])
    if value is None and len(args) == 3:
        return args[2]
    return value


@register.simple_tag
def format_phone(*args):
    # Phone could be in one arg, or split (area, phone, ext)
    return utility_service.format_phone(''.join([x for x in args if x]))


@register.simple_tag()
def term_description(term_code):
    return utility_service.term_description(term_code)


@register.simple_tag(takes_context=True)
def check_feature(context, *args, **kwargs):
    feature = args[0]
    is_enabled = utility_service.feature_is_enabled(feature)
    context[f"{feature}_enabled"] = is_enabled
    context[f"{feature}_disabled"] = not is_enabled
    return ''


@register.simple_tag()
def banweb_url():
    return utility_service.get_banweb_url()

# # # # # # # # # # # # # # # # # # #
# AUTHENTICATION CATEGORY
# # # # # # # # # # # # # # # # # # #


@register.simple_tag(takes_context=True)
def check_authority(context, *args, **kwargs):
    authority_name = args[0]
    has_it = auth_service.has_authority(authority_name)
    var_name = args[1] if len(args) > 1 else authority_name
    context[f"has_{var_name}"] = has_it
    context[f"does_not_have_{var_name}"] = not has_it
    return ''


@register.simple_tag(takes_context=True)
def check_admin_menu(context, *args, **kwargs):
    # All power users see the admin menu
    admin_menu_roles = DynamicRole().power_user()

    # Other PSU plugins may include items for specific roles other than power-user roles
    for admin_link in context['plugin_admin_links']:
        if 'authorities' in admin_link:
            plus = utility_service.csv_to_list(admin_link['authorities'])
            admin_menu_roles.extend(plus if plus else [])

    has_it = auth_service.has_authority(list(set(admin_menu_roles)))
    var_name = args[0] if len(args) > 0 else 'admin_menu'
    context[f"has_{var_name}"] = has_it
    context[f"does_not_have_{var_name}"] = not has_it
    return ''


@register.simple_tag(takes_context=True)
def set_auth_object(context):
    context['auth_object'] = auth_service.get_auth_object()
    return ''


@register.simple_tag(takes_context=True)
def set_current_user(context):
    context['current_user'] = auth_service.get_user()
    return ''


@register.simple_tag(takes_context=True)
def display_name(context):
    return auth_service.get_user().display_name


# # # # # # # # # # # # # # # # # # #
# STATIC CONTENT CATEGORY
# # # # # # # # # # # # # # # # # # #


@register.simple_tag
def static_content_url():
    return utility_service.get_static_content_url()


@register.simple_tag
def wdt_content_url(*args, **kwargs):
    return static_content.wdt_url(kwargs.get('version'))


@register.simple_tag
def jquery(*args, **kwargs):
    return static_content.jquery(*args, **kwargs)


@register.simple_tag
def bootstrap(*args, **kwargs):
    return static_content.bootstrap(*args, **kwargs)


@register.simple_tag
def font_awesome(*args, **kwargs):
    return static_content.font_awesome(*args, **kwargs)


@register.simple_tag
def datatables(*args, **kwargs):
    return static_content.datatables(*args, **kwargs)


@register.simple_tag
def chosen(*args, **kwargs):
    return static_content.chosen(*args, **kwargs)


@register.simple_tag
def wdt_stylesheet(css_file, version=None):
    return static_content.wdt_stylesheet(css_file, version)


@register.simple_tag
def wdt_javascript(js_file, version=None):
    return static_content.wdt_javascript(js_file, version)


@register.tag()
def image(parser, token):
    return html_generating.ImageNode(token.split_contents())


# # # # # # # # # # # # # # # # # # #
# HTML-GENERATING CATEGORY
# # # # # # # # # # # # # # # # # # #


@register.inclusion_tag('_components/pagination.html')
def pagination(paginated_results):
    """Example: {%pagination polls%}"""
    return html_generating.pagination(paginated_results)


@register.tag()
def fa(parser, token):
    """Render a screen-reader-friendly FontAwesome4 icon"""
    return html_generating.FaNode(token.split_contents())


@register.tag()
def select_menu(parser, token):
    return html_generating.SelectNode(token.split_contents())


@register.tag()
def id_photo(parser, token):
    """Example: {%id_photo user="mjg"%} or {%id_photo user=user_instance%} """
    return html_generating.PhotoNode(token.split_contents())


@register.tag()
def header_nav_menu_item(parser, token):
    """Example:  """
    return html_generating.HeaderNavMenuItem(token.split_contents())


@register.tag()
def header_nav_tab(parser, token):
    """Example:  """
    return html_generating.HeaderNavTab(token.split_contents())


@register.inclusion_tag('_components/id_tag.html', takes_context=True)
def id_tag(context, user_instance_or_info):
    """Example: {%id_tag "mjg"%} or {%id_card current_user%} """
    model = context.flatten()
    model['user_instance'] = User(user_instance_or_info, allow_gravatar=False)
    return model


@register.inclusion_tag('_components/id_card.html', takes_context=True)
def id_card(context, user_instance_or_info):
    """Example: {%id_card "mjg"%} or {%id_card current_user%} """
    model = context.flatten()
    model['user_instance'] = User(user_instance_or_info, allow_gravatar=False)
    return model


# # # # # # # # # # # # # # # # # # #
# UNLIKELY TO BE RE-USED CATEGORY
# # # # # # # # # # # # # # # # # # #


@register.inclusion_tag('_components/admin_script.html', takes_context=True)
def admin_script(context):
    return {'scripts': utility_service.get_admin_scripts(context.request, auth_service.get_user().username)}


@register.inclusion_tag('_components/downtime_messages.html')
def downtime_messages():
    """Display any Banner downtime messages"""
    # Get the Finti URL for downtime messages
    finti_downtime_url = f"{settings.FINTI_URL}/org/v1/gurinfo/get_text"
    finti_downtime_env = 'oprd' if utility_service.is_production() else 'stage'
    return {'finti_downtime_url': finti_downtime_url, 'finti_downtime_env': finti_downtime_env}
