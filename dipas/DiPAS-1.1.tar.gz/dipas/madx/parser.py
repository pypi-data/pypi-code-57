"""Functionality for parsing MADX files.

Some details of the parsing procedure are configured (and may be altered) by the following module-level attributes.

Attributes
----------
replacement_string_for_dots_in_variable_names : str
    The parser does not support dots in variable names (it only supports variable names that are valid Python
    identifiers) and so each dot in a variable name will be replaced by the string indicated by this attribute.
negative_offset_tolerance : float
    If during sequence expansion (`pad_sequence` more specifically) a negative offset between two elements is
    encountered the parser will raise a `ParserError` if this offset is smaller than this attribute.
minimum_offset_for_drift : float
    During sequence expansion (`pad_sequence` more specifically) an implicit drift space will be padded by an explicit
    drift space only if the offset between the two involved elements is greater than this attribute.
allow_popup_variables : bool, default = True
    If an expression consists of a single variable name which cannot be resolved (i.e. that variable was not defined
    before), then the parser will fallback on (float) zero. If this parameter is false a `ParserError` will be raised
    instead. Example for a "popup variable": ``quadrupole, k1 = xyz`` where ``xyz`` was not defined before. This will
    either fall back on ``0.0`` or raise an error, depending on this parameter.
rng_default_seed : int
    The default seed for the random number generator used for evaluating calls to functions such as
    "ranf" (np.random.random) or "gauss" (np.random.normal).
command_str_attributes : set
    Command attributes with names that are part of this set are assumed to be strings and will hence not be evaluated
    (i.e. not name resolution, evaluation of formulas, etc). By default this only lists argument names that are strings
    by MADX definitions.
special_names : dict
    During evaluation of expressions this dict will be used for resolving any names that are encountered. By default
    this contains functions such as ``"asin": np.arcsin`` or constants like ``"pi": np.pi``.
particle_dict : dict
    Given a `BEAM` command the parser computes the relativistic beta and gamma factors from the given quantities
    (actually it augments the BEAM command by all other quantities). This dict is used for resolving particles names
    given by ``BEAM, particle = xyz;`` (i.e. selects the corresponding `charge` and `mass`).
patterns : dict
    Contains regex patterns for MADX statements (e.g. comments, variable definitions, etc) mapped to by a corresponding
    (descriptive) name. If a pattern is matched a corresponding statement handler will be invoked which must have been
    previously registered via `register_handler` (or inserted into `statement_parsers`).
statement_handlers : dict
    This dict maps pattern names (keys of the ``patterns`` dict) to corresponding statement handlers. A handler will be
    invoked when the corresponding statement pattern matched a statement. For more details on the signature of such a
    handler, see :func:`register_handler`.
VARIABLE_INDICATOR : str
    The string which is used to indicate *flow variables* in comments (by default this is ``[flow] variable``).
prepare_script : list
    Contains functions that that perform preparation steps prior to parsing the script. All the listed preparation steps
    are performed in order on the particular previous result. This signature of such preparation step function should
    be ``(str) -> str``, i.e. accept the current version of the (partially) prepared script and return a new version.
    The last function must return a list of single statements when given the prepared script
    (i.e. ``(str) -> List[str]``).
prepare_statement : list
    Contains functions that perform preparation steps for each single statement in order, prior to parsing it. The
    signature of these functions should be ``(str) -> str``, i.e. accepting the current version of the (partially)
    prepared statement and return a new version.
"""

from __future__ import annotations

import ast
from collections import defaultdict
import copy
from dataclasses import dataclass, field
import functools
import itertools as it
import operator
import os
import re
from typing import Any, Callable, Dict, Iterable, Iterator, List, Match, Optional, Sequence, Tuple, Union
import warnings

import numpy as np
import pandas as pd
import scipy.constants as constants
import scipy.special
import scipy.stats

from ..utils import format_doc, func_chain, pad_max_shape, remove_duplicates, safe_math_eval


__all__ = ['parse_file', 'parse_script']

replacement_string_for_dots_in_variable_names = '_'
negative_offset_tolerance = -1e-6
minimum_offset_for_drift =   1e-6
allow_popup_variables = True
rng_default_seed = 123456789
command_str_attributes = {'particle', 'range', 'class', 'pattern', 'flag', 'file', 'period', 'sequence', 'refer',
                          'apertype', 'name'}

special_names = {x: getattr(np, x)
                 for x in ['sqrt', 'log', 'log10', 'exp', 'sin', 'cos', 'tan', 'sinh', 'cosh',
                           'tanh', 'sinc', 'abs', 'floor', 'ceil', 'round']}
special_names['asin'] = np.arcsin
special_names['acos'] = np.arccos
special_names['atan'] = np.arctan
special_names['erf'] = scipy.special.erf
special_names['erfc'] = scipy.special.erfc
special_names['ranf'] = np.random.uniform
special_names['gauss'] = np.random.normal
special_names['pi'] = np.pi
special_names['twopi'] = 2 * np.pi
special_names['degrad'] = 180 / np.pi
special_names['raddeg'] = np.pi / 180
special_names['e'] = np.exp(1)
special_names['emass'] = constants.physical_constants['electron mass energy equivalent in MeV'][0] / 1e3
special_names['pmass'] = constants.physical_constants['proton mass energy equivalent in MeV'][0] / 1e3
special_names['nmass'] = constants.physical_constants['atomic mass constant energy equivalent in MeV'][0] / 1e3
special_names['mumass'] = constants.physical_constants['muon mass energy equivalent in MeV'][0] / 1e3
special_names['clight'] = constants.speed_of_light
special_names['qelect'] = constants.elementary_charge
special_names['hbar'] = constants.hbar
special_names['erad'] = constants.physical_constants['classical electron radius'][0]
special_names['prad'] = special_names['erad'] * special_names['emass'] / special_names['pmass']
# Random number generators.
special_names['ranf'] = np.random.random
special_names['gauss'] = np.random.normal
special_names['tgauss'] = lambda x: scipy.stats.truncnorm.rvs(-x, x)

