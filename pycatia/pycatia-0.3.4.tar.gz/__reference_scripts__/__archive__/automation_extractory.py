import datetime
import logging
import os
import re
import textwrap
from pathlib import Path

import inflection
import pyperclip
from bs4 import BeautifulSoup

now = datetime.datetime.now()


def remove_line_breaks(text):
    if text is None:
        return None

    text = text.strip()
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = ' '.join(text.split())

    text = textwrap.wrap(text, 60)

    return text


def clean_example(example):
    """

    :param example:
    :return:
    """

    example = remove_line_breaks(example)

    return example


def clean_description(description):
    """

    :param description:
    :return: 
    """

    description = remove_line_breaks(description)

    return description


def clean_function(function):
    """

    :param function:
    :return:
    """
    function_text = []

    for i, row in enumerate(function.find_all('tr')):
        line = []

        for td in row.find_all('td'):
            text = clean_link(td.text.strip())
            line.append(text)

        function_text.append(line)

    return function_text


def clean_link(link):
    """

    :param link:
    :return:
    """

    new_link = []
    if 'activateLink' in link:
        link = link.split('activateLink')
        for l in link:
            if '(' in l:
                new_link.append(l.split('(')[1].split(')')[0].split(',')[0].strip('\''))
            else:
                new_link.append(l)
    else:
        return link

    link = "".join(new_link)
    link = link.replace("  ", " ")

    return link


def clean_parameters(parameters):
    """

    :param parameters:
    :return:
    """

    if parameters is None:
        return parameters

    parameters = parameters.strip().split('\n')

    return parameters


def clean_method_info(anchor, method):
    """
    
    :param anchor: 
    :param method: 
    :return: dict()
    """

    example = None
    parameters = None

    # logging.debug(f'anchor text: {anchor}')
    function = anchor.find('table')
    contents = anchor.find('dl').text

    if 'Parameters:' in contents:
        split_contents = anchor.find('dl').text.split('Parameters:')
        description = split_contents[0]
        parameters = split_contents[1]
    else:
        description = contents

    if parameters and 'Example:' in parameters:
        try:
            parameters, example = parameters.split('Example:', 1)
        except ValueError:
            pyperclip.copy(parameters)
            raise Exception(f'There was a problem splitting {parameters}.')

    method['parameters'] = clean_parameters(parameters)
    method['function'] = clean_function(function)
    method['function_inputs'] = get_function_parameters(function)
    method['description'] = clean_description(description)
    method['example'] = clean_example(example)

    return method


def create_content_dict():
    content_sample = {
        'description': None,
        'example': None,
        'function': None,
        'parameters': None,
        'python_name': None,
        'type': None,
        'vba_name': None,
    }

    return content_sample


def create_list_of_methods(dl_tag, method_list, _type):
    dts = dl_tag.find_all('dt')

    for dt in dts:
        content = create_content_dict()
        content['vba_name'] = dt.text.strip()
        content['python_name'] = convert_to_camel_case(content['vba_name'])
        content['type'] = type
        method_list.append(content)

    return method_list


def create_list_of_properties(dl_tag, method_list, _type):
    dts = dl_tag.find_all('dt')

    for dt in dts:
        content = create_content_dict()
        content['vba_name'] = dt.text.strip()
        content['python_name'] = convert_to_camel_case(content['vba_name'])
        content['type'] = type
        # hack: for badly formatted source file interface_PageSetup_15675.htm that didn't close out a tag

        if content['vba_name'] == "Example:":
            continue

        method_list.append(content)

    return method_list


def convert_to_camel_case(string_):
    """

    :param string_:
    :return:
    """
    string_ = string_.replace('3D', '_3d')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string_)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_class_details(soup):
    """

    :param soup:
    :return:
    """

    class_name_tag = soup.find('h1')
    class_name = class_name_tag.text.split(' ')[0]
    class_description = ""
    for i, tag in enumerate(class_name_tag.next_siblings):

        if tag.name == 'hr':
            break
        else:

            if hasattr(tag, 'string') \
                    and tag.string is not None \
                    and 'generatedFatherClass' not in tag.string \
                    and tag.string != "":
                class_description = class_description + '\n' + tag.string.strip()

    class_description = class_description.strip().split('\n')

    return class_name, class_description


