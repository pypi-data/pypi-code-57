""" Integration tests to test the capability of adding EVCs. """


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
    return start_cli('-A', filename)


def evc_manager(filename):
    """ Instantiate EvcManager """
    return EvcManager(cli_option=instantiate_cli(filename))


class TestAddPathWithUserDefinedPaths:
    """ Test all combinations for is_active """

    def setup_class(self):
        """ Setup class. Instantiate evc_manager """
        Singleton._instances.clear()
        self.evc_mgr = evc_manager('add_evc_correct_request_with_path.yaml')  # pylint: disable=W0201
        results = self.evc_mgr.add_evcs()
        if results['attention_required']:
            raise ValueError(results['results']['msgs'])
        self.evcs = self.evc_mgr.backend.get_evcs()  # pylint: disable=W0201

    def test_evc_ep005_option1(self):
        """ Test if EP005_Option_1_Both_primary_and_backup_dynamic_1
        was created with two dynamic paths
          paths:
            - -
            - -
        """
        # Retrieve EVCs
        # Find EVC EP005_Option_1_Both_primary_and_backup_dynamic_1
        # Confirm if there are two paths
        # Confirm if each path is equal to the ones provided.
        found = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_1_Both_primary_and_backup_dynamic_1":
                assert len(evc.paths) == 2
                found = True
        assert found

    def test_evc_ep005_option2(self):
        """ Test if EP005_Option_2_Both_primary_and_backup_dynamic_2
        was created with two dynamic paths
          paths:

        """
        # Retrieve EVCs
        # Find EVC EP005_Option_2_Both_primary_and_backup_dynamic_2
        # Confirm if there are two paths
        # Confirm if each path is equal to the ones provided.
        found = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_2_Both_primary_and_backup_dynamic_2":
                assert len(evc.paths) == 2
                found = True
        assert found

    def test_evc_ep005_option3(self):
        """ Test if EP005_Option_3_Primary_and_backup_defined
        was created with two dynamic paths
          paths:
              - - name: Ampath2-SanJuan
                - name: Ampath1-Ampath2
                - name: Ampath1-Sax
                - name: SouthernLight2-Sax
                - name: AndesLight-SouthernLight2
              - - name: Ampath2-AndesLight2
                - name: AndesLight-AndesLight2
                - name: Ampath2-SanJuan
        """
        # Retrieve EVCs
        # Find EVC EP005_Option_3_Primary_and_backup_defined
        # Confirm if there are two paths
        # Confirm if each path is equal to the ones provided.
        found = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_3_Primary_and_backup_defined":
                found = True
                primary_instance = evc.paths[0]
                primary = list()
                for path_instance in primary_instance:
                    primary.append(path_instance.name)
                assert (('Ampath2-SanJuan' in primary and
                         'Ampath1-Ampath2' in primary and
                         'Ampath1-Sax' in primary and
                         'SouthernLight2-Sax' in primary and
                         'AndesLight-SouthernLight2' in primary) and
                        len(primary) == 5)

                backup_instance = evc.paths[1]
                backup = list()
                for path_instance in backup_instance:
                    backup.append(path_instance.name)
                assert ('Ampath2-AndesLight2' in backup and
                        'AndesLight-AndesLight2' in backup and
                        'Ampath2-SanJuan' in backup) and len(backup) == 3
        if not found:
            raise

    def test_evc_ep005_option4(self):
        """ Test if EP005_Option_4_Just_primary_defined_dynamic_backup
        was created with two dynamic paths
          paths:
              - - name: Ampath1-Sax
                - name: SouthernLight2-Sax
                - name: AndesLight-SouthernLight2
              - -
        """
        # Retrieve EVCs
        # Find EVC EP005_Option_4_Just_primary_defined_dynamic_backup
        # Confirm if there are two paths
        # Confirm if each path is equal to the ones provided.
        found = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_4_Just_primary_defined_dynamic_backup":
                found = True
                primary_instance = evc.paths[0]
                primary = list()
                for path_instance in primary_instance:
                    primary.append(path_instance.name)
                assert (('Ampath1-Sax' in primary and
                         'SouthernLight2-Sax' in primary and
                         'AndesLight-SouthernLight2' in primary) and
                        len(primary) == 3)

                if not len(evc.paths[1]):
                    raise
        if not found:
            raise

    def test_evc_ep005_option5(self):
        """ Test if EP005_Option_5_Just_primary_defined_no_backup
        was created with two dynamic paths
          paths:
              - - name: Ampath1-Sax
                - name: SouthernLight2-Sax
                - name: AndesLight-SouthernLight2
        """
        # Retrieve EVCs
        # Find EVC EP005_Option_5_Just_primary_defined_no_backup
        # Confirm if there are two paths
        # Confirm if each path is equal to the ones provided.
        found = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_5_Just_primary_defined_no_backup":
                found = True
                if len(evc.paths) > 1:
                    raise
                primary_instance = evc.paths[0]
                primary = list()
                for path_instance in primary_instance:
                    primary.append(path_instance.name)
                assert (('Ampath1-Sax' in primary and
                         'SouthernLight2-Sax' in primary and
                         'AndesLight-SouthernLight2' in primary) and
                        len(primary) == 3)
        if not found:
            raise

    def test_evc_ep005_option5a(self):
        """ Test if EP005_Option_5a_Just_primary_and_dynamic
        was created with two dynamic paths
          paths:
            - -
        """
        # Retrieve EVCs
        # Find EVC EP005_Option_5a_Just_primary_and_dynamic
        # Confirm if there are two paths
        # Confirm if each path is equal to the ones provided.
        found = False
        for evc in self.evcs:
            if evc.name == "EP005_Option_5a_Just_primary_and_dynamic":
                found = True
                if len(evc.paths) != 1:
                    raise
        if not found:
            raise
        assert True