particle_dict = {
    'positron':   {'charge':  1, 'mass': special_names['emass']},
    'electron':   {'charge': -1, 'mass': special_names['emass']},
    'proton':     {'charge':  1, 'mass': special_names['pmass']},
    'antiproton': {'charge': -1, 'mass': special_names['pmass']},
    'posmuon':    {'charge':  1, 'mass': special_names['mumass']},
    'negmuon':    {'charge': -1, 'mass': special_names['mumass']},
    'ion':        {'charge':  1, 'mass': special_names['nmass']},
}

identifier_pattern = re.compile('[a-z][a-z0-9_.]*')
value_pattern = re.compile(r'(?:".+?"|[a-z0-9_.\-+*/{}(),> ]+)')
attribute_pattern = re.compile(r'(?P<name>%(identifier)s)(?:\s*(?P<assignment>:?=)\s*(?P<value>%(value)s))?'
                               % {'identifier': identifier_pattern.pattern, 'value': value_pattern.pattern})
patterns = {
    'comment': re.compile(r'^(?:!|//)\s*(.*)$'),
    'variable': re.compile(
        r'''
        ^
        (?:
            CONST \s*
        )?
        (?P<name>
            %(identifier)s
        )
        (?:
            ->
            (?P<attr>
                %(identifier)s
            )
        )?
        \s* (?P<assignment>:?=) \s*
        (?P<value>
            %(value)s
        )
        $
        ''' % {'identifier': identifier_pattern.pattern, 'value': value_pattern.pattern},
        re.I | re.X
    ),
    'command': re.compile(
        r'''
        ^
        (?:
            (?P<label>
                %(identifier)s
            )
            : \s*
        )?
        (?P<keyword>
            %(identifier)s
        )
        \s*
        (?:
            , \s*
            (?P<attributes>
                %(attribute)s
                (?:
                    \s* , \s*
                    %(attribute)s
                )*
            )
        )?
        $
        ''' % {'identifier': identifier_pattern.pattern,
               'attribute': re.sub(r'\?P<[a-z]+>', '?:', attribute_pattern.pattern)},
        re.I | re.X
    ),
    'line': re.compile(
        r'''
        ^
        (?P<label>
            %(identifier)s
        )
        : \s*
        LINE \s* = \s*
        (?P<elements>
            \( (?: - | -?[1-9][0-9]* \s* [*] \s* | %(identifier)s | \s* , \s* | \s* [()] \s* )+ \)
        )
        ''' % {'identifier': identifier_pattern.pattern},
        re.I | re.X
    )
}

VARIABLE_INDICATOR = '[flow] variable'

find_all_csp = functools.partial(re.findall, re.compile('(?:{.*?}|".*?"|[^,])+'))
find_all_csp.__doc__ = 'Find all comma separated parts, skipping commas which are part of strings "" or arrays {}.'


def _generate_math_ops(op):
    def left(self, other):
        if isinstance(other, (DeferredExpression, Variable)):
            other = other.value
        new_value = op(self.value, other)
        return Variable(new_value) if (isinstance(self, Variable) or isinstance(other, Variable)) else new_value

    def right(self, other):
        new_value = op(other, self.value)
        return Variable(new_value) if isinstance(self, Variable) else new_value

    return functools.update_wrapper(left, op), functools.update_wrapper(right, op)


@dataclass
class DeferredExpression:
    """Represents an expression used with deferred assignment (indicated by ``:=``)."""
    expr: str
    variables: dict = field(default_factory=dict, repr=False)
    commands: dict = field(default_factory=dict, repr=False)

    @property
    def value(self):
        """Evaluate the expression."""
        return eval_expr(self.expr, self.variables, self.commands)

    __add__, __radd__ = _generate_math_ops(operator.add)
    __sub__, __rsub__ = _generate_math_ops(operator.sub)
    __mul__, __rmul__ = _generate_math_ops(operator.mul)
    __truediv__, __rtruediv__ = _generate_math_ops(operator.truediv)
    __pow__, __rpow__ = _generate_math_ops(operator.pow)


@dataclass
class Variable:
    """Indicates and wraps the initial value of a flow variable."""
    source: Union[float, DeferredExpression]

    @property
    def value(self):
        """Get the initial value of the variable."""
        if isinstance(self.source, DeferredExpression):
            return self.source.value
        return self.source

    __add__, __radd__ = _generate_math_ops(operator.add)
    __sub__, __rsub__ = _generate_math_ops(operator.sub)
    __mul__, __rmul__ = _generate_math_ops(operator.mul)
    __truediv__, __rtruediv__ = _generate_math_ops(operator.truediv)
    __pow__, __rpow__ = _generate_math_ops(operator.pow)

    @classmethod
    def unwrap(cls, v: Union['Variable', DeferredExpression]):
        """Retrieve the numerical value of the given variable or deferred expression.

        Returns
        -------
        is_variable : bool
            Indicates whether the value is considered variable (can be non-obvious if wrapped by a deferred expression).
        value : float
            The numerical value of the variable / deferred expression.
        """
        value = v.value
        if isinstance(value, (Variable, DeferredExpression)):
            is_variable, value = cls.unwrap(value)
        else:
            is_variable = False
        return isinstance(v, Variable) | is_variable, float(value) if is_variable else value


del _generate_math_ops


def evaluate_object(num: Union[Any, DeferredExpression, Variable]) -> Any:
    """Get the actual object from a deferred expression or variable or combination thereof."""
    if isinstance(num, (DeferredExpression, Variable)):
        num = num.value
    if isinstance(num, Variable):
        num = num.value
    return num


