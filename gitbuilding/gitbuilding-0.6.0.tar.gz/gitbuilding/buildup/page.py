"""
This submodule deals with BuildUp pages. A Page object is created for each markdown
(buildup) file in the documentation directory.
"""

import os
import logging
from copy import copy
from gitbuilding.buildup.part import Part, PartList
from gitbuilding.buildup.buildup import BuildUpParser
from gitbuilding.buildup.files import FileInfo

_LOGGER = logging.getLogger('BuildUp')

class Page:
    """
    This class represents one BuildUp page. It can be used to: track its relation to
    other pages using the step_tree; to count the parts in the page; and to export a
    pure markdown page.
    """

    def __init__(self, file_obj, doc):
        self._file_obj = file_obj
        self._doc = doc
        self._title = ""
        self._overloaded_path = None

        self._raw_text = self.get_raw()
        self._part_list = PartList(self._doc)
        self._all_parts = None
        self._bom_page = None

        self._step_tree = None
        self._parser = BuildUpParser(self._raw_text, self.filepath)
        self._title = self._parser.get_title()

    @property
    def summary(self):
        """
        Page summary is either the title or the first 10 characters plus "..."
        """
        if self._title != "":
            return self.title
        if len(self._raw_text) > 17:
            return self._raw_text[:14]+'...'
        return self._raw_text

    @property
    def title(self):
        """
        Read only property that returns the title of the page as read
        from the fist H1 level title in page.
        """
        return self._title

    @property
    def filepath(self):
        """
        Read only property that the full filepath of the page relative to
        the root directory of the documentation
        """
        return self._file_obj.path

    @property
    def pagedir(self):
        '''
        The directory of the input page
        '''
        return os.path.dirname(self.filepath)

    @property
    def filename(self):
        '''
        The filename of the input page and output pages
        '''
        return os.path.basename(self.filepath)

    @property
    def counted(self):
        '''
        Sets whether the main part list has been counted (this happens after running
        count_page)
        '''
        return self._part_list.counted

    @property
    def part_list(self):
        """
        Returns the part list for the page this is a PartList object.
        """
        return self._part_list

    @property
    def steps(self):
        """
        Returns a list of all the steps in the page (as the url relative to the root
        of the project). This is only the steps defined in the page. Not the full tree.
        This comes directly from the parser there is no garuntee that the the url
        refers to a valid page!
        """
        return self._parser.steps

    @property
    def images(self):
        """
        Returns a list of Image objects, one for each image
        """
        return self._parser.images

    @property
    def plain_links(self):
        """
        Returns a list of Link objects, one for each link that is not a build up link
        """
        return self._parser.plain_links

    @property
    def all_links(self):
        """
        Returns a list of Link objects, one for each link in the page.
        Doesn't return images. See all_links_and_images()
        """
        return self._parser.all_links

    @property
    def all_links_and_images(self):
        """
        Returns a list of Link and Image objects, one for each link/image
        in the page.
        """
        return self._parser.all_links_and_images

    @property
    def bom_page(self):
        """
        Returns the FileInfo object for the bill of materials page if
        it has been created. Will return None is no OutputFil object has
        been created.
        """
        return self._bom_page

    @property
    def _url_translator(self):
        if self._overloaded_path is None:
            filepath = self.filepath
        else:
            filepath = self._overloaded_path
        return self._doc.url_rules.create_translator(filepath)

    @property
    def _part_url_translator(self):
        if self._overloaded_path is None:
            filepath = self.filepath
        else:
            filepath = self._overloaded_path
        return self._doc.url_rules.create_translator(filepath,
                                                     part_translator=True)

    def rebuild(self, md, overload_path=None):
        """
        This is to replace the raw text and rebuild.
        This can be used to live edit a single page.
        md is the input markdown to use instead of the pages markdown
        overload_path is used to overload the path input to the
          URL_Translator. This is useful if you are displaying the
          live edited text and a different URL.
        """

        self._overloaded_path = overload_path
        _LOGGER.info('Changing page', extra={'set_active_page': self.filename})
        self._raw_text = md

        self._part_list = PartList(self._doc)
        self._all_parts = None
        self._step_tree = None
        self._bom_page = None

        self._parser = BuildUpParser(self._raw_text, self.filepath)

        self._title = self._parser.get_title()
        self.count_page()
        self.get_step_tree()
        self.count_all()
        result = self.generate_output()
        _LOGGER.info('Changing page', extra={'set_active_page': None})
        self._overloaded_path = None
        return result

    def __eq__(self, other):
        """
        Checks for equality using the file name. Used to find pages in lists.
        """
        return self.filepath == other

    def get_raw(self):
        """
        Returns the raw BuildUp file contents.
        """
        return self._file_obj.content

    def count_page(self):
        """
        Counts all of the part on the page and puts them into a PartList object
        """

        for part_link in self._parser.reference_defined_parts:
            part = Part(part_link, self._doc, indexed=True)
            self._part_list.append(part)
        for part_link in self._parser.inline_parts:
            part = Part(part_link, self._doc, indexed=False)
            self._part_list.count_part(part)

        # Once part refs all scanned, if qty for page was undefined initially
        # set to quantity used.
        self._part_list.finish_counting()

    def get_all_parts(self):
        """
        Returns an aggregate list of all parts for the page.
        This must be called after the pages has been counted.
        """

        if self._all_parts is None:
            self.count_all()
        return self._all_parts

    def count_all(self):
        """
        Creates an aggregate list of parts for the page.
        This aggregate lists if for parts on the page and for any parts in pages
        linked to with a step link. This counting is recursive through step links.
        """
        if not self.counted:
            raise RuntimeError("Page trying to form aggregate list before counting.")

        if self._all_parts is None:
            self._all_parts = PartList(self._doc, AggregateList=True)
            self._all_parts.merge(self._part_list)
            for step in self._doc.get_page_objects(self.steps):
                self._all_parts.merge(step.get_all_parts())

    def _write_bom(self, processed_text):
        """
        Write the bill of the materials into text and links to the bill of materials
        page if required. Currently also builds the BOM page - split later
        """
        # Add all BOMs into the page
        boms = self._parser.inline_boms
        if len(boms) > 0:
            bom_text = self._all_parts.bom_md(self._doc.config.page_bom_title,
                                              self._part_url_translator,
                                              exclude_refs=self._part_list)
        for bom in boms:
            processed_text = processed_text.replace(bom, bom_text)

        # Add links to bill of materials page and make page
        bom_links = self._parser.bom_links
        if len(bom_links) > 0:
            self._bom_page = self.make_bom_page()
        for bomlink in bom_links:
            bom_url = self._url_translator.simple_translate(self._bom_page.path)
            processed_text = processed_text.replace(bomlink, f"{bom_url}")
        return processed_text

    def _write_in_page_step_headings(self, processed_text):
        """
        Writes in the headings for each in-page step. Adds ID for in-page links,
        and class for fancy CSS
        """
        for i, in_page_step in enumerate(self._parser.in_page_steps):
            kramdown_block = "{:"
            kramdown_block += f'id="{in_page_step["id"]}" '
            kramdown_block += 'class="page-step"}'
            step_heading = f"## Step {i+1}: {in_page_step['heading']} {kramdown_block}"
            processed_text = processed_text.replace(in_page_step["fullmatch"],
                                                    step_heading)
        return processed_text

    def _replace_step_links(self, processed_text):
        """
        Takes replaces all step links it with processed markdown
        """

        for link in self._parser.step_links:
            #Overriding the input link text if it was just a .
            text_override = None
            if link.linktext == ".":
                page = self._doc.get_page_by_path(link.link_rel_to_root)
                if page is not None:
                    text_override = page.title
            rep_text = link.link_md(self._url_translator, text_override)
            processed_text = processed_text.replace(link.fullmatch,
                                                    rep_text)
        return processed_text

    def _replace_plain_links(self, processed_text):
        """
        Takes replaces all non buildup links it with processed markdown
        the only processing here is the url translation rules
        """
        for link in self._parser.plain_links:
            rep_text = link.link_md(self._url_translator)
            processed_text = processed_text.replace(link.fullmatch,
                                                    rep_text)
        return processed_text

    def _replace_images(self, processed_text):
        """
        Takes replaces all images it with processed markdown
        the only processing here is the url translation rules
        """
        for image in self._parser.images:
            rep_text = image.image_md(self._url_translator)
            processed_text = processed_text.replace(image.fullmatch,
                                                    rep_text)
        return processed_text

    def _replace_part_links(self, processed_text):
        """
        Takes replaces all part links with processed (Kramdown) markdown
        """
        for link in self._parser.part_links:
            rep_text = f'[{link.linktext}]'
            part = self._part_list.getpart(link.linktext)
            if part is not None:
                if part.link.location_undefined:
                    rep_text += '{: Class="missing"}'
            processed_text = processed_text.replace(link.fullmatch, rep_text)
        return processed_text

    def _replace_link_refs(self, processed_text):
        """
        Takes replaces link references with BuildUp data and replace it with a
        standard markdown link reference.
        """

        for link_ref in self._parser.link_refs:
            translator = self._url_translator
            if link_ref.linktext in self._part_list:
                translator = self._part_url_translator
            processed_text = processed_text.replace(link_ref.fullmatch,
                                                    link_ref.link_ref_md(translator))
        return processed_text

    def _add_missing_link_refs(self, processed_text):
        """
        Adds link reference for any part that doesn't have one
        """
        for part in self._part_list:
            refnames = [ref.linktext for ref in self._parser.link_refs]
            if part.name not in refnames:
                processed_text += "\n"
                processed_text += part.link.link_ref_md(self._part_url_translator)
        return processed_text

    def generate_output(self):
        """
        Does the final stages of building the output markdown
        """

        processed_text = copy(self._raw_text)
        if self == self._doc.landing_page:
            if self._doc.config.remove_landing_title:
                processed_text = processed_text.replace(self._parser.get_title_match(), "", 1)
        processed_text = self._write_bom(processed_text)
        processed_text = self._write_in_page_step_headings(processed_text)
        processed_text = self._replace_step_links(processed_text)
        processed_text = self._replace_part_links(processed_text)
        processed_text = self._replace_images(processed_text)
        processed_text = self._replace_plain_links(processed_text)
        processed_text = self._replace_link_refs(processed_text)
        processed_text = self._add_missing_link_refs(processed_text)

        return processed_text

    def get_step_tree(self, breadcrumbs=None):
        """
        This function traverses returns the step tree for a page. Any page that is
        finding its current step tree should pass it's breadcrumbs
        """

        if breadcrumbs is None:
            breadcrumbs = []
        else:
            breadcrumbs = copy(breadcrumbs)

        if self.filepath in breadcrumbs:
            trail = ''
            for crumb in breadcrumbs:
                trail += crumb + ' -> '
            trail += self.filepath
            _LOGGER.warning("The steps in the documentation form a loop! [%s] "
                            "This can cause very weird behaviour.",
                            trail,
                            extra={'this':'that'})
            return {self.filepath: []}

        if self._step_tree is None:
            breadcrumbs.append(self.filepath)
            self._parse_step_tree(breadcrumbs)
        return self._step_tree

    def _parse_step_tree(self, breadcrumbs=None):
        """
        This function traverses the steps in the page to create a complete downward step tree
        it uses the same function of other steps until all pages downstream have completed.
        Breadcrumbs showing the path down the step tree is passed on to allow checks for loops
        in the step definition. This stops infinite loops occurring.
        """
        if breadcrumbs is None:
            breadcrumbs = [self.filepath]

        list_of_subtrees = []
        for step in self._doc.get_page_objects(self.steps, warn=True):
            list_of_subtrees.append(step.get_step_tree(breadcrumbs))
        # Note that page object is not hashable so the step tree key is the path.
        self._step_tree = {self.filepath: list_of_subtrees}

    def make_bom_page(self):
        """
        Makes separate Bill of materials page for the all parts on this page (including those
        in steps). Returns the filepath of the resulting file and the markdown in a dictionary
        """

        filepath = self.filepath[:-3] + "_BOM.md"
        # Bill of material markdown
        # Fine to use self._url_translator as the BOM page will be in same
        # output directory
        md = self._all_parts.bom_md("# Bill of Materials",
                                    self._url_translator)

        return FileInfo(filepath,
                        dynamic_content=True,
                        content=md)
