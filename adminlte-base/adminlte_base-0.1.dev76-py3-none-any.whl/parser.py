from collections import deque
from contextlib import contextmanager
import glob
from io import StringIO
import itertools
import logging
import os
import pathlib
import re
from textwrap import indent
import types

from jinja2 import Environment, FileSystemLoader, select_autoescape, Markup
from jinja2 import nodes


logger = logging.getLogger(__name__)


OPERATOR_PRIORITIES = {
    '**': 100,
    'u+': 90, 'u-': 90,
    '*': 80, '/': 80, '%': 80, '//': 80,
    '+': 70, '-': 70,
    'eq': 60, 'ne': 60, 'gt': 60, 'gteq': 60, 'lt': 60, 'lteq': 60,
    'in': 50, 'notin': 50,
    'is': 40, 'isnot': 40,
    'not': 30,
    'and': 20,
    'or': 10,
}


def not_supported_syntax(msg=None):
    msg = msg or 'Syntax does not support.'
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            original = getattr(JinjaCodeGenerator, func.__name__)
            src = original(self, *args, **kwargs)
            return self.syntax_error(f'{src}: {msg}', args[0].lineno)
        return wrapper
    return decorator


class Error(Exception):
    pass


class SyntaxError(Error):
    """Синтаксическая ошибка при генерации конечного шаблона."""


class Config(dict):
    """Application configuration."""

    def load(self, filename):
        """Loads a configuration from the Python module and updates the current settings."""
        m = types.ModuleType('config')
        m.__file__ = filename

        with open(filename, mode='rb') as f:
            exec(compile(f.read(), filename, 'exec'), m.__dict__)

        for prop in dir(m):
            if prop.isupper():
                self[prop] = getattr(m, prop)

    def get_only(self, option_prefix):
        """Returns options whose names begin with the specified prefix."""
        result = {}

        for key, val in self.items():
            if key.startswith(option_prefix):
                key = key.replace(option_prefix, '').lower()
                result[key] = val

        return result


class Converter(object):
    __generators_map = {}

    def __init__(self, output_syntax):
        self.config = Config()
        self.config.setdefault('OUTPUT_SYNTAX', output_syntax)
        # self.env = Environment(**self.config.get_only('ENVIRONMENT_'))

    @classmethod
    def attach_code_generator(cls, name, class_=None):
        """Adds new target template syntax."""
        def decorator(class_):
            cls.__generators_map[name] = class_
            return class_

        if class_ is None:
            return decorator

        if callable(class_):
            return decorator(class_)

        raise Error('Invalid argument class_')

    def convert(self, source_stream, output_stream):
        """
        Converts a template to the syntax of the  target template engine.

        Arguments
            source_stream (io.TextIOWrapper): the stream that contains the source code for the template.
            output_stream (io.TextIOWrapper): the stream to which the result will be written.
        """
        env = Environment(**self.config.get_only('ENVIRONMENT_'))
        ast = env.parse(source_stream.read())
        output_stream.write(
            self.get_code_generator().ast2str(ast)
        )

    # def execute(self, name):
    #     source, filename, uptodate = self.env.loader.get_source(self.env, name)
    #     ast = self.env.parse(source)
    #     print(self.get_code_generator().ast2str(ast))

    def get_code_generator(self):
        """Gets the code generator instance for the current syntax."""
        syntax = self.config['OUTPUT_SYNTAX']
        class_ = self.__generators_map.get(syntax)

        if class_ is None:
            raise Error(f'Not found code generator for "{syntax}" syntax.')

        return class_(**self.config.get_only('GENERATOR_'))

    @classmethod
    def get_supported_syntax(cls):
        """Returns a list of syntax available for conversion."""
        return cls.__generators_map.keys()


