from tcell_agent.version import VERSION
import os


class AgentConfig(dict):
    def __init__(self):
        dict.__init__(self)

        self['agent_type'] = 'Python'
        self['agent_version'] = VERSION
        self['default_cache_dir'] = os.path.abspath('tcell/cache')
        self['default_config_file_dir'] = os.getcwd()
        self['default_log_dir'] = os.path.abspath('tcell/logs')
        self['default_preload_policy_file_dir'] = os.getcwd()
        self['overrides'] = {
            'applications': [{
                'enable_json_body_inspection': True
            }]
        }

        if os.environ.get('TCELL_AGENT_HOME') and not os.environ.get('TCELL_AGENT_CONFIG'):
            self['overrides']['config_file_dir'] = os.getcwd()
