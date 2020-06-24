"""
This sub module contains the BaseLink class and its child classes Link,
LibraryLink, WebLink, and Image. Instead of constructing a Link, LibraryLink,
or WebLink use `make_link`. This will return the correct object type.
Image is used only for displaying images i.e. links that start with an !. For
a reference to an image use `make_link`.
"""

# Testing for this module is handled by test_buildup rather than directly running
# the functions as it provides a more realisic running of the objects.

import os
import re
import logging
from dataclasses import make_dataclass

from gitbuilding.buildup.files import FileInfo

_LOGGER = logging.getLogger('BuildUp')

def _fully_normalise_link(url, page):
    """
    in the case that the page is located at 'folder/page.md' and the url is
    '../folder/path.md'. os.path.normpath(url) does not collapse it to 'path.md'
    this will.
    """
    if url == '':
        return ''
    page_dir = os.path.dirname(page)
    joined = os.path.join(page_dir, url)
    joined = os.path.normpath(joined)
    return os.path.relpath(joined, page_dir)

def _complete_ref_style_link(linktext, link_references):
    """
    If this is a reference style link the link location is added
    from the link references
    """
    if link_references is None:
        return ""
    if linktext in link_references:
        ref_index = link_references.index(linktext)
        return link_references[ref_index].raw_linklocation
    return ""

def _is_web_link(linklocation):
    """
    Returns True if the link is a web link not a local link.
    """
    return re.match(r"^(https?:\/\/)", linklocation) is not None

def _library_match(linklocation):
    """
    Matches whether the link is to a part in a library:
    Returns a tuple with the library path, the output directory
    for the library and the part name. If not a library link returns
    None
    """
    # match if the part's link is in the format `abc.yaml#abc` or
    # `abc.yml#abc`
    libmatch = re.match(r"^((.+)\.ya?ml)#(.+)$", linklocation)
    if libmatch is None:
        return None
    library_path = libmatch.group(1)
    #The directory the library will write to:
    library_dir = libmatch.group(2)
    part = libmatch.group(3)
    return (library_path, library_dir, part)

_LINKINFO_CLS = make_dataclass('LinkInfo', ["fullmatch",
                                            "linktext",
                                            "linklocation",
                                            "alttext",
                                            "buildup_data"])

def make_link(link_dict, page, link_type=1, link_references=None):
    """
    Will create the correct link object, either Link, WebLink, or LibraryLink.
    link_type input should be BaseLink.LINK_REF (=0) or BaseLink.IN_LINE_FULL
    (=1 - default) depending on whether the link is a reference or and in-line
    link. If it is a reference style in-line link, the type will automatically
    adjust to BaseLink.IN_LINE_REF (=2).
    """
    link_info = _LINKINFO_CLS(**link_dict)
    if link_type != BaseLink.LINK_REF:
        if link_info.linklocation == "":
            link_type = BaseLink.IN_LINE_REF
            link_info.linklocation = _complete_ref_style_link(link_info.linktext,
                                                              link_references)
    if _is_web_link(link_info.linklocation):
        return WebLink(link_info, page, link_type)
    lib_match = _library_match(link_info.linklocation)
    if lib_match is not None:
        return LibraryLink(link_info, page, link_type, lib_match)
    return Link(link_info, page, link_type)

class BaseLink():
    """
    A base class for a link. Can is used to do a number of things from completing
    reference style links. Translating links to be relative to different pages
    and generating the output FileInfo objects. Do not use it directly. Use a the
    child class:
    * Image
    or the function
    the function `make_link`. This  will assign the correct type between `Link`,
    `WebLink`, and `LibraryLink`.
    """
    LINK_REF = 0
    IN_LINE_FULL = 1
    IN_LINE_REF = 2

    def __init__(self, link_info, page, link_type):
        self._page = page
        self._fullmatch = link_info.fullmatch
        self._linktext = link_info.linktext
        self._linklocation = link_info.linklocation
        self._link_type = link_type
        self._alttext = link_info.alttext
        self._data = link_info.buildup_data

    def __eq__(self, obj):
        return obj == self._linktext

    @property
    def fullmatch(self):
        """
        The full regex match for the link in the original BuildUp
        """
        return self._fullmatch

    @property
    def linktext(self):
        """
        The text inside the square brackets for the link in BuildUp
        """
        return self._linktext

    @property
    def raw_linklocation(self):
        """The raw input link location. Reference style links have
        location completed"""
        return self._linklocation

    @property
    def link_rel_to_page(self):
        """
        Link address relative to the BuildUp page
        """
        return _fully_normalise_link(self._linklocation, self._page)

    @property
    def link_rel_to_root(self):
        """
        Location of the link relative to the root BuildUp directory
        """
        location = self.link_rel_to_page
        if location == "":
            return ""
        page_dir = os.path.dirname(self._page)
        root_link = os.path.join(page_dir, location)
        root_link = os.path.normpath(root_link)
        return root_link

    @property
    def location_undefined(self):
        """
        Returns a boolean value stating whether the link is undefined
        """
        return self.link_rel_to_page == ""

    @property
    def alttext(self):
        """
        Returns the alt-text of the link
        """
        return self._alttext

    @property
    def build_up_dict(self):
        """
        Returns the dictionary of buildup properties as set by the buildup data
        """
        return self._data

    @property
    def content_generated(self):
        """Returns true if the content is generated in build up and otherwise
        return false"""
        #Note the link_rel_to_page has converted library links into .md links
        if self.link_rel_to_page.endswith('.md'):
            return True
        if self._linklocation.startswith('{{'):
            return True
        return False

    def as_output_file(self):
        """ Returns the link as an FileInfo object.
        If the link is to a buildup file `None` is returned as this is generated
        elsewhere.
        """
        if self.content_generated or self.location_undefined:
            return None
        return FileInfo(self.link_rel_to_root)

    def link_ref_md(self, url_translator):
        """
        Returns a plain markdown link reference for the link.
        Input is a URLTranslator object
        """
        location = self.output_url(url_translator)
        return f'[{self.linktext}]:{location} "{self.alttext}"'

    def link_md(self, url_translator, text_override=None):
        """
        Returns a plain markdown link for the link object, i.e. the part
        in the text not the reference.
        If this is a link reference object None is returned.
        Input is a URLTranslator object
        Optionally the link text can be overridden, this doesn't work for
        a reference style link as it would break it.
        """
        if self._link_type == self.LINK_REF:
            return None
        if self._link_type == self.IN_LINE_REF:
            return f'[{self.linktext}]'
        # A full inline link
        location = self.output_url(url_translator)
        if text_override is None:
            text = self.linktext
        else:
            text = text_override
        return f'[{text}]({location} "{self.alttext}")'

    def output_url(self, url_translator):
        """
        Uses url_translator a URLTranslator object
        to generate a link to the correct place.
        """
        return url_translator.translate(self)


