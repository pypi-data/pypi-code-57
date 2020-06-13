from __future__ import print_function

from dagster import check
from dagster.utils.indenting_printer import IndentingPrinter

from .config_type import ConfigType, ConfigTypeKind
from .field import resolve_to_config_type
from .iterate_types import config_schema_snapshot_from_config_type
from .snap import ConfigSchemaSnapshot


def _print_type_from_config_type(config_type, print_fn=print, with_lines=True):
    check.inst_param(config_type, 'config_type', ConfigType)
    return _print_type(
        config_schema_snapshot_from_config_type(config_type), config_type.key, print_fn, with_lines
    )


def _print_type(config_schema_snapshot, config_type_key, print_fn, with_lines):
    check.inst_param(config_schema_snapshot, 'config_schema_snapshot', ConfigSchemaSnapshot)
    check.str_param(config_type_key, 'config_type_key')
    check.callable_param(print_fn, 'print_fn')
    check.bool_param(with_lines, 'with_lines')

    if with_lines:
        printer = IndentingPrinter(printer=print_fn)
    else:
        printer = IndentingPrinter(printer=print_fn, indent_level=0)
    _do_print(config_schema_snapshot, config_type_key, printer, with_lines=with_lines)
    printer.line('')


def _do_print(config_schema_snapshot, config_type_key, printer, with_lines=True):
    line_break_fn = printer.line if with_lines else lambda string: printer.append(string + ' ')

    config_type_snap = config_schema_snapshot.get_config_snap(config_type_key)
    kind = config_type_snap.kind

    if kind == ConfigTypeKind.ARRAY:
        printer.append('[')
        _do_print(config_schema_snapshot, config_type_snap.inner_type_key, printer)
        printer.append(']')
    elif kind == ConfigTypeKind.NONEABLE:
        _do_print(config_schema_snapshot, config_type_snap.inner_type_key, printer)
        printer.append('?')
    elif kind == ConfigTypeKind.SCALAR_UNION:
        printer.append('(')
        _do_print(config_schema_snapshot, config_type_snap.scalar_type_key, printer)
        printer.append(' | ')
        _do_print(config_schema_snapshot, config_type_snap.non_scalar_type_key, printer)
        printer.append(')')
    elif ConfigTypeKind.has_fields(kind):
        line_break_fn('{')
        with printer.with_indent():
            for field_snap in sorted(config_type_snap.fields):
                name = field_snap.name
                if field_snap.is_required:
                    printer.append(name + ': ')
                else:
                    printer.append(name + '?: ')
                _do_print(
                    config_schema_snapshot, field_snap.type_key, printer, with_lines=with_lines,
                )
                line_break_fn('')

        printer.append('}')
    elif config_type_snap.given_name:
        printer.append(config_type_snap.given_name)
    else:
        check.failed('not supported')


def print_config_type_key_to_string(config_schema_snapshot, config_type_key, with_lines=True):
    prints = []

    def _push(text):
        prints.append(text)

    _print_type(config_schema_snapshot, config_type_key, _push, with_lines)

    if with_lines:
        return '\n'.join(prints)
    else:
        return ' '.join(prints)


def print_config_type_to_string(config_type, with_lines=True):
    prints = []

    def _push(text):
        prints.append(text)

    _print_type_from_config_type(resolve_to_config_type(config_type), _push, with_lines=with_lines)

    if with_lines:
        return '\n'.join(prints)
    else:
        return ' '.join(prints)
