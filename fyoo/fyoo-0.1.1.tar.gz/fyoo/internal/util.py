import json
from typing import List, Optional, Tuple
import yaml


def _parse_template_context(context_format: Optional[str], context_string: str):
    parse_methods = {
        'json': json.loads,
        'yaml': yaml.safe_load,
    }
    if context_format in parse_methods:
        result = parse_methods[context_format](context_string)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Context was not a dictionary with format '{context_format}'")
    if context_format is not None:
        raise ValueError(f"Unrecognized context format '{context_format}'")

    for parse_method in parse_methods.values():
        try:
            result = parse_method(context_string)
            if isinstance(result, dict):
                return result
        except:  # pylint: disable=bare-except
            pass
    raise ValueError(
        f"Unable to parse context. Try specifying 'context_format' to one of {','.join(parse_methods.keys())}"
    )


def generate_fyoo_context(
        context_format: Optional[str],
        context_strings: Optional[List[str]],
        additional_vars: Optional[List[Tuple[str, str]]],
) -> dict:
    result_template = dict()
    if context_strings:
        for context_string in context_strings:
            result_template.update(_parse_template_context(context_format, context_string))
    if additional_vars:
        for key, value in additional_vars:
            result_template[key] = value
    return result_template



def set_type(string) -> Tuple[str, str]:
    eq_index = string.index('=')
    return string[:eq_index], string[eq_index + 1:]
