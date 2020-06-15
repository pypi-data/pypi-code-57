# File: vdex.py
#
# Copyright (c) 2007-2008 by Martin Raspe
# Bibliotheca Hertziana (Max-Planck-Institute for Art History), Rome, Italy
# This code was written for the ZUCCARO Project
# see http://zuccaro.biblhertz.it
#
# German Free Software License (D-FSL)
#
# This Program may be used by anyone in accordance with the terms of the
# German Free Software License
# The License may be obtained under <http://www.d-fsl.org>.

#

__author__ = "Martin Raspe, Jens Klein"
__docformat__ = "plaintext"

from collections import OrderedDict
from io import BytesIO
from lxml import etree
from xml.parsers.expat import ExpatError

import six
import string


VDEX_FLAT_PROFILE_TYPES = ("thesaurus", "glossaryOrDictionary", "flatTokenTerms")
FALSE_VALUES = ("", "0", "false", "False", "no", "No")


class VDEXError(Exception):
    """
    Denotes an error while handling an IMS-VDEX vocabulary with a VDEXManager
    """


class VDEXManager(object):
    """
    Reads an IMS-VDEX vocabulary and constructs a VocabularyDict for ArcheTypes.
      See "IMS Vocabulary Definition Exchange": http://www.imsglobal.org/vdex/.
      XML binding: http://www.imsglobal.org/vdex/vdexv1p0/imsvdex_bindv1p0.html
      Not yet supported:
          term/mediadescriptor elements
          relationship elements

    Two dimensional Matrix specification:
    The first row is always the header.
    The first headers start with Level X, whereas each column
    represents an additional depth level. If your vdex tree is 3 levels
    deep you will have three Level headers.
    The next columns are for each language.
    The order is alphabetical. For each language, two columns will be
    added, one named Caption XX, the other Description XX.
    A vocabulary with a depth of 3 levels and two languages will
    therefor have 7 columns.
    the other rows represent a single term of the vocabulary.
    A child element of one of the root elements would fill its
    key in the Column "Level 2" The other Level fields would be empty.
    A term of Level 2 will always be below its Level 1 term, with no
    other Level 1 term between them.
    To see an example, create a VDEXManager instance with a vdex file, and
    call the exportMatrix method.
    """

    vdex_namespace = "http://www.imsglobal.org/xsd/imsvdex_v1p0"
    default_language = "en"
    unnamed_term = "(unnamed term)"
    fallback_to_default_language = False
    order_significant = False
    term_dict = {}

    def __init__(
        self, file=None, matrix=None, lang=None, namespace=None, fallback=None
    ):
        """
        constructs a VDEX manager and parses a XML vocabulary
        file: a file or string that is parsed
        matrix: a two dimensional matrix that is parsed into a vdex file
        lang: set the default language for output ('*' for multilingual terms)
        namespace: declares the IMS-VDEX namespace in the vocab file
          ('' handles VDEX files without any declared namespace).
        fallback: if no translation is found for the given language
          should the term be returned in the default language
          or as self.unnamed_term ?
        """
        if isinstance(matrix, six.string_types):
            raise AttributeError(
                "This is the new imsvdex version. You "
                "tried to pass the default language as "
                "the matrix. Consider to use named arguments"
            )
        if lang is not None:
            self.default_language = lang
        if namespace is not None:
            self.vdex_namespace = namespace
        if fallback is not None:
            self.fallback_to_default_language = fallback
        if matrix is not None:
            self.parseMatrix(matrix)
        if file is not None:
            self.parse(file)
        if file and matrix:
            raise AttributeError(
                "You gave me a a matrix and a file, it is "
                "not defined what takes precedence. You may "
                "only set one of the two parameters"
            )

    def isVDEX(self):
        """
        checks if the parsed XML seems to be a valid VDEX vocabulary
        """
        # this method does not perform a complete schema validation
        # it just checks for a root element named 'vdex' in the expected  namespace
        return self.tree.getroot().tag == self.vdexTag("vdex")

    def parse(self, file):
        """
        parses a VDEX vocabulary file or XML string
        """
        if isinstance(file, bytes):
            file = BytesIO(file)
        elif isinstance(file, six.text_type):
            file = BytesIO(file.encode("utf-8"))
        try:
            self.tree = etree.parse(file)
        except (SyntaxError, ExpatError) as e:
            raise VDEXError("Parse error in vocabulary XML: %s" % e)
        try:
            filename = file.name
        except AttributeError:
            filename = "parsed XML text"
        if not self.isVDEX():
            raise VDEXError("Vocabulary format not correct in %s" % filename)
        self.order_significant = self.isOrderSignificant()
        self.makeTermDict()
        return self.tree

    def serialize(self, file=None):
        """
        returns the vocabulary as XML
        """
        return etree.tostring(self.tree, encoding="utf-8", standalone=True)

    def getVocabIdentifier(self):
        """
        returns the vocabulary identifier
        """
        xpath = self.vdexTag("vocabIdentifier")
        return self.tree.findtext(xpath)

    def getVocabName(self, lang=None):
        """
        returns the vocabulary name in the given (or default) language.
        If lang is '*', returns a dict of all translations keyed by language
        """
        xpath = "%s/%s" % (self.vdexTag("vocabName"), self.vdexTag("langstring"))
        captions = self.tree.findall(xpath)
        return self.getLangstring(captions, lang, default="(unnamed vocabulary)")

    def getVocabMetadata(self):
        """
        returns the VDEX metadata element(s) for the Vocabulary
        """
        xpath = self.vdexTag("metadata")
        return self.tree.getroot().findall(xpath)

    def getVocabWildcard(self, foreign_ns, tagname):
        """
        returns 'wildcard' element(s) (with a foreign namespace) for the Vocabulary
        """
        xpath = self.nsTag(foreign_ns, tagname)
        return self.tree.getroot().findall(xpath)

    def isFlat(self):
        """
        returns true if the VDEX profile type denotes a flat vocabulary
        """
        vdex = self.tree.getroot()
        return vdex.get("profileType") in VDEX_FLAT_PROFILE_TYPES

    def isOrderSignificant(self):
        """
        returns true if the order of the VDEX vocabulary is significant
        """
        vdex = self.tree.getroot()
        return vdex.get("orderSignificant") not in FALSE_VALUES

    def showLeafsOnly(self):
        """
        this is not declared in VDEX vocabs, so we return false
        """
        return False

    def getVocabularyDict(self, lang=None):
        """
        returns a vocabulary dictionary (for ArcheTypes) in the given language.
        If lang is '*', returns dicts of all translations keyed by language
        """
        return self.getTerms(self.tree.getroot(), lang)

    def getTerms(self, element, lang=None):
        """
        get all term elements recursively
          returns a hierarchic dictionary structure of the vocabulary
        """
        xpath = self.vdexTag("term")
        terms = element.findall(xpath)
        if len(terms) == 0:
            return None
        # we should not only test order significance globally, but also for every term
        if self.order_significant:
            result = OrderedDict()
        else:
            result = {}
        for term in terms:
            key = self.getTermIdentifier(term)
            value = self.getTermCaption(term, lang)
            result[key] = (value, self.getTerms(term, lang))
        return result

    def getTermIdentifier(self, term):
        """
        returns the termIdentifier for a given term element
        """
        xpath = self.vdexTag("termIdentifier")
        return term.findtext(xpath)

    def getTermCaption(self, term, lang=None):
        """
        returns the translated caption for a term
          for lang == "*" the method returns a dictionary with all translations
          keyed by language
        """
        if term is None:
            return None
        xpath = "%s/%s" % (self.vdexTag("caption"), self.vdexTag("langstring"))
        captions = term.findall(xpath)
        return self.getLangstring(captions, lang)

    def getTermDescription(self, term, lang=None):
        """
        returns the translated description for a term
          for lang == "*" the method returns a dictionary with all translations
          keyed by language
        """
        if term is None:
            return None
        xpath = "%s/%s" % (self.vdexTag("description"), self.vdexTag("langstring"))
        descriptions = term.findall(xpath)
        return self.getLangstring(descriptions, lang, default="")

    def getLangstring(self, elements, lang=None, default=None):
        """
        returns the langstring in the given language.
        for lang == "*" the method returns a dictionary with all translations
        keyed by language
        """
        if lang == "*":
            return self.getAllLangstrings(elements)
        if lang is None:
            lang = self.default_language
        if default is None:
            default = self.unnamed_term
        result = None
        for element in elements:
            if element.get("language") == lang:
                result = element.text
            if self.fallback_to_default_language:
                if element.get("language") == self.default_language:
                    default = element.text
        if result is None:
            result = default
        return result

    def getAllLangstrings(self, elements):
        """
        returns a dictionary with all translations keyed by language
        """
        return {element.get("language"): element.text for element in elements}

    def getTermById(self, identifier):
        """
        returns the VDEX term element for a given term identifier
        """
        return self.term_dict.get(identifier, None)

    def getTermCaptionById(self, identifier, lang=None):
        """
        returns the caption(s) for a given term identifier
        """
        term = self.getTermById(identifier)
        return self.getTermCaption(term, lang)

    def getTermDescriptionById(self, identifier, lang=None):
        """
        returns the description(s) for a given term identifier
        """
        term = self.getTermById(identifier)
        return self.getTermDescription(term, lang)

    def getTermMetadataById(self, identifier):
        """
        returns the VDEX metadata element(s) inside a term
          for a given term identifier
        """
        term = self.getTermById(identifier)
        xpath = self.vdexTag("metadata")
        return term.findall(xpath)

    def getTermWildcardById(self, identifier, namespace, tagname):
        """
        returns 'wildcard' element(s) (with a foreign namespace)
          inside a term for a given term identifier
        """
        term = self.getTermById(identifier)
        xpath = self.nsTag(namespace, tagname)
        return term.findall(xpath)

    def getTagname(self, nsname):
        # not needed here
        if not nsname[:1] == "{":
            return nsname
        namespace_uri, tagname = string.split(nsname[1:], "}", 1)
        return tagname

    def nsTag(self, namespace, tagname):
        """
        returns a tag with a namespace of the form '{namespace_uri}tagname'
          or just the tag name if an empty namespace was given
        """
        if namespace == "":
            return tagname
        else:
            return "{%s}%s" % (namespace, tagname)

    def vdexTag(self, tagname):
        """
        returns a tag with the VDEX namespace or just the tag name
          if the VDEX namespace is the empty string
        """
        return self.nsTag(self.vdex_namespace, tagname)

    def vdexSearchTerm(self, *tags):
        """
        return a Search path element with each tag of the list of
        tags concatenated by /
        """
        return "/".join([self.vdexTag(tag) for tag in tags])

    def makeTermDict(self):
        """
        constructs a flat dictionary of term elements, keyed by termIdentifier
        """
        # the .// prefix finds all items recursively
        xpath = ".//" + self.vdexTag("term")
        terms = self.tree.getroot().findall(xpath)
        self.term_dict = {}
        for term in terms:
            key = self.getTermIdentifier(term)
            self.term_dict[key] = term

    def exportMatrix(self):
        """
        Return a two dimensional matrix representation of the vdex file
        """
        # First full iteration, get all languages
        if not hasattr(self, "tree"):
            return []
        languages = sorted(
            filter(
                lambda x: x,
                set([x.attrib.get("language", "") for x in self.tree.findall("//*")]),
            )
        )
        depth = 0
        rows = []
        children_fathers_level = {}

        # Second full iteration. Convert xml tree to a flat python structure
        # Depth is maintained by an index, but parent relationships is only
        # maintained by ordering.
        for term in self.tree.findall("//" + self.vdexSearchTerm("term")):
            row = {}
            row["key"] = term.find(self.vdexSearchTerm("termIdentifier")).text.strip()
            captions = {}
            descriptions = {}
            for lang in languages:
                captions[lang] = ""
                descriptions[lang] = ""
            for caption in term.findall(self.vdexSearchTerm("caption", "langstring")):
                if "language" in caption.attrib:
                    captions[caption.attrib["language"]] = caption.text.strip()
            for description in term.findall(
                self.vdexSearchTerm("description", "langstring")
            ):
                if "language" in description.attrib:
                    descriptions[description.attrib["language"]] = (
                        description.text and description.text.strip() or ""
                    )
            row["captions"] = captions
            row["descriptions"] = descriptions

            # If this item is a child of something, the father must have
            # been parsed before, and stored its level in
            # children_fathers_level. Once for each child with the child
            # as the key
            father_level = children_fathers_level.get(term, -1)
            own_level = father_level + 1
            depth = max(own_level, depth)
            for child_term in term.findall(self.vdexSearchTerm("term")):
                children_fathers_level[child_term] = own_level
            row["level"] = own_level
            rows.append(row)

        # Now that we know the maximum depth of the tree, we can build the two
        # dimensional matrix.
        retval_rows = []
        header_row = ["Level %i" % x for x in range(depth + 1)]
        for lang in languages:
            header_row.extend(["Caption %s" % lang, "Description %s" % lang])
        retval_rows.append(header_row)
        for row in rows:
            retval_row = ["" for x in range(depth + 1 + 2 * len(languages))]
            retval_row[row["level"]] = row["key"]
            for lang_count, lang in enumerate(languages):
                offset = depth + 1
                retval_row[offset + lang_count * 2] = row["captions"][lang]
                retval_row[offset + lang_count * 2 + 1] = row["descriptions"][lang]
            retval_rows.append(retval_row)
        return retval_rows

    def parseMatrix(self, matrix):
        """
        Setup a manager based on a matrix
        """
        languages = []
        state = "Levels"
        parents = []
        for column, cell in enumerate(matrix[0]):
            if not (
                cell.startswith("Level ")
                or cell.startswith("Description ")
                or cell.startswith("Caption ")
            ):
                raise AttributeError("Data is not valid, unknown header")
            if state == "Levels":
                if cell.startswith("Level "):
                    parents.append(None)
                    continue
                elif cell.startswith("Caption "):
                    state = "Caption"
                    languages.append(cell[8:])
                    continue
                else:
                    raise AttributeError(
                        "Data is not valid, after Level " "header must come the caption"
                    )
            elif state == "Caption":
                if cell.startswith("Description "):
                    state = "Description"
                    continue
                else:
                    raise AttributeError(
                        "Data is not valid, after Caption "
                        "header must come the description"
                    )
            elif state == "Description":
                if cell.startswith("Caption "):
                    state = "Caption"
                    if not hasattr(languages, cell[8:]):
                        languages.append(cell[8:])
                    else:
                        raise AttributeError(
                            "Data is not valid, languages " "may not appear twice!"
                        )
                else:
                    raise AttributeError(
                        "Data is not valid, after Description"
                        " must come a new Caption"
                    )
            else:
                raise AttributeError(
                    "Programming error, unknown state during "
                    "Header parsing encountered. Sorry!"
                )
        depth = len(parents)

        def addSubElem(parent, elementName, text=None):
            retval = etree.SubElement(parent, self.vdexTag(elementName))
            if text is not None:
                retval.text = text
            return retval

        root = etree.Element(self.vdexTag("vdex"), nsmap={None: self.vdex_namespace})
        # WARNING!! We do a dirty trick here. When the first elements
        # Want to get their root element, they have a depth of 0
        # They will then ask for parents[0-1]. So it gets the last
        # element. Be aware of that!
        parents.append(root)
        for row in matrix[1:]:
            row_depth = None
            for i in range(depth):
                if row[i]:
                    if row_depth is not None:
                        raise AttributeError(
                            "The Matrix contains an element "
                            "can't decide on on which level "
                            "it should exist"
                        )
                    else:
                        row_depth = i
            parent = parents[row_depth - 1]
            term = addSubElem(parent, "term")
            parents[row_depth] = term
            addSubElem(term, "termIdentifier", row[row_depth])
            captions = [row[x] for x in range(len(parents) - 1, len(row), 2)]
            descriptions = [row[x] for x in range(len(parents), len(row), 2)]

            if any(captions):
                caption = addSubElem(term, "caption")
                for index, translation in enumerate(captions):
                    if not translation:
                        continue
                    langstring = addSubElem(caption, "langstring", translation)
                    langstring.attrib["language"] = languages[index]

            if any(descriptions):
                description = addSubElem(term, "description")
                for index, translation in enumerate(descriptions):
                    if not translation:
                        continue
                    langstring = addSubElem(description, "langstring", translation)
                    langstring.attrib["language"] = languages[index]

        self.tree = etree.ElementTree(root)
        self.order_significant = self.isOrderSignificant()
        self.makeTermDict()
