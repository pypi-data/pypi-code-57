import itertools as it
import keyword
import operator as op
import os
import re
import tempfile
import unittest

import numpy as np
import scipy.special
import scipy.stats

from dipas.madx.builder import write_attribute_increment, write_attribute_assignment, write_attribute_value, \
    write_command, write_attributes
from dipas.madx.parser import eval_expr, parse_file, parse_script, parse_attributes, parse_statement, \
    special_names, resolve_calling_sites, DeferredExpression, safe_math_eval, register_handler, statement_handlers
from dipas.madx.parser import replace_dots_in_variable_names, remove_multi_line_comments, remove_comments, \
    remove_whitespace, normalize_variable_indicators, VARIABLE_INDICATOR, Command, Line, Variable, extract_sequence, \
    pad_sequence
from dipas.madx.parser import label_every_element, select_by_range, filter_by_class, filter_by_pattern, \
    extract_error_definitions, generate_error_specifications
from dipas.madx.parser import ParserError
from dipas.madx.parser import sequence_to_data_frame, data_frame_to_sequence
import dipas.madx.parser
from dipas.madx.utils import run_script


def _dedent_script(script):
    script = script.strip(' \n')
    script = re.sub(r'^ *$(?=\n)', '', script, flags=re.MULTILINE)
    indentation = min(map(len, re.findall(r'^ +', script, flags=re.MULTILINE)))
    return re.sub(rf'^ {{{indentation}}}', '', script, flags=re.MULTILINE).strip('\n')


class TestSafeMathEval(unittest.TestCase):
    def test_error(self):
        for x in ('import os', '().__class__', '(1, 2)', '1 + 2; 3 * 4', '{1: 2}', '[1]', 'lambda: None',
                  '__builtins__', '{1, 2}', '{}', '()', '[]', '1, 2'):
            with self.subTest(x=x):
                self.assertRaises(ValueError, safe_math_eval, x)

    # noinspection PyArgumentList,PyTypeChecker
    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            safe_math_eval(10)


class TestEvalExpr(unittest.TestCase):
    def test_str(self):
        self.assertEqual(eval_expr('"1"'), '1')
        self.assertEqual(eval_expr('"1 * 2"'), '1 * 2')
        self.assertEqual(eval_expr('"test"'), 'test')
        self.assertEqual(eval_expr('test'), 0.)

    def test_int(self):
        for x in ('1', '123'):
            self.assertEqual(eval_expr(x), int(x))

    def test_float(self):
        for x in ('1.', '1.0', '0.123e-6'):
            self.assertEqual(eval_expr(x), float(x))
        # int takes precedence over float.
        self.assertEqual(eval_expr('1'), 1)

    def test_array(self):
        self.assertListEqual(eval_expr('{1, 2*3, 4+5}').tolist(), [1, 6, 9])
        self.assertListEqual(eval_expr('{1, {2*3 , 4 + 5}}'), [1, [6, 9]])
        self.assertListEqual(eval_expr('{1 + 1, {2 * 3, { 4 }}}'), [2, [6, [4]]])
        self.assertListEqual(eval_expr('{(1 + 2) * 3}').tolist(), [9])

    def test_rng(self):
        for name in ('ranf', 'gauss'):
            np.random.seed(0)
            expected = special_names[name]()
            np.random.seed(0)
            self.assertEqual(eval_expr(f'{name}()'), float(str(expected)))
            np.random.seed(0)
            self.assertEqual(eval_expr(f'2 * {name}() + 1'), 2 * float(str(expected)) + 1)
        np.random.seed(0)
        expected = scipy.stats.truncnorm.rvs(-2, 2)
        np.random.seed(0)
        self.assertEqual(eval_expr('tgauss(2)'), float(str(expected)))
        np.random.seed(0)
        self.assertEqual(eval_expr('2 * tgauss(2) + 1'), 2 * float(str(expected)) + 1)

    def test_expr(self):
        self.assertEqual(eval_expr('2 * cos(pi / 3) + (1 / log10(100))'), 2 * np.cos(np.pi / 3) + (1 / np.log10(100)))
        # noinspection PyTypeChecker
        self.assertEqual(eval_expr('erf(2) * erfc(3)'), scipy.special.erf(2) * scipy.special.erfc(3))
        self.assertEqual(eval_expr('twopi * (pmass + nmass) / qelect'),
                         special_names['twopi']
                         * (special_names['pmass'] + special_names['nmass'])
                         / special_names['qelect'])

    def test_deferred_expr(self):
        e = DeferredExpression('2 * 3')
        self.assertIs(eval_expr(e), e)

    def test_impossible_name_resolution(self):
        dipas.madx.parser.allow_popup_variables = False
        try:
            with self.assertRaises(NameError):
                eval_expr('unknown')
        finally:
            dipas.madx.parser.allow_popup_variables = True
        with self.assertRaises(NameError):
            eval_expr('a * b')

    def test_error(self):
        for x in ('import os', '().__class__', '(1, 2)', '1 + 2; 3 * 4', '{1: 2}', '[1]', 'lambda: None',
                  '__builtins__', '()', '[]', '1, 2'):
            with self.subTest(x=x):
                self.assertRaises(ValueError, eval_expr, x)
        with self.assertRaises(ValueError):
            eval_expr('''(
            )''')
        with self.assertRaises(ValueError):
            eval_expr('''[
            1
            ,
            2
            ]''')
        for x in dir(__builtins__):
            with self.subTest(x=x):
                if x.startswith('__') or 'import' in x.lower():
                    self.assertRaises(ValueError, eval_expr, x)
                elif x not in special_names and not keyword.iskeyword(x):
                    self.assertEqual(eval_expr(x), 0.)
                    dipas.madx.parser.allow_popup_variables = False
                    try:
                        with self.assertRaises(NameError):
                            eval_expr(x)
                    finally:
                        dipas.madx.parser.allow_popup_variables = True

    # noinspection PyArgumentList,PyTypeChecker
    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            eval_expr(10)


class TestParseStatement(unittest.TestCase):
    def test_comment(self):
        stmt = '// This is a comment'
        stmt_type, match = parse_statement(stmt)
        self.assertEqual(stmt_type, 'comment')
        self.assertEqual(match.group(1), stmt[3:])

        stmt = '// a = 1'
        stmt_type, match = parse_statement(stmt)
        self.assertEqual(stmt_type, 'comment')
        self.assertEqual(match.group(1), stmt[3:])

        stmt = '! another comment'
        stmt_type, match = parse_statement(stmt)
        self.assertEqual(stmt_type, 'comment')
        self.assertEqual(match.group(1), stmt[2:])

    def test_variable(self):
        stmt_type, match = parse_statement('a = 1')
        self.assertEqual(stmt_type, 'variable')
        self.assertEqual(match.group('name'), 'a')
        self.assertEqual(match.group('value'), '1')

        stmt_type, match = parse_statement('const test = ranf()')
        self.assertEqual(stmt_type, 'variable')
        self.assertEqual(match.group('name'), 'test')
        self.assertEqual(match.group('value'), 'ranf()')
        self.assertEqual(match.group('assignment'), '=')

        stmt_type, match = parse_statement('const test_123 := 10 * (nmass + pmass)')
        self.assertEqual(stmt_type, 'variable')
        self.assertEqual(match.group('name'), 'test_123')
        self.assertEqual(match.group('value'), '10 * (nmass + pmass)')
        self.assertEqual(match.group('assignment'), ':=')

        stmt_type, match = parse_statement('quad1->k1 = 0.123')
        self.assertEqual(stmt_type, 'variable')
        self.assertEqual(match.group('name'), 'quad1')
        self.assertEqual(match.group('attr'), 'k1')
        self.assertEqual(match.group('value'), '0.123')

    def test_deferred_assignment(self):
        stmt_type, match = parse_statement('k1 := 0.123')
        self.assertEqual(stmt_type, 'variable')
        self.assertEqual(match.group('name'), 'k1')
        self.assertEqual(match.group('value'), '0.123')
        self.assertEqual(match.group('assignment'), ':=')

    def test_command(self):
        stmt_type, match = parse_statement('test_label: test_command, a = 1, b = "2 abc"')
        self.assertEqual(stmt_type, 'command')
        self.assertEqual(match.group('label'), 'test_label')
        self.assertEqual(match.group('keyword'), 'test_command')
        self.assertEqual(match.group('attributes'), 'a = 1, b = "2 abc"')

        stmt_type, match = parse_statement('abc123')
        self.assertEqual(stmt_type, 'command')
        self.assertEqual(match.group('label'), None)
        self.assertEqual(match.group('keyword'), 'abc123')
        self.assertEqual(match.group('attributes'), None)

        stmt_type, match = parse_statement('abc123, flag')
        self.assertEqual(stmt_type, 'command')
        self.assertEqual(match.group('label'), None)
        self.assertEqual(match.group('keyword'), 'abc123')
        self.assertEqual(match.group('attributes'), 'flag')

        stmt_type, match = parse_statement('xyz: abc123, flag, flag2, x = {1, 2, 3}, y = (1 + 2) * 3')
        self.assertEqual(stmt_type, 'command')
        self.assertEqual(match.group('label'), 'xyz')
        self.assertEqual(match.group('keyword'), 'abc123')
        self.assertEqual(match.group('attributes'), 'flag, flag2, x = {1, 2, 3}, y = (1 + 2) * 3')

        stmt_type, match = parse_statement('xyz: abc123, x = {1 + 1, {2 * 3, { 4 }}}, y = {(1 + 2) * 3}')
        self.assertEqual(stmt_type, 'command')
        self.assertEqual(match.group('label'), 'xyz')
        self.assertEqual(match.group('keyword'), 'abc123')
        self.assertEqual(match.group('attributes'), 'x = {1 + 1, {2 * 3, { 4 }}}, y = {(1 + 2) * 3}')

        with self.subTest('Test command without attributes'):
            stmt_type, match = parse_statement('label: command')
            self.assertEqual(stmt_type, 'command')
            self.assertEqual(match.group('label'), 'label')
            self.assertEqual(match.group('keyword'), 'command')
            self.assertIs(match.group('attributes'), None)

        with self.subTest('Test command without attributes and without label'):
            stmt_type, match = parse_statement('command')
            self.assertEqual(stmt_type, 'command')
            self.assertIs(match.group('label'), None)
            self.assertEqual(match.group('keyword'), 'command')
            self.assertIs(match.group('attributes'), None)

        self.assertTupleEqual(parse_statement('label: command, d = "1" + 2'), (None, None))

    def test_line_definition(self):
        stmt_type, match = parse_statement('test: LINE=(a, -(b, c), d)')
        self.assertEqual(stmt_type, 'line')
        self.assertEqual(match.group('label'), 'test')
        self.assertEqual(match.group('elements'), '(a, -(b, c), d)')
        stmt_type, match = parse_statement('test: LINE=(element_1, -other_element, 2*a_b_c, -3*element.name)')
        self.assertEqual(stmt_type, 'line')
        self.assertEqual(match.group('label'), 'test')
        self.assertEqual(match.group('elements'), '(element_1, -other_element, 2*a_b_c, -3*element.name)')
        stmt_type, match = parse_statement('test: LINE=(e1, -3*(a, b, c), 2*(x, -(y, z)))')
        self.assertEqual(stmt_type, 'line')
        self.assertEqual(match.group('label'), 'test')
        self.assertEqual(match.group('elements'), '(e1, -3*(a, b, c), 2*(x, -(y, z)))')

    def test_unknown_statement(self):
        self.assertTupleEqual(parse_statement("This statement cannot be parsed"), (None, None))
        self.assertTupleEqual(parse_statement("beam, energy = ?"), (None, None))
        self.assertTupleEqual(parse_statement("beam,, energy = 1"), (None, None))


