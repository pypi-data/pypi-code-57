import os
import json
from halo import Halo

from devyzer.commands.__init__ import Command
from devyzer.constants import DEFAULT_CONFIG_NAME
from devyzer.utils.cli import load_json_from_file, save_json_to_file, get_current_configuration
from devyzer.state import SessionState


class SaveProjectEntitiesCommand(Command):
    def name(self):
        return 'save-project-entities'

    def run(self, args, sio, project_configuration):
        with Halo(text='Saving project entities locally ...', text_color='cyan', color='cyan',
                  spinner='dots') as sp:
            try:
                local_configurations = {}
                local_configuration_file = os.getcwd() + "/" + DEFAULT_CONFIG_NAME
                if os.path.exists(local_configuration_file):
                    local_configurations = load_json_from_file(local_configuration_file)

                local_configurations.update(project_configuration)
                save_json_to_file(project_configuration, local_configuration_file)
                sp.succeed("Entities saved successfully .")

            except Exception as e:

                sp.fail(str(e))
                return False
        return True

class SaveProjectEntitiesCommandSilent(Command):
    def name(self):
        return 'save-project-entities-silent'

    def run(self, args, sio, project_configuration):

        try:
            local_configurations = {}
            local_configuration_file = os.getcwd() + "/" + DEFAULT_CONFIG_NAME
            if os.path.exists(local_configuration_file):
                local_configurations = load_json_from_file(local_configuration_file)
            local_configurations.update(project_configuration)
            save_json_to_file(project_configuration, local_configuration_file)
        except Exception as e:
            return False
        return True


class SendProjectEntitiesCommand(Command):
    def name(self):
        return 'send-project-entities'

    def run(self, args, sio, project_configuration):

        with Halo(text='Sending local entities to remote ...', text_color='cyan', color='cyan',
                  spinner='dots') as sp:
            try:

                current_configuration = get_current_configuration()
                if current_configuration is None:
                    sio.emit('user_uttered', {"message": '/no_configurations_found'})
                    return True

                # todo: validate local project id with the incomming project id to ensure
                #  that they are same else notify user

                sio.emit('user_uttered',
                         {"message": '/incoming_configuration',
                          "session_id": SessionState.session_id,
                          'metadata': {
                              'configurations': current_configuration
                          }})

            except Exception as e:

                sp.fail(str(e))
                return False
        return True
