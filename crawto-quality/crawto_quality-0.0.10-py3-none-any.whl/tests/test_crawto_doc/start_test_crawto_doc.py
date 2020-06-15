import astor  # type: ignore
import ast
from itertools import zip_longest
import os
import re
import argparse
from dataclasses import dataclass
from typing import List, Optional, Union, Tuple, Any

ASTtype = Union[ast.arg, ast.Assign, ast.If, ast.Return]


class CrawtoDocBase:
    @property
    def docs_offset(self):
        self._docs_offset = (self.ast_col_offset + 4) * " "
        return self._docs_offset

    @docs_offset.setter
    def docs_offset(self):
        return self._docs_offset

    @property
    def description(self) -> str:
        if not self.doc_string:
            self._description = f"""<#TODO Description>\n"""
            return self._description
        self._description = """{self.doc_string}"""
        return self._description

    @description.setter
    def description(self):
        return self._description

    @staticmethod
    def check_dunder(function_name: str):
        return re.fullmatch(r"__[a-z]+__", function_name)

    @staticmethod
    def check_internal_method(function_name: str) -> bool:
        return function_name[0] == "_"

    @staticmethod
    def check_property_decorators(ast_function: ast.FunctionDef) -> bool:
        for i in ast_function.decorator_list:
            if type(i) is ast.Name and i.id == "property":
                return True
            elif type(i) is ast.Attribute:
                return True
        return False

    @staticmethod
    def import_statement() -> Tuple[str, str]:
        dirname, file = os.path.split(os.path.abspath(__file__))
        dirname = dirname.split(os.sep)[-1]
        file = file.split(".")[0]
        return dirname, file


class CrawtoClass(CrawtoDocBase):
    def __init__(
        self,
        *,
        bases: List,
        body: List,
        col_offset: int,
        decorator_list: List,
        end_col_offset: int,
        end_lineno: int,
        keywords,
        lineno,
        name: str,
        doc_string: Optional[str] = None,
    ):
        self.ast_bases = bases
        self.ast_body = body
        self.ast_col_offset = col_offset
        self.ast_decorator_list = decorator_list
        self.ast_end_col_offset = end_col_offset
        self.ast_end_lineno = end_lineno
        self.ast_keywords = keywords
        self.ast_lineno = lineno
        self.ast_name = name
        self.doc_string = doc_string

    @property
    def init(self):
        for i in self.ast_body:
            if type(i) is ast.FunctionDef and i.name == "__init__":
                self._init = CrawtoFunction(
                    **i.__dict__, doc_string=ast.get_docstring(i), class_=self.ast_name
                )
                self._init.__setattr__("ast_col_offset", self.ast_col_offset)
                return self._init

    @init.setter
    def init(self):
        return self._init

    @property
    def attributes(self):
        self._attributes = (
            f"""\n{self.docs_offset}Attributes\n{self.docs_offset}----------"""
        )
        methods = self.methods
        assigns = [
            assign
            for method in methods
            for assign in method.ast_body
            if type(assign) is ast.Assign
        ]
        attrs = [
            target.attr
            for targets in assigns
            for target in targets.targets
            if type(target) is ast.Attribute
        ]
        for i in attrs:
            self._attributes += (
                f"""\n{self.docs_offset}{i} : <#TODO Attribute Description>\n"""
            )
        return self._attributes

    @attributes.setter
    def attributes(self):
        return self._attributes

    @property
    def bases(self):
        self._bases = [i.id for i in self.ast_bases]
        return self._bases

    @bases.setter
    def bases(self):
        return self._bases

    @property
    def methods(self):
        self._methods = [
            CrawtoFunction(
                **i.__dict__, doc_string=ast.get_docstring(i), is_method=True
            )
            for i in self.ast_body
            if (
                type(i) is ast.FunctionDef
                and not self.check_dunder(i.name)
                and not self.check_internal_method(i.name)
                and not self.check_property_decorators(i)
            )
        ]
        return self._methods

    @methods.setter
    def methods(self):
        return self._methods

    @property
    def example(self):
        self._example = f"""\n{self.docs_offset}Examples\n{self.docs_offset}--------"""
        dirname, file = self.import_statement()
        self._example += f"""\n{self.docs_offset}>>> from {dirname} import {file}"""
        self._example += f"""\n{self.docs_offset}>>> example = {self.ast_name}({self.init.args.example_inputs})"""
        for method in self.methods:
            self._example += f"""\n{self.docs_offset}>>> example.{method.ast_name}({method.args.example_inputs})"""
            self._example += f"""\n{self.docs_offset}<#TODO Method Return Value>"""
        return self._example

    @example.setter
    def example(self):
        return self._example

    @property
    def docs(self):
        f = f""
        f += f"{self.description}"
        if self.init:
            f += f"{self.init.parameters}"
        try:
            f += f"""{self.attributes}"""
        except AttributeError:
            pass
        try:
            f += f"""{ self.example}"""
        except AttributeError:
            pass
        self._docs = f'"""{f}\n{self.docs_offset}"""'
        return self._docs

    @docs.setter
    def docs(self):
        return self._docs

    @property
    def method_docs_dict(self):
        self._method_docs_dict = {k.ast_name: k.docs for k in self.methods}
        return self._method_docs_dict

    @method_docs_dict.setter
    def method_docs_dict(self):
        return self._method_docs_dict