class TestCommand(unittest.TestCase):
    def test_bases(self):
        c = Command('c', dict(x=1, y=2))
        d = Command('d', dict(x=5, z=3), base=c)
        self.assertDictEqual(d.attributes, dict(x=5, y=2, z=3))
        e = Command('e', dict(u=123, v=456), base=d)
        self.assertDictEqual(e.attributes, dict(x=5, y=2, z=3, u=123, v=456))

    def test_del_get_set_item(self):
        c = Command('c', dict(x=1, y=2))
        d = Command('d', dict(x=5, z=3), base=c)
        e = Command('e', dict(u=123, v=456), base=d)
        self.assertEqual(c['x'], 1)
        self.assertEqual(c['y'], 2)
        self.assertEqual(d['x'], 5)
        self.assertEqual(d['y'], 2)
        self.assertEqual(d['z'], 3)
        self.assertEqual(e['x'], 5)
        self.assertEqual(e['y'], 2)
        self.assertEqual(e['z'], 3)
        self.assertEqual(e['u'], 123)
        self.assertEqual(e['v'], 456)

        e['x'] = 789
        self.assertEqual(c['x'], 1)
        self.assertEqual(d['x'], 5)
        self.assertEqual(e['x'], 789)

        del e['x']
        self.assertEqual(c['x'], 1)
        self.assertEqual(d['x'], 5)
        self.assertEqual(e['x'], 5)

        del e['x']
        self.assertEqual(c['x'], 1)
        self.assertEqual(d['x'], 1)
        self.assertEqual(e['x'], 1)

        with self.assertRaises(KeyError):
            del d['u']

        del e['z']
        with self.assertRaises(KeyError):
            __ = e['z']
        with self.assertRaises(KeyError):
            __ = d['z']

    def test_root(self):
        c1 = Command('c1', dict(x=1))
        c2 = Command('c2', dict(x=2), base=c1)
        c3 = Command('c3', dict(x=3), base=c2)
        self.assertIs(c3.base, c2)
        self.assertIs(c3.root, c1)


class TestLine(unittest.TestCase):
    def test_simple(self):
        context = {x: Command(x) for x in 'abcd'}
        line = ('a', 'b', 'c', 'd', 'a', 'd')
        expanded = tuple(Line(line).expand(context))
        self.assertEqual(len(expanded), len(line))
        self.assertTrue(all(it.starmap(op.eq, zip(expanded, tuple(context[x] for x in line)))))

    def test_nested(self):
        context = {x: Command(x) for x in 'abcde'}
        context['top'] = Line(['a', 'b', 's', 'b', 'a', 's', 'a', 'b'])
        context['s'] = Line(['c', 'd', 'e'])
        expanded = tuple(context['top'].expand(context))
        expected = tuple(context[x] for x in 'a b c d e b a c d e a b'.split())
        self.assertEqual(len(expanded), len(expected))
        self.assertTrue(all(it.starmap(op.eq, zip(expanded, expected))))

    def test_reflection_and_repetition(self):
        context = {x: Command(x) for x in 'abcdefgh'}
        context['r'] = Line(['g', 'h'])
        context['s'] = Line(['c', 'r', 'd'])
        context['top'] = Line(['2*s', 2*Line(['e', 'f']), '-s', -3*Line(['a', 'b']), '-2*c'])
        expanded = tuple(context['top'].expand(context))
        expected = tuple(context[x] for x in 'c g h d c g h d e f e f d h g c b a b a b a c c'.split())
        self.assertEqual(len(expanded), len(expected))
        self.assertEqual(''.join(c.keyword for c in expanded), ''.join(c.keyword for c in expected))
        self.assertTrue(all(it.starmap(op.eq, zip(expanded, expected))))

    def test_parse(self):
        parsed = Line.parse('(2*s, 2*(e,f), -s, -(a,b), -2*c)')
        self.assertEqual(parsed.elements[0], '2*s')
        self.assertTupleEqual(parsed.elements[1].elements, ('e', 'f', 'e', 'f'))
        self.assertEqual(parsed.elements[2], '-s')
        self.assertTupleEqual(parsed.elements[3].elements, ('-b', '-a'))
        self.assertEqual(parsed.elements[4], '-2*c')
        context = {x: Command(x) for x in 'abcdefgh'}
        context['r'] = Line(['g', 'h'])
        context['s'] = Line(['c', 'r', 'd'])
        expanded = tuple(parsed.expand(context))
        expected = tuple(context[x] for x in 'c g h d c g h d e f e f d h g c b a c c'.split())
        self.assertEqual(len(expanded), len(expected))
        self.assertEqual(''.join(c.keyword for c in expanded), ''.join(c.keyword for c in expected))
        self.assertTrue(all(it.starmap(op.eq, zip(expanded, expected))))

        parsed = Line.parse('(2 * (a, b), -3 * (c, 2*(d, e)))')
        self.assertTupleEqual(parsed.elements[0].elements, ('a', 'b', 'a', 'b'))
        self.assertTupleEqual(parsed.elements[1].elements[0].elements, ('-e', '-d', '-e', '-d'))
        self.assertEqual(parsed.elements[1].elements[1], '-c')
        self.assertTupleEqual(parsed.elements[1].elements[2].elements, ('-e', '-d', '-e', '-d'))
        self.assertEqual(parsed.elements[1].elements[3], '-c')
        self.assertTupleEqual(parsed.elements[1].elements[4].elements, ('-e', '-d', '-e', '-d'))
        self.assertEqual(parsed.elements[1].elements[5], '-c')
        context = {x: Command(x) for x in 'abcde'}
        expanded = tuple(parsed.expand(context))
        expected = tuple(context[x] for x in 'a b a b e d e d c e d e d c e d e d c'.split())
        self.assertEqual(len(expanded), len(expected))
        self.assertEqual(''.join(c.keyword for c in expanded), ''.join(c.keyword for c in expected))
        self.assertTrue(all(it.starmap(op.eq, zip(expanded, expected))))

    def test_errors(self):
        with self.assertRaises(TypeError):
            2.0 * Line('abc')

    def test_parse_error(self):
        with self.assertRaises(TypeError):
            Line.parse('(2 * [1, 2])')
        with self.assertRaises(TypeError):
            Line.parse('import os')


# noinspection PyTypeChecker
class TestDeferredExpression(unittest.TestCase):
    def test(self):
        e = DeferredExpression('1 + 2 * 3')
        self.assertEqual(e.value, 7)
        self.assertEqual(e.value, 7)

    def test_math_with_numbers(self):
        e = DeferredExpression('1 + 2')
        self.assertEqual(3 * e, 9)
        self.assertEqual(e * 3, 9)
        self.assertEqual(3.0 * e, 9.0)
        self.assertEqual(e * 3.0, 9.0)

    def test_math_with_other_expressions(self):
        e1 = DeferredExpression('1 + 2')
        e2 = DeferredExpression('4 + 5')
        e3 = DeferredExpression('e1 * e2', {'e1': e1, 'e2': e2})
        self.assertEqual(e3.value, 27)
        e4 = DeferredExpression('e1 + e2 * e3', {'e1': e1, 'e2': e2, 'e3': e3})
        self.assertEqual(e4.value, 3 + 9*27)