@dataclass
class Command:
    """Represents a MADX command."""
    keyword: str
    local_attributes: dict = field(default_factory=dict)
    label: str = None
    base: 'Command' = None

    def __contains__(self, item):
        return item in self.attributes

    def __copy__(self):
        return type(self)(self.keyword, self.local_attributes.copy(), self.label, self.base)

    def __delitem__(self, key):
        try:
            del self.local_attributes[key]
        except KeyError:
            if self.base is not None:
                del self.base[key]
            else:
                raise

    def __getitem__(self, item):
        try:
            return self.local_attributes[item]
        except KeyError:
            if self.base is not None:
                return self.base[item]
            else:
                raise

    def __setitem__(self, key, value):
        self.local_attributes[key] = value

    def get(self, *args):
        """Wrapper for self.attributes.get."""
        return self.attributes.get(*args)

    @property
    def attributes(self) -> Dict[str, Any]:
        """Retrieve all attributes including inherited ones."""
        base_attributes = self.base.attributes if self.base is not None else {}
        base_attributes.update(self.local_attributes)
        return base_attributes

    @property
    def root(self):
        """Retrieve the root command from which this command has been derived.
           `root` goes all the way back while `base` goes only one level back.
        """
        if self.base is not None:
            return self.base.root
        return self


class Line:
    """Represents a beamline definition (`LINE`)."""
    elements: Tuple[Union[str, 'Line'], ...]
    label : str
    keyword = 'line'  # For compatibility with `Command`.

    def __init__(self, elements: Sequence[Union[str, 'Line']], label: str = None):
        self.elements = tuple(elements)
        self.label = label

    def __neg__(self):
        return Line([-x if isinstance(x, Line) else f'-{x}' for x in reversed(self.elements)])

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise TypeError(f'Cannot multiply line by object of type {type(other)}')
        if other == -1:
            return self.__neg__()
        new = Line(abs(other) * self.elements)  # No need to copy here because in the end a Line holds `str` elements.
        if other < 0:
            new = -new
        return new

    def expand(self, context: Dict[str, Any]) -> Iterator[Command]:
        for item in self.elements:
            if not isinstance(item, Line):
                match = re.match(r'^(?:(-)|(-?\d+)(?: *[*] *))?(%s)$' % identifier_pattern.pattern, item)
                item = context[match.group(3)]
                count = -1 if match.group(1) else int(match.group(2) or 1)
                if not isinstance(item, Line):
                    # Need to copy here because otherwise we have the exact same `Command` instance multiple times in
                    # the beamline. This would lead to unexpected behavior when for example applying alignment errors
                    # because there, due to multiple `SELECT`s, duplicate commands are filtered out.
                    yield from map(copy.copy, it.repeat(item, abs(count)))
                    continue
                item = count * item
            yield from item.expand(context)

    @classmethod
    def parse(cls, expr_string: str) -> 'Line':
        """Parse the given beamline definition into a corresponding `Line` object."""

        class NodeVerifier(ast.NodeVisitor):
            def visit(self, node):
                if not isinstance(node, (ast.BinOp, ast.Load, ast.Mult, ast.Name, ast.Num, ast.Tuple, ast.UnaryOp,
                                         ast.USub)):
                    raise TypeError(f'Invalid node type in sequence definition: {type(node)} ({repr(expr_string)})')
                self.generic_visit(node)

        class USubTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                if isinstance(node.left, ast.UnaryOp) and isinstance(node.right, ast.Tuple):
                    op, operand = node.left.op, node.left.operand
                    node.left = operand
                    node = ast.UnaryOp(op=op, operand=node)
                return node

        class RepetitionTransformer(ast.NodeTransformer):
            def visit_BinOp(self, node):
                if isinstance(node.right, ast.Tuple):
                    node.right.elts = [copy.deepcopy(x) for x in node.left.n * node.right.elts]
                    self.generic_visit(node.right)
                    return node.right
                return node

        class ReflectionTransformer(ast.NodeTransformer):
            def visit_UnaryOp(self, node):
                if isinstance(node.operand, ast.Tuple):
                    node.operand.elts = [
                        ast.UnaryOp(op=node.op, operand=x) if not isinstance(x, ast.UnaryOp) else x.operand
                        for x in node.operand.elts[::-1]
                    ]
                    self.generic_visit(node.operand)
                    return node.operand
                return node

        class StringifyTransformer(ast.NodeTransformer):
            def visit_Name(self, node):
                return ast.Str(s=node.id)

            def visit_BinOp(self, node):
                if isinstance(node.left, ast.Num):
                    return ast.Str(s=f'{node.left.n}*{node.right.id}')
                elif isinstance(node.left, ast.UnaryOp):
                    return ast.Str(s=f'-{node.left.operand.n}*{node.right.id}')

            def visit_UnaryOp(self, node):
                return ast.Str(s=f'-{node.operand.id}')

        def convert_to_line(obj):
            if isinstance(obj, tuple):
                return cls(tuple(convert_to_line(x) for x in obj))
            return obj

        root = ast.parse(expr_string).body[0]
        if not isinstance(root, ast.Expr):
            raise TypeError(f'Line definition must be an expression, not {type(root)} ({repr(expr_string)})')
        NodeVerifier().visit(root.value)
        USubTransformer().visit(root)
        RepetitionTransformer().visit(root)
        ReflectionTransformer().visit(root)
        StringifyTransformer().visit(root)
        root = ast.Expression(root.value)
        root = ast.fix_missing_locations(root)
        return convert_to_line(eval(compile(root, '<string>', 'eval')))


CommandLike = Union[Command, Line]
Variables = Dict[str, Union[str, int, float, list, Variable, DeferredExpression]]
Context = Dict[str, CommandLike]
Commands = List[CommandLike]


