import os

import yaml
from pkg_resources import resource_filename

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

permission_table_file = os.path.join(resource_filename("enhanced_adb", "res"), "permission.yml")
with open(permission_table_file, encoding="utf-8") as file:
    permission_table = yaml.load(file, Loader=Loader)
    permission_data = permission_table['data']

str_res_file = os.path.join(resource_filename("enhanced_adb", "res"), "res_string.yml")
with open(str_res_file, encoding="utf-8") as file:
    str_res_table = yaml.load(file, Loader=Loader)
