"""
The main submodule for parsing BuildUp. This constains both the BuildUpParser class
and classes Links and Images. It also contains the function that parses the inline
part data.
"""

import re
import os
import logging

from gitbuilding.buildup.files import FileInfo

_LOGGER = logging.getLogger('BuildUp')

IMAGE_REGEX = r'(!\[([^\]]*)\]\(\s*([^\)\n\r\t\"]+?)\s*(?:\"([^\"\n\r]*)\")?\s*\))'

def _process_value(value, empty_is_true):
    if value is None:
        if empty_is_true:
            value = True
    else:
        #if not none it is a string.
        #Strip any whitespace from either end
        value = value.strip()
        if value.startswith(("'", '"')):
            #remove quotes from quoted values
            value = value[1:-1]
        elif value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
    return value

def parse_inline_data(data, empty_is_true=True):
    """
    Parses the inline key:value pair data. Keys are either strings or boolean
    set with the string "true" or "false" (case insensitive). To set the literal
    string true or false put the value in quotes. Keys are case insensive and can
    only contain the caracters a-z. Values should be in single or double qoutes
    unless they only contain alpha-numeric characters, spaces and or the literal
    `?` or `.` characters.
    """
    # This regex finds a key value pair at the start of the data string
    # the pair ends in the end of the string or a comma
    # The key can is case insensitve and can only be the letters a-z or _
    # The value can only have the letter a-z numbers, spaces, or anything in '?!.-_/%'
    # For any other characters the value should be in quotes
    reg = re.compile(r'^\s*([a-zA-Z_]+)(?:\s*:\s*'
                     r'''([a-zA-Z 0-9\?!\.\-_\/%]*|\"[^\n\r\"]*\"|\'[^\n\r\']*\'))?'''
                     r'\s*(?:$|,)')
    data_dict = {}
    alldata = data
    while len(data.lstrip()) > 0:
        match = reg.match(data)
        if match is None:
            _LOGGER.warning("Cannot parse the buildup data %s.", alldata)
            return None
        key = match.group(1)
        value = _process_value(match.group(2), empty_is_true=empty_is_true)
        data_dict[key.lower()] = value
        data = data[match.end(0):]
    return data_dict