# noinspection PyTypeChecker
class TestVariables(unittest.TestCase):
    def test_math(self):
        v = Variable(2) + 5
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 7)

        v = 2 * Variable(3)
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 6)

        # noinspection PyUnresolvedReferences
        v = Variable(2) ** Variable(5)
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 32)

        v = Variable(2)
        v += 5
        v *= Variable(10)
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 70)

    def test_deferred_expressions(self):
        v = Variable(DeferredExpression('1 + 2')) * 5
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 15)

        v = 5 * Variable(DeferredExpression('2 * 3'))
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 30)

        v = Variable(DeferredExpression('1 + 2'))
        v *= 4
        v += Variable(5)
        self.assertIsInstance(v, Variable)
        self.assertEqual(v.value, 17)

    def test_unwrap(self):
        v1 = Variable(1)
        e1 = DeferredExpression('2 * v1', {'v1': v1})
        v2 = Variable(e1)
        e2 = DeferredExpression('3 * v2', {'v2': v2})
        v3 = Variable(e2)
        e3 = DeferredExpression('4 * v3', {'v3': v3})
        v4 = Variable(e3)
        self.assertEqual(Variable.unwrap(v1), (True, 1))
        self.assertEqual(Variable.unwrap(e1), (True, 2))
        self.assertEqual(Variable.unwrap(v2), (True, 2))
        self.assertEqual(Variable.unwrap(e2), (True, 6))
        self.assertEqual(Variable.unwrap(v3), (True, 6))
        self.assertEqual(Variable.unwrap(e3), (True, 24))
        self.assertEqual(Variable.unwrap(v4), (True, 24))

        e1 = DeferredExpression('2 * 3')
        e2 = DeferredExpression('4 * e1', {'e1': e1})
        self.assertEqual(Variable.unwrap(e2), (False, 24))


class TestParseAttributes(unittest.TestCase):
    def test(self):
        attrs = parse_attributes('a = 1, b = 2, c = false, d, e = ranf()')
        self.assertEqual(attrs[0][0], 'a')
        self.assertEqual(attrs[0][1], '=')
        self.assertEqual(attrs[0][2], '1')
        self.assertEqual(attrs[1][0], 'b')
        self.assertEqual(attrs[1][2], '2')
        self.assertEqual(attrs[2][0], 'c')
        self.assertEqual(attrs[2][2], 'false')
        self.assertEqual(attrs[3][0], 'd')
        self.assertEqual(attrs[3][2], 'true')
        self.assertEqual(attrs[4][0], 'e')
        self.assertEqual(attrs[4][2], 'ranf()')

    def test_quoted_strings(self):
        attrs = parse_attributes('a = "test string", b = "string, with, commas"')
        self.assertEqual(attrs[0][2], '"test string"')
        self.assertEqual(attrs[1][2], '"string, with, commas"')

    def test_arrays(self):
        attrs = parse_attributes('a = {1, 2, 3}, b = "{1, 2, 3}"')
        self.assertEqual(attrs[0][2], '{1, 2, 3}')
        self.assertEqual(attrs[1][2], '"{1, 2, 3}"')
        attrs = parse_attributes('x = {1 + 1, {2 * 3, { 4 }}}, y = {(1 + 2) * 3}')
        self.assertEqual(attrs[0][2], '{1 + 1, {2 * 3, { 4 }}}')
        self.assertEqual(attrs[1][2], '{(1 + 2) * 3}')

    def test_deferred_assignment(self):
        attrs = parse_attributes('a := ranf()')
        self.assertEqual(attrs[0][2], 'ranf()')

    def test_empty(self):
        self.assertSequenceEqual(parse_attributes(''), [])


class TestParseScript(unittest.TestCase):
    def test(self):
        script = '''
            // This is a comment.
            a = 1;
            b = 2 * a;
            c: command, d = 3*b;
        '''
        script = self.dedent_script(script)
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertSequenceEqual(commands, [Command('command', {'d': 6}, 'c')])
        self.assertDictEqual(context, dict(c=commands[0]))
        self.assertDictEqual(variables, dict(a=1, b=2))

    def test_command_without_attributes(self):
        parsed_script = parse_script('label: command;')
        self.assertSequenceEqual(parsed_script.commands, [Command('command', label='label')])
        self.assertDictEqual(parsed_script.context, dict(label=parsed_script.commands[0]))
        self.assertDictEqual(parsed_script.variables, {})

    def test_command_without_attributes_and_without_label(self):
        parsed_script = parse_script('command;')
        self.assertSequenceEqual(parsed_script.commands, [Command('command')])
        self.assertDictEqual(parsed_script.context, {})
        self.assertDictEqual(parsed_script.variables, {})

    def test_derived_command(self):
        parsed_script = parse_script(self.dedent_script('''
            Q1: quadrupole, l = 1.0, k1 = 2.0;
            Q1, k1 = 4.0;
        '''))
        commands = parsed_script.commands
        self.assertEqual(len(commands), 2)
        self.assertIs(commands[1].base, commands[0])
        self.assertEqual(commands[0].label, 'q1')
        self.assertIs(commands[1].label, None)
        self.assertEqual(commands[0]['l'], 1.0)
        self.assertEqual(commands[0]['k1'], 2.0)
        self.assertEqual(commands[1]['l'], 1.0)
        self.assertEqual(commands[1]['k1'], 4.0)
        self.assertDictEqual(parsed_script.context, dict(q1=commands[0]))
        self.assertDictEqual(parsed_script.variables, {})

    def test_update_attribute(self):
        script = '''
            label: command, a = 1;
            label->a = 2;
        '''
        script = self.dedent_script(script)
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertSequenceEqual(commands, [Command('command', {'a': 2}, 'label')])
        self.assertDictEqual(context, dict(label=commands[0]))
        self.assertDictEqual(variables, {})

    def test_deferred_assignment(self):
        script = self.dedent_script('''
            a := 1;
            b := 1 + a;
            command, c = b;
            a = 2;
            command, d = b;
        ''')
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertEqual(commands[0]['c'], 2)
        self.assertEqual(commands[1]['d'], 3)
        self.assertDictEqual(context, {})
        self.assertEqual(variables['a'], 2)
        self.assertIsInstance(variables['b'], DeferredExpression)
        self.assertEqual(variables['b'].expr, '1+a')
        self.assertEqual(variables['b'].value, 3)

        script = self.dedent_script('''
            a := 2*ranf();
            command, x = a;
            command, y = a;
            command, z = a;
        ''')
        np.random.seed(0)
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        np.random.seed(0)
        self.assertEqual(commands[0]['x'], 2*np.random.random())
        self.assertEqual(commands[1]['y'], 2*np.random.random())
        self.assertEqual(commands[2]['z'], 2*np.random.random())
        self.assertDictEqual(context, {})
        self.assertIsInstance(variables['a'], DeferredExpression)
        self.assertEqual(variables['a'].expr, '2*ranf()')

        script = self.dedent_script('''
            a := 2 * 1;
            b := 3 * a;
            c := 4 * b;
            d := 5 * c;
            e := 6 * d;
            command, a = a, b = b, c = c, d = d, e = e;
            c = 10;
            command, a = a, b = b, c = c, d = d, e = e;
        ''')
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertEqual(commands[0]['a'], 2)
        self.assertEqual(commands[0]['b'], 6)
        self.assertEqual(commands[0]['c'], 24)
        self.assertEqual(commands[0]['d'], 120)
        self.assertEqual(commands[0]['e'], 720)
        self.assertEqual(commands[1]['a'], 2)
        self.assertEqual(commands[1]['b'], 6)
        self.assertEqual(commands[1]['c'], 10)
        self.assertEqual(commands[1]['d'], 50)
        self.assertEqual(commands[1]['e'], 300)
        self.assertDictEqual(context, {})
        # noinspection PyTypeChecker
        self.assertSequenceEqual([type(variables[x]) for x in 'abcde'],
                                 [DeferredExpression]*2 + [int] + [DeferredExpression]*2)

        script = self.dedent_script('''
            command, x := ranf();
        ''')
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertIsInstance(commands[0]['x'], DeferredExpression)
        self.assertDictEqual(context, {})
        self.assertDictEqual(variables, {})

    def test_flow_variables(self):
        script = '''
            a = 1;  // {variable_indicator};
            // {variable_indicator}
            b = 2;
            c1: command, x = a, y = b, z = 3;
            c1->z = 4;  // {variable_indicator}
        '''.format(variable_indicator=VARIABLE_INDICATOR)
        script = self.dedent_script(script)
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertSequenceEqual(commands,
                                 [Command('command', {'x': Variable(1), 'y': Variable(2), 'z': Variable(4)}, 'c1')])
        self.assertDictEqual(context, dict(c1=commands[0]))
        self.assertIsInstance(variables['a'], Variable)
        self.assertEqual(variables['a'].value, 1)
        self.assertIsInstance(variables['b'], Variable)
        self.assertEqual(variables['b'].value, 2)

    def test_flow_variables_with_deferred_assignment(self):
        script = self.dedent_script('''
            dx := gauss();  // {variable_indicator}
            ealign, dx = dx, range = "Q1"; 
            ealign, dx = dx, range = "Q2"; 
            ealign, dx = dx, range = "Q3"; 
        '''.format(variable_indicator=VARIABLE_INDICATOR))
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertIsInstance(commands[0]['dx'], Variable)
        self.assertIsInstance(commands[1]['dx'], Variable)
        self.assertIsInstance(commands[2]['dx'], Variable)
        self.assertIsInstance(commands[0]['dx'].source, DeferredExpression)
        self.assertIsInstance(commands[1]['dx'].source, DeferredExpression)
        self.assertIsInstance(commands[2]['dx'].source, DeferredExpression)
        np.random.seed(0)
        value = commands[0]['dx'].value
        np.random.seed(0)
        self.assertEqual(value, np.random.normal())
        self.assertDictEqual(context, {})
        self.assertIsInstance(variables['dx'], Variable)

    # noinspection PyUnresolvedReferences
    def test_line_definition(self):
        script = self.dedent_script('''
            q1: quadrupole;
            q2: quadrupole;
            q3: quadrupole;
            l1: LINE=(q1,2*q2,3*q3);
            l2: LINE=(-l1, -2*(q1, q2, q3), -3*l1);
        ''')
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertSequenceEqual([type(x) for x in commands], [Command]*3 + [Line]*2)
        self.assertDictEqual(context,
                             dict(q1=commands[0], q2=commands[1], q3=commands[2], l1=commands[3], l2=commands[4]))
        self.assertDictEqual(variables, {})
        self.assertSequenceEqual(context['l1'].elements, ['q1', '2*q2', '3*q3'])
        self.assertSequenceEqual(context['l2'].elements[1].elements, ['-q3', '-q2', '-q1', '-q3', '-q2', '-q1'])

    def test_misplaced_variable_indicator(self):
        script = self.dedent_script('''
            // {variable_indicator}
            c1: command, x = 1;
        '''.format(variable_indicator=VARIABLE_INDICATOR))
        with self.assertRaises(ParserError):
            parse_script(script)

    def test_attribute_references_with_deferred_expressions(self):
        script = self.dedent_script('''
            k1l := 8;
            l = 2;
            q: quadrupole, k1 := k1l/l;
            x = q->k1;
            y = 2*q->k1 + q->k1*3;
            z := 2*q->k1 + q->k1*3;
            p: quadrupole, k1 = 5*q->k1 + y + z, k1_def := 5*q->k1 + y + z;
            a = p->k1 + p->k1_def;
        ''')
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertIsInstance(variables['k1l'], DeferredExpression)
        self.assertEqual(variables['k1l'].value, 8)
        self.assertIsInstance(context['q'], Command)
        self.assertIsInstance(context['q']['k1'], DeferredExpression)
        self.assertEqual(context['q']['k1'].value, 4.)
        self.assertEqual(variables['x'], 4.)
        self.assertEqual(variables['y'], 20.)
        self.assertIsInstance(variables['z'], DeferredExpression)
        self.assertEqual(variables['z'].value, 20.)
        self.assertEqual(context['p']['k1'], 60.)
        self.assertIsInstance(context['p']['k1_def'], DeferredExpression)
        self.assertEqual(context['p']['k1_def'].value, 60.)
        self.assertEqual(variables['a'], 120.)

    def test_attribute_references_with_deferred_expressions_and_variables(self):
        script = self.dedent_script('''
            k1l := 8;  // {variable_indicator}
            l = 2;
            q: quadrupole, k1 := k1l/l;
            x = q->k1;
            y = 2*q->k1 + q->k1*3;
            z := 2*q->k1 + q->k1*3;
            p: quadrupole, k1 = 5*q->k1 + y + z, k1_def := 5*q->k1 + y + z;
            a = p->k1 + p->k1_def;
        '''.format(variable_indicator=VARIABLE_INDICATOR))
        parsed_script = parse_script(script)
        commands, context, variables = parsed_script.commands, parsed_script.context, parsed_script.variables
        self.assertIsInstance(variables['k1l'], Variable)
        self.assertEqual(variables['k1l'].value, 8)
        self.assertIsInstance(context['q'], Command)
        self.assertIsInstance(context['q']['k1'], DeferredExpression)
        self.assertIsInstance(context['q']['k1'].value, Variable)
        self.assertEqual(context['q']['k1'].value.value, 4.)
        self.assertEqual(variables['x'], 4.)
        self.assertEqual(variables['y'], 20.)
        self.assertIsInstance(variables['z'], DeferredExpression)
        self.assertEqual(variables['z'].value, 20.)
        self.assertEqual(context['p']['k1'], 60.)
        self.assertIsInstance(context['p']['k1_def'], DeferredExpression)
        self.assertEqual(context['p']['k1_def'].value, 60.)
        self.assertEqual(variables['a'], 120.)

    def test_unknown_statement(self):
        script = self.dedent_script('''
            // This is a comment.
            a = 1;
            --> oops ;
            b = 2 * a;
            c: command, d = 3*b;
        ''')
        with self.assertRaises(ParserError) as context:
            parse_script(script)
        self.assertIn('--> oops', str(context.exception))

    def test_illegal_statement(self):
        script = self.dedent_script('''
            // This is a comment.
            a = 1;
            illegal: command, d = 1 / 0;
            b = 2 * a;
            c: command, d = 3*b;
        ''')
        with self.assertRaises(ParserError) as context:
            parse_script(script)
        self.assertIn('illegal: command, d = 1 / 0', str(context.exception))

    def test_parse_file(self):
        script = self.dedent_script('''
            // This is a comment.
            a = 1;
            b = 2 * a;
            c: command, d = 3*b;
        ''')
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'test')
            with open(f_name, 'w') as fh:
                fh.write(script)
            self.assertEqual(parse_file(f_name), parse_script(script))

    @staticmethod
    def dedent_script(script):
        """Remove leading white space as well as leading and trailing newlines from each line of the script."""
        return re.sub(r'^\s+', '', script, flags=re.MULTILINE).strip('\n')


