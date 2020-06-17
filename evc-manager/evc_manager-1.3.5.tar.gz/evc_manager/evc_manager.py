""" SDN EVC manager. Main module """


from .libs.core.cli import CliOptions
from .libs.core.log import info
from .libs.core.log import process_result
from .libs.core.import_evc import import_evcs
from .libs.core.parse_add_range_evcs import process_add_range
from .libs.core.evc_list import EvcsList
from .backends.kytos_eline import KytosEline
from .backends.oess import Oess


class EvcManager(object):
    """ EVC Manager Class """

    def __init__(self, cli_option=None):
        self.cli_options = CliOptions() if not cli_option else cli_option
        self.backend = Oess() if self.cli_options.is_oess else KytosEline()
        self.backend.authenticate()
        # We are always required to know the existing EVCs
        self.current_evcs = EvcsList(evc_list=self.backend.get_evcs())

    def list_evcs(self):
        """ List EVCs (CLI option -L) """
        return self.current_evcs.to_dict()

    def add_evc(self, new_evc):
        """ Add an EVC """
        found_evc = self.current_evcs.find(new_evc)
        if not found_evc:
            info('Creating EVC %s...' % new_evc.name)
            return self.backend.add_evc(new_evc)
        else:
            return {'result': 'error',
                    'msg': 'EVC %s already exists.' % new_evc.name}

    def add_evcs(self, new_evcs=None):
        """ Add EVCs (CLI option -A) """
        if not new_evcs:
            new_evcs = import_evcs(source_file=CliOptions().file_content)

        results = []
        for new_evc in new_evcs:
            results.append(self.add_evc(new_evc))
        return process_result(msg=results)

    def add_evcs_range(self):
        """ Add range of EVCs (CLI option -R) """
        file_content = process_add_range(CliOptions().file_content)
        new_evcs = import_evcs(source_file=file_content)
        return self.add_evcs(new_evcs=new_evcs)

    def change_evc(self, evc_to_change):
        """ Add an EVC """
        found_evc = self.current_evcs.find(evc_to_change)
        if found_evc:
            info('Changing EVC %s...' % evc_to_change.name)
            backend_evc_id = found_evc.current_config.backend_evc_id
            evc_to_change.current_config.backend_evc_id = backend_evc_id
            return self.backend.add_evc(evc_to_change, change=True)
        else:
            return {'result': 'error',
                    'msg': 'EVC %s does not exist.' % evc_to_change.name}

    def change_evcs(self, evcs_to_change=None):
        """ Change EVCs (CLI option -C) """
        if not evcs_to_change:
            evcs_to_change = import_evcs(source_file=CliOptions().file_content)

        results = []
        for evc_to_change in evcs_to_change:
            results.append(self.change_evc(evc_to_change))
        return process_result(msg=results)

    def delete_evc(self, evc_to_delete):
        """ Delete an EVC """
        found_evc = self.current_evcs.find(evc_to_delete)
        if found_evc:
            return self.backend.delete_evc(found_evc)
        else:
            return {'result': 'error',
                    'msg': 'EVC %s not found/deleted.' % evc_to_delete.name}

    def delete_evcs(self):
        """ Delete EVCs (CLI option -D) """

        evcs_to_delete = import_evcs(source_file=CliOptions().file_content)

        results = []
        for evc_to_delete in evcs_to_delete:
            results.append(self.delete_evc(evc_to_delete))
        return process_result(results)

    def move_evc(self, evc_to_move):
        """ Move EVC """
        nni = CliOptions().move_from_nni

        found_evc = self.current_evcs.find(evc_to_move)
        if found_evc:
            backend_evc_id = found_evc.current_config.backend_evc_id
            evc_to_move.current_config.backend_evc_id = backend_evc_id

            return self.backend.move_evc(evc_to_move,
                                         found_evc.get_primary_path(),
                                         found_evc.get_backup_path(),
                                         nni)
        else:
            return {'result': 'error',
                    'msg': 'EVC %s does not exist.' % evc_to_move.name}

    def move_evcs(self):
        """ Move EVCs (CLI option -M) """
        evcs_to_move = import_evcs(source_file=CliOptions().file_content)

        results = []
        for evc_to_move in evcs_to_move:
            results.append(self.move_evc(evc_to_move))
        return process_result(results)

    def run(self):
        """ Run """

        if self.cli_options.is_list:
            return self.list_evcs()
        elif self.cli_options.is_add:
            return self.add_evcs()
        elif self.cli_options.is_add_range:
            return self.add_evcs_range()
        elif self.cli_options.is_change:
            return self.change_evcs()
        elif self.cli_options.is_delete:
            return self.delete_evcs()
        elif self.cli_options.is_move:
            return self.move_evcs()

        return process_result(msg='Invalid CLI option selected.')