class BuildUpParser():
    """
    This is main parser for reading the buildup.
    It is not really a parser, it is just about 8 or so regexs that find the BuildUp
    specific syntax.
    An object is initialised with the raw text to parse, the directory of the page the
    text is from so that the any relative links can be translated
    """

    def __init__(self, raw_text, page_dir):
        self._raw_text = raw_text
        self._page_dir = page_dir
        self._link_refs = []
        self._step_links = []
        self._part_links = []
        self._images = []
        self._plain_links = []

        self._find_links()

    @property
    def link_refs(self):
        """
        Returns a list of Link objects, one for each link reference in the page
        """
        return self._link_refs

    @property
    def step_links(self):
        """
        Returns a list of Link objects, one for each link to a step on the page
        """
        return self._step_links

    @property
    def part_links(self):
        """
        Returns a list of Link objects, one for each inline part link on the page
        """
        return self._part_links

    @property
    def images(self):
        """
        Returns a list of Image objects, one for each image
        """
        return self._images

    @property
    def plain_links(self):
        """
        Returns a list of Link objects, one for each link that is not a build up link
        """
        return self._plain_links

    @property
    def all_links(self):
        """
        Returns a list of Link objects, one for each link in the page.
        Doesn't return images. See all_links_and_images()
        """
        return self._plain_links+self._part_links+self._step_links

    @property
    def all_links_and_images(self):
        """
        Returns a list of Link and Image objects, one for each link/image
        in the page.
        """
        return self.all_links+self.images

    @property
    def in_page_steps(self):
        """
        Returns the in-page steps for your page in a dictionary with:
        heading, id, fullmatch
        """
        return self._get_in_page_steps()

    @property
    def steps(self):
        """
        Returns a simple list of the filespaths of all pages linked to a steps
        """
        return [link.link_rel_to_root for link in self._step_links]

    @property
    def inline_boms(self):
        """
        Returns a list of each fullmatch of the syntax for an in-line bill of materials
        """
        return re.findall(r"(\{\{[ \t]*BOM[ \t]*\}\})", self._raw_text, re.MULTILINE)

    @property
    def bom_links(self):
        """
        Returns a list of each fullmatch of the syntax for an in-line bill of materials
        """
        return re.findall(r"(\{\{[ \t]*BOMlink[ \t]*\}\})", self._raw_text, re.MULTILINE)

    @property
    def reference_defined_parts(self):
        """
        Returns a list of link objets for the parts defined by references
        """
        list_of_parts = []
        for link_ref in self._link_refs:
            if link_ref.build_up_dict is not None:
                list_of_parts.append(link_ref)
        return list_of_parts

    @property
    def inline_parts(self):
        """
        Returns a list of link objets for the parts defined inline
        """
        list_of_parts = []
        for part_link in self._part_links:
            list_of_parts.append(part_link)
        return list_of_parts

    def get_title(self):
        """
        Gets the page title by looking for the first heading with a single #
        """
        return self._match_title()[1]

    def get_title_match(self):
        """
        Gets the match to page title by looking for the first heading with a
        single #
        """
        return self._match_title()[0]

    def _match_title(self):
        headings = re.findall(r"(^#(?!#)[ \t]*(.*)$)",
                              self._raw_text,
                              re.MULTILINE)
        if len(headings) > 0:
            title = headings[0]
        else:
            title = ("", "")
        return title

    def _find_links(self):
        self._link_refs = self._get_link_references()
        all_build_up_links, self._plain_links = self._get_links()
        self._set_step_and_part_links(all_build_up_links)
        self._images = self._get_images()

    def _get_link_references(self):
        """
        Function to find link reference of any reference style links.
        Returns a list of Link objects
        """

        # Looking for link references. These must use "*" or '*' to define alt-text not (*)
        # Group 1: link text
        # Group 2: link location
        # Group 3: either a ' or a ", captured so regex can find the equivalent
        # Group 4: alt text
        link_ref_matches = re.findall(r"""(^[ \t]*\[(.+)\]:[ \t]*([^\"\' \t]*)"""
                                      r"""(?:[ \t]+(\"|')((?:\\\4|(?!\4).)*?)\4)?[ \t]*$)""",
                                      self._raw_text,
                                      re.MULTILINE)

        link_refs = []
        for link_ref in link_ref_matches:
            alttext = link_ref[4]
            # Search for buildup data in alt-text
            data_match = re.findall(r"""({([^:](?:[^}\'\"]|\'[^\'\r\n]*\')*)})""",
                                    alttext)
            if len(data_match) == 0:
                buildup_data = None
            else:
                if len(data_match) > 1:
                    _LOGGER.warning("Multiple sets of data found in link reference alt-text: %s",
                                    alttext)
                # Only match the last group of data found, warning if more than one
                # buildup_data is the text inside braces
                buildup_data = data_match[-1][1]
                # Replace all including braces
                alttext = alttext.replace(data_match[-1][0], "")
            if link_ref[2] == "":
                location = ""
            else:
                location = link_ref[2]
            link_ref_dict = {"fullmatch": link_ref[0],
                             "linktext": link_ref[1],
                             "linklocation": location,
                             "alttext": alttext,
                             "buildup_data": buildup_data}
            link_refs.append(Link(link_ref_dict,
                                  self._page_dir,
                                  link_type=Link.LINK_REF))

        return link_refs


    def _get_links(self):
        """
        Function to find all markdown links
        Returns two list of Link objects
        The first is a list of buildup links (links with {} after them)
        The second is a list of plain markdown links
        """

        build_up_links = []
        plain_links = []
        link_matches = re.findall(r'(?<!\!)(\[([^\[\]]+?)\]'
                                  r'(?:\(\s*(\S+)\s*(?:\"([^\"]+)\")?\s*\))?'
                                  r"""(?:{([^:](?:[^}\'\"]|"""
                                  r'\"[^\"\r\n]*\"|'
                                  r"\'[^\'\r\n]*\')*)})?)",
                                  self._raw_text,
                                  re.MULTILINE)

        for link in link_matches:
            if link[2] == "":
                linklocation = ""
            else:
                linklocation = link[2]
            link_dict = {"fullmatch": link[0],
                         "linktext": link[1],
                         "linklocation": linklocation,
                         "alttext": link[3],
                         "buildup_data": link[4]}
            link_obj = Link(link_dict, self._page_dir, link_references=self._link_refs)
            if link_obj.data is None:
                plain_links.append(link_obj)
            else:
                build_up_links.append(link_obj)
        return build_up_links, plain_links

    def _get_images(self):
        """
        Function to find images
        Returns a list of Image objects
        """

        # Find images in the text
        # Group 1: all
        # Group 2: alt-text
        # Group 3: image-path
        # group 4: hover text
        images_info = re.findall(IMAGE_REGEX,
                                 self._raw_text,
                                 re.MULTILINE)

        images = []
        for image in images_info:
            image_location = image[2]
            image_dict = {"fullmatch": image[0],
                          "alttext": image[1],
                          "imagelocation": image_location,
                          "hovertext": image[3]}
            images.append(Image(image_dict, self._page_dir, link_references=self._link_refs))
        return images

    def _set_step_and_part_links(self, all_build_up_links):
        """
        Sorts the links into the step links and part links
        """
        for link in all_build_up_links:
            link_info = link.build_up_dict
            if link_info is None:
                continue

            if "step" in link_info:
                if isinstance(link_info["step"], bool):
                    is_step = link_info["step"]
                else:
                    _LOGGER.warning("Invalid value given for `step` in %s. This link"
                                    " will be treated as a part.",
                                    link.fullmatch)
                    is_step = False
            else:
                is_step = False

            if is_step:
                if link.link_rel_to_page == "":
                    _LOGGER.warning("The link '%s' is a step, but links to nowhere.",
                                    link.fullmatch)
                self._step_links.append(link)
            else:
                self._part_links.append(link)

    def _get_in_page_steps(self):
        """
        Returns h2 headings with data info afterwards. Used to locate page steps.
        """

        in_page_steps = []
        step_ids = []

        # regex:
        # Group 1 (heading[0]) Full match
        # Group 2 (heading[1]) is the heading text
        # Group 3 (heading[2]) is the inline buildup data
        headings = re.findall(r"^(##(?!#)[ \t]*(.*?)[ \t]*{([^:][^}\n]*)})$",
                              self._raw_text,
                              re.MULTILINE)

        def clean_id(id_in):
            id_out = id_in.replace(' ', '-')
            id_out = id_out.lower()
            return re.sub(r'[^a-z0-9\_\-]', '', id_out)

        for heading in headings:
            heading_info = parse_inline_data(heading[2], empty_is_true=False)

            if "pagestep" in heading_info:
                step_id = heading_info["pagestep"]
                if step_id is None:
                    step_id = clean_id(heading[1])
                elif clean_id(step_id) != step_id:
                    old_id = step_id
                    step_id = clean_id(step_id)
                    _LOGGER.warning('Step ID "%s" not valid, changed to "%s"', old_id, step_id)

                if step_id not in step_ids:
                    step_ids.append(step_id)
                else:
                    _LOGGER.warning('Step ID "%s" is already used', step_id)
                in_page_steps.append({"heading": heading[1],
                                      "id": step_id,
                                      "fullmatch": heading[0]})
                del heading_info["pagestep"]

            if len(heading_info.keys()) > 0:
                keynames = ""
                for key in heading_info:
                    keynames += key + ", "
                _LOGGER.warning("Unused keys '%s' in heading [%s]",
                                keynames[:-2],
                                heading[1],
                                extra={'fussy':True})
        return in_page_steps


