import logging
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfFileReader

import subprocess

import bs4

from rho_pdf_diff.document import Document

logger = logging.getLogger(__name__)


class PDFToTextError(Exception):
    pass


def get_pdf_xml(path_to_pdf: str) -> bytes:
    """ Use pdftotext to generate text and bounding box info in XML format """
    try:
        xml = subprocess.check_output(['pdftotext', '-bbox',
                                       '-raw',  # This option retains the
                                       # ordering of text.
                                       path_to_pdf,
                                       '/dev/stdout'])
    except subprocess.CalledProcessError:
        raise PDFToTextError("pdftotext failed to extract text from {0}. The "
                             "document may not be a valid PDF"
                             .format(path_to_pdf))
    except Exception as e:
        logger.exception(e)
        raise e
    return xml


def decrypt(path_to_pdf: str):
    """ Use pdftops and epstopdf to replace an encrypted pdf with
     a decrypted versions."""
    with open(path_to_pdf, 'rb') as pdf_obj:
        is_encrypted = PdfFileReader(pdf_obj).isEncrypted
    if is_encrypted:
        # If it is, get around the encryption by converting to ps and back
        with NamedTemporaryFile() as tmp:
            subprocess.call(["pdftops", path_to_pdf, tmp.name])
            subprocess.call(["epstopdf", tmp.name, path_to_pdf])
            # How to ensure these are installed?
    return None


def build_document(path_to_pdf: str) -> Document:
    """ Create Document objects from pdf filepaths """
    xml = get_pdf_xml(path_to_pdf=path_to_pdf)
    decrypt(path_to_pdf=path_to_pdf)
    soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    doc_tag = soup.find('doc')
    doc = Document.from_xml(doc_tag=doc_tag)
    return doc