# noinspection PyUnresolvedReferences
@dataclass
class Script:
    """Represents the content of a MADX script (or a part of the script, during the parsing procedure).

    Attributes
    ----------
    variables : Variables
        Holds all variable definitions of the form ``x :?= y;``.
    commands : Commands
        Holds all labeled and unlabeled commands.
    context : Context
        Holds all labeled commands, by label.
    """
    variables: Variables = field(default_factory=dict, metadata='Variable definitions')
    commands: Commands = field(default_factory=list, metadata='Command definitions')
    context: Context = field(default_factory=dict, metadata='Commands by label')


@dataclass
class State:
    script: Script
    flow_variable: bool = False


StatementHandler = Callable[[Match, State], State]
statement_handlers: Dict[str, StatementHandler] = {}


def register_handler(*args, override=False) -> Optional[Callable[[StatementHandler], StatementHandler]]:
    """A statement handler is invoked when the corresponding statement type is encountered.

    It should have the following signature: ``match: Match, state: State`` where `match` is the regex match object
    emerging from the corresponding `Pattern` in `patterns` and `state` has the following attributes::

        script: Script
        flow_variable: bool

    `script` contains the script's content up to the current parsing point and `flow_variable` indicates whether a
    *flow variable* has been requested; this flag is set by special comments of the form `` [flow] variable`` and it is
    unset after being processed by the `handle_variable` statement handler.
    Usually a handler should return the same state tuple it has received (though nothing prevents it from returning a
    new one).

    This function can be used as a decorator ``@register_handler`` in which case the name of the decorated function
    should be `handle_xyz` where `xyz` is the same of the corresponding pattern key in `patterns` which should trigger
    invoking this handler.
    An alternative usage is via ``register_handler(key, handler)`` where `key` again corresponds to `patterns` and
    `handler` is a `StatementHandler`.

    Parameters
    ----------
    args : str or callable, optional
        Optionally indicate the `patterns` key and provide the corresponding handler. If not given, the decorator will
        infer the key from the function name (`handle_key`).
    override : bool, optional
        Whether to override an existing handler for the given statement type or not (default is false).

    Returns
    -------
    function
        If `args` is empty it will return a corresponding decorator for registering the handler. If `args` is not empty
        if must contain a `str` and `StatementHandler` and nothing will be returned.
    """
    explicit_key = args[0] if args else None

    def _decorator(func: StatementHandler) -> StatementHandler:
        key = explicit_key or func.__name__.replace('handle_', '', 1)
        if override:
            statement_handlers.pop(key)
        return statement_handlers.setdefault(key, func)

    if args:
        _decorator(args[1])
        return None

    return _decorator


@register_handler()
def handle_variable(match: Match, state: State) -> State:
    variables, context = state.script.variables, state.script.context
    if match.group('assignment') == ':=':
        value = DeferredExpression(match.group('value'), variables, context)
    else:
        value = eval_expr(match.group('value'), variables, context)
    if state.flow_variable:
        value = Variable(value)
        state.flow_variable = False
    if match.group('attr') is None:
        variables[match.group('name')] = value
    else:
        context[match.group('name')][match.group('attr')] = value
    return state


@register_handler()
def handle_command(match: Match, state: State) -> State:
    variables, context, commands = state.script.variables, state.script.context, state.script.commands
    attributes = {}
    for n, a, v in parse_attributes(match.group('attributes') or ''):
        if n in command_str_attributes:
            attributes[n] = v.strip('"')
        elif a == ':=':
            attributes[n] = DeferredExpression(v, variables, context)
        else:
            attributes[n] = eval_expr(v, variables, context)
    base_command = context.get(match.group('keyword'))
    command = Command(match.group('keyword'), attributes, match.group('label'), base_command)
    if command.label is not None:
        context[command.label] = command
    commands.append(command)
    return state


@register_handler()
def handle_line(match: Match, state: State) -> State:
    line = Line.parse(match.group('elements'))
    line.label = match.group('label')
    state.script.context[match.group('label')] = line
    state.script.commands.append(line)
    return state


@register_handler()
def handle_comment(match: Match, state: State) -> State:
    if match.group(1) == VARIABLE_INDICATOR:
        state.flow_variable = True
    return state


def resolve_calling_sites(f_name: str, path: str = None) -> str:
    """Recursively fill in the content of other scripts referred to by ``CALL, file = ...``."""
    if path is None:
        path, f_name = os.path.split(f_name)
    with open(os.path.join(path, f_name)) as fh:
        return re.sub(
            r'(?:^|(?<=[\n;]))(?P<indent> *)'
            r'call *, *'
            r'file *= *(?P<quotes>[\'"]?)(?P<f_name>[^\'"]+?)(?P=quotes) *;',
            lambda match: '\n'.join(
                f'{match.group("indent")}{line}'
                for line in resolve_calling_sites(match.group('f_name'), path).splitlines()
            ),
            fh.read()
        )


def remove_multi_line_comments(script: str) -> str:
    """Remove multi-line comments indicated by ``/* ... */``."""
    return re.sub(r'/\*.*?\*/\s*', '', script, flags=re.DOTALL)


def normalize_variable_indicators(script: str) -> str:
    """Removes additional text from comments that act as flow variable indicators and places the comment before the
       variable definition (or attribute reference)."""
    return re.sub(rf'(.+;)?\s*(?://|!).*{re.escape(VARIABLE_INDICATOR)};? *$',
                  rf'// {VARIABLE_INDICATOR};\n\1',
                  script, flags=re.MULTILINE)


def remove_comments(script: str) -> str:
    """Remove comments except for flow variable indicators.

    .. Important::
       At this step `script` must contain only normalized flow variable indicators
       (see :data:`normalize_variable_indicator`), i.e. without additional text in the comment.

    .. Note:: This also removes comment-like strings enclosed by `""`, e.g. ``text = "// comment-like";``).
    """
    return re.sub(rf'\s*(//|!)(?! {re.escape(VARIABLE_INDICATOR)}).*;? *$', '', script, flags=re.MULTILINE)


