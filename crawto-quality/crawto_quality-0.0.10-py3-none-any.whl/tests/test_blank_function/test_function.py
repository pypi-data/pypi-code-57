import pytest
from crawto_doc import CrawtoClass, create_documentation


def test_function():
    success = create_documentation("tests/test_blank_function/start_test_function.py", "tests/test_blank_function/results_test_function.py")
    assert success
