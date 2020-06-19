#!/usr/bin/env python3

from .weasyprint_builder import WeasyPrintPDFBuilder
from typing import Dict, Any
from sphinx.application import Sphinx
from sphinx.util.osutil import make_filename


version = (0, 1, 0)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension('sphinx.builders.html')

    app.add_builder(WeasyPrintPDFBuilder)
    app.add_config_value(
        'weasyprint_theme_options',
        lambda self: self.html_theme_options,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_basename',
        lambda self: make_filename(self.project),
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_theme',
        lambda self: self.html_theme,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_title',
        lambda self: self.html_title,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_theme_path',
        lambda self: self.html_theme_path,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_short_title',
        lambda self: self.html_short_title,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_style',
        None,
        'weasyprint',
        [str]
    )
    app.add_config_value(
        'weasyprint_css_files',
        [],
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_show_copyright',
        True,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_show_sphinx',
        True,
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_main_selector',
        '',
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_footer_selector',
        '',
        'weasyprint'
    )
    app.add_config_value(
        'weasyprint_header_selector',
        '',
        'weasyprint'
    )

    return {
        'version': version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
