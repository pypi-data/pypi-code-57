#!/usr/bin/env python3

from copy import deepcopy

from .pyppeteer_builder import PyppeteerPDFBuilder
from typing import Dict, Any
from sphinx.application import Sphinx
from sphinx.util.osutil import make_filename


version = (0, 1, 0)


DEFAULT_PDF_OPTIONS = {
    'printBackground': True,
    'format': 'A4',
    'margin': {
        'top': '20mm',
        'bottom': '20mm',
        'left': '10mm',
        'right': '10mm'
    }
}


def on_config_inited(app, config):
    """ Change config on the fly """
    pdf_options = deepcopy(DEFAULT_PDF_OPTIONS)
    pdf_options.update(app.config.pyppeteer_pdf_options)
    app.config.pyppeteer_pdf_options = pdf_options


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension('sphinx.builders.html')

    app.add_builder(PyppeteerPDFBuilder)
    app.connect('config-inited', on_config_inited)

    app.add_config_value(
        'pyppeteer_theme_options',
        lambda self: self.html_theme_options,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_pdf_options',
        DEFAULT_PDF_OPTIONS,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_basename',
        lambda self: make_filename(self.project),
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_theme',
        lambda self: self.html_theme,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_title',
        lambda self: self.html_title,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_theme_path',
        lambda self: self.html_theme_path,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_short_title',
        lambda self: self.html_short_title,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_style',
        None,
        'pyppeteer',
        [str]
    )
    app.add_config_value(
        'pyppeteer_css_files',
        [],
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_show_copyright',
        True,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_show_sphinx',
        True,
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_main_selector',
        '',
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_footer_selector',
        '',
        'pyppeteer'
    )
    app.add_config_value(
        'pyppeteer_header_selector',
        '',
        'pyppeteer'
    )

    return {
        'version': version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