def replace_line_feeds(script: str) -> str:
    """Replace line feeds followed by any number of whitespace or tab characters by a single whitespace."""
    return re.sub(r'\r?\n[ \t]*', ' ', script)


def replace_dots_in_variable_names(script: str) -> str:
    """Replace dots in variable names since for evaluating expressions variable names must conform to the Python
       standard for identifiers.

    Warns
    -----
    UserWarning
        In case the script defines already a variable with one of the replaced names (hence provoking a name conflict).
    """

    def _replace(match):
        new = match.group(0).replace('.', replacement_string_for_dots_in_variable_names)
        if new in script:
            warnings.warn(f'Replacing variable name "{match.group(0)}" with "{new}" but this name is already used')
        return new

    return re.sub('[a-z][a-z0-9_]*[.][a-z0-9_.]*', _replace, script)


def remove_whitespace(script: str) -> str:
    """Remove whitespace but not within doubly quotes or within single-line comments."""
    return re.sub(r'(".*?"|//.*?(?:\n|$))|[^\S\n]+', lambda m: m.group(1) or '', script)


def replace_singly_with_doubly_quotes(script: str) -> str:
    """Replace ``'`` with ``"`` quotes."""
    return script.replace('\'', '"')


prepare_script = [
    remove_multi_line_comments,
    normalize_variable_indicators,
    remove_comments,
    replace_line_feeds,
    lambda s: s.split(';'),
]

prepare_statement = [
    str.lower,
    replace_dots_in_variable_names,
    replace_singly_with_doubly_quotes,  # The parser expects doubly quotes for strings.
    remove_whitespace,
    str.strip,
]


class ParserError(Exception):
    """Error raised if a MADX script could not be parsed successfully."""
    pass


def parse_file(f_name: str) -> Script:
    """Auxiliary function for `parse_script` working on file names which also resolves references to other scripts
       via ``CALL, file = ...``.

    Parameters
    ----------
    f_name : str
        File name pointing to the MADX script.

    Returns
    -------
    See :func:`parse_script`.
    """
    return parse_script(resolve_calling_sites(f_name))


@format_doc(variable_indicator=VARIABLE_INDICATOR)
def parse_script(script: str) -> Script:
    """Parses a MADX script and returns the relevant commands list as well as command variable definitions.

    Flow variables should be declared on a separate statement and indicated using one of the following syntax options:

    .. code-block:: text

       q1_k1 = 0;  // < optional text goes here > {variable_indicator}
       q1: quadrupole, l=1, k1=q1_k1;

       // < optional text goes here > {variable_indicator}
       q1_k1 = 0;
       q1: quadrupole, l=1, k1=q1_k1;

       q1: quadrupole, l=1, k1=0;
       q1->k1 = 0;  // < optional text goes here > {variable_indicator}

    .. Important::
       If the script contains any ``CALL, file = ...`` commands these will not be resolved (just parsed as such).
       Use `parse_file` for that purpose.

    Parameters
    ----------
    script : str
        The MADX script's content.

    Returns
    -------
    script : Script

    Raises
    ------
    ParserError
        If a misplaced variable indicator is encountered, e.g. not followed by a variable definition.
    """
    statements = filter(None, map(str.strip, func_chain(*prepare_script)(script)))
    state = State(Script())
    for statement in statements:
        p_type, match = parse_statement(func_chain(*prepare_statement)(statement))
        if p_type is None:
            raise ParserError(f'Cannot parse statement: {statement}')
        if state.flow_variable and p_type != 'variable':
            raise ParserError(f'Variable indicator is not followed by or does not correspond to '
                              f'variable definition: {statement}')
        try:
            state = statement_handlers[p_type](match, state)
        except Exception as err:
            raise ParserError(f'Cannot parse statement: {statement}\n    -> {err!s}')
    return state.script


def parse_statement(stmt: str) -> Union[Tuple[str, Match], Tuple[None, None]]:
    """Parse a MADX statement into its corresponding type and a `re.Match` object containing relevant information.

    The supported statement types are described by `madx.patterns`.

    Parameters
    ----------
    stmt : str
        Will be parsed into one of the types described by `madx.patterns`.

    Returns
    -------
    stmt_type : str
        The corresponding key in `madx.patterns`.
    match : re.Match
        The corresponding matched pattern in `madx.patterns`.

    If the statement cannot be parsed into one of the supported types `(None, None)` will be returned.
    """
    for p_type, pattern in patterns.items():
        match = re.match(pattern, stmt)
        if match is not None:
            return p_type, match
    return None, None


def parse_attributes(attr_string: str) -> List[Tuple[str, str, str]]:
    """Parses an attribute string into its single components.

    Parameters
    ----------
    attr_string : str
        Attribute string with single attributes delimited by ",".

    Returns
    -------
    attributes : list
        Containing tuples of the form ``(name, assignment_type, value)``.
    """
    attributes = [re.match(attribute_pattern, attr.strip()) for attr in find_all_csp(attr_string)]
    attributes = [m.group('name', 'assignment', 'value') for m in attributes]
    return [(n, a, v if v is not None else 'true') for n, a, v in attributes]


def eval_expr(expr: Union[str, DeferredExpression], variables: dict = None, commands: dict = None) -> Any:
    """Evaluate a (compound) expression and interpolate any contained variable names.

    Name resolution and variable interpolation is performed according to the values provided via `madx.special_names`
    updated by the parameter `variables`. Attribute names of the form ``label->attr`` are resolved via `commands`.

    Parameters
    ----------
    expr : str
        The expression to be evaluated; may contain variable names that can be resolved through either
        `madx.special_names` or `variables`.
    variables : dict
        Variable definitions (possibly emerging from previous MADX statements).
    commands : dict
        Previously labeled MADX commands, used for resolving ``label->attr`` references.

    Returns
    -------
    The evaluated expression.

    Raises
    ------
    ParserError
        See :func:`utils.safe_math_eval`.

    See Also
    --------
    :func:`utils.safe_math_eval` : For evaluating mathematical expressions.
    """
    value = _eval_expr(expr, variables, commands)
    if isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
        value = np.array(value)
    return value


