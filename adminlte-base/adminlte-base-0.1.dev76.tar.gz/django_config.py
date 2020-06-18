def replace_with_include(template):
    def f(_, **kwargs):
        return 'include', (f"'{template}'", 'with'), kwargs
    return f


ENVIRONMENT_AUTOESCAPE = False
ENVIRONMENT_EXTENSIONS = ['jinja2.ext.i18n']


GENERATOR_FUNCTIONS_MAPPER = {
    'sidebar_menu': replace_with_include('adminlte_full/markup/sidebar_menu.html'),
    'navbar_dropdown': replace_with_include('adminlte_full/markup/navbar_dropdown.html'),
    'adminlte.create_url': 'url',
    '_': 'trans',
    'gettext': 'trans',
}

GENERATOR_TEMPLATE_TAGS = {
    r'^adminlte\.[a-z0-9_]+$': 'adminlte_full',
    r'^adminlte_macro\.[a-z0-9_]+$': 'adminlte_full',
    r'^gravatar$': 'adminlte_full',
    r'^humanize$': 'adminlte_full',
    '^(_|gettext|trans)$': 'i18n',
}