class CodeGenerator(object):
    #: Разделитель параметров функций и элементов последовательностей
    arguments_separator = ', '

    block_start_string = '{% '
    block_end_string = ' %}'
    variable_start_string = '{{ '
    variable_end_string = ' }}'

    #: Синтаксис вызова функции
    call_function_template = '{name}({arguments})'

    #: Отображение имен фильтров шаблонизатора Jinja в имена фильтров целевого шаблонизатора
    builtin_filters = {}

    #: Отображение имен функций исходного шаблона в имена функций целевого шаблонизатора
    builtin_functions_mapper = {}

    #: Отображение операторов исходного шаблона в операторы целевого шаблонизатора
    operators_mapper = {
        'eq': '==',
        'ne': '!=',
        'gt': '>',
        'gteq': '>=',
        'lt': '<',
        'lteq': '<=',
        'not': 'not',
        'notin': 'not in',
        'isnot': 'is not',
        'u+': '+',
        'u-': '-',
    }

    def __init__(self, silent=False, functions_mapper=None):
        """
        Arguments:
            silent (bool):
            functions_mapper (dict):
        """
        self.counter = itertools.count()
        self.silent = silent
        self.functions_mapper = {
            **self.builtin_functions_mapper,
            **(functions_mapper or {})
        }

    def ast2str(self, node: nodes.Template):
        """Returns the generated code for the target template engine using AST."""
        return self.nodes2str(node.body)

    def get_block_stmt(self, s, *args, sep=' '):
        """Returns an instruction wrapped in a template syntax tag."""
        s = sep.join([i for i in [s, *args] if i])
        return f'{self.block_start_string}{s}{self.block_end_string}'

    def get_operator(self, oper):
        """Returns the operator for the target template engine."""
        return self.operators_mapper.get(oper, oper)

    def get_operator_priority(self, oper):
        """Returns the priority of the operator."""
        return OPERATOR_PRIORITIES.get(oper, 0)

    def get_print_stmt(self, s):
        """Returns an instruction wrapped in template output tags."""
        return f'{self.variable_start_string}{s}{self.variable_end_string}'

    def get_unique_identifier(self):
        """Get a new unique identifier."""
        return f'var_{next(self.counter)}'

    def node2str(self, node, **kwargs):
        """Returns the node as a string."""
        node_type = node.__class__.__name__.lower()
        method = getattr(self, f'{node_type}2str', None)

        if method is None:
            raise Error(f'Unsupported node type "{node_type}".')

        return method(node, **kwargs)

    def marksafeifautoescape2str(self, node: nodes.MarkSafeIfAutoescape):
        # fixme: !!!!!!!
        return self.node2str(node.expr)

    def nodes2str(self, nodes, sep=''):
        """Returns all passed nodes as a string."""
        return sep.join(filter(None, map(self.node2str, nodes)))

    def syntax_error(self, msg, lineno=0, fallback=''):
        """Выбрасывает исключение."""
        if not self.silent:
            raise SyntaxError(msg)
        logger.warning(f'Line {lineno}: {msg}')
        return fallback

    # Constants, variables ans getters

    @not_supported_syntax()
    def assign2str(self, node: nodes.Assign):
        """Returns the assignment statement as a string."""

    def const2str(self, node: nodes.Const, **_):
        """Returns a constant value as a string."""
        return repr(node.value)

    def args2native(self, args):
        """Возвращает позиционные аргументы, приведенные к типу tuple."""
        result = []

        for arg in args:
            if not isinstance(arg, str):
                arg = self.node2str(arg)
            result.append(arg)

        return tuple(result)

    def dict2native(self, node: nodes.Dict):
        """Возвращает узел, являющийся словарем, приведеный к типу dict."""
        result = {}

        for node in node.items:
            result[self.name2str(node.key)] = self.node2str(node.value)

        return result

    def dict2str(self, d: nodes.Dict):
        """Возвращает узел, являющийся словарем, в виде строки."""
        return '{%s}' % self.arguments_separator.join(
            f'{k}: {v}' for k, v in self.dict2native(d).items()
        )

    def getattr2str(self, node: nodes.Getattr, **_):
        """Возвращает в виде строки обращение к атрибуту объекту."""
        return '{}.{}'.format(self.node2str(node.node), node.attr)

    def getitem2str(self, node: nodes.Getitem, **_):
        """Возвращает в виде строки обращение к объекту по ключу."""
        return '{}[{}]'.format(self.node2str(node.node), self.node2str(node.arg))

    def kwargs2native(self, kwargs):
        """Возвращает именованные аргументы, приведенные к типу dict."""
        return {i.key: self.node2str(i.value) for i in kwargs}

    def list2str(self, node: nodes.List):
        """Возвращает узел, являющийся списком, в виде строки."""
        return '[%s]' % self.nodes2str(node.items, sep=self.arguments_separator)

    def name2str(self, node: nodes.Name, **_):
        """Возвращает имя идентификатора в виде строки."""
        return node.name

    def tuple2str(self, node: nodes.Tuple):
        """Возвращает узел, являющийся кортежем, в виде строки."""
        result = self.nodes2str(node.items, sep=self.arguments_separator)
        return f'({result})' if node.ctx == 'load' else result

    @not_supported_syntax()
    def with2str(self, node: nodes.With):
        """Returns the with statement makes it possible to create a new inner scope as a string."""

    # Operators

    def _binexpr2str(self, node: nodes.BinExpr, parent_priority=None):
        """Возвращает выражение с бинарным оператором в виде строки."""
        return self._make_expression(node.operator, node.left, node.right, parent_priority=parent_priority)

    def _make_expression(self, oper, left, right, parent_priority=None):
        """Возвращает выражение с одним или двумя операндами с учетом приоритета."""
        priority = self.get_operator_priority(oper)
        result = deque([self.get_operator(oper)])

        if left is not None:
            result.appendleft(self.node2str(left, parent_priority=priority))

        if right is not None:
            result.append(self.node2str(right, parent_priority=priority))

        return self.prioritize(' '.join(result), priority, parent_priority)

    def _test2str(self, node: nodes.Test, parent_priority=None, operator='is'):
        """Возвращает выражение с оператором IS, либо NOT IS в виде строки."""
        result = '{} {} {}'.format(self.node2str(node.node), self.get_operator(operator), node.name)

        arguments = self.arguments2str(node.args, node.kwargs, node.dyn_args, node.dyn_kwargs)
        if arguments:
            result += f'({arguments})'

        return self.prioritize(result, self.get_operator_priority(operator), parent_priority)

    def _unaryexpr2str(self, node: nodes.UnaryExpr, parent_priority=None):
        """Возвращает выражение с унарным оператором в виде строки."""
        return self._make_expression(node.operator, None, node.node, parent_priority=parent_priority)

    add2str = _binexpr2str
    sub2str = _binexpr2str
    mul2str = _binexpr2str
    div2str = _binexpr2str
    mod2str = _binexpr2str
    floordiv2str = _binexpr2str
    pow2str = _binexpr2str
    and2str = _binexpr2str
    or2str = _binexpr2str

    def compare2str(self, node: nodes.Compare, parent_priority=None):
        """Возвращает выражение с операторами сравнения в виде строки."""
        priority = self.get_operator_priority(node.ops[0].op)
        result = [
            self.node2str(node.expr, parent_priority=priority)
        ]

        for op in node.ops:
            result.append(self._make_expression(op.op, None, op.expr))

        return self.prioritize(' '.join(result), priority, parent_priority)

    def neg2str(self, node: nodes.Neg, parent_priority=None):
        """Возвращает выражение с унарным оператором - в виде строки."""
        node.operator = 'u-'
        return self._unaryexpr2str(node, parent_priority=parent_priority)

    def not2str(self, node: nodes.Not, parent_priority=None):
        """Возвращает выражение с логическим оператором NOT в виде строки."""
        if isinstance(node.node, nodes.Test):
            return self.test2str(node.node, parent_priority=parent_priority, operator='isnot')
        return self._unaryexpr2str(node, parent_priority=parent_priority)

    def pos2str(self, node: nodes.Pos, parent_priority=None):
        """Возвращает выражение с унарным оператором + в виде строки."""
        node.operator = 'u+'
        return self._unaryexpr2str(node, parent_priority=parent_priority)

    def prioritize(self, expr, priority, parent_priority):
        """Wraps the passed expression in parentheses if the priority of the parent statement is higher."""
        if parent_priority and priority < parent_priority:
            return f'({expr})'
        return expr

    def test2str(self, node: nodes.Test, parent_priority=None, operator='is'):
        """Возвращает выражение с оператором IS, либо NOT IS в виде строки."""
        test_type = f'test_{node.name}'
        method = getattr(self, test_type, self._test2str)
        return method(node, parent_priority=parent_priority, operator=operator)

    # Output

    def _do_filter2str(self, value, name, args, kwargs, dyn_args, dyn_kwargs):
        output = f'{value}|{name}'
        arguments = self.arguments2str(args, kwargs, dyn_args, dyn_kwargs)
        return f'{output}({arguments})' if arguments else output

    def filter2str(self, node: nodes.Filter):
        """Возвращает значение, к которому применен фильтр в виде строки."""
        name = node.name

        if name in self.builtin_filters:
            name = self.builtin_filters[name]

        return self._do_filter2str(
            self.node2str(node.node), name,
            node.args, node.kwargs, node.dyn_args, node.dyn_kwargs
        )

    def output2str(self, output: nodes.Output):
        """Возвращает в виде строки все данные, которые должны быть отображены в конечном файле."""
        result = []

        for node in output.nodes:
            if isinstance(node, nodes.TemplateData):
                result.append(node.data)
            else:
                out = self.node2str(node)

                if out:
                    result.append(self.get_print_stmt(out))

        return ''.join(result)

    # Callable and arguments

    def nodes2list(self, nodes):
        return [self.node2str(node) for node in nodes]

    def arguments2str(self, args=None, kwargs=None, dyn_args=None, dyn_kwargs=None):
        """Возвращает все переданные аргументы в виде строки."""
        arguments = []

        if args:
            if not isinstance(args, tuple):
                args = self.args2native(args)
            arguments.append(self.arguments_separator.join(args))

        if kwargs:
            if not isinstance(kwargs, dict):
                kwargs = self.kwargs2native(kwargs)

            kwargs = (f'{k}={v}' for k, v in kwargs.items())
            arguments.append(self.arguments_separator.join(kwargs))

        if dyn_args is not None:
            arguments.append(self.dyn_args2str(dyn_args))

        if dyn_kwargs is not None:
            arguments.append(self.dyn_kwars2str(dyn_kwargs))

        return self.arguments_separator.join(arguments)

    def make_call_function_string(self, name, args, kwargs, dyn_args, dyn_kwargs):
        """Возвращает вызов функции или метода в виде строки."""
        arguments = self.arguments2str(args, kwargs, dyn_args, dyn_kwargs)
        return self.call_function_template.format(name=name, arguments=arguments).strip()

    def call2str(self, call: nodes.Call, **_):
        """Возвращает вызов функции или метода в виде строки."""
        name = self.get_function_name(call, use_mapping=True)
        args = self.args2native(call.args)
        kwargs = self.kwargs2native(call.kwargs)

        if callable(name):
            name, args, kwargs = name(self.get_function_name(call), *args, **kwargs)

        return self.make_call_function_string(name, args, kwargs, call.dyn_args, call.dyn_kwargs)

    def dyn_args2str(self, args):
        """Возвращает переменное количество позиционных аргументов в виде строки."""
        return f'*{self.node2str(args)}'

    def dyn_kwars2str(self, kwargs):
        """Возвращает переменное количество именованных аргументов в виде строки."""
        return f'**{self.node2str(kwargs)}'

    def get_function_name(self, call: nodes.Call, use_mapping=False):
        """Returns the name of the function from the call object."""
        target = call.node

        if isinstance(target, nodes.Name):
            name = target.name
        elif isinstance(target, nodes.Getattr):
            name = f'{self.node2str(target.node)}.{target.attr}'
        else:
            raise Error('Unsupported node type for call')

        if use_mapping and name in self.functions_mapper:
            name = self.functions_mapper[name]

        return name

    # Template structure

    def keyword2str(self, node: nodes.Keyword):
        return f'{node.key}={self.node2str(node.value)}'

    @not_supported_syntax()
    def block2str(self, block: nodes.Block):
        """Returns the block in the template as a string."""

    @not_supported_syntax()
    def callblock2str(self, node):
        """"""

    @not_supported_syntax()
    def extends2str(self, node: nodes.Extends):
        """Returns the inheritance statement from the parent template as a string."""

    @not_supported_syntax()
    def import2str(self, node: nodes.Import):
        """Returns the import statement as a string."""

    @not_supported_syntax()
    def include2str(self, node: nodes.Include):
        """Returns the include statement as a string."""

    @not_supported_syntax()
    def for2str(self, node: nodes.For):
        """Returns the for statement as a string."""

    @not_supported_syntax()
    def if2str(self, node: nodes.If):
        """Returns the if statement as a string."""

    template2str = ast2str


