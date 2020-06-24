"""
This module handles all the Builder classes that produce outputs.
Currently the outputs are
* HTML provided by StaticSiteBuilder
* Markdown provided by MarkdownBuilder
to make a custom Builder you can inherit from the Builder class.
"""

import os
import shutil
import logging
from gitbuilding.render import GBRenderer, URLRulesHTML
from gitbuilding.buildup import Documentation, URLRules, read_directory
from gitbuilding.config import load_config_from_file
from gitbuilding import utilities

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

class Builder():
    """
    Base class for Builder classes. Do not use this class.
    """

    def __init__(self, conf, url_rules, rem_title=False):
        """
        `conf is the configuration file`
        rem_title is set to true to override configuration and
        remove the title from the landing page
        """
        configuration = load_config_from_file(conf)
        if rem_title:
            configuration.remove_landing_title = True
        license_file = utilities.handle_licenses(configuration)
        self._doc = Documentation(configuration, url_rules)
        file_list = read_directory('.', exclude_list=configuration.exclude)
        if license_file is not None:
            file_list.append(license_file)
        self._doc.buildall(file_list)
        self._out_dir = "_build"

    @property
    def doc(self):
        """
        Returns the buildup Documentation object for the site.
        """
        return self._doc

    def _make_clean_directory(self):
        """
        Make a clean and empty directory for the static html
        """
        if os.path.exists(self._out_dir):
            shutil.rmtree(self._out_dir)
        os.mkdir(self._out_dir)

    def build(self):  # pylint: disable=no-self-use
        """
        This method should be overridden for in derived classes
        """
        raise RuntimeError('`build` should be overridden by other Builder classes')

class MarkdownBuilder(Builder):
    """
    Class to build a markdown directory from a BuildUp directory.
    """

    def __init__(self, conf, url_rules=None):
        """
        `conf is the configuration file`
        """

        if url_rules is None:
            url_rules = URLRules(rel_to_root=False)

        def fix_missing(url, anchor):
            if url == "" and  anchor == "":
                return "missing.md", anchor
            return url, anchor

        url_rules.add_modifier(fix_missing)

        super(MarkdownBuilder, self).__init__(conf, url_rules)


    def _write_missing_page(self):
        """
        Write the page for any part which is missing from the documentation
        """
        missing_page_file = os.path.join(self._out_dir, "missing.md")
        with open(missing_page_file, "w", encoding='utf-8') as html_file:
            html_file.write("# GitBuilding Missing Part")

    def _build_file(self, outfile):
        """
        Writes the markdown for any buildup page and copies over other
        output files
        """
        if outfile.path.startswith('..'):
            _LOGGER.warning('Skipping %s.', outfile.path)
            return
        full_out_path = os.path.join(self._out_dir, outfile.path)
        full_out_dir = os.path.dirname(full_out_path)
        if not os.path.exists(full_out_dir):
            os.makedirs(full_out_dir)
        if outfile.dynamic_content:
            with open(full_out_path, "w", encoding='utf-8') as output_file:
                output_file.write(outfile.content)
        else:
            if os.path.exists(outfile.location_on_disk):
                if not os.path.isdir(outfile.location_on_disk):
                    shutil.copy(outfile.location_on_disk, full_out_path)

    def build(self):
        """
        Builds the whole markdown folder
        """

        self._make_clean_directory()
        self._write_missing_page()
        for outfile in self.doc.output_files:
            self._build_file(outfile)

class StaticSiteBuilder(Builder):
    """
    Class to build a static website from a BuildUp directory.
    """

    def __init__(self, conf, url_rules=None):
        """
        `conf is the configuration file`
        """

        if url_rules is None:
            url_rules = URLRulesHTML()

        super(StaticSiteBuilder, self).__init__(conf, url_rules, rem_title=True)

        root = self._doc.config.website_root

        self._renderer = GBRenderer(self._doc.config, root=root)

        # site dir is not setable as we would then need to do all the checks for
        # not writing over a specific directory
        self._out_dir = "_site"

    def _write_missing_page(self):
        """
        Write the page for any part which is missing from the documentation
        """
        missing_page_file = os.path.join(self._out_dir, "missing.html")
        with open(missing_page_file, "w", encoding='utf-8') as html_file:
            html_file.write(self._renderer.missing_page())

    def _build_file(self, outfile):
        """
        Writes the HTML for any .md page
        Copies any other files to the static site directory
        """
        if outfile.path.startswith('..'):
            _LOGGER.warning('Skipping %s.', outfile.path)
            return
        full_out_path = os.path.join(self._out_dir, outfile.path)
        full_out_dir = os.path.dirname(full_out_path)
        if not os.path.exists(full_out_dir):
            os.makedirs(full_out_dir)
        if outfile.dynamic_content:
            if outfile.path == self.doc.config.landing_page:
                full_out_path = os.path.join(self._out_dir, "index.html")
            else:
                full_out_path = os.path.splitext(full_out_path)[0]+'.html'
            with open(full_out_path, "w", encoding='utf-8') as html_file:
                page_html = self._renderer.render_md(outfile.content,
                                                     os.path.splitext(outfile.path)[0],
                                                     editorbutton=False)
                html_file.write(page_html)
        else:

            if os.path.splitext(full_out_path)[1] == '.stl':
                html_path = os.path.splitext(full_out_path)[0]+'.html'
                with open(html_path, "w", encoding='utf-8') as html_file:
                    page_html = self._renderer.stl_page(outfile.path)
                    html_file.write(page_html)
            if os.path.exists(outfile.location_on_disk):
                if not os.path.isdir(outfile.location_on_disk):
                    shutil.copy(outfile.location_on_disk, full_out_path)

    def _copy_static_files(self):
        """
        Copies all the static web files that come as default with gitbuilding.
        This includes the CSS, the favicons, and the 3D viewer
        """
        gbpath = os.path.dirname(__file__)
        static_dir = os.path.join(gbpath, "static")
        for root, _, files in os.walk(static_dir):
            for filename in files:
                if not "live-editor" in root or "local-server" in root:
                    filepath = os.path.join(root, filename)
                    out_file = os.path.join(self._out_dir, os.path.relpath(filepath, gbpath))
                    out_dir = os.path.dirname(out_file)
                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)
                    shutil.copy(filepath, out_file)

    def _copy_local_assets(self):
        """
        Copies all assets from the local directory. This is custom CSS and favicons
        """
        for root, _, files in os.walk("assets"):
            for filename in files:
                filepath = os.path.join(root, filename)
                out_file = os.path.join(self._out_dir, filepath)
                out_dir = os.path.dirname(out_file)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                shutil.copy(filepath, out_file)

    def build(self):
        """
        Builds the whole static site
        """

        self._make_clean_directory()
        self._write_missing_page()
        for outfile in self.doc.output_files:
            self._build_file(outfile)
        self._copy_static_files()
        if os.path.exists("assets"):
            self._copy_local_assets()