class TestRegisterHandler(unittest.TestCase):
    def test_decorator_override(self):
        old_handler = statement_handlers['variable']

        @register_handler(override=True)
        def handle_variable(match, state):
            state.script.variables[match.group('name')] = 'foo'
            return state

        parsed_script = parse_script('a = 1;')
        self.assertDictEqual(parsed_script.variables, dict(a='foo'))
        self.assertDictEqual(parsed_script.context, {})
        self.assertListEqual(parsed_script.commands, [])

        register_handler('variable', lambda m, s: s)
        parsed_script = parse_script('a = 1;')
        self.assertDictEqual(parsed_script.variables, dict(a='foo'))
        self.assertDictEqual(parsed_script.context, {})
        self.assertListEqual(parsed_script.commands, [])

        register_handler('variable', lambda m, s: s, override=True)
        parsed_script = parse_script('a = 1;')
        self.assertDictEqual(parsed_script.variables, {})
        self.assertDictEqual(parsed_script.context, {})
        self.assertListEqual(parsed_script.commands, [])

        statement_handlers['variable'] = old_handler


class TestResolveCallingSites(unittest.TestCase):
    def test_no_calling_site(self):
        script = 'label1: command, x = 1;\nlabel2: command, y = 2;'
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'test')
            with open(f_name, 'w') as fh:
                fh.write(script); fh.flush()
            self.assertEqual(resolve_calling_sites(f_name), script)

    def test_single_site(self):
        with tempfile.TemporaryDirectory() as td:
            f_name_1 = os.path.join(td, 'test1')
            f_name_2 = os.path.join(td, 'test2')
            script1 = f'call, file = "{f_name_2}";'
            script2 = 'label1: command, a = 5;\nlabel2: command, b = 7;'
            with open(f_name_1, 'w') as fh:
                fh.write(script1)
            with open(f_name_2, 'w') as fh:
                fh.write(script2)
            self.assertEqual(resolve_calling_sites(f_name_1), script2)

        with tempfile.TemporaryDirectory() as td:
            f_name_1 = os.path.join(td, 'test1')
            f_name_2 = os.path.join(td, 'test2')
            script1 = f'label1: command, x = 1;\ncall, file = "{f_name_2}";\nlabel2: command, y = 2;'
            script2 = 'f2_l1: command, a = 5;\nf2_l2: command, b = 7;'
            with open(f_name_1, 'w') as fh:
                fh.write(script1)
            with open(f_name_2, 'w') as fh:
                fh.write(script2)
            self.assertEqual(resolve_calling_sites(f_name_1), script1.replace(f'call, file = "{f_name_2}";', script2))

    def test_single_with_indent(self):
        with tempfile.TemporaryDirectory() as td:
            f_name_1 = os.path.join(td, 'test1')
            f_name_2 = os.path.join(td, 'test2')
            script1 = f'label1: command, x = 1;\n    call, file = "{f_name_2}";\nlabel2: command, y = 2;'
            script2 = 'f2_l1: command, a = 5;\nf2_l2: command, b = 7;'
            script2_indented = '    f2_l1: command, a = 5;\n    f2_l2: command, b = 7;'
            with open(f_name_1, 'w') as fh:
                fh.write(script1)
            with open(f_name_2, 'w') as fh:
                fh.write(script2)
            self.assertEqual(resolve_calling_sites(f_name_1), script1.replace(f'    call, file = "{f_name_2}";',
                                                                              script2_indented))

    def test_multiple_sites(self):
        with tempfile.TemporaryDirectory() as td:
            f_name_1 = os.path.join(td, 'test1')
            f_name_2 = os.path.join(td, 'test2')
            f_name_3 = os.path.join(td, 'test3')
            script1 = f'label1: command, x = 1;\n    call, file = {f_name_2};\nlabel2: command, y = 2;'
            script2 = f'f2_l1: command, a = 5;\n    call, file = \'{f_name_3}\';\nf2_l2: command, b = 7;'
            script3 = 'f3_l1: command, f = 27;\nf3_l2: command, g = 36;'
            with open(f_name_1, 'w') as fh:
                fh.write(script1)
            with open(f_name_2, 'w') as fh:
                fh.write(script2)
            with open(f_name_3, 'w') as fh:
                fh.write(script3)
            expected = (
                'label1: command, x = 1;\n'
                '    f2_l1: command, a = 5;\n'
                '        f3_l1: command, f = 27;\n'
                '        f3_l2: command, g = 36;\n'
                '    f2_l2: command, b = 7;\n'
                'label2: command, y = 2;'
            )
            self.assertEqual(resolve_calling_sites(f_name_1), expected)


