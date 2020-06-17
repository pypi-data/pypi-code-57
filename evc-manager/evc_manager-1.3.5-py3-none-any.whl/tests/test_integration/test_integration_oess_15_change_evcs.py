""" Integration tests to test the capability of changing EVCs. """


import os
import pytest
from evc_manager import EvcManager
from ...libs.core.cli import CliOptions, create_parser
from ...libs.core.singleton import Singleton


pytestmark = pytest.mark.skip("all tests depend of virtual box")


FOLDER = './tests/test_integration/content_files/'
CORRECT_CLI = ['-u', 'admin',
               '-t', 'admin',
               '-p', 'sparc123',
               '-O', 'https://192.168.56.12/oess/',
               '-v', 'info',
               '-q']


def prepare_cli(option, source_file):
    """ Prepare CLI options adding action and source file """
    source_file = os.path.abspath(FOLDER + source_file)
    cli_options = CORRECT_CLI
    cli_options.append(option)
    cli_options.append('-f')
    cli_options.append(source_file)
    return cli_options


def start_cli(action, source_file):
    """ Prepare CLI """
    parser = create_parser()
    args = parser.parse_args(prepare_cli(action, source_file))
    return CliOptions(parser, args)


def instantiate_cli(filename):
    """ Instantiate CLI """
    return start_cli('-C', filename)


def evc_manager(filename):
    """ Instantiate EvcManager """
    return EvcManager(cli_option=instantiate_cli(filename))


class TestChangeEVCs:
    """ Test changes applied to the EVCs """

    def setup_class(self):
        """ Instantiate evc_manager """
        Singleton._instances.clear()
        self.evc_mgr = evc_manager('change_evc_correct_request.yaml')  # pylint: disable=W0201
        results = self.evc_mgr.change_evcs()
        if results['attention_required']:
            raise ValueError(results['results']['msgs'])
        self.evcs = self.evc_mgr.backend.get_evcs()  # pylint: disable=W0201

    def test_evc_example01(self):
        """ Test if EvcExample1 had the device and VLAN correctly changed
        from
            unis:
                - device: SanJuan
                  interface_name: s4-eth1
                  tag:
                    type: vlan
                    value: 111
                - device: SouthernLight2
                  interface_name: s3-eth1
                  tag:
                    type: vlan
                    value: 111
        to
            unis:
                - device: Ampath1
                  interface_name: s1-eth1
                  tag:
                    type: vlan
                    value: 111
                - device: SouthernLight2
                  interface_name: s3-eth1
                  tag:
                    type: vlan
                    value: 112
        """
        found_evc = False
        found_uni_1 = False
        found_uni_2 = False
        for evc in self.evcs:
            if evc.name == "EvcExample1":
                found_evc = True
                assert len(evc.unis) == 2
                for uni in evc.unis:
                    if uni.device == "Ampath1":
                        if uni.interface_name == "s1-eth1":
                            if uni.tag.value == 111:
                                found_uni_1 = True
                    elif uni.device == "SouthernLight2":
                        if uni.interface_name == "s3-eth1":
                            if uni.tag.value == 112:
                                found_uni_2 = True

        assert found_evc and found_uni_1 and found_uni_2

    def test_evc_example02(self):
        """ Test if EvcExample2 had the device and VLAN correctly changed
        from
            unis:
              - device: Ampath1
                interface_name: s1-eth1
                tag:
                  type: vlan
                  value: 333
              - device: Ampath3
                interface_name: s8-eth1
                tag:
                  type: vlan
                  value: 333
        to
            unis:
              - device: Ampath1
                interface_name: s1-eth1
                tag:
                  type: vlan
                  value: 222 <--
              - device: SouthernLight2 <--
                interface_name: s3-eth1
                tag:
                  type: vlan
                  value: 222
        """
        found_evc = False
        found_uni_1 = False
        found_uni_2 = False
        for evc in self.evcs:
            if evc.name == "EvcExample2":
                found_evc = True
                assert len(evc.unis) == 2
                for uni in evc.unis:
                    if uni.device == "Ampath1":
                        if uni.interface_name == "s1-eth1":
                            if uni.tag.value == 222:
                                found_uni_1 = True
                    elif uni.device == "SouthernLight2":
                        if uni.interface_name == "s3-eth1":
                            if uni.tag.value == 222:
                                found_uni_2 = True

        assert found_evc and found_uni_1 and found_uni_2

    def test_evc_example03(self):
        """ Test if EP005_Option_5_Just_primary_defined_no_backup
         had the VLANs correctly changed to 905 and the paths moved from
            paths:
              - - name: Ampath1-Sax
                - name: SouthernLight2-Sax
                - name: AndesLight-SouthernLight2
        to
            paths:
              - - name: Ampath2-AndesLight2
                - name: Ampath1-Ampath2
                - name: AndesLight-AndesLight2
              - -
        """
        found = False
        found_uni_1 = False
        found_uni_2 = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_5_Just_primary_defined_no_backup":
                found = True
                assert len(evc.unis) == 2
                for uni in evc.unis:
                    if uni.device == "AndesLight":
                        if uni.interface_name == "s5-eth1":
                            if uni.tag.value == 905:
                                found_uni_1 = True
                    elif uni.device == "Ampath1":
                        if uni.interface_name == "s1-eth1":
                            if uni.tag.value == 905:
                                found_uni_2 = True
                if found_uni_1 and found_uni_2:
                    primary_instance = evc.paths[0]
                    primary = list()
                    for path_instance in primary_instance:
                        primary.append(path_instance.name)
                    assert (('Ampath2-AndesLight2' in primary and
                             'Ampath1-Ampath2' in primary and
                             'AndesLight-AndesLight2' in primary) and
                            len(primary) == 3)

                    if not len(evc.paths[1]):
                        raise
        if not found and found_uni_1 and found_uni_2:
            raise
