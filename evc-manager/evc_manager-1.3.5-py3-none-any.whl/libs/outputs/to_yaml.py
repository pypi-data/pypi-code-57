""" YAML module. Used to read and write in YAML format """

from datetime import datetime
from yaml import dump
import yaml
from ..core.cli import CliOptions


class MyDumper(yaml.Dumper):  # pylint: disable=R0901
    """ Ignore aliases when printing dictionaries using YAML """
    def ignore_aliases(self, _data):  # pylint: disable=W0221
        return True


def minimize_unis(unis):
    """ Export just the minimal set of attributes for UNIs:
        device
        interface_name
        tag:
            value
    """
    new_unis = list()
    for uni in unis:
        new_uni = dict()
        new_uni['device'] = uni['device']
        new_uni['interface_name'] = uni['interface_name']
        new_uni['tag'] = dict()
        new_uni['tag']['value'] = uni['tag']['value']
        new_unis.append(new_uni)
        del new_uni
    return new_unis


def minimize(ctks):
    """ Export just the minimal set of attributes:
    name,
    unis:
        device
        interface_name
        tag:
            value
    """
    new_ctks = list()

    for ctk in ctks:
        evc_copy = dict()
        evc_copy['name'] = ctk['name']
        evc_copy['unis'] = minimize_unis(ctk['unis'])
        new_ctks.append(evc_copy)
        del evc_copy
    return new_ctks


def print_yaml(ctks):
    """ Exported function to print in YAML """
    print("Number of Circuits: %s " % len(ctks))

    if CliOptions().output_format == 'yaml_minimal':
        ctks = minimize(ctks)

    evcs = dict()
    evcs['evcs'] = ctks
    evcs['version'] = '1.0'

    now = datetime.now()
    now.strftime("%Y/%m/%d %H:%M:%S")
    evcs['date'] = now

    with open(CliOptions().destination_file, 'w') as yaml_file:
        dump(evcs, yaml_file, default_flow_style=False, Dumper=MyDumper)
        print("List of circuits saved on file: %s " %
              CliOptions().destination_file)
