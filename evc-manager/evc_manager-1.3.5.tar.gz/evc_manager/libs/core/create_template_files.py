""" This module will be used by CLI option  -T to create
template input files.
"""
import sys
import os
import errno
import yaml
from yaml import dump


class MyDumper(yaml.Dumper):  # pylint: disable=R0901
    """ Ignore aliases when printing dictionaries using YAML """
    def ignore_aliases(self, _data):  # pylint: disable=W0221
        return True


def create_template(version, action):
    """
    Return the template with the action provided
    Args:
        version: interface version
        action: action to be added
    Return:
        dict
    """
    unis = list()
    for name in ["a", "z"]:
        uni = dict()
        uni["device"] = "device_name_%s" % name
        uni["interface_name"] = "interface_name_%s" % name
        uni["tag"] = dict()
        uni["tag"]["type"] = "vlan"
        if action == "add_range":
            uni["tag"]["value"] = "[first_vlan_id, last_vlan_id]"
        else:
            uni["tag"]["value"] = "vlan_id"

        unis.append(uni)

    evc = dict()
    evc["name"] = "evc_name"
    evc["unis"] = unis

    evcs = list()
    evcs.append(evc)

    template = dict()
    template["version"] = version
    template["action"] = action
    template["evcs"] = evcs
    return template


def create_template_files(version="1.0",
                          parent_dir="./",
                          folder="evc_manager_templates"):
    """ Create a folder with a file for add, add_range, change, delete,
    and move."""

    # Create folder. Verify permissions and errors.
    # folder name: evc_manager_templates

    # Path
    path = os.path.join(parent_dir, folder)

    try:
        os.mkdir(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

    for action in ["add", "add_range", "delete", "move", "change"]:
        # create file with content from create_template(version, action)
        filename = "%s/evc_%s" % (folder, action)
        with open(filename, 'w') as template_file:
            dump(create_template(version, action),
                 template_file,
                 default_flow_style=False,
                 Dumper=MyDumper)

        fix_add_range_quotes(filename)

    sys.exit(0)


def fix_add_range_quotes(filename):
    """  work around the YAML limitations to accept [ ] as begin
    and end of a string used for add_range. As YAML
    adds ' (single quotes) and the evc_manager doesn't support ',
    we need to remove them"""
    if filename.find("add_range") > 0:
        sed_option = "s/\\'//g"
        bash_command = "sed \"%s\" %s" % (sed_option, filename)
        os.system("%s > %s" % (bash_command, "%s.tmp" % filename))
        # Since Mac OS doesn't support sed -i ....
        os.system("mv %s %s" % ("%s.tmp" % filename, filename))