def _eval_expr(expr: Union[str, DeferredExpression], variables: dict = None, commands: dict = None) -> Any:
    """Performs the actual evaluation of expressions."""
    if isinstance(expr, DeferredExpression):
        return expr
    if not isinstance(expr, str):
        raise TypeError(f'Expression must be str not {type(expr)}')
    if expr.startswith('{') and expr.endswith('}'):
        return [_eval_expr(e.strip(), variables, commands) for e in find_all_csp(expr[1:-1])]
    if expr.startswith('"') and expr.endswith('"'):
        return expr.strip('"')
    if re.match('^(true|false)$', expr):
        return expr == 'true'
    try:
        return int(expr)
    except ValueError:
        pass
    try:
        return float(expr)
    except ValueError:
        pass

    def _replace_attribute_reference(match):
        val = commands[match.group('label')][match.group('attr')]
        if isinstance(val, (DeferredExpression, Variable)):
            val = val.value
        if isinstance(val, Variable):  # Names can be resolved to variables during evaluation of a deferred expression.
            val = val.value
        return str(val)

    expr = re.sub(r'(?P<label>%(id)s)->(?P<attr>%(id)s)' % {'id': identifier_pattern.pattern},
                  _replace_attribute_reference, expr)
    try:
        value = safe_math_eval(expr, dict(special_names, **(variables or {})))
    except NameError as err:
        if allow_popup_variables and expr == str(err).split("'")[1]:
            return 0.
        raise
    if isinstance(value, DeferredExpression):  # If the expression consisted only of a deferred variable.
        value = value.value
    return value


def extract_sequence(commands: Iterable[CommandLike], context: Dict[str, CommandLike], label: Optional[str] = None) \
        -> Tuple[Dict, List[Command]]:
    """Extract the sequence that corresponds to the given label from the provided command list.

    A sequence can either be defined via the `SEQUENCE` command or it can be a `LINE` command.

    Parameters
    ----------
    commands : iterable of Command
        Initial command list, usually obtained from parsing a MADX script, containing the requested sequence.
    context : dict
        Command definitions used for expanding beamlines for example.
    label : str, optional
        Label of the sequence (from the `USE` command). If `None` then the first `SEQUENCE` encountered is considered.

    Returns
    -------
    attributes : dict
        The attributes of the sequence command (`{}` if the sequence was a `LINE` definition).
    sequence : list of Command
        The sequence's commands.

    Raises
    ------
    ParserError
        If no sequence with the specified label was found or the command corresponding to the label is not a sequence.
    """
    commands = iter(commands)
    if label is None:
        seq = next((c for c in commands if c.keyword == 'sequence'), None)
    else:
        seq = next((c for c in commands if c.label == label), None)
    if isinstance(seq, Command) and seq.keyword == 'sequence':
        return seq.attributes, list(it.takewhile(lambda c: c.keyword != 'endsequence', commands))
    elif isinstance(seq, Line):
        return {}, list(seq.expand(context))
    elif isinstance(seq, Command):
        raise ParserError(f'Command with label "{label}" is not a sequence: {seq}')
    else:
        raise ParserError(f'No sequence with label "{label}" found')


def label_every_element(seq: Sequence[Command],
                        *, template: Callable[[Command], str] = operator.attrgetter('keyword')) -> Sequence[Command]:
    """Fill in missing labels in the given sequence according to the given template function.

    .. Note:: The template is called for every element, its return value is assigned only to those without label.

    Parameters
    ----------
    seq : sequence of Command
        Commands will be updated in-place.
    template : callable, optional
        The argument is the command itself and the return value should be the corresponding label.
        The default is to fallback on the command's keyword.

    Returns
    -------
    labeled_seq : sequence
        The same sequence as `seq`, commands updated in-place.
    """
    for cmd in seq:
        label = template(cmd)  # In case `template` has side effects.
        if not cmd.label:
            cmd.label = label
    return seq


def extract_error_definitions(script: Iterable[Command], seq_label: str) -> Iterator[Command]:
    """Extract all error definitions as well as `SELECT` statements that are relevant for the given sequence label.

    .. Note:: If a `SELECT` command does not specify its `sequence` it is taken relevant nevertheless.

    Yields
    ------
    cmd : Command
        Statements relevant for error definitions.
    """
    for cmd in script:
        condition = (
            cmd.keyword == 'select' and cmd['flag'] == 'error' and cmd.get('sequence', seq_label) == seq_label
            or cmd.keyword in {'ealign', 'efcomp', 'eoption'}
        )
        if condition:
            yield cmd