class CrawtoFunction(CrawtoDocBase):
    def __init__(
        self,
        *,
        args: List,
        body: List,
        col_offset: int,
        decorator_list: List,
        end_col_offset: int,
        end_lineno: int,
        lineno: int,
        name: str,
        returns,
        type_comment,
        doc_string: Optional[str] = None,
        is_method: bool = False,
        class_=None,
    ):
        self.ast_args = args
        self.ast_body = body
        self.ast_col_offset = col_offset
        self.ast_decorator_list = decorator_list
        self.ast_end_col_offset = end_col_offset
        self.ast_end_lineno = end_lineno
        self.ast_lineno = lineno
        self.ast_name = name
        self.ast_returns = returns
        self.ast_type_comment = type_comment
        self.doc_string = doc_string
        self.is_method = is_method
        self.class_ = class_

    @property
    def args(self):
        self._args = CrawtoArgs(**self.ast_args.__dict__)
        return self._args

    @args.setter
    def args(self):
        return self._args

    @property
    def parameters(self):
        self._parameters = (
            f"""\n{self.docs_offset}Parameters\n{self.docs_offset}----------\n"""
        )
        for i in self.args.arg_list:
            self._parameters += (
                f"""{self.docs_offset}{i.name} : {i.type_def}{i.default}\n\n"""
            )
        return self._parameters

    @parameters.setter
    def parameters(self):
        return self._parameters

    @property
    def returns(self):
        if self.ast_name != "__init__":
            return_value = None
            if type(self.ast_body[-1]) is ast.Return:
                try:
                    return_value = self.ast_body[-1].value.id
                except AttributeError:
                    return_value = "<#TODO return value>"
            self._return = (
                f"""\n{self.docs_offset}Returns\n{self.docs_offset}-------\n"""
            )
            self._return += (
                f"""{self.docs_offset}{return_value} : <#TODO return description>"""
            )
            return self._return

    @returns.setter
    def returns(self):
        return self._returns

    @property
    def example(self):
        if not self.is_method:
            self._example = (
                f"""\n\n{self.docs_offset}Examples\n{self.docs_offset}--------"""
            )
            dirname, file = self.import_statement()
            self._example += f"""\n{self.docs_offset}>>> from {dirname} import {file}"""
            self._example += f"""\n{self.docs_offset}>>> {self.ast_name}({self.args.example_inputs})"""
            self._example += f"""\n{self.docs_offset}<#TODO Method Return Value>"""
        else:
            self._example = ""
        return self._example

    @example.setter
    def example(self):
        return self._example

    @property
    def docs(self):
        f = self.description + self.parameters
        if self.returns:
            f += self.returns
        f += self.example
        f += f"""\n{self.docs_offset}"""
        self._docs = f'"""{f}"""'
        return self._docs

    @docs.setter
    def docs(self):
        return self._docs


class CrawtoArgs:
    def __init__(
        self,
        posonlyargs: List,
        args: List,
        vararg: Optional[ast.arg],
        kwonlyargs: List,
        kw_defaults: List,
        kwarg: Optional[ast.arg],
        defaults: List,
    ):
        self.ast_posonlyargs = posonlyargs
        self.ast_args = args
        self.ast_vararg = vararg
        self.ast_kwonlyargs = kwonlyargs
        self.ast_kw_defaults = kw_defaults
        self.ast_kwarg = kwarg
        self.ast_defaults = defaults

    @property
    def arg_list(self):
        # args
        args = self.ast_args[::-1]
        defaults = self.ast_defaults[::-1]
        arg_default = [
            Arg(name=k.arg, ast_annotation=k.annotation, default_input=v,)
            for k, v in zip_longest(args, defaults, fillvalue="no_default")
            if k.arg != "self"
        ][::-1]
        # vararg
        if self.ast_vararg is not None:
            vararg = [
                Arg(
                    name=self.ast_vararg.arg,
                    ast_annotation=self.ast_vararg.annotation,
                    default_input="no_default",
                )
            ]
        else:
            vararg = []
        # kwargs
        if self.ast_kwarg is not None:
            kwargs = [
                Arg(
                    name=self.ast_kwarg.arg,
                    ast_annotation=self.ast_kwarg.annotation,
                    default_input="no_default",
                )
            ]
        else:
            kwargs = []
        # keyword args
        kwonlyargs = self.ast_kwonlyargs
        kw_defaults = self.ast_kw_defaults
        keywords = [
            Arg(name=k.arg, ast_annotation=k.annotation, default_input=v)
            for k, v in zip(kwonlyargs, kw_defaults)
            if k.arg != "self"
        ]
        self._arg_list = arg_default + vararg + keywords + kwargs
        return self._arg_list

    @arg_list.setter
    def arg_list(self):
        return self._arg_list

    @property
    def example_inputs(self):
        self._example_inputs = ", ".join(
            [f"{i.name}={i.example}" for i in self.arg_list]
        )
        return self._example_inputs

    @example_inputs.setter
    def example_inputs(self):
        return self._example_inputs