@Converter.attach_code_generator('jinja')
class JinjaCodeGenerator(CodeGenerator):
    def assign2str(self, node: nodes.Assign):
        return self.get_block_stmt(
            'set', self.node2str(node.target), '=', self.node2str(node.node)
        )

    def block2str(self, block: nodes.Block):
        return ''.join([
            self.get_block_stmt('block', block.name, 'scoped' if block.scoped else ''),
            self.nodes2str(block.body),
            self.get_block_stmt('endblock', block.name),
        ])

    def extends2str(self, node: nodes.Extends):
        return self.get_block_stmt('extends', f'"{node.template.value}"')

    def for2str(self, node: nodes.For):
        # print(node.test)

        result = [
            self.get_block_stmt(
                'for', self.node2str(node.target), 'in', self.node2str(node.iter),
                'recursive' if node.recursive else ''
            ),
            self.nodes2str(node.body),
        ]

        if node.else_:
            result.append(self.get_block_stmt('else'))
            result.append(self.nodes2str(node.else_))

        result.append(self.get_block_stmt('endfor'))

        return ''.join(result)

    def if2str(self, node: nodes.If):
        expr = self.node2str(node.test)
        result = [
            self.get_block_stmt('if', expr),
            self.nodes2str(node.body)
        ]

        for elif_ in node.elif_:
            result.extend([
                self.get_block_stmt('elif', self.node2str(elif_.test)),
                self.nodes2str(elif_.body)
            ])

        if node.else_:
            result.extend([self.get_block_stmt('else'), self.nodes2str(node.else_)])

        result.append(self.get_block_stmt('endif'))

        return ''.join(result)

    def import2str(self, node: nodes.Import):
        return self.get_block_stmt(
            'import', f'"{node.template.value}"', 'as', node.target,
            'with context' if node.with_context else ''
        )

    def include2str(self, node: nodes.Include):
        result = ['include', self.node2str(node.template)]

        if node.ignore_missing:
            result.append('ignore missing')

        if not node.with_context:
            result.append('without context')

        return self.get_block_stmt(*result)

    def with2str(self, node: nodes.With):
        """Returns the with statement makes it possible to create a new inner scope as a string."""
        variables = []

        for name, value in zip(node.targets, node.values):
            variables.append(f'{name.name}={self.node2str(value)}')

        return ''.join([
            self.get_block_stmt('with', self.arguments_separator.join(variables)),
            self.nodes2str(node.body),
            self.get_block_stmt('endwith')
        ])