def generate_error_specifications(script: Iterable[Command], seq: Sequence[Command]) \
        -> Dict[int, Dict[str, Union[float, Variable, DeferredExpression]]]:
    """Generate errors which are specified by the provided script via `EALIGN` and `EFCOMP` (alongside `SELECT`).

    .. Note::
       All `SELECT` statements found in `script` are applied, regardless of the `sequence` they specify.
       Filtering by sequence should therefore be done beforehand, e.g. with `extract_error_definitions`.

    Parameters
    ----------
    script : iterable of Command
        This command list needs to contain both the relevant `SELECT` as well as the `EALIGN` and `EFCOMP` commands
        (+ `EOPTION` if needed). Other non-relevant commands will be skipped over.
    seq : sequence of Command
        The sequence containing the elements to which the errors specifications refer.

    Returns
    -------
    error_dict : dict
        The error specifications per element. Keys are index positions within the sequence and values are dicts
        containing the errors.

    Raises
    ------
    NotImplementedError
        If an error is specified which is not yet implemented.
    """
    def _is_magnet_type(elem, m_type) -> bool:
        return bool(list(filter_by_class(Command('select', {'class': m_type}), [elem])))

    def _handle_select(command, state):
        if command['flag'] == 'error':
            if command.get('clear'):
                state['select'].clear()
            else:
                state['select'].append(functools.partial(select_from_sequence, command))
        return state

    def _handle_eoption(command, state):
        if 'seed' in command:
            np.random.seed(command['seed'])
        state['add'] = command.get('add', state['add'])
        return state

    def _handle_ealign(command, state):
        if set(command.attributes) & not_implemented:
            raise NotImplementedError(f'Error definitions: {set(command.attributes) & not_implemented}')
        for element in _select_elements(state):
            error_spec = state['errors'][index_positions[id(element)]]['alignment']
            if not state['add']:
                error_spec.clear()
            for err_name, err_value in command.attributes.items():
                error_spec[err_name] = error_spec.get(err_name, 0.) + err_value
        return state

    def _handle_efcomp(command, state):
        for element in _select_elements(state):
            error_spec = state['errors'][index_positions[id(element)]]['fields']
            if not state['add']:
                error_spec.clear()
            for err_name, err_value in command.attributes.items():
                err_value = evaluate_object(err_value)
                if err_name in {'dknr', 'dksr'}:
                    radius = command['radius']
                    order = command.get('order', 0)
                    if _is_magnet_type(element, 'multipole'):
                        kl_values = evaluate_object(element[f'k{"n" if radius > 0 else "s"}l'])
                        kl_ref = kl_values[order] if order < len(kl_values) else 0.
                    else:
                        try:
                            order = next(i for t, i in magnet_reference_orders.items() if _is_magnet_type(element, t))
                        except StopIteration:  # element is not a magnet.
                            continue
                        kl_ref = evaluate_object(element.get(f'k{order}', 0.) * element['l'])
                    indices = np.arange(err_value.size)
                    factorial = np.insert(np.cumprod(indices + 1)[:-1], 0, 1.0)
                    err_value = err_value * kl_ref * radius ** (order - indices) * factorial / factorial[order]
                    err_name = err_name[:-1]  # Match the following `if` condition to add as absolute errors.
                if err_name in {'dkn', 'dks'}:
                    # "dknr" can override "dkn" of the same command for example, if "add" is not set.
                    old_value = error_spec.get(err_name, np.zeros(1)) if state['add'] else np.zeros(1)
                    old_value, err_value = pad_max_shape(old_value, err_value)
                    error_spec[err_name] = old_value + err_value
        return state

    def _select_elements(state):
        return remove_duplicates([e for s in state['select'] for e in s(seq)], op=operator.is_)

    handlers = defaultdict(lambda: lambda command, state: state)  # Do nothing for non-relevant commands.
    handlers.update({f.__name__[8:]: f for f in [_handle_select, _handle_eoption, _handle_ealign, _handle_efcomp]})

    not_implemented = {'arex', 'arey', 'dphi', 'ds', 'dtheta'}  # implemented: dx, dy, dpsi, mrex, mrey, mscalx, mscaly
    magnet_reference_orders = {'rbend': 0, 'sbend': 0, 'quadrupole': 1, 'sextupole': 2, 'octupole': 3}

    index_positions = {id(x): i for i, x in enumerate(seq)}

    np.random.seed(rng_default_seed)
    state_dict = {'select': [], 'add': False, 'errors': defaultdict(lambda: {'alignment': {}, 'fields': {}})}
    for cmd in script:
        state_dict = handlers[cmd.keyword](cmd, state_dict)
    for spec in state_dict['errors'].values():
        spec.update(spec.pop('alignment'))
        field_errors = spec.pop('fields')
        spec.update({f'k{i}l' : dk for i, dk in enumerate(field_errors.pop('dkn', []))})
        spec.update({f'k{i}sl': dk for i, dk in enumerate(field_errors.pop('dks', []))})
    return dict(state_dict['errors'])


def select_from_sequence(select: Command, sequence: Sequence[Command]) -> Iterator[Command]:
    """Select elements from the given sequence according to the rules specified by the given `select` command.

    This applies the following steps in order:

    1. `select_by_range`
    2. `filter_by_class`
    3. `filter_by_pattern`

    Yields
    ------
    cmd : Command
        Commands that match the given criteria.
    """
    return filter_by_pattern(select, filter_by_class(select, select_by_range(select, sequence)))


