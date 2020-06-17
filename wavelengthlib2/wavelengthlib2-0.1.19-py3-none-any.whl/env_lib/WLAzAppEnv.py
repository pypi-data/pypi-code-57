''' 
    WLAzAppEnv is a class intended to be used as an environment wrapper for Azure Serverless Function calls.
    It is created within the constructor of WL_Az_http_func_handler() class
    WLAzAppEnv establishes whether this execution is a Dev, TEST or PROD execution
    and delivers parameter value accordingly from two .ini config file (project and app)
    It offers a logging mechanism which write to Azure Application Insight for other code to use
    It accesses Azure KeyVault secret values if requested
    This class is designed as a singleton - meaning only one instance of this class may exist for an execution. 
    Any attempt to create a 2nd (or more) instance of this object will return the first instance created
'''
import sys
import os
import logging
from configparser import SafeConfigParser


WL_ENV_INI_FILENAME = 'wl_project_config.ini'
WL_APP_INI_FILENAME = 'wl_app_config.ini'
WL_ENV_PARAM = 'WL_APP_ENV'

def _get_parameter_value(env_p, app_p, env_name, param_name):
    try:
        wl_lib_path_env = env_p.get('ENV', param_name)
    except:
        wl_lib_path_env = None

    try:
        wl_lib_path_app = app_p.get(env_name, param_name)
    except:
        wl_lib_path_app = None

    return  wl_lib_path_app if wl_lib_path_app else wl_lib_path_env

def _init_logger():
    logger = logging.getLogger()
    h = logging.StreamHandler(sys.stdout)
    h.flush = sys.stdout.flush
    logger.addHandler(h)
    return logger

class WLAzAppEnv(object):
    _instance = None

    def __new__(self, proj_root_dir, app_name, using_azure_keyvault=True):
        ''' for first call creat and return an instance of WLAppEnv - for all future calls return the same object
            Access the config parser .ini files
            Initialise the log stash
            Connect to the Azure Key Vault

        Args: n/a
            
        Returns: the instance 
        '''          
        if self._instance is None:
            self._instance = super(WLAzAppEnv, self).__new__(self)

            self.wl_project_root = proj_root_dir
            self.app_name = app_name
            self.using_azure_keyvault = using_azure_keyvault

            proj_ini_file = self.wl_project_root + '/' + WL_ENV_INI_FILENAME
            self.env_parser = SafeConfigParser()
            self.env_parser.read(proj_ini_file)

            try:
                self.env_name = os.environ[WL_ENV_PARAM]
            except:
                self.env_name = self.env_parser.get('ENV', 'WLEnvironment')

            app_ini_file = proj_root_dir + '/' + app_name + '/' + WL_APP_INI_FILENAME
            self.app_parser = SafeConfigParser()
            self.app_parser.read(app_ini_file)

            self.env_log = f'Env = {self.env_name} Proj Root = {self.wl_project_root}; '
            self.env_log += f'\nproj_ini_file={proj_ini_file}; '
            self.env_log += f'\nApp ini = {app_ini_file}; '

            self.logger = _init_logger()
            self.logger.info(self.env_log)
            sys.stdout.flush

            self.app_log = ''
            self.log_mode = 'LOG_AND_PRINT'

            if self.using_azure_keyvault:
                from azure.identity import ClientSecretCredential
                from azure.keyvault.secrets import SecretClient
                tenant_id = self.env_parser.get('ENV', 'TenantID')
                client_id = self.env_parser.get('ENV', 'ClientID')
                client_secret = self.env_parser.get('ENV', 'ClientSecret')
                key_vault_name = self.env_parser.get('ENV', 'KeyVaultName')
                key_vault_uri = f'https://{key_vault_name}.vault.azure.net/'

                _credential = ClientSecretCredential(
                    tenant_id = tenant_id,
                    client_id = client_id,
                    client_secret = client_secret
                )

                try:
                    self.sc = SecretClient(vault_url=key_vault_uri, credential=_credential)
                except:
                    self.sc = None
                    self.env_log += f'Azure Key Vault [{key_vault_name}] could not be accessed; '
            else:
                self.sc = None

        return self._instance

    def get_env_name(self):
        ''' get the name of the environment one of DEV, TEST or PROD

        Args: n/a
            
        Returns:
            str: the name of the enviroment
        '''  
        return self.env_name

    def get_app_name(self):
        ''' get the name of the app

        Args: n/a
            
        Returns:
            str: the name of the app
        '''  
        return self.app_name

    def get_parameter(self, param_name):
        ''' get the vaue of a parameter - if directed get from Azure Key Vault

        Args: 
            param_name (str): the name of the parameter
            
        Returns:
            str: the value of the parameter
        '''  
        p_val = _get_parameter_value(self.env_parser, self.app_parser,  self.env_name, param_name)
        if p_val == '$azkv.secret' and self.using_azure_keyvault:
            p_val = self.get_secret_value(param_name)
        return p_val

    def log_message(self, mess, print_mode = 'PRINT'):
        ''' save a message in the log and print it if requested

        Args: 
            mess (str): log message
            print_mode (str): PRINT or NO_PRINT
            
        Returns:
            n/a
        '''  
        self.app_log += f'\n{mess};'
        if self.log_mode == 'LOG_AND_PRINT' and print_mode != 'NO_PRINT':
            self.logger.info(mess)
            sys.stdout.flush
        return

    def clear_app_log_messages(self):
        ''' delete the log message

        Args: 
            n/a
            
        Returns:
            n/a
        '''  
        self.app_log = ''
        return 

    def get_log_messages(self):
        ''' get all the log messages

        Args: 
            n/a
            
        Returns:
            str: all the log messages
        '''  
        return self.env_log + '\n' + self.app_log

    def get_secret_value(self, secret_name):
        ''' get a secret value from the Azure Key Vault

        Args: 
            secret_name (str): the name of the secret
            
        Returns:
            secret_val (str): value of the secret in the vault (None if not found)
        '''  
        secret_val = None
        if self.sc:
            try:
                secret_val = self.sc.get_secret(secret_name).value
            except:
                secret_val = None
        return secret_val

    
