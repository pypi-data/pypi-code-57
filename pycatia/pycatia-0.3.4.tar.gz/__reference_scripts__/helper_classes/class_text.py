import datetime
from pathlib import Path

import inflection

from helper_classes.conversions import convert_type
from helper_classes.conversions import type_conversion
from helper_classes.spelling import correct_spelling
from helper_classes.system_service import create_service

from .imports import create_imports

now = datetime.datetime.now()
caa_tag_line = f'CAA V5 Visual Basic Help ({ now })'


def get_enum_types():

    enum_path = Path('/home/evereux/python/projects/pycatia/__reference_scripts__/enum_files')

    # get a list of the enum types
    enum_files = enum_path.rglob('enum*.htm')

    enum_types_cat = []
    enum_types_py = []

    for file in enum_files:
        cat = file.stem.split('_')[1]
        py = inflection.underscore(cat)
        enum_types_cat.append(cat)
        enum_types_py.append(py)


    return enum_types_cat, enum_types_py


enum_cat, enum_py = get_enum_types()


def sp(pad=4):

    return " " * pad


def count_spaces_start(s):

    n = 0

    if s[0] != " ":
        return n

    for c in s:
        if c == " ":
            n += 1
        if c != " ":
            break

    return n


def previous_line_padding(text):

    post_pad = text.strip(" |")
    pos = len(text) - len(post_pad)
    previous_pad = text[:pos]

    return previous_pad


def split_line(line, pad_text=None, max_width=80, split_required=False):

    if (len(line) + len(pad_text)) > max_width:
        if " = " in line:
            return pad_text + line + '\n'
        if " : " in line:
            return pad_text + line + '\n'
        if " " in line:
            pos = line[:max_width].rfind(" ")
            start = line[:pos]
            end = line[pos:].lstrip()
            line = pad_text + start + '\n'
            pad_text = previous_line_padding(line)
            line = line + split_line(end, pad_text=pad_text, max_width=max_width, split_required=True)
    else:
        return pad_text + line + '\n'

    return line


def pad_list(lines, pad=8, v=False, text=""):
    """
    returns string from list with padding.
    """

    max_width = 80

    p = ""

    n = count_spaces_start(lines[0])

    if v is True:
        p = "| "

    for line in lines:

        pre_pad = sp(pad) + p
        line = line.rstrip(" ")
        line = line.rstrip(" ")

        line = line[n:].strip('\n')
        line = split_line(line, pad_text=pre_pad, max_width=max_width)

        text = text + line

    return text.rstrip(" |\n")


def parse_properties(properties, class_name=""):

    text = ""
    all_returns = []

    if properties is None:
        return text, all_returns

    for prop in properties:

        # if prop == 'smooth_angle_threshold':
        #     print(properties[prop])
        #     exit()

        returns = properties[prop]['returns']
        all_returns.append(returns)
        returns_doc = properties[prop]["returns"]
        r = None

        if returns:
            if returns[0].isupper():
                r = f'{ returns }(self.{ class_name }.{ properties[prop]["original_name"] })'
            else:
                r = f'self.{ class_name }.{ properties[prop]["original_name"]}'
            if returns in enum_cat:
                r = f'self.{class_name}.{properties[prop]["original_name"]}'
                returns_doc = f'enum {inflection.underscore(returns)}'


        t = f'{ sp(4) }@property\n' \
            f'{ sp(4) }def { prop }(self):\n' \
            f'{ sp(8) }"""\n' \
            f'{ sp(8) }.. note::\n' \
            f'{ sp(12) }{ caa_tag_line }\n' \
            f'{ pad_list(properties[prop]["text"], pad=16, v=True) }\n' \
            f'\n' \
            f'{ sp(8) }:return: { returns_doc }\n' \
            f'{ sp(8) }"""\n' \
            f'\n' \
            f'{ sp(8) }return { r }\n' \
            f'\n' \


        text = text + t

        if not properties[prop]['read_only']:
            t = f'{ sp(4) }@{ prop }.setter\n' \
                f'{ sp(4) }def { prop }(self, value):\n' \
                f'{ sp(8) }"""\n' \
                f'{ sp(8) }:param { returns_doc } value:\n' \
                f'{ sp(8) }"""\n' \
                f'\n' \
                f'{ sp(8) }self.{ class_name }.{ properties[prop]["original_name"] } = value\n' \
                f'\n' \

            text = text + t

    text = text.replace("\t", "")

    return text, all_returns