def select_by_range(select: Command, sequence: Sequence[Command]) -> Iterator[Command]:
    """Select elements from the given sequence according to the `range` argument of the given `select` command.

    .. Note:: Using the format ``X[n]``, the occurrence count `n` starts at 1.
    .. Note:: Using the format ``x/y`` the second element `y` is included.

    Raises
    ------
    ValueError
        If the specified range has the wrong format.

    Warns
    -----
    UserWarning
        If the end index of the range specification does not match an element but the start index did.
    """
    START_MARKER, END_MARKER = '#s', '#e'
    range_pattern = re.compile(r'^(?P<name>%(identifier)s|%(start)s|%(end)s)(?:\[(?P<count>[0-9]+)\])?$'
                               % {'identifier': identifier_pattern.pattern, 'start': START_MARKER, 'end': END_MARKER})
    counts = defaultdict(int)  # Running class counts.

    def _match_command(cmd: Command, name_: str, count_: Union[int, str, type(None)]) -> bool:
        """name_ indicates the label if count_ is None and otherwise, if label is None, the keyword;
           then the n-th instance of that class is considered (indicated by count_);
           counts are indexed starting at 1.
           Note that within a sequence `base;` creates an instance of class `base` while `label: base;` creates a new
           class `label` and then instantiates it, i.e. creates an instance of class `label`.
        """
        if count_ is None:
            return name_ == cmd.label
        cls_name = cmd.label or cmd.keyword
        return name_ == cls_name and counts[cls_name] == int(count_)

    try:
        range_ = select['range']
    except KeyError:
        range_ = START_MARKER, END_MARKER
    else:
        range_ = range_.split('/')

    r_matches = tuple(re.match(range_pattern, x) for x in range_)
    if any(x is None for x in r_matches):
        raise ValueError(f'Illegal range specification: {range_}')

    if len(r_matches) == 1 or r_matches[0].string == r_matches[1].string:
        try:
            yield sequence[{START_MARKER: 0, END_MARKER: -1}[r_matches[0].string]]
        except KeyError:
            count = r_matches[0].group('count')
            if count is None:
                filtered = filter(lambda cmd: _match_command(cmd, r_matches[0].group('name'), None), sequence)
                count = 1
            else:
                filtered = filter(lambda cmd: _match_command(cmd, r_matches[0].group('name'), 0), sequence)
                count = int(count)
            yield from it.islice(filtered, count - 1, count)
        return

    r_matches = iter(r_matches)
    name, count = next(r_matches).group('name', 'count')
    in_range = name == START_MARKER
    if in_range:
        name, count = next(r_matches).group('name', 'count')
    for command in sequence:
        counts[command.label or command.keyword] += 1
        match = _match_command(command, name, count)
        in_range ^= match
        if in_range or match:
            yield command
        if match:
            try:
                name, count = next(r_matches).group('name', 'count')
            except StopIteration:
                break
    else:
        if in_range and name != END_MARKER:
            warnings.warn(f'End index did not match anything: name: {repr(name)}, count: {count}')


def filter_by_class(select: Command, sequence: Iterable[Command]) -> Iterator[Command]:
    """Filter the given sequence by the specified `class` argument of the given `select` command."""

    def _get_aro(cmd: Command) -> Iterator[str]:
        """Attribute resolution order, i.e. the ancestor chain of the command."""
        yield cmd.keyword
        if cmd.base is not None:
            yield from _get_aro(cmd.base)

    if 'class' in select:
        yield from filter(lambda cmd: select['class'] in _get_aro(cmd), sequence)
    else:
        yield from iter(sequence)


def filter_by_pattern(select: Command, sequence: Iterable[Command]) -> Iterator[Command]:
    """Filter the given sequence by the specified `pattern` argument of the given `select` command."""
    if 'pattern' in select:
        pattern = re.compile(select['pattern'])
        yield from filter(lambda cmd: cmd.label is not None and re.match(pattern, cmd.label), sequence)
    else:
        yield from iter(sequence)


def pad_sequence(sequence: Iterable[Command], l: float, *,
                 refer: str = 'center', drift_label: Callable[[int], str] = 'pad_drift_{}'.format) -> Iterator[Command]:
    """Pad sequence with drift spaces, filling implicit gaps.

    .. Note:: Only implicit gaps of minimum 1 micrometer are considered.

    Parameters
    ----------
    sequence : iterable of Command
    l : float
        Total length of the sequence.
    refer : {'entry', 'center', 'centre', 'exit'}
        Specifies which part of the target is taken as the reference point at which the position along the beamline
        is given (via `at`).
    drift_label : callable
        Will be called with the total target index (starting at 0), should return a corresponding (unique) label.

    Yields
    ------
    padded_sequence : iterable of Command
        The sequence padded with drift spaces, labels chosen via `drift_label`.

    Raises
    ------
    ParserError
        If a negative offset between two neighboring elements is found. The tolerance for such offsets is controlled
        by the global variable `negative_offset_tolerance`.
    """
    try:
        length_factor = {'entry': 0, 'center': 0.5, 'centre': 0.5, 'exit': 1}[refer]
    except KeyError:
        raise ValueError(f'Invalid reference point indicator: {refer}') from None
    end_marker = Command('#e', dict(at=l))
    positions = {'#s': 0}
    s = 0
    for i, command in enumerate(it.chain(sequence, [end_marker])):
        pos = positions[command.attributes.get('from', '#s')] + command.attributes['at']
        length = command.get('l', 0)
        offset = (pos - length_factor*length) - s
        if offset < negative_offset_tolerance:
            raise ParserError(f'Negative offset between element {command} and the previous one: {offset:e}')
        elif offset >= minimum_offset_for_drift:
            yield Command('drift', {'l': offset, 'at': s + length_factor*offset}, drift_label(i))
        if command is not end_marker:
            yield command
        s = pos + (1 - length_factor) * length  # Update `s` to point to the exit of the element.
        positions[command.label] = pos + (0.5 - length_factor) * length  # "from" is relative to the element's center.


def sequence_to_data_frame(sequence: Sequence[Command]) -> pd.DataFrame:
    """Convert the given sequence of elements (commands) to a data frame.

    The resulting data frame's indices correspond to the elements' labels and the columns correspond to their attributes.
    Attribute values are NaN (not-a-number) where no such attribute is applicable.

    Parameters
    ----------
    sequence : sequence of Command

    Returns
    -------
    data : pd.DataFrame
        Indices are element labels, columns are element attributes. Values are filled with NaN wherever the corresponding
        attribute is not applicable. Contains additional columns "keyword" which indicates the commands' keywords
        and "type" which indicates the commands' root keyword.
    """
    return pd.DataFrame.from_dict({cmd.label: {**cmd.attributes, 'keyword': cmd.keyword, 'type': cmd.root.keyword}
                                   for cmd in sequence}, orient='index')


def data_frame_to_sequence(data: pd.DataFrame) -> List[Command]:
    """Convert the given data frame to a sequence of elements (commands).

    For details see :func:`sequence_to_data_frame`. This is the inverse operation of that function.
    """
    return [Command(values['keyword'], values.drop(['keyword', 'type']).dropna().to_dict(), label,
                    base=Command(values['type']))
            for label, values in data.iterrows()]