@dataclass
class Arg:
    name: str
    default_input: Union[ast.Constant, str]
    ast_annotation: Optional[ast.Name]

    @property
    def default(self):
        if self.default_input is None:
            self._default = f", default=None"
        elif self.default_input != "no_default":
            self._default = f", default={self.default_input.value}"
        else:
            self._default = ""
        return self._default

    @default.setter
    def default(self):
        return self._default

    @property
    def example(self):
        if self.default_input == "no_default":
            self._example = "<#TODO Example Value>"
        elif self.default_input.value is None:
            self._example = str(self.default_input.value)
        else:
            self._example = f"""'{str(self.default_input.value)}'"""
        return self._example

    @example.setter
    def example(self):
        return self._example

    @property
    def type_def(self):
        if self.type_annotation is None:
            self._type_def = "<#TODO type definition>"
        else:
            self._type_def = self.type_annotation
        return self._type_def

    @type_def.setter
    def type_def(self):
        return self._type_def

    @property
    def type_annotation(self):
        if (
            type(self.ast_annotation) is ast.Subscript
            or type(self.ast_annotation) is ast.Attribute
        ):
            self._type_annotation = self.ast_annotation.value.id
        elif self.ast_annotation:
            self._type_annotation = self.ast_annotation.id
        else:
            self._type_annotation = self.ast_annotation
        return self._type_annotation

    @type_annotation.setter
    def type_annotation(self):
        return self._type_annotation


def add_class_doc_to_ast(ast_class: ast.ClassDef) -> None:
    classdef = CrawtoClass(
        **ast_class.__dict__, doc_string=ast.get_docstring(ast_class)
    )
    class_docstring = classdef.docs
    new_class_doc = [ast.parse(class_docstring).body[0]]
    if ast.get_docstring(ast_class):
        ast_class.body.pop(0)
    ast_class.body = new_class_doc + ast_class.body
    for j in ast_class.body:
        if type(j) is ast.FunctionDef and j.name in classdef.method_docs_dict.keys():
            method_docstring = classdef.method_docs_dict[j.name]
            new_method_doc = [ast.parse(method_docstring).body[0]]
            if ast.get_docstring(j):
                j.body.pop(0)
            j.body = new_method_doc + j.body


def add_function_doc_to_ast(ast_function: ast.FunctionDef) -> None:
    functiondef = CrawtoFunction(
        **ast_function.__dict__, doc_string=ast.get_docstring(ast_function)
    )
    function_docstring = ast.parse(functiondef.docs)
    expr = function_docstring.body[0]
    new_function_doc = [expr]
    if ast.get_docstring(ast_function):
        ast_function.body.pop(0)
    ast_function.body = new_function_doc + ast_function.body


def create_documentation(filename: str, new_filename: str) -> str:
    a = astor.code_to_ast.parse_file(filename)
    for i in a.body:
        if type(i) is ast.ClassDef:
            add_class_doc_to_ast(i)
        elif type(i) is ast.FunctionDef:
            add_function_doc_to_ast(i)
    y = ast.fix_missing_locations(a)
    y = astor.to_source(y)
    with open(new_filename, "w") as new_file:
        new_file.write(y)
    return f"Successfully saved the documented file at {new_file}"


class DocStringParser:
    def __init__(self, doc_string: str):
        self.doc_string: str = doc_string
        description, ignore, remainder = self.doc_string.rpartition(
            "Parameters\n    ----------\n"
        )
        self.description = description.strip()
        self.parameter_string, ignore, remainder = remainder.rpartition(
            "Attributes\n    ----------\n"
        )
        self.attribute_string, ignore, remainder = remainder.rpartition(
            "Examples\n    --------\n"
        )
        self.example_string: str = remainder.strip()
        if (
            self.description
            and self.parameter_string
            and self.attribute_string
            and self.example_string
        ):
            self.conforming_docstring: bool = True

    @staticmethod
    def parse_attr_param_doc_string(doc_string_part: str) -> List:
        param_list = doc_string_part.split("\n\n")
        param_list = [i.strip() for i in param_list]
        return [
            list(
                map(
                    lambda x: x.strip(),
                    (i.split(":")[0], *i.split(":")[1].split(", default=")),
                )
            )
            for i in param_list
            if i
        ]

    @property
    def parameters(self):
        params = self.parse_attr_param_doc_string(self.parameter_string)
        self.params = [Parameter(*i) for i in params]
        return self.params

    @property
    def attributes(self):
        attrs = self.parse_attr_param_doc_string(self.attribute_string)
        self.attrs = [Attribute(*i) for i in attrs]
        return self.attrs


@dataclass
class Parameter:
    name: str
    type_annotation: str
    default_value: str


@dataclass
class Attribute:
    name: str
    type_annotation: str
    default_value: str = "no_default"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file you need to document", type=str)
    parser.add_argument("new_file", help="the name of the new file", type=str)
    args = parser.parse_args()
    success = create_documentation(args.file, args.new_file)
    print(success)
