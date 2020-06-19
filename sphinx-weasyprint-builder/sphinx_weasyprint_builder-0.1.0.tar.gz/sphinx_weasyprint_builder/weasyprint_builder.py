#!/usr/bin/env python3

import os
from typing import Dict, Set, Tuple
from copy import deepcopy

from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.util import progress_message
from sphinx.util.osutil import os_path
from sphinx.locale import __
from sphinx.util import logging

from bs4 import BeautifulSoup

import weasyprint
from .loghandler import init_wpsphinx_log


logger = logging.getLogger('weasyprint')


init_wpsphinx_log()


def extract(soup, selector: str) -> None:
    elements = soup.select(selector)
    for element in elements:
        element.extract()


class PdfGenerator:
    """
    From WeasyPrint 47 documentation Tips & Tricks
    """
    def __init__(
        self, base_url: str,
        main_selector: str,
        footer_selector: str,
        header_selector: str
    ) -> None:
        self.base_url = base_url
        with open(self.base_url) as htmlfile:
            self.main_html = htmlfile.read()

        self.footer_html = None
        self.header_html = None

        if not (footer_selector or header_selector):
            return

        if not main_selector:
            logger.error(
                __('You must define a selector for content if you set selector for footer or header.'))
            return

        main_soup = BeautifulSoup(self.main_html, 'html.parser')
        if footer_selector:
            footer_soup = deepcopy(main_soup)
            if header_selector:
                extract(footer_soup, header_selector)
            extract(footer_soup, main_selector)

        if header_selector:
            header_soup = deepcopy(main_soup)
            if footer_selector:
                extract(header_soup, footer_selector)
            extract(header_soup, main_selector)
            extract(main_soup, header_selector)

        if footer_selector:
            extract(main_soup, footer_selector)

        self.main_html = str(main_soup)
        if footer_soup:
            self.footer_html = str(footer_soup)

        if header_soup:
            self.header_html = str(header_soup)

    def _compute_overlay_element(self, element: str) -> weasyprint.HTML:
        html = weasyprint.HTML(
            string=getattr(self, f'{element}_html'),
            base_url=self.base_url,
        )
        element_doc = html.render()
        element_page = element_doc.pages[0]
        element_body = PdfGenerator.get_element(
            element_page._page_box.all_children(), 'body'
        )
        element_body = element_body.copy_with_children(
            element_body.all_children()
        )

        return element_body

    def _apply_overlay_on_main(
        self, main_doc, header_body=None, footer_body=None
    ) -> None:
        for page in main_doc.pages:
            page_body = PdfGenerator.get_element(
                page._page_box.all_children(), 'body'
            )

            if header_body:
                page_body.children += header_body.all_children()
            if footer_body:
                page_body.children += footer_body.all_children()

    def write_pdf(self, target: str) -> None:
        if self.header_html:
            header_body = self._compute_overlay_element(
                'header'
            )
        else:
            header_body = None
        if self.footer_html:
            footer_body = self._compute_overlay_element(
                'footer'
            )
        else:
            footer_body = None

        html = weasyprint.HTML(
            string=self.main_html,
            base_url=self.base_url,
        )
        main_doc = html.render()

        if self.header_html or self.footer_html:
            self._apply_overlay_on_main(main_doc, header_body, footer_body)
        main_doc.write_pdf(target)

    @staticmethod
    def get_element(boxes, element):
        for box in boxes:
            if box.element_tag == element:
                return box
            return PdfGenerator.get_element(box.all_children(), element)


class WeasyPrintPDFBuilder(SingleFileHTMLBuilder):
    name = 'weasyprint'
    epilog = __('The PDF file has been saved in %(outdir)s.')
    embedded = True
    search = False

    def _get_translations_js(self) -> str:
        return

    def copy_translation_js(self) -> None:
        return

    def copy_stemmer_js(self) -> None:
        return

    def copy_html_favicon(self) -> None:
        return

    def get_theme_config(self) -> Tuple[str, Dict]:
        return (
            self.config.weasyprint_theme,
            self.config.weasyprint_theme_options
        )

    def init_js_files(self) -> None:
        return

    def add_js_file(self, filename: str, **kwargs: str) -> None:
        return

    def prepare_writing(self, docnames: Set[str]) -> None:
        super(WeasyPrintPDFBuilder, self).prepare_writing(docnames)
        if self.config.weasyprint_style is not None:
            stylename = self.config.weasyprint_style
        elif self.theme:
            stylename = self.theme.get_config('theme', 'stylesheet')
        else:
            stylename = 'default.css'

        self.globalcontext['use_opensearch'] = False
        self.globalcontext['docstitle'] = self.config.weasyprint_title
        self.globalcontext['shorttitle'] = self.config.weasyprint_short_title
        self.globalcontext['show_copyright'] = \
            self.config.weasyprint_show_copyright
        self.globalcontext['show_sphinx'] = self.config.weasyprint_show_sphinx
        self.globalcontext['style'] = stylename
        self.globalcontext['favicon'] = None

    def finish(self) -> None:
        super(WeasyPrintPDFBuilder, self).finish()
        progress_message('Starting conversion to PDF with WeasyPrint')
        infile = os.path.join(
            self.outdir,
            os_path(self.config.master_doc) + self.out_suffix
        )
        outfile = os.path.join(
            self.outdir,
            self.config.weasyprint_basename + '.pdf'
        )
        generator = PdfGenerator(
            infile,
            self.config.weasyprint_main_selector,
            self.config.weasyprint_footer_selector,
            self.config.weasyprint_header_selector)
        generator.write_pdf(outfile)
