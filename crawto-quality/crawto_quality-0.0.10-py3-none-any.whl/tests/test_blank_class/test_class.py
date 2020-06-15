import pytest
from crawto_doc import CrawtoClass, create_documentation, DocStringParser, Parameter,Attribute
import astor
import ast

def test_class():
    success = create_documentation("tests/test_blank_class/start_test_class.py", "tests/test_blank_class/results_test_class.py")
    assert success

def test_docs_output(filename="tests/test_blank_class/start_test_class.py"):
    a = astor.code_to_ast.parse_file(filename)
    c_class = CrawtoClass(**a.body[0].__dict__,doc_string=ast.get_docstring(a))
    docs = c_class.docs
    dsp = DocStringParser(docs)
    assert dsp.description == '"""<#TODO Description>'
    # assert dsp.parameters[0] == Parameter(name="strategy", type_annotation='<#TODO type definition>', default_value='warn')
    # assert dsp.parameters[1] ==Parameter(name='random_state', type_annotation='<#TODO type definition>', default_value='None')
    # assert dsp.parameters[2] ==Parameter(name='constant', type_annotation='<#TODO type definition>', default_value='None')
    #
    # assert dsp.attributes[0] == Attribute(name='sparse_output_', type_annotation='<#TODO Attribute Description>', default_value='no_default')
    # assert dsp.attributes[1] == Attribute(name='n_outputs_', type_annotation='<#TODO Attribute Description>', default_value='no_default')
    # assert dsp.attributes[2] == Attribute(name='n_features_in_', type_annotation='<#TODO Attribute Description>', default_value='no_default')
    assert dsp.example_string

    #        == """>>> from crawto-quality import crawto_doc
    # >>> example = DummyClassifier(strategy=warn, random_state=None, constant=None)
    # >>> example.fit(X=<#TODO Example Value>, y=<#TODO Example Value>, sample_weight=None)
    #     <#TODO Method Return Value>
    # >>> example.predict(X=<#TODO Example Value>)
    #     <#TODO Method Return Value>
    # >>> example.predict_proba(X=<#TODO Example Value>)
    #     <#TODO Method Return Value>
    # >>> example.predict_log_proba(X=<#TODO Example Value>)
    #     <#TODO Method Return Value>
    # >>> example.score(X=<#TODO Example Value>, y=<#TODO Example Value>, sample_weight=None)
    #     <#TODO Method Return Value>
    # >>> example.outputs_2d_() \
    #     <#TODO Method Return Value>
    #     """