def get_function_parameters(html):
    """
    Traverses html table to get method input parameters

        Example table:

        <table>
            <tr><td>o Func <b>AddNew3DCorner</b>(</td><td><script type="text/javascript"> activateLink('Reference','Reference')</script> </td><td><tt>iElement1</tt>,</td></tr>
            <tr><td></td><td><script type="text/javascript"> activateLink('Reference','Reference')</script> </td><td><tt>iElement2</tt>,</td></tr>
            <tr><td></td><td><script type="text/javascript"> activateLink('HybridShapeDirection','HybridShapeDirection')</script> </td><td><tt>iDirection</tt>,</td></tr>
            <tr><td></td><td><script type="text/javascript"> activateLink('double','double')</script> </td><td><tt>iRadius</tt>,</td></tr>
            <tr><td></td><td><script type="text/javascript"> activateLink('long','long')</script> </td><td><tt>iOrientation1</tt>,</td></tr>
            <tr><td></td><td><script type="text/javascript"> activateLink('long','long')</script> </td><td><tt>iOrientation2</tt>,</td></tr>
            <tr><td></td><td><script type="text/javascript"> activateLink('boolean','boolean')</script> </td><td><tt>iTrim</tt>) As <script type="text/javascript"> activateLink('HybridShapeCorner','HybridShapeCorner')</script> </td></tr>
        </table>

        Example table text.

        o Func AddNew3DCorner(
                          activateLink('Reference','Reference') iElement1,
                          activateLink('Reference','Reference') iElement2,
                          activateLink('HybridShapeDirection','HybridShapeDirection') iDirection,
                          activateLink('double','double') iRadius,
                          activateLink('long','long') iOrientation1,
                          activateLink('long','long') iOrientation2,
                          activateLink('boolean','boolean') iTrim)
                              As  activateLink('HybridShapeCorner','HybridShapeCorner')

    :param html:
    :return:
    """

    table_text = html.text

    soup_rows = html.find_all('tt')
    variables = []
    num_pattern = re.compile(r"([0-9]+)")
    for row in soup_rows:
        variable = row.text
        variable = convert_to_camel_case(variable)
        has_integer = re.search(num_pattern, variable)
        if has_integer:
            variable = "_".join(re.split(num_pattern, variable))
            variable = variable[:-1]
        variables.append(variable)

    return variables


def pretty_print_examples(example, tabs=4, wrapper=False):
    if example is None or example == "":
        return ""

    text = ""
    spaces = " " * (4 * tabs)

    for t in example:
        t = t.strip()
        text = text + spaces + '| ' + t + '\n'

    header = spaces + '| Examples:\n'

    text = header + text

    return text


def pretty_print_function(items, tabs=4):
    if items is None:
        return ""

    spaces = " " * (4 * tabs)
    text = spaces + '| '

    pad = ""
    ppad = ""

    for k, item in enumerate(items):
        for kk, t in enumerate(item):
            # text = text + ppad + t
            if k == 0 and kk == 0:
                ppad = " " * len(t)
                text = text + t
            if k == 0 and kk > 0:
                text = text + "    " + t
            if k > 0 and kk == 0:
                text = text + ppad + t
            if k > 0 and kk > 0:
                text = text + "    " + t
        text = text + '\n' + spaces + '| '

    return text


def pretty_print_parameters(items, tabs=4, wrapper=False):
    if items is None:
        return ""

    if wrapper:
        joined_text = ''.join(items)
        items = textwrap.wrap(joined_text, 70)

    text = ""
    spaces = " " * (4 * tabs)
    for t in items:
        text = text + spaces + '| ' + t + '\n'

    return text


def pretty_print_params(params):
    if params == "":
        return ""
    params = [x.strip() for x in params.split(',')]
    _string = ""
    for p in params:
        _string = _string + f'        :param {p}:\n'
    return _string


def read_soup_file(soup_file):
    try:
        with open(soup_file, 'r', encoding="ISO-8859-1") as file:
            soup = BeautifulSoup(file, 'lxml')
    except UnicodeDecodeError:
        raise Exception(f"Couldn't read file: {soup_file}")

    return soup


