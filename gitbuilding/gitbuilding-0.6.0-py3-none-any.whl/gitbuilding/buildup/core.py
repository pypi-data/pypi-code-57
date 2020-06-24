"""
This submodule contains the main BuildUp Documentation class.
"""

from copy import deepcopy
import logging
from dataclasses import is_dataclass
from gitbuilding.buildup.page import Page
from gitbuilding.buildup.libraries import Libraries
from gitbuilding.buildup.files import FileInfo
from gitbuilding.buildup.url import URLRules
from gitbuilding.buildup.link import LibraryLink
from gitbuilding.buildup.config import ConfigSchema

_LOGGER = logging.getLogger('BuildUp')

class Documentation:
    """
    This class represents the documentation in a BuildUp project. All other objects
    representing Pages, Libraries, Parts, Partlists, Links, etc are held within this
    the Documentation object. The most simple use of the Documentation object is to
    initialise it with a configuration and then run `buildall` with a list of input
    files.
    """

    def __init__(self, configuration, url_rules=None):

        self._landing_page = None
        self._pages = []
        self._libs = Libraries([])
        self._output_files = []
        if is_dataclass(configuration):
            self._input_config = configuration
        elif isinstance(configuration, dict):
            self._input_config = ConfigSchema().load(configuration)
        else:
            raise TypeError("configuration should be a dataclass or dictionary")
        self._config = deepcopy(self._input_config)

        if url_rules is None:
            self._url_rules = URLRules()
        else:
            if not isinstance(url_rules, URLRules):
                raise TypeError('url_rules must a URLRules object')
            self._url_rules = url_rules

    @property
    def config(self):
        """
        Read only property that returns the config object
        """
        return self._config

    @property
    def landing_page(self):
        """
        Somewhat confusing read only property. This option is the
        Page object of the landing page. `config.landing_page` is
        the path to the landing page. This may be changed in future
        versions!
        """
        return self._landing_page

    @property
    def pages(self):
        """Read only property that returns the list of pages (list of
        Page objects) in the documentation. The list is returned so any
        modifications to the returned list will affect the Documentation.
        """
        return self._pages

    @property
    def libs(self):
        """
        Read only property that returns the list of libraries (list of
        Library objects) in the documentation. The list is returned so any
        modifications to the returned list will affect the Documentation.
        """
        return self._libs

    @property
    def output_files(self):
        '''
        List of all output files as FileInfo objects
        '''
        return self._output_files

    @property
    def url_rules(self):
        '''
        Returns the URLRules object to set how output urls are formatted
        '''

        return self._url_rules

    def get_file(self, path):
        '''If a file with at this path in the output exists a
        FileInfo object is returned

        If the file is not in the output None is returned'''
        if path in self._output_files:
            return self.output_files[self.output_files.index(path)]
        return None


    def get_page_by_path(self, filepath):
        """
        Returns the page object matching the file path, or None if missing
        """
        if filepath in self._pages:
            return self._pages[self._pages.index(filepath)]
        return None

    def get_page_objects(self, path_list, warn=False):
        """
        Returns a list of valid page objects for an input list of paths. Any missing
        paths are silently ignored. Therefore an invalid input list results in an
        empty output list. Set `warn=True` to log a warning for each missing page
        """
        obj_list = []
        for path in path_list:
            if path in self._pages:
                obj_list.append(self.get_page_by_path(path))
            elif warn:
                _LOGGER.warning('Missing page "%s"', path)
        return obj_list

    def _create_all_pages(self, filelist):
        """
        Creates a Page object for each markdown page in the input filelist.
        """

        self._pages = []
        for file_obj in filelist:
            if file_obj.dynamic_content and file_obj.path.endswith('.md'):
                self._pages.append(Page(file_obj, self))


    def _check_landing_page(self):
        """
        Checks if the landing page exists. Also looks for index.md as this
        is the standard landing page once we change to html
        """

        if "index.md" in self._pages:
            if self._config.landing_page is None:
                self._config.landing_page = "index.md"
            elif self._config.landing_page != "index.md":
                _LOGGER.warning("Landing page is set to %s but also `index.md` exists. "
                                "This may cause unreliable behaviour",
                                self._config.landing_page)

        if self._config.landing_page in self._pages:
            self._landing_page = self._pages[self._pages.index(self._config.landing_page)]

    def _make_navigation(self):
        """
        If the navigation is not set in the configuration a Navigation
        is automatically created
        """
        url_translator = self.url_rules.create_translator('index.md')

        if self._landing_page is not None and len(self._landing_page.steps) > 0:
            pages = self.get_page_objects(self._landing_page.steps)
        else:
            pages = [page for page in self._pages if page != self._landing_page]

        for page in pages:
            link = url_translator.simple_translate(page.filepath)
            self._config.navigation.append({'title': page.summary, 'link': link})

    def _collate_output_files(self):
        """
        Returns a list of all files that need to be output
        for plain markdown output.
        """
        all_output_files = []

        for page in self._pages:
            all_output_files.append(FileInfo(page.filepath,
                                             dynamic_content=True,
                                             content=page.generate_output()))
            if page.bom_page is not None:
                all_output_files.append(page.bom_page)
            for link in page.all_links_and_images:
                linked_file = None
                if link.content_generated:
                    if isinstance(link, LibraryLink):
                        linked_file = self._libs.part_page(*link.library_location)
                else:
                    linked_file = link.as_output_file()
                if linked_file is not None:
                    if linked_file not in all_output_files:
                        all_output_files.append(linked_file)
        return all_output_files

    def buildall(self, filelist):
        """
        Builds the output documentation as a list of FileInfo objects based on the input
        documentation directory defined by `filelist` (also a list of FileInfo objects)
        """
        # By deepcopying the input config this refreshes the config state
        # if this is not the first time the documentation has run the config will
        # contain information generated from the buildup files, such as navigation or
        # project title
        self._config = deepcopy(self._input_config)
        self._libs = Libraries(filelist)
        self._create_all_pages(filelist)
        self._check_landing_page()

        if self._config.title is None:
            if self._config.landing_page is None:
                self._config.title = "Untitled project"
            else:
                self._config.title = self._landing_page.title

        # count parts and find steps on all pages
        for page in self._pages:
            _LOGGER.info('Changing page', extra={'set_active_page': page.filename})
            page.count_page()

        # build step_tree for all pages
        for page in self._pages:
            _LOGGER.info('Changing page', extra={'set_active_page': page.filename})
            page.get_step_tree()

        for page in self._pages:
            _LOGGER.info('Changing page', extra={'set_active_page': page.filename})
            page.count_all()

        _LOGGER.info('Changing page', extra={'set_active_page': None})

        self._make_navigation()
        self._output_files = self._collate_output_files()

        for filename in self._config.force_output:
            if filename not in self._output_files:
                try:
                    #append this file to the output list
                    self._output_files.append(filelist[filelist.index(filename)])
                except ValueError:
                    _LOGGER.warning('"%s" is on the forced output list but the file'
                                    'cannot be found', filename)

        return self._output_files