@Converter.attach_code_generator('django')
class DjangoCodeGenerator(CodeGenerator):
    """Django template language."""

    arguments_separator = ' '

    call_function_template = '{name} {arguments}'

    def __init__(self, silent=False, functions_mapper=None, template_tags=None):
        super().__init__(silent, functions_mapper=functions_mapper)
        self.template_tags = template_tags or {}
        self.loaded_libraries = set()

    def assign2str(self, node: nodes.Assign):
        name = node.target

        if not isinstance(name, nodes.Name):
            return self.syntax_error('Django only supports constant variable names.', node.lineno)

        value = node.node

        if not self.is_template_tag(value):
            return self.syntax_error('Django only supports template tags as variable values.', node.lineno)

        return self.get_block_stmt(self.call2str(value), 'as', self.node2str(node.target))

    def ast2str(self, node: nodes.Template):
        result = super().ast2str(node)

        if self.loaded_libraries:
            pattern = re.compile(r'({%\s+extends.+?%})')
            repl = self.get_block_stmt('load', *self.loaded_libraries)

            result, inserted = pattern.subn(r'\1\n{}'.format(repl), result)

            if not inserted:
                result = f'{repl}\n{result}'

        return result

    def block2str(self, block: nodes.Block):
        return ''.join([
            self.get_block_stmt('block', block.name),
            self.nodes2str(block.body),
            self.get_block_stmt('endblock', block.name),
        ])

    def compare2str(self, node: nodes.Compare, parent_priority=None):
        """
        Разворачивает все выражения с операторами сравнения, идущими друг за другом через оператор and.
        Хотя Python интерпретирует подобные инструкции таким же образом,
        использовать с осторожностью, возможно изменение результата выражения.
        """
        def iterator(left, ops):
            for op in ops:
                yield self._make_expression(op.op, left, op.expr, parent_priority=parent_priority)
                left = op.expr

        result = iterator(node.expr, node.ops)
        result = f' {self.get_operator("and")} '.join(result)

        if len(node.ops) > 1:
            result = self.prioritize(result, self.get_operator_priority('and'), parent_priority)

        return result

    extends2str = JinjaCodeGenerator.extends2str

    def for2str(self, node: nodes.For):
        result = []
        iterable = node.iter

        if self.is_template_tag(iterable):
            template_tag = self.call2str(iterable)
            iterable = self.get_unique_identifier()
            result.append(self.get_block_stmt(template_tag, 'as', iterable))
            result.append('\n')
        else:
            iterable = self.node2str(iterable)

        result.append(self.get_block_stmt('for', self.node2str(node.target), 'in', iterable))
        result.append(self.nodes2str(node.body))

        if node.else_:
            result.append(self.get_block_stmt('empty'))
            result.append(self.nodes2str(node.else_))

        result.append(self.get_block_stmt('endfor'))

        return ''.join(result)

    def getitem2str(self, node: nodes.Getitem, **_):
        if not isinstance(node.arg, nodes.Const):
            return self.syntax_error('Django does not support access to attributes by not const key.', node.lineno)
        return '{}.{}'.format(self.node2str(node.node), node.arg.value)

    def _do_filter2str(self, value, name, args=None, kwargs=None, dyn_args=None, dyn_kwargs=None):
        for tag_name, lib in self.template_tags.items():
            if re.match(tag_name, name):
                self.loaded_libraries.add(lib)

        output = f'{value}|{name}'

        if len(args) > 1:
            self.syntax_error('Filters in Django can only take one positional argument.')

        if kwargs:
            self.syntax_error('Filters in Django do not support keyword arguments.')

        argument = self.arguments2str(args=args[:1])

        return f'{output}:{argument}' if argument else output

    @not_supported_syntax('Django does not support a variable number of positional arguments.')
    def dyn_args2str(self, args):
        pass

    @not_supported_syntax('Django does not support a variable number of keyword arguments')
    def dyn_kwars2str(self, kwargs):
        pass

    def if2str(self, node: nodes.If):
        result = JinjaCodeGenerator.if2str(self, node)

        if re.search(r'\(|\)', result.splitlines().pop()):
            self.syntax_error('Django does not support brackets in conditional expressions.', lineno=node.lineno)

        return result

    def import2str(self, node: nodes.Import):
        """Возвращает инструкцию импорта в виде строки."""
        if node.target in self.template_tags.values():
            return self.get_block_stmt('load', node.target)
        logger.warning('The import instruction will be ignored because no match is found with the library with template tags.')
        return ''

    def include2str(self, node: nodes.Include):
        """Возвращает инструкцию включения в виде строки."""
        if isinstance(node.template, nodes.List):
            return self.syntax_error(
                'Django does not support providing a list of templates that are checked for existence before inclusion.',
                node.lineno
            )

        if node.ignore_missing:
            self.syntax_error('Django always throws an exception if a template is not found.', node.lineno)

        if not node.with_context:
            self.syntax_error('Django always passes context to the included template.', node.lineno)

        return self.get_block_stmt('include', self.node2str(node.template))

    def is_template_tag(self, call):
        """Returns true if the call object is a template tag."""
        if not isinstance(call, nodes.Call):
            return False

        if call.args or call.kwargs or call.dyn_args or call.dyn_kwargs:
            return True

        name = self.get_function_name(call, use_mapping=True)

        for tag_name in self.template_tags:
            if re.match(tag_name, name):
                return True

        return False

    def make_call_function_string(self, name, args, kwargs, dyn_args, dyn_kwargs):
        for tag_name, lib in self.template_tags.items():
            if re.match(tag_name, name):
                self.loaded_libraries.add(lib)
        return super().make_call_function_string(name, args, kwargs, dyn_args, dyn_kwargs)

    def output2str(self, output: nodes.Output):
        """Возвращает в виде строки все данные, которые должны быть отображены в конечном файле."""
        result = []

        for node in output.nodes:
            if isinstance(node, nodes.Call) and self.is_template_tag(node):
                result.append(self.get_block_stmt(self.call2str(node)))
            elif isinstance(node, nodes.TemplateData):
                result.append(node.data)
            else:
                out = self.node2str(node)

                if out:
                    result.append(self.get_print_stmt(out))

        return ''.join(result)

    def with2str(self, node: nodes.With):
        result = []
        variables = []
        body = []

        for name, value in zip(node.targets, node.values):
            if self.is_template_tag(value):
                body.extend([
                    '\n', self.get_block_stmt(self.node2str(value), 'as', name.name)
                ])
            else:
                value = self.node2str(value)
                variables.append(f'{name.name}={value}')

        for n in node.body:
            if isinstance(n, nodes.Assign) and not self.is_template_tag(n.node):
                variables.append(f'{n.target.name}={self.node2str(n.node)}')
            else:
                body.append(self.node2str(n))

        result.append(self.get_block_stmt('with', self.arguments_separator.join(variables)))
        result.extend(body)
        result.append(self.get_block_stmt('endwith'))

        return ''.join(result)