class Link():
    """
    A class for a link. Can is used to do a number of things from completing
    reference style links. Translating links to be relative to different pages
    and generating the output FileInfo objects.
    """
    LINK_REF = 0
    IN_LINE_FULL = 1
    IN_LINE_REF = 2

    def __init__(self, link_dict, page_dir, link_type=1, link_references=None):
        self._page_dir = page_dir
        self._fullmatch = link_dict["fullmatch"]
        self._linktext = link_dict["linktext"]
        self._link_type = link_type
        self._alttext = link_dict["alttext"]
        self._data = link_dict["buildup_data"]
        if self._data == "":
            self._data = None

        if self._link_type == self.LINK_REF:
            if link_dict["linklocation"].lower() in ['', "missing"]:
                self._linklocation = ''
                return

        self._linklocation = link_dict["linklocation"]
        if os.path.isabs(self._linklocation):
            _LOGGER.warning('Absolute path "%s" removed, only relative paths are supported.',
                            {self._linklocation})
            self._linklocation = ""

        if self.web_link:
            pass
        elif self._linklocation == "":
            #if is was a link_ref it would have returned above
            self._link_type = self.IN_LINE_REF
            if link_references is not None:
                self._complete_ref_style_link(link_references)
        else:
            self._linklocation = os.path.normpath(self._linklocation)

    def _complete_ref_style_link(self, link_references):
        """
        If this is a reference style link the link location is added
        from the link references
        """

        if self._linktext in link_references:
            ref_index = link_references.index(self._linktext)
            self._linklocation = link_references[ref_index].raw_linklocation

    @property
    def web_link(self):
        """
        Returns True if the link is a web link not a local link.
        """
        return re.match(r"^(https?:\/\/)", self._linklocation) is not None

    @property
    def library_link(self):
        """
        Returns True if the link is to a library part.
        """
        return self.library_location is not None

    @property
    def library_location(self):
        """
        If part is a library link returns a tuple of the library file
        and the part name.
        Returns None if is not a library link.
        """
        libmatch = self._library_match()
        if libmatch is None:
            return None
        library_path, _, part = libmatch
        return (library_path, part)

    def _library_match(self):
        """
        Matches whether the link is to a part in a library:
        Returns a tuple with the library path, the output directory
        for the library and the part name. If not a library link returns
        None
        """
        # match if the part's link is in the format `abc.yaml#abc` or
        # `abc.yml#abc`
        libmatch = re.match(r"^((.+)\.ya?ml)#(.+)$", self._linklocation)
        if libmatch is None:
            return None
        library_path = libmatch.group(1)
        #The directory the library will write to:
        library_dir = libmatch.group(2)
        part = libmatch.group(3)
        return (library_path, library_dir, part)

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
        Location of the link relative to the BuildUp page
        """
        libmatch = self._library_match()
        if libmatch is not None:
            _, library_dir, part = libmatch
            return os.path.join(library_dir, part+'.md')
        return self._linklocation

    @property
    def link_rel_to_root(self):
        """
        Location of the link relative to the root BuildUp directory
        """
        location = self.link_rel_to_page
        if location == "":
            return ""
        if self.web_link:
            return self._linklocation
        root_link = os.path.join(self._page_dir, location)
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
    def data(self):
        """
        Returns the buildup data text of the link, this will be none for links without
        data
        """
        return self._data

    @property
    def build_up_dict(self):
        """
        Returns the dictionary of buildup properties as set by the buildup data
        """
        if self.data is not None:
            link_info = parse_inline_data(self.data)
        else:
            link_info = None
        return link_info

    @property
    def content_generated(self):
        """Returns true if the content is generated in build up and otherwise
        return false"""
        #Note the link_rel_to_page has converted library links into .md links
        if self.link_rel_to_page.endswith('.md'):
            return True
        if self._linklocation.startswith('{{'):
            return True
        if self.location_undefined:
            return True
        return False

    def as_output_file(self):
        """ Returns the link as an FileInfo object.
        If the link is to a buildup file `None` is returned as this is generated
        elsewhere.
        `None` is also returned for a web link
        """
        if self.content_generated or self.web_link:
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

        if self.web_link:
            return self._linklocation
        return url_translator.translate(self)


class Image(Link):
    """
    A child class of Link to deal with the subtle differences of Links
    and Images in markdown.
    """

    def __init__(self, image_dict, page_dir, link_references=None):

        image_dict["linktext"] = ''
        image_dict["buildup_data"] = ''
        image_dict["linklocation"] = image_dict["imagelocation"]
        super(Image, self).__init__(image_dict,
                                    page_dir=page_dir,
                                    link_references=link_references)
        self._hovertext = image_dict["hovertext"]


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

    def _library_match(self):
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
