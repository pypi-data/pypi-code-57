#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Helper module.

Main entrypoint for processing template operations.

"""

import os
from jinja2 import TemplateNotFound, Environment, FileSystemLoader

from pyth.utils import find_template_dir, sanitize_path


class Helper(): # pylint: disable=too-few-public-methods
    """Main helper class.

    This class is the glue for the template and data. The result is outputed
    in a file in the current directory.

    :param templates_dir: The path of templates directory intended to
        override the default.
    :type templates_dir: str
    """

    __template_dir = None
    __loader = None
    __environment = None

    def __init__(self, templates_dir=None):
        self.__init_template_context(templates_dir)

    def __init_template_context(self, path):
        """Initialisation method.

        Prepare the template context of the helper. It is based on the
        file system loader of Jinja2 librairies.
        """

        _override_path = None
        if path:
            path = sanitize_path("", basedir=path)
            if os.path.exists(path):
                _override_path = path
        self.__template_dir = _override_path or find_template_dir()

        if self.__template_dir:
            self.__loader = FileSystemLoader(self.__template_dir)
            self.__environment = Environment(loader=self.__loader)

    def render_template(self, template_name, context_data=None):
        """Process template with input data.

        Renders the template accoding to data with a simple
        jinja render template method.

        :param template_name: The name of the template to be processed.
        :param context_data: The data to pass to the template. It can be an
            iterable or dict.
        :type template_name: str
        :type context_data: object
        :rtype: str
        :returns: The rendered text from template and data.
        """

        if not self.__template_dir:
            print("Warning - Template directory not set.")
            return None

        try:
            _template = self.__environment.get_template(template_name)
            _rendered_text = _template.render(data=context_data)
            return _rendered_text
        except TemplateNotFound as tnf:
            print(f"Error with template - '{tnf}'.")
            print(f"Not found in '{self.__template_dir}'.")
            print("Make sure template exists and corretcly named.")
            return None
