import pytest
from crawto_doc import CrawtoClass, create_documentation
import astor
import ast


def test_crawto_doc():
    success = create_documentation(
        "tests/test_crawto_doc/start_test_crawto_doc.py",
        "tests/test_crawto_doc/results_test_crawto_doc.py")
    assert success

def test_docs_output(filename="tests/test_crawto_doc/start_test_crawto_doc.py",):
    tree = astor.code_to_ast.parse_file(filename)
    c_class = CrawtoClass(**tree.body[13].__dict__,doc_string=ast.get_docstring(tree.body[13]))
