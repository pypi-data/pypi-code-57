#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Template module.

This module provides functions for handling
template.
"""

import os
from jinja2 import Environment, FileSystemLoader

from pyth.utils import sanitize_path


def templating(template_path, context_data=None):
    """Process template for input data.

    Create the template environment and render according to
    template object and context data.

    :param template_path: The string representing the template path.
    :param context_data: The data to pass to the template. It can be an
    iterable or dict.
    :type template_path: str
    :type context_data: object
    :rtype: str
    :returns: The rendered text from template and data.
    """

    # clean template path
    template_path = sanitize_path(template_path)
    # dir of template file
    template_dir = os.path.dirname(template_path)
    # only file name
    template_name = os.path.basename(template_path)
    loader = FileSystemLoader(template_dir)
    env = Environment(loader=loader)
    template = env.get_template(template_name)

    return template.render(data=context_data)