@Converter.attach_code_generator('mako')
class MakoSyntax(CodeGenerator):
    """Mako template language."""

    block_start_string = '<%'
    block_end_string = '>'
    variable_start_string = '${'
    variable_end_string = '}'

    def get_inline_block_stmt(self, s, *args, sep=' '):
        pass

    def block2str(self, block: nodes.Block):
        return '<%block name="{name}">{body}</%block>'.format(
            name=block.name,
            body=self.nodes2str(block.body)
        )

    def extends2str(self, node: nodes.Extends):
        return f'<%inherit file="{node.template.value}"/>'


@Converter.attach_code_generator('flask2django')
def flask2django(*args, **kwargs):
    def url_for(_, endpoint, *args, **kwargs):
        """Callback для функции url_for."""
        if endpoint == "'static'" or endpoint.endswith(".static'"):
            endpoint = endpoint.strip('\'"').split('.')

            if len(endpoint) == 2:
                blueprint, _ = endpoint
            else:
                blueprint = None

            filename = kwargs['filename'].strip('\'"')
            filename = f"'{blueprint}/{filename}'" if blueprint else f"'{filename}'"
            return 'static', (filename,), {}

        return 'url', (endpoint, *args), kwargs

    functions_mapper = kwargs.setdefault('functions_mapper', {})
    functions_mapper.update({
        'super': 'block.super',
        'url_for': url_for,
    })

    template_tags = kwargs.setdefault('template_tags', {})
    template_tags.update({
        'static': 'static',
    })

    return DjangoCodeGenerator(*args, **kwargs)


if __name__ == '__main__':
    c = Converter('mako')
    c.config.load('not_found.py')