class Link(BaseLink):
    '''
    A link to another file in the Documentation directory. See also LibraryLink
    and WebLink. This class should always be created with `make_link` which will
    create the correct link type. The child class Image can be created directly
    with its constructor.
    '''

    def __init__(self, link_info, page, link_type=1):
        super(Link, self).__init__(link_info, page, link_type)
        if self._link_type == self.LINK_REF:
            if self._linklocation.lower() == "missing":
                self._linklocation = ''
                return

        if os.path.isabs(self._linklocation):
            _LOGGER.warning('Absolute path "%s" removed, only relative paths are supported.',
                            {self._linklocation})
            self._linklocation = ""
        self._linklocation = self._linklocation

    @property
    def link_rel_to_root(self):
        """
        Location of the link relative to the root BuildUp directory
        """
        # Overloading to fix anchor only links
        location = self.link_rel_to_page
        if location.startswith('#'):
            return self._page+location
        return super(Link, self).link_rel_to_root


class WebLink(BaseLink):
    """
    A child class of BaseLink for links to external webpages. Bypasses
    most of the link translation, etc
    """

    @property
    def link_rel_to_page(self):
        """
        Returns just the url as it is a web link.
        """
        return self._linklocation

    @property
    def link_rel_to_root(self):
        """
        Returns just the url as it is a web link.
        """
        return self._linklocation

    def as_output_file(self):
        """
        Overload output file to None, as weblinks have no
        ouput file
        """
        return None

    def output_url(self, url_translator):
        """
        Overload output url to ignore translation
        """
        return self._linklocation

    @property
    def content_generated(self):
        return False


class LibraryLink(BaseLink):
    """
    A child class of BaseLink for links to parts in Libraries. It translates
    the from the link in the library to the final markdown page. Then other
    translations happen as standard.
    """

    def __init__(self, link_info, page, link_type, lib_match):
        super(LibraryLink, self).__init__(link_info, page, link_type)
        libname = _fully_normalise_link(lib_match[1], page)
        #The id/key in the part library
        self._part_id = lib_match[2]
        self._output_rel_to_page = os.path.join(libname,
                                                self._part_id+'.md')
        page_dir = os.path.dirname(page)
        root_link = os.path.join(page_dir, lib_match[0])
        #This is the libray relative to the root
        self._library_file = os.path.normpath(root_link)


    @property
    def link_rel_to_page(self):
        """
        Location of the output part page relative to the BuildUp page
        """
        return self._output_rel_to_page

    @property
    def library_location(self):
        """
        Returns a tuple of the library file (relative to the root dir) and the
        part name.
        """
        return (self._library_file, self._part_id)

    @property
    def content_generated(self):
        """
        Always returns true as LibraryLinks always generate content
        """
        return True


class Image(Link):
    """
    A child class of Link to deal with the subtle differences of Links
    and Images in markdown.
    """

    def __init__(self, image_dict, page, link_references=None):

        image_dict["linktext"] = ''
        image_dict["buildup_data"] = ''
        image_dict["linklocation"] = image_dict["imagelocation"]
        self._hovertext = image_dict["hovertext"]
        del image_dict["imagelocation"]
        del image_dict["hovertext"]
        link_info = _LINKINFO_CLS(**image_dict)
        if link_info.linklocation == "":
            link_type = BaseLink.IN_LINE_REF
            link_info.linklocation = _complete_ref_style_link(link_info.linktext,
                                                              link_references)
        else:
            link_type = BaseLink.IN_LINE_FULL

        super(Image, self).__init__(link_info,
                                    page=page,
                                    link_type=link_type)

    @property
    def image_rel_to_page(self):
        """
        Location of the image file relative to the BuildUp page
        """
        return self.link_rel_to_page

    @property
    def image_rel_to_root(self):
        """
        Location of the image file relative to the root BuildUp directory
        """
        return self.link_rel_to_root

    @property
    def hovertext(self):
        """
        Returns the hover text of the link
        """
        return self._hovertext

    def _library_match(self): # pylint: disable=no-self-use
        """
        This overrides the Link version of this functions and just
        returns false as an image cannot be a library.
        """
        return None

    def image_md(self, url_translator):
        """
        Returns a the plain markdown for the image
        """

        location = self.output_url(url_translator)
        return f'![{self.alttext}]({location} "{self.hovertext}")'

    def link_md(self, url_translator, _=None):
        """
        Redirects to `image_md`
        Perhaps warn if this is used?
        """
        return self.image_md(url_translator)
