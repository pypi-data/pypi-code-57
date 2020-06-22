# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.assess import patch_manager
from contrast.applies.deserialization import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

import logging

logger = logging.getLogger("contrast")


DESERIALIZER = "PyYAML"
LOAD = "load"
LOAD_ALL = "load_all"
YAML = "yaml"


def load(original_load, patch_policy=None, *args, **kwargs):
    result = apply_rule(original_load, DESERIALIZER, args[0], args, kwargs)

    if not load.sent_warning:
        _announce_yaml_load_warning(LOAD)
        load.sent_warning = True

    return result


def load_all(original_load, patch_policy=None, *args, **kwargs):
    result = apply_rule(original_load, DESERIALIZER, args[0], args, kwargs)

    if not load_all.sent_warning:
        _announce_yaml_load_warning(LOAD_ALL)
        load_all.sent_warning = True

    return result


def _announce_yaml_load_warning(func_name):
    logger.warning(
        "Identified call to PyYaml.%s, consider using PyYaml.safe_load instead.",
        func_name,
    )


def patch_pyyaml(yaml_module):
    """
    PyYaml 5.1 has new updates to warn a user about unsafe yaml loading:

    https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation

    We don't need to patch full_load because it calls yaml.load(value, Loader=FullLoader)
    """
    patch_cls_or_instance(yaml_module, LOAD, load)
    patch_cls_or_instance(yaml_module, LOAD_ALL, load_all)


def register_patches():
    register_post_import_hook(patch_pyyaml, YAML)


def reverse_patches():
    yaml = sys.modules.get("yaml")
    if not yaml:
        return

    for name in [LOAD, LOAD_ALL]:
        patch_manager.reverse_patch(yaml, name)


load.sent_warning = False
load_all.sent_warning = False