class TestReplaceDotsInVariableNames(unittest.TestCase):
    def test(self):
        self.assertEqual(replace_dots_in_variable_names('some.variable'), 'some_variable')
        self.assertEqual(
            _dedent_script(replace_dots_in_variable_names('''
                a_b_c = 1;
                d.e.f = 2;
                label.1: command, x = 1;
                z = label.1->x * 5;
            ''')),
            _dedent_script('''
                a_b_c = 1;
                d_e_f = 2;
                label_1: command, x = 1;
                z = label_1->x * 5;
            ''')
        )

    def test_already_used_variable_name(self):
        with self.assertWarns(UserWarning):
            replace_dots_in_variable_names('the.variable = 1; the_variable = 2;')


class TestRemoveMultiLineComments(unittest.TestCase):
    def test(self):
        script = '''
        a = 1;
        /* This
        is
        a multi-line
        comment
        */
        b = 2;
        '''
        script = TestParseScript.dedent_script(script)
        self.assertEqual(remove_multi_line_comments(script), 'a = 1;\nb = 2;')

    def test_multiple(self):
        script = '''
        /* Multi-line comment here */
        a = 1;
        /* Another comment here */
        b = 2;
        '''
        script = TestParseScript.dedent_script(script)
        self.assertEqual(remove_multi_line_comments(script), 'a = 1;\nb = 2;')