def create_python_file(class_name, class_description, properties, methods, target_dir):
    reference_info_header = f'        .. note::\n' \
                            f'            CAA V5 Visual Basic help\n\n'
    header = "#! /usr/bin/python3.6\n" \
             f"# module initially auto generated using V5Automation.chm from CATIA R25 on {str(now)}\n\n"

    class_description = pretty_print_parameters(class_description, tabs=4, wrapper=True)

    import_text = 'from pycatia.system_interfaces.base_object import AnyObject\n' \
                  'from pycatia.system_interfaces.collection import Collection\n\n'

    class_text = f'\nclass {class_name}(inherited_from):\n' \
                 f'    """\n' \
                 f'{reference_info_header}' \
                 f'{class_description}\n' \
                 f'    """\n\n' \
                 f'    def __init__(self, com_object):\n' \
                 f'        super().__init__(com_object)\n' \
                 f'        self.{inflection.underscore(class_name)} = com_object' \
                 f'     \n\n'

    repr_text = f'    def __repr__(self):\n' \
                f"        return f'{class_name}()'\n"

    property_text = ""

    for _property in properties:

        parameters = pretty_print_parameters(_property['parameters'], tabs=4)
        description = pretty_print_parameters(_property['description'], tabs=4)
        function = pretty_print_function(_property['function'], tabs=4)
        function_inputs = ', '.join(_property['function_inputs'])
        examples = pretty_print_examples(_property['example'], tabs=4)
        parm_inputs = pretty_print_params(function_inputs)

        if function_inputs == "":
            function_inputs = "self"
        else:
            function_inputs = "self, " + function_inputs

        property_text = property_text + f"    @property\n" \
                                        f"    def {_property['python_name']}({function_inputs}):\n" \
                                        f'        """\n' \
                                        f'{reference_info_header}' \
                                        f"                | {_property['vba_name']}\n" \
                                        f"{function}\n" \
                                        f"{description}" \
                                        f"{examples}" \
                                        f"\n" \
                                        f"{parm_inputs}" \
                                        f"        :return:\n" \
                                        f'        """\n' \
                                        f"        return self.{inflection.underscore(class_name)}.{_property['vba_name']}\n\n"

        if all([
            'Returns' in description,
            'or' in description,
            'sets' in description
        ]):
            property_text = property_text + f"    @{_property['python_name']}.setter\n" \
                                            f"    def {_property['python_name']}(self, value):\n" \
                                            f'        """\n' \
                                            f'            :param type value:\n' \
                                            f'        """\n' \
                                            f"        self.{inflection.underscore(class_name)}.{_property['vba_name']} = value \n\n"

    method_text = ""

    for method in methods:
        parameters = pretty_print_parameters(method['parameters'], tabs=4)
        description = pretty_print_parameters(method['description'], tabs=4)
        function = pretty_print_function(method['function'], tabs=4)
        function_inputs = ', '.join(method['function_inputs'])
        examples = pretty_print_examples(method['example'], tabs=4)
        parm_inputs = pretty_print_params(function_inputs)

        if function_inputs == "":
            function_inputs_h = "self"
        else:
            function_inputs_h = "self, " + function_inputs

        method_text = method_text + f"    def {method['python_name']}({function_inputs_h}):\n" \
                                    f'        """\n' \
                                    f'{reference_info_header}' \
                                    f"                | {method['vba_name']}\n" \
                                    f"{function}\n" \
                                    f"{description}" \
                                    f"                |\n" \
                                    f"                | Parameters:\n" \
                                    f"{parameters}\n" \
                                    f"{examples}" \
                                    f"\n" \
                                    f"{parm_inputs}" \
                                    f"        :return:\n" \
                                    f'        """\n' \
                                    f"        return self.{inflection.underscore(class_name)}.{method['vba_name']}({function_inputs})\n\n"

    text = header + import_text + class_text + property_text + method_text + repr_text

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    target_file_name = target_dir / (class_name.lower() + '.py')

    with open(target_file_name, 'w') as py_file:
        py_file.write(text)


def the_extractory(root_dir, file):
    soup_file = os.path.join(root_dir, file)

    if not os.path.isfile(soup_file):
        raise FileNotFoundError

    sub_folder = root_dir.replace("_files-r25", "")
    target_dir = Path.cwd().parent / sub_folder

    # pp = pprint.PrettyPrinter(indent=4)

    soup = read_soup_file(soup_file)

    class_name, class_description = get_class_details(soup)

    dls = soup.find_all('dl')

    methods = []
    properties = []

    try:
        for dl in dls:
            if "Property Index" in dl.text:
                properties = create_list_of_properties(dl, properties, 'property')

            if "Method Index" in dl.text:
                methods = create_list_of_methods(dl, methods, 'method')

        for i, property in enumerate(properties):
            logging.debug(f"{source_htm_file}: Searching for vba_property anchor name: {property['vba_name']}")
            anchor = soup.find('a', {'name': property['vba_name']})
            try:
                properties[i] = clean_method_info(anchor, property)
            except IndexError:
                raise IndexError(f'There was a problem with cleaning the property: {property} or anchor:{anchor}')

        for i, method in enumerate(methods):
            anchor = soup.find('a', {'name': method['vba_name']})
            # logging.debug(f'method info: {method}, anchor: {anchor}')
            try:
                methods[i] = clean_method_info(anchor, method)
            except IndexError:
                raise IndexError(f'There was a problem with cleaning the method: {method} or anchor:{anchor}')
    except ValueError:
        raise Exception(f'There was a problem processing file :{file}')

    create_python_file(class_name, class_description, properties, methods, target_dir)


if __name__ == '__main__':

    root_dir = 'v5automation_files-r25/generated/interfaces/'

    skip_files = ['interface_OrderGenerator_25474.htm',
                  'interface_BehaviorVBScript_37776.htm',
                  'interface_StrMembers_26420.htm',
                  'interface_StrPlates_25478.htm',
                  'interface_StrObjectExt_28481.htm',
                  'interface_StrFeatureFactory_36096.htm',
                  'interface_StrObjectFactory_34319.htm',
                  'interface_SfmMember_41159.htm',
                  'interface_SfmObjectExt_44255.htm',
                  'interface_ABQAnalysisModel_28479.htm']

    global source_htm_file
    source_htm_file = ''
    FORMAT = f'{source_htm_file} %(message)s'
    logging.basicConfig(level='DEBUG', format=FORMAT)

    for root, dirs, files in os.walk(root_dir):
        files = [f for f in files if f.endswith(".htm") and f not in skip_files]
        for source_htm_file in files:
            logging.debug(f"Processing file {root} {source_htm_file}.")
            the_extractory(root, source_htm_file)
