#!/usr/bin/env python3

import os
import asyncio
from typing import Dict, Set, Tuple

from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.util import progress_message, logging
from sphinx.util.osutil import os_path
from sphinx.locale import __

import pyppeteer
from .loghandler import init_ppsphinx_log


logger = logging.getLogger('pyppeteer*')


class PyppeteerPDFBuilder(SingleFileHTMLBuilder):
    name = 'pyppeteer'
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
            self.config.pyppeteer_theme,
            self.config.pyppeteer_theme_options
        )

    def init_js_files(self) -> None:
        return

    def add_js_file(self, filename: str, **kwargs: str) -> None:
        return

    def prepare_writing(self, docnames: Set[str]) -> None:
        super(PyppeteerPDFBuilder, self).prepare_writing(docnames)
        if self.config.pyppeteer_style is not None:
            stylename = self.config.pyppeteer_style
        elif self.theme:
            stylename = self.theme.get_config('theme', 'stylesheet')
        else:
            stylename = 'default.css'

        self.globalcontext['use_opensearch'] = False
        self.globalcontext['docstitle'] = self.config.pyppeteer_title
        self.globalcontext['shorttitle'] = self.config.pyppeteer_short_title
        self.globalcontext['show_copyright'] = \
            self.config.pyppeteer_show_copyright
        self.globalcontext['show_sphinx'] = self.config.pyppeteer_show_sphinx
        self.globalcontext['style'] = stylename
        self.globalcontext['favicon'] = None

    def finish(self) -> None:
        super(PyppeteerPDFBuilder, self).finish()
        progress_message('Starting conversion to PDF with Pyppeteer')
        infile = os.path.join(
            self.outdir,
            os_path(self.config.master_doc) + self.out_suffix
        )
        outfile = os.path.join(
            self.outdir,
            self.config.pyppeteer_basename + '.pdf'
        )

        url = 'file://' + infile
        pdf_options = self.config.pyppeteer_pdf_options
        pdf_options['path'] = outfile
        init_ppsphinx_log()

        evloop = asyncio.get_event_loop()
        evloop.run_until_complete(
            self.generate_pdf(url, pdf_options)
        )

    async def generate_pdf(self, url: str, pdf_options: dict) -> None:
        """
        Generate PDF

        Parameters
        ----------

        url:
            Url to the file

        pdf_options:
            Dict with options for the pdf coroutine
        """
        # Disable security to allow SVG use.
        browser = await pyppeteer.launch({
            'args': [
                '--allow-file-access-from-file',
                '--disable-web-security',
            ]
        })
        try:
            page = await browser.newPage()
            await page.goto(url)
            await page.pdf(pdf_options)
            await browser.close()
        finally:
            await browser.close()