class TestRemoveComments(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(remove_comments('a = 1;  // ... comment ...'), 'a = 1;')
        self.assertEqual(remove_comments('a = 1;! ... comment ...'), 'a = 1;')

    def test_multi_line(self):
        script = '''
        a = 1;  // ... comment ...
        // Full-line comment;
        b = 2;! Comment with "!"
        c = 3; // {variable_indicator}
        // {variable_indicator};
        d = 4;
        '''.format(variable_indicator=VARIABLE_INDICATOR)
        script = TestParseScript.dedent_script(script)
        self.assertEqual(remove_comments(script),
                         'a = 1;\nb = 2;\nc = 3; // {vi}\n// {vi};\nd = 4;'.format(vi=VARIABLE_INDICATOR))


class TestRemoveWhitespace(unittest.TestCase):
    def test_no_quotes(self):
        self.assertEqual(remove_whitespace('a : = 1;\nb: command, x = 2;'), 'a:=1;\nb:command,x=2;')

    def test_quotes(self):
        self.assertEqual(remove_whitespace('b: command, x = "some string ...";'), 'b:command,x="some string ...";')

    def test_variable_indicator(self):
        self.assertEqual(remove_whitespace(f'// {VARIABLE_INDICATOR}'), f'// {VARIABLE_INDICATOR}')


class TestNormalizeVariableIndicator(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(normalize_variable_indicators(f'a = 1;  // optional comment {VARIABLE_INDICATOR}'),
                         f'// {VARIABLE_INDICATOR};\na = 1;')
        self.assertEqual(normalize_variable_indicators(f'a = 1;!   {VARIABLE_INDICATOR}   '),
                         f'// {VARIABLE_INDICATOR};\na = 1;')

    def test_multi_line(self):
        script = '''
        a = 1;  // This is an optional comment followed by {variable_indicator}
        b = 2;  ! {variable_indicator};
        '''.format(variable_indicator=VARIABLE_INDICATOR)
        script = TestParseScript.dedent_script(script)
        self.assertEqual(normalize_variable_indicators(script),
                         '// {vi};\na = 1;\n// {vi};\nb = 2;'.format(vi=VARIABLE_INDICATOR))


class TestExtractSequence(unittest.TestCase):
    def test_one(self):
        commands = [
            Command('test'),
            Command('sequence', label='sequence_1'),
            Command('element', label='element_1'),
            Command('element', label='element_2'),
            Command('endsequence'),
            Command('something_else')
        ]
        attrs, sequence = extract_sequence(commands, {})
        self.assertSequenceEqual(sequence, commands[2:4])
        self.assertDictEqual(attrs, {})
        attrs, sequence = extract_sequence(commands, {}, label='sequence_1')
        self.assertSequenceEqual(sequence, commands[2:4])
        self.assertDictEqual(attrs, {})

    def test_multiple(self):
        commands = [
            Command('test'),
            Command('sequence', dict(l=2), label='sequence_1'),
            Command('element', label='element_1'),
            Command('element', label='element_2'),
            Command('endsequence'),
            Command('something_else'),
            Command('sequence', dict(l=4, refer='entry'), label='sequence_2'),
            Command('other_element', label='element_x'),
            Command('other_element', label='element_y'),
            Command('other_element', label='element_z'),
            Command('endsequence'),
            Command('some_other_command')
        ]
        attrs, sequence = extract_sequence(commands, {})
        self.assertSequenceEqual(sequence, commands[2:4])
        self.assertDictEqual(attrs, {'l': 2})
        attrs, sequence = extract_sequence(commands, {}, label='sequence_1')
        self.assertSequenceEqual(sequence, commands[2:4])
        self.assertDictEqual(attrs, {'l': 2})
        attrs, sequence = extract_sequence(commands, {}, label='sequence_2')
        self.assertSequenceEqual(sequence, commands[7:10])
        self.assertDictEqual(attrs, {'l': 4, 'refer': 'entry'})

    def test_line_definition(self):
        context = {f'q{i}': Command('quadrupole', dict(l=i)) for i in range(4)}
        context['foo'] = Line(['q2', 'q3'], label='foo')
        commands = [Command('something'), context['foo'],
                    Line(['q0', Line(['q1', 'q2']), 'q3', '-2*foo'], label='bar'),
                    Command('something_else')]
        with self.assertRaises(ParserError):
            extract_sequence(commands, context)
        attrs, sequence = extract_sequence(commands, context, label='foo')
        self.assertDictEqual(attrs, {})
        self.assertSequenceEqual(sequence, [context['q2'], context['q3']])
        attrs, sequence = extract_sequence(commands, context, label='bar')
        self.assertDictEqual(attrs, {})
        self.assertSequenceEqual(
            sequence,
            [context[f'q{i}'] for i in range(4)] + 2*[context['q3'], context['q2']]
        )

    def test_no_sequence_found(self):
        commands = [Command('test'), Command('element', label='element_1'), Command('element', label='element_2')]
        with self.assertRaises(ParserError):
            extract_sequence(commands, {})
        commands = [Command('sequence', dict(l=2), label='s1'), Command('element', label='e1'), Command('endsequence')]
        with self.assertRaises(ParserError):
            extract_sequence(commands, {}, label='s2')

    def test_target_command_is_not_a_sequence(self):
        commands = [Command('sequence', dict(l=2), label='s1'), Command('element', label='e1'), Command('endsequence')]
        with self.assertRaises(ParserError):
            extract_sequence(commands, {}, label='e1')


# noinspection PyTypeChecker
class TestPadSequence(unittest.TestCase):
    def test_no_padding_required(self):
        sequence = [
            Command('command', {'at': 5, 'l': 10}),
            Command('command', {'at': 12, 'l': 4}),
            Command('command', {'at': 17, 'l': 6}),
        ]
        self.assertSequenceEqual(list(pad_sequence(sequence, 20)), sequence)

    def test_center(self):
        sequence = [
            Command('command', {'at': 4, 'l': 2}),
            Command('command', {'at': 7, 'l': 2}),
            Command('command', {'at': 9, 'l': 2}),
            Command('command', {'at': 15, 'l': 2}),
        ]
        self.assertSequenceEqual(list(pad_sequence(sequence, 16, drift_label=str)), [
            Command('drift', {'at': 1.5, 'l': 3.0}, '0'),
            sequence[0],
            Command('drift', {'at': 5.5, 'l': 1.0}, '1'),
            sequence[1],
            sequence[2],
            Command('drift', {'at': 12.0, 'l': 4.0}, '3'),
            sequence[3]
        ])

    def test_entry(self):
        sequence = [
            Command('command', {'at': 4, 'l': 2}),
            Command('command', {'at': 7, 'l': 2}),
            Command('command', {'at': 9, 'l': 2}),
            Command('command', {'at': 15, 'l': 2}),
        ]
        self.assertSequenceEqual(list(pad_sequence(sequence, 17, refer='entry', drift_label=str)), [
            Command('drift', {'at': 0.0, 'l': 4.0}, '0'),
            sequence[0],
            Command('drift', {'at': 6.0, 'l': 1.0}, '1'),
            sequence[1],
            sequence[2],
            Command('drift', {'at': 11.0, 'l': 4.0}, '3'),
            sequence[3]
        ])

    def test_exit(self):
        sequence = [
            Command('command', {'at': 4, 'l': 2}),
            Command('command', {'at': 7, 'l': 2}),
            Command('command', {'at': 9, 'l': 2}),
            Command('command', {'at': 15, 'l': 2}),
        ]
        self.assertSequenceEqual(list(pad_sequence(sequence, 15, refer='exit', drift_label=str)), [
            Command('drift', {'at': 2.0, 'l': 2.0}, '0'),
            sequence[0],
            Command('drift', {'at': 5.0, 'l': 1.0}, '1'),
            sequence[1],
            sequence[2],
            Command('drift', {'at': 13.0, 'l': 4.0}, '3'),
            sequence[3]
        ])

    def test_from(self):
        sequence = [
            Command('command', {'at': 2, 'l': 1}, label='e1'),
            Command('command', {'at': 1.5, 'from': 'e1', 'l': 1}, label='e2'),
            Command('command', {'at': 6, 'l': 2}, label='e3'),
            Command('command', {'at': 4.5, 'from': 'e2', 'l': 1}, label='e4'),
        ]
        self.assertSequenceEqual(list(pad_sequence(sequence, 10, refer='entry', drift_label=str)), [
            Command('drift', {'at': 0.0, 'l': 2.0}, '0'),
            sequence[0],
            Command('drift', {'at': 3.0, 'l': 1.0}, '1'),
            sequence[1],
            Command('drift', {'at': 5.0, 'l': 1.0}, '2'),
            sequence[2],
            Command('drift', {'at': 8, 'l': 1.0}, '3'),
            sequence[3]
        ])

    def test_invalid_reference_point_indicator(self):
        with self.assertRaises(ValueError):
            list(pad_sequence([], 0, refer='invalid'))

    def test_negative_offset(self):
        with self.assertRaises(ParserError):
            list(pad_sequence([Command('c', dict(at=2)), Command('c', dict(at=1))], 2))


class TestLabelEveryElement(unittest.TestCase):
    def test_default_template(self):
        seq = label_every_element([
            Command('command1', dict(), label='e1'),
            Command('command2', dict()),
            Command('command3', dict(), label='e3'),
            Command('command4', dict()),
            Command('command5', dict()),
        ])
        expected = ['e1', 'command2', 'e3', 'command4', 'command5']
        self.assertSequenceEqual([x.label for x in seq], expected)

    def test_custom_template(self):
        count = it.count(1)
        # noinspection PyTypeChecker
        seq = label_every_element([
            Command('command', dict(), label='e1'),
            Command('command', dict()),
            Command('command', dict(), label='e3'),
            Command('command', dict()),
            Command('command', dict()),
        ], template=lambda c: f'e{next(count)}')
        self.assertSequenceEqual([x.label for x in seq], [f'e{i}' for i in range(1, 6)])

    def test_duplicate_labels(self):
        seq = label_every_element([
            Command('cmd', dict()),
            Command('cmd', dict()),
            Command('cmd', dict()),
            Command('cmd', dict()),
            Command('cmd', dict()),
        ])
        expected = ['cmd', 'cmd', 'cmd', 'cmd', 'cmd']
        self.assertSequenceEqual([x.label for x in seq], expected)


class TestExtractErrorDefinitions(unittest.TestCase):
    def test(self):
        script = parse_script(_dedent_script('''
            hkicker, kick = 0.1;
            select, flag = error, clear;
            select, flag = error, range = "q1";
            select, flag = error, class = sbend, sequence = "other_sequence";
            eoption, seed = 0, add;
            ealign, dx := ranf();
            select, flag = error, sequence = test, range = "quadrupole[2]";
            some_other_command, xyz = 123;
            dy = 0.1;  // vertical displacement {variable_indicator}
            dpsi := 2 * gauss();  // {variable_indicator}
            ealign, dy = dy, dpsi := dpsi;
        '''.format(variable_indicator=VARIABLE_INDICATOR))).commands
        self.assertEqual(len(script), 9)
        errors = list(extract_error_definitions(script, 'test'))
        self.assertEqual(len(errors), 6)
        self.assertSequenceEqual(errors, [script[i] for i in [1, 2, 4, 5, 6, 8]])


class TestGenerateErrorSpecifications(unittest.TestCase):
    def test_single_error(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}, label='q2'),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "q1";
            ealign, dx = 0.5;
        ''')).commands
        errors = generate_error_specifications(script, sequence)
        self.assertDictEqual(errors, {0: {'dx': 0.5}})

    def test_single_error_rng(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}),
            Command('quadrupole', {'k1': 0.3, 'l': 3.0}),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "quadrupole[1]/quadrupole[2]";
            eoption, seed = 0;
            ealign, dx := ranf();
        ''')).commands
        errors = generate_error_specifications(script, sequence)
        np.random.seed(0)
        self.assertDictEqual(errors, {0: {'dx': np.random.random()}, 1: {'dx': np.random.random()}})

    def test_single_error_multiple_select(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}),
            Command('quadrupole', {'k1': 0.3, 'l': 3.0}),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "quadrupole[2]";
            select, flag = error, range = "quadrupole[2]";
            select, flag = error, range = "quadrupole[1]";
            eoption, seed = 0, add;
            ealign, dx := ranf();
        ''')).commands
        errors = generate_error_specifications(script, sequence)
        np.random.seed(0)
        self.assertDictEqual(errors, {1: {'dx': np.random.random()}, 0: {'dx': np.random.random()}})

    def test_add_errors(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}, label='q2'),
            Command('quadrupole', {'k1': 0.3, 'l': 3.0}, label='q3'),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "q1";
            select, flag = error, range = "q3";
            eoption, add;
            ealign, dx = 0.125;
            ealign, dx = 0.125;
            select, flag = error, range = "q2";
            ealign, dx = 0.25, dy = 1.0;
            select, flag = error, clear;
            select, flag = error, range = "q3";
            eoption, add = false;
            ealign, dx = 1.0, dy = 2.0;
        ''')).commands
        errors = generate_error_specifications(script, sequence)
        self.assertDictEqual(errors, {0: {'dx': 0.50, 'dy': 1.0},
                                      1: {'dx': 0.25, 'dy': 1.0},
                                      2: {'dx': 1.00, 'dy': 2.0}})

    def test_by_class(self):
        sequence = [
            Command('q1', {'k1': 0.1, 'l': 1.0}, label='e1'),
            Command('q2', {'k1': 0.2, 'l': 2.0}, label='e2'),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, class = "e1";
            select, flag = error, class = "q2";
            ealign, dx = 0.5;
        ''')).commands
        errors = generate_error_specifications(script, sequence)
        self.assertDictEqual(errors, {1: {'dx': 0.5}})

    def test_variables(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}, label='q2'),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "q1";
            dx = 0.25;  // {variable_indicator}
            dy := 0.50;  // {variable_indicator}
            ealign, dx = dx, dy = dy;
        '''.format(variable_indicator=VARIABLE_INDICATOR))).commands
        errors = generate_error_specifications(script, sequence)
        self.assertIsInstance(errors[0]['dx'], Variable)
        self.assertIsInstance(errors[0]['dy'], Variable)
        self.assertDictEqual(errors, {0: {'dx': Variable(0.25), 'dy': Variable(0.50)}})

    def test_complete(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('sbend', {'angle': 0.25, 'l': 4.0}, label='s1'),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}, label='q2'),
            Command('sbend', {'angle': 0.50, 'l': 8.0}, label='s2'),
            Command('quadrupole', {'k1': 0.3, 'l': 3.0}, label='q3'),
        ]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "q1";
            select, flag = error, class = sbend, sequence = "label_should_not_matter";
            eoption, seed = 0, add;
            ealign, dx := ranf();
            select, flag = error, sequence = test, range = q2;
            dy = 0.1;  // vertical displacement {variable_indicator}
            dpsi := 2 * gauss();  // {variable_indicator}
            ealign, dy = dy, dpsi := dpsi;
        '''.format(variable_indicator=VARIABLE_INDICATOR))).commands
        errors = generate_error_specifications(script, sequence)
        np.random.seed(0)
        expected = {0: {'dx': np.random.random(), 'dy': Variable(float(str(0.1)))},
                    1: {'dx': np.random.random(), 'dy': Variable(float(str(0.1)))},
                    3: {'dx': np.random.random(), 'dy': Variable(float(str(0.1)))},
                    2: {'dy': Variable(float(str(0.1)))}}
        expected[0]['dpsi'] = Variable(2 * np.random.normal())
        expected[1]['dpsi'] = Variable(2 * np.random.normal())
        expected[3]['dpsi'] = Variable(2 * np.random.normal())
        expected[2]['dpsi'] = Variable(2 * np.random.normal())
        self.assertDictEqual(errors, expected)

    def test_field_errors_quadrupole(self):
        sequence = [
            Command('quadrupole', {'k1': 0.25, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.50, 'l': 4.0}, label='q2'),
        ]
        script = _dedent_script('''
            beam, beta = 0.6, particle = proton;
            
            seq: sequence, l = 5, refer = entry;
                q1: quadrupole, k1 = 0.25, l = 1.0, at = 0;
                q2: quadrupole, k1 = 0.50, l = 4.0, at = 1;
            endsequence;
            
            use, sequence = seq;
        
            eoption, add = true;
            select, flag = error, clear;
            select, flag = error, range = "q1";
            efcomp, dkn = {0, 0.0625}, dknr = {0, 0.375}, radius = 0.50, order = 1;
            select, flag = error, range = "q2";
            efcomp, dkn = {0, 0.1250}, dknr = {0, 0.750}, radius = 0.25, order = 1;
            select, flag = error, full;
            esave, file = "test_errors";
        ''')
        errors = generate_error_specifications(parse_script(script).commands, sequence)
        errors = {p: {k.upper(): v for k, v in err.items()} for p, err in errors.items()}
        errors_ref = run_script(script, ['test_errors'], madx=os.path.expanduser('~/bin/madx'))['test_errors']
        errors_ref.set_index('NAME', inplace=True)
        expected = {0: {'K0L': 0., 'K1L': 0.46875}, 1: {'K0L': 0., 'K1L': 1.625}}
        self.assertDictEqual(errors_ref.loc['Q1', ['K0L', 'K1L']].to_dict(), errors[0])
        self.assertDictEqual(errors_ref.loc['Q2', ['K0L', 'K1L']].to_dict(), errors[1])
        self.assertDictEqual(errors[0], expected[0])
        self.assertDictEqual(errors[1], expected[1])
        self.assertDictEqual(errors_ref.loc['Q1', ['K0L', 'K1L']].to_dict(), expected[0])
        self.assertDictEqual(errors_ref.loc['Q2', ['K0L', 'K1L']].to_dict(), expected[1])

    def test_field_errors_multipole(self):
        sequence = [
            Command('multipole', {'knl': np.array([0.0625, 0.1875, 0.4375, 0.9375, 1.9375, 3.9375, 7.9375, 15.9375]),
                                  'l': 0.0}, label='m1'),
            Command('multipole', {'knl': np.array([0.0625, 0.1875, 0.4375, 0.9375, 1.9375, 3.9375, 7.9375, 15.9375]),
                                  'l': 0.0}, label='m2'),
        ]
        script = _dedent_script('''
            beam, beta = 0.6, particle = proton;

            seq: sequence, l = 1, refer = entry;
                m1: multipole, knl = {0.0625, 0.1875, 0.4375, 0.9375, 1.9375, 3.9375, 7.9375, 15.9375}, l = 0.0, at = 0;
                m2: multipole, knl = {0.0625, 0.1875, 0.4375, 0.9375, 1.9375, 3.9375, 7.9375, 15.9375}, l = 0.0, at = 1;
            endsequence;

            use, sequence = seq;

            eoption, add = true;
            select, flag = error, clear;
            select, flag = error, range = "m1";
            efcomp, dkn = {1, 2, 4, 8, 16, 32, 64, 128}, dknr = {0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8},
                radius = 0.50, order = 3;
            select, flag = error, range = "m2";
            efcomp, dkn = {1, 3, 7, 15, 31, 63, 127, 255}, dknr = {0.03125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4},
                radius = 0.25, order = 5;
            select, flag = error, full;
            esave, file = "test_errors";
        ''')
        errors = generate_error_specifications(parse_script(script).commands, sequence)
        errors = {p: {k.upper(): v for k, v in err.items()} for p, err in errors.items()}
        errors_ref = run_script(script, ['test_errors'], madx=os.path.expanduser('~/bin/madx'))['test_errors']
        errors_ref.set_index('NAME', inplace=True)
        columns = [f'K{i}L' for i in range(len(sequence[0]['knl']))]
        for (pos, index), col in it.product(enumerate(['M1', 'M2']), columns):
            with self.subTest(element=index, order=col):
                self.assertAlmostEqual(errors_ref.loc[index, col], errors[pos][col], delta=1e-6)

    def test_not_implemented(self):
        sequence = [Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1')]
        script = parse_script(_dedent_script('''
            select, flag = error, clear;
            select, flag = error, range = "q1";
            ealign, dtheta = 0.1;
        ''')).commands
        with self.assertRaises(NotImplementedError):
            generate_error_specifications(script, sequence)


class TestSelectByRange(unittest.TestCase):
    def test_single_element(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q2'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q3'),
        ]
        selection = list(select_by_range(Command('select', {'range': 'q1'}), sequence))
        self.assertSequenceEqual(selection, sequence[0:1])

        selection = list(select_by_range(Command('select', {'range': 'q2'}), sequence))
        self.assertSequenceEqual(selection, sequence[1:2])

        selection = list(select_by_range(Command('select', {'range': 'q3'}), sequence))
        self.assertSequenceEqual(selection, sequence[2:3])

        with self.assertRaises(ValueError):
            list(select_by_range(Command('select', {'range': 'invalid range specification'}), sequence))

    def test_single_element_with_special_markers(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q2'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q3'),
        ]
        selection = list(select_by_range(Command('select', {'range': '#s'}), sequence))
        self.assertSequenceEqual(selection, sequence[:1])

        selection = list(select_by_range(Command('select', {'range': '#e'}), sequence))
        self.assertSequenceEqual(selection, sequence[-1:])

    def test_multiple_elements(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q2'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q3'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q4'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q5'),
        ]
        selection = list(select_by_range(Command('select', {'range': 'q2/q4'}), sequence))
        self.assertSequenceEqual(selection, sequence[1:4])

        selection = list(select_by_range(Command('select', {'range': 'q1/q1'}), sequence))
        self.assertSequenceEqual(selection, sequence[:1])

        selection = list(select_by_range(Command('select', {'range': 'q1/q5'}), sequence))
        self.assertSequenceEqual(selection, sequence)

        selection = list(select_by_range(Command('select', {'range': 'q6/q3'}), sequence))
        self.assertSequenceEqual(selection, [])

        with self.assertWarns(UserWarning):
            list(select_by_range(Command('select', {'range': 'q1/q6'}), sequence))

    def test_special_markers(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q2'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q3'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q4'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q5'),
        ]
        selection = list(select_by_range(Command('select', {'range': 'q2/#e'}), sequence))
        self.assertSequenceEqual(selection, sequence[1:])

        selection = list(select_by_range(Command('select', {'range': '#s/q3'}), sequence))
        self.assertSequenceEqual(selection, sequence[:3])

        selection = list(select_by_range(Command('select', {'range': '#s/#e'}), sequence))
        self.assertSequenceEqual(selection, sequence)

    def test_occurrence_count(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}),
            Command('quadrupole', {'k1': 0.2, 'l': 2.0}),
            Command('quadrupole', {'k1': 0.3, 'l': 3.0}),
            Command('quadrupole', {'k1': 0.4, 'l': 4.0}),
            Command('quadrupole', {'k1': 0.5, 'l': 5.0}),
        ]
        selection = list(select_by_range(Command('select', {'range': 'quadrupole[1]/quadrupole[5]'}), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence))))

        selection = list(select_by_range(Command('select', {'range': 'quadrupole[3]/quadrupole[4]'}), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[2:4]))))

        selection = list(select_by_range(Command('select', {'range': 'quadrupole[2]'}), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[1:2]))))

        selection = list(select_by_range(Command('select', {'range': 'quadrupole[2]/quadrupole[2]'}), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[1:2]))))

        selection = list(select_by_range(Command('select', {'range': 'quadrupole[2]/#e'}), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[1:]))))

        selection = list(select_by_range(Command('select', {'range': '#s/quadrupole[2]'}), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[:2]))))

        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q1'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q2'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q3'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q4'),
            Command('quadrupole', {'k1': 0.1, 'l': 1.0}, label='q5'),
        ]
        for i in range(5):
            selection = list(select_by_range(Command('select', {'range': f'q{i + 1}'}), sequence))
            self.assertEqual(len(selection), 1)
            self.assertIs(selection[0], sequence[i])
            selection = list(select_by_range(Command('select', {'range': f'q{i + 1}/q{i + 1}'}), sequence))
            self.assertEqual(len(selection), 1)
            self.assertIs(selection[0], sequence[i])
            selection = list(select_by_range(Command('select', {'range': f'q{i + 1}[1]'}), sequence))
            self.assertEqual(len(selection), 1)
            self.assertIs(selection[0], sequence[i])
            selection = list(select_by_range(Command('select', {'range': f'q{i + 1}[1]/q{i + 1}[1]'}), sequence))
            self.assertEqual(len(selection), 1)
            self.assertIs(selection[0], sequence[i])
            with self.assertRaises(StopIteration):
                next(select_by_range(Command('select', {'range': f'quadrupole[{i + 1}]'}), sequence))

    def test_on_script(self):
        script = '''
            q1: quadrupole, k1 = 0.5, l = 1.0;
            q2: q1, k1 = 0.25;
            
            e0: quadrupole;
                q2;
            e2: q2;
                q1;
            e4: q1;
        '''
        commands = parse_script(script).commands
        self.assertEqual(len(commands), 7)
        sequence = commands[2:]

        selection = list(select_by_range(Command('select', dict(range='e0/e2')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[:3]))))

        selection = list(select_by_range(Command('select', dict(range='#s/e2')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[:3]))))

        selection = list(select_by_range(Command('select', dict(range='q1[1]/#e')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[-2:]))))

        selection = list(select_by_range(Command('select', dict(range='q2[1]/q1[1]')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[1:-1]))))

        with self.assertRaises(StopIteration):
            next(select_by_range(Command('select', dict(range='q2[2]/q1[2]')), sequence))

        with self.assertRaises(StopIteration):
            next(select_by_range(Command('select', dict(range='quadrupole[1]/#e')), sequence))

        selection = list(select_by_range(Command('select', dict(range='e2')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[2:3]))))

        selection = list(select_by_range(Command('select', dict(range='e2[1]')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[2:3]))))

        selection = list(select_by_range(Command('select', dict(range='#s')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[:1]))))

        selection = list(select_by_range(Command('select', dict(range='#e')), sequence))
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(selection, sequence[-1:]))))


class TestFilterByClass(unittest.TestCase):
    def test(self):
        sequence = [
            Command('abc', {'x': 0, 'y': 1}, label='l1'),
            Command('def', {'x': 2, 'y': 3}, label='l2'),
            Command('abc', {'x': 4, 'y': 5}, label='l3'),
            Command('ghi', {'x': 6, 'y': 7}, label='l4'),
            Command('abc', {'x': 8, 'y': 9}, label='l5'),
        ]
        filtered = list(filter_by_class(Command('select', {'class': 'abc'}), sequence))
        self.assertSequenceEqual(filtered, sequence[::2])
        filtered = list(filter_by_class(Command('select', {'class': 'def'}), sequence))
        self.assertSequenceEqual(filtered, sequence[1:2])
        filtered = list(filter_by_class(Command('select', {'class': 'ghi'}), sequence))
        self.assertSequenceEqual(filtered, sequence[3:4])

    def test_inherited(self):
        base_1 = Command('base_1', {}, label='base_1_label')
        base_2 = Command('base_2', {}, label='base_2_label')
        sequence = [
            Command('abc', {'x': 0, 'y': 1}, label='l1', base=base_1),
            Command('def', {'x': 2, 'y': 3}, label='l2', base=base_2),
            Command('abc', {'x': 4, 'y': 5}, label='l3', base=base_1),
            Command('ghi', {'x': 6, 'y': 7}, label='l4', base=base_2),
            Command('abc', {'x': 8, 'y': 9}, label='l5', base=base_1),
        ]
        filtered = list(filter_by_class(Command('select', {'class': 'base_1'}), sequence))
        self.assertSequenceEqual(filtered, sequence[::2])
        filtered = list(filter_by_class(Command('select', {'class': 'base_2'}), sequence))
        self.assertSequenceEqual(filtered, sequence[1::2])

    def test_on_script(self):
        script = '''
            q1: quadrupole, k1 = 0.5, l = 1.0;
            q2: q1, k1 = 0.25;

            e0: quadrupole;
            e1: q2;
            e2: q2;
            e3: q1;
            e4: q1;
        '''
        commands = parse_script(script).commands
        self.assertEqual(len(commands), 7)
        sequence = commands[2:]

        selection = list(filter_by_class(Command('select', {'class': 'quadrupole'}), sequence))
        self.assertSequenceEqual(selection, sequence)

        selection = list(filter_by_class(Command('select', {'class': 'q1'}), sequence))
        self.assertSequenceEqual(selection, sequence[1:])

        selection = list(filter_by_class(Command('select', {'class': 'q2'}), sequence))
        self.assertSequenceEqual(selection, sequence[1:3])

        selection = list(filter_by_class(Command('select', {'class': 'q3'}), sequence))
        self.assertSequenceEqual(selection, [])


class TestFilterByPattern(unittest.TestCase):
    def test(self):
        sequence = [
            Command('abc', {'x': 0, 'y': 1}, label='label_123'),
            Command('def', {'x': 2, 'y': 3}, label='other_label_456'),
            Command('ghi', {'x': 4, 'y': 5}, label='label_label'),
            Command('jkl', {'x': 6, 'y': 7}, label='label___123'),
            Command('mno', {'x': 8, 'y': 9}, label='label___456'),
        ]
        filtered = list(filter_by_pattern(Command('select', dict(pattern=r'label_[0-9]+')), sequence))
        self.assertSequenceEqual(filtered, sequence[:1])
        filtered = list(filter_by_pattern(Command('select', dict(pattern=r'label_.*[0-9]+')), sequence))
        self.assertSequenceEqual(filtered, [sequence[0], sequence[3], sequence[4]])
        filtered = list(filter_by_pattern(Command('select', dict(pattern=r'label_{2,}[0-9]{3}')), sequence))
        self.assertSequenceEqual(filtered, sequence[3:])
        filtered = list(filter_by_pattern(Command('select', dict(pattern=r'other_label_456')), sequence))
        self.assertSequenceEqual(filtered, sequence[1:2])
        filtered = list(filter_by_pattern(Command('select', dict(pattern=r'.+')), sequence))
        self.assertSequenceEqual(filtered, sequence)

    def test_on_script(self):
        script = '''
            q1: quadrupole, k1 = 0.5, l = 1.0;
            q2: q1, k1 = 0.25;

            e0: quadrupole;
            e1: q2;
            e2: q2;
            e3: q1;
            e4: q1;
        '''
        commands = parse_script(script).commands
        self.assertEqual(len(commands), 7)
        sequence = commands[2:]

        selection = list(filter_by_pattern(Command('select', {'pattern': 'q[0-9]'}), sequence))
        self.assertSequenceEqual(selection, [])

        selection = list(filter_by_pattern(Command('select', {'pattern': 'e[0-4]'}), sequence))
        self.assertSequenceEqual(selection, sequence)

        selection = list(filter_by_pattern(Command('select', {'pattern': 'e[1-3]'}), sequence))
        self.assertSequenceEqual(selection, sequence[1:4])


class TestConversionFromSequenceToDataFrame(unittest.TestCase):
    def test(self):
        script = '''
            q1: quadrupole, k1 = 0.5, l = 1.0;
            q2: q1, k1 = 0.25;
            s1: sbend, angle = 2.0, l = 4.0;

            e0: quadrupole;
            e1: q2;
            e2: s1;
            e3: q1;
            e4: q1;
        '''
        commands = parse_script(script).commands[3:]
        df = sequence_to_data_frame(commands)
        self.assertListEqual(df.index.to_list(), [f'e{i}' for i in range(5)])
        self.assertTrue(np.isnan(df.loc['e0', 'l']))
        self.assertTrue(np.isnan(df.loc['e0', 'k1']))
        self.assertTrue(np.isnan(df.loc['e0', 'angle']))
        self.assertEqual(df.loc['e0', 'keyword'], 'quadrupole')
        self.assertEqual(df.loc['e0', 'type'], 'quadrupole')
        self.assertEqual(df.loc['e1', 'l'], 1.0)
        self.assertEqual(df.loc['e1', 'k1'], 0.25)
        self.assertTrue(np.isnan(df.loc['e1', 'angle']))
        self.assertEqual(df.loc['e1', 'keyword'], 'q2')
        self.assertEqual(df.loc['e1', 'type'], 'quadrupole')
        self.assertEqual(df.loc['e2', 'l'], 4.0)
        self.assertTrue(np.isnan(df.loc['e2', 'k1']))
        self.assertEqual(df.loc['e2', 'angle'], 2.0)
        self.assertEqual(df.loc['e2', 'keyword'], 's1')
        self.assertEqual(df.loc['e2', 'type'], 'sbend')
        self.assertEqual(df.loc['e3', 'l'], 1.0)
        self.assertEqual(df.loc['e3', 'k1'], 0.5)
        self.assertTrue(np.isnan(df.loc['e3', 'angle']))
        self.assertEqual(df.loc['e3', 'keyword'], 'q1')
        self.assertEqual(df.loc['e3', 'type'], 'quadrupole')
        self.assertEqual(df.loc['e4', 'l'], 1.0)
        self.assertEqual(df.loc['e4', 'k1'], 0.5)
        self.assertTrue(np.isnan(df.loc['e4', 'angle']))
        self.assertEqual(df.loc['e4', 'keyword'], 'q1')
        self.assertEqual(df.loc['e4', 'type'], 'quadrupole')
        back = data_frame_to_sequence(df)
        self.assertListEqual([c.label for c in commands], [c.label for c in back])
        self.assertListEqual([c.root.keyword for c in commands], [c.root.keyword for c in back])
        for c1, c2 in zip(commands, back):
            self.assertDictEqual(c1.attributes, c2.attributes)


class TestBuilder(unittest.TestCase):
    def test_write_attribute_assignment(self):
        self.assertEqual(write_attribute_assignment('label', 'attr', 1.0), 'label->attr = 1.0;')
        self.assertEqual(write_attribute_assignment('label', 'attr', [1, 2, 3]), 'label->attr = {1, 2, 3};')

    def test_write_attribute_increment(self):
        self.assertEqual(write_attribute_increment('label', 'attr', 0.0), 'label->attr = label->attr + 0.0;')
        self.assertEqual(write_attribute_increment('label', 'attr', 1.0), 'label->attr = label->attr + 1.0;')
        self.assertEqual(write_attribute_increment('label', 'attr', -2.0), 'label->attr = label->attr - 2.0;')

    def test_write_command(self):
        self.assertEqual(write_command('keyword', {'a': 1.0, 'b': [1, 2]}, label='label'),
                         'label: keyword, a = 1.0, b = {1, 2}')

    def test_write_attributes(self):
        self.assertEqual(write_attributes({'a': 1.0, 'b': [1, 2], 'c': 'test', 'd': -2.0}),
                         'a = 1.0, b = {1, 2}, c = "test", d = -2.0')

    def test_write_attribute_value(self):
        self.assertEqual(write_attribute_value(1.0), '1.0')
        self.assertEqual(write_attribute_value(-1.0), '-1.0')
        self.assertEqual(write_attribute_value([1, 2, 3]), '{1, 2, 3}')
        self.assertEqual(write_attribute_value((1., 2, 3)), '{1.0, 2, 3}')
        self.assertEqual(write_attribute_value('string'), '"string"')


if __name__ == '__main__':
    unittest.main()