def parse_methods(methods, class_name=""):

    text = ""
    all_returns = []
    if methods is None:
        return text, all_returns

    for method in methods:

        returns = methods[method]['returns']
        all_returns.append(returns)
        returns_doc = returns
        r = None

        if returns:
            if returns[0].isupper():
                r = f'{ returns }(self.{ class_name }.{ methods[method]["original_name"] }())'
            else:
                r = f'self.{ class_name }.{ methods[method]["original_name"]}()'
            if returns in enum_cat:
                r = f'self.{class_name}.{methods[method]["original_name"]}()'
                returns_doc = f'enum {inflection.underscore(returns)}'
            if returns in type_conversion:
                r = f'self.{class_name}.{methods[method]["original_name"]}()'
                returns_doc = f'{ convert_type(returns)}'
        else:
            r = f'self.{class_name}.{methods[method]["original_name"]}()'
            returns_doc = f'{ convert_type(returns)}'

        params = methods[method]['parms']
        p = "self"
        pms = ""
        c_types = []
        c_names = []
        all_string = False

        if len(p) > 0:
            for i in params:
                name = i['name']
                c_type = convert_type(i['type'])
                if name:
                    p = p + f", {inflection.underscore(i['name'])}=None"
                    pms = pms + f"{ sp(8) }:param { c_type } { inflection.underscore(name) }:\n"
                    c_postfix = ""
                    if c_type[0].isupper():
                        c_postfix = '.com_object'
                    c_names.append(inflection.underscore(name + c_postfix))
                    c_types.append(c_type)

        if r:
            if len(c_names) > 0:
                args = ', '.join(c_names)
                r = r.replace("()", "(" + args + ")")

        not_ss = ['str', 'AnyObject', 'float', 'int']
        want_ss = any([i not in not_ss for i in c_types])
        # print(method, c_types, want_ss, len(c_names))

        ss = ""
        if methods[method]['is_sub'] and len(c_names) > 0 and want_ss:
            ss = create_service(methods[method], method)

        t = f'{ sp(4) }def { method }({ p }):\n' \
            f'{ sp(8) }"""\n' \
            f'{ sp(8) }.. note::\n' \
            f'{ sp(12) }{ caa_tag_line })\n' \
            f'{ pad_list(methods[method]["text"], pad=16, v=True) }\n' \
            f'\n' \
            f'{pms}' \
            f'{ sp(8) }:return: { returns_doc }\n' \
            f'{ sp(8) }"""\n' \
            f'{ sp(8) }return { r }\n' \
            f'{ss}\n' \

        text = text + t

    text = text.replace("\t", "")
    # strip white space at end of file and add newline.
    text = text.rstrip()
    text = text + '\n'

    return text, all_returns


def find_parent(hierarchy):

    clean_hierarchy = []
    for item in hierarchy:
        item = item.strip()
        if item:
            clean_hierarchy.append(item)
    if len(clean_hierarchy) < 2:
        parent = 'AnyObject'
    else:
        str_parent = clean_hierarchy[-2]
        parent = str_parent.rsplit('.', 1)[-1]
    return parent


def create_class_text(details):

    properties, p_returns = parse_properties(details['properties'], class_name=inflection.underscore(details["class_name"]))
    methods, m_returns = parse_methods(details['methods'], class_name=inflection.underscore(details["class_name"]))

    parent = find_parent(details["hierarchy"])

    all_returns = set(p_returns + m_returns + [parent])

    imports = create_imports(all_returns)

    text = '#! usr/bin/python3.6\n' \
           f'"""\n' \
           f'{ sp(4) }Module initially auto generated using V5Automation files from CATIA V5 R28 on { now }\n\n' \
           f'{ sp(4) }.. warning::\n' \
           f'{ sp(8) }The notes denoted \"CAA V5 Visual Basic Help\" are to be used as reference only.\n' \
           f'{ sp(8) }They are there as a guide as to how the visual basic / catscript functions work\n' \
           f'{ sp(8) }and thus help debugging in pycatia.\n' \
           f'{ sp(8) }\n' \
           f'"""\n' \
           '\n' \
           f'{imports}\n' \
           '\n' \
           '\n' \
           f'class { details["class_name"] }({ parent }):\n' \
           f'\n' \
           f'{ sp(4) }"""\n' \
           f'{ sp(8) }.. note::\n' \
           f'{ sp(12) }{ caa_tag_line }\n' \
           f'\n' \
           f'{ pad_list(details["hierarchy"], pad=16, v=True) }\n' \
           f'{ pad_list(details["description"], pad=16, v=True) }\n' \
           f'{ sp(4) }\n' \
           f'{ sp(4) }"""\n' \
           f'\n' \
           f'{ sp(4) }def __init__(self, com_object):\n' \
           f'{ sp(8) }super().__init__(com_object)\n' \
           f'{ sp(8) }self.{ inflection.underscore(details["class_name"]) } = com_object\n' \
           f'\n' \

    text = text + properties
    text = text + methods

    text = text.rstrip()
    text = text + '\n'

    text = text + f"""\n    def __repr__(self):
        return f'{ details["class_name"] }(name="{{ self.name }}")'
"""

    text = correct_spelling(text)

    return text
