"""
Utility methods
"""
import logging
import shelve
import tempfile
from os.path import basename, join
from urllib.request import urlopen

from lxml import etree


LOGGER = logging.getLogger(__name__)


def get_schema(schemaurl):
    """
    Return XMLSchema from the specified location.
    """
    cachefile = join(tempfile.gettempdir(), basename(schemaurl))
    with shelve.open(cachefile) as cache:
        key = 'schemastr'
        # use cached contents if possible (can't pickle lxml objects or we'd
        # cache the schema instead of just the string)
        try:
            schemastr = cache[key]
        except KeyError:
            with urlopen(schemaurl) as url:
                schemastr = cache[key] = url.read()
    schematree = etree.fromstring(schemastr)
    schema = etree.XMLSchema(schematree)
    return schema


def validate(qp2file):
    """
    Returns: bool True if qp2file is valid XML and conforms to its schema,
                  else False
    """
    try:
        xmltree = etree.parse(qp2file)
        schemaurl = xmltree.getroot().attrib['validationSchema']
        schema = get_schema(schemaurl)
        schema.assertValid(xmltree)
    except Exception as ex:
        LOGGER.error(ex)
        return False
    return True
