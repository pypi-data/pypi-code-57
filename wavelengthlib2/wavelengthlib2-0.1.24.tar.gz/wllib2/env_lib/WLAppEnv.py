''' 
    WLAppEnv is a class intended to be used as an environment wrapper applications.
    It establishes whether this environment is a DEV, TEST or PROD execution
    and delivers parameter value accordingly from two .ini config files (env and app)
    It looks for a Windows environment valrible called WL_PROJECT_ROOT which tells it where the project root is - one up from this directory
    The wavelength_env.ini config file, which is in the same folder as this file is...
    - should be different in DEV/TEST/PROD setups
    - holds the wl_environment_name param name which defines whether the application is sunninga s DEV, TEST or PROD
    - holds parameters which are specific to the environment DEV/TEST/PROD
    The app_name argument to the constructor assume this is a the name of the sub-folder under the project _root where the appliction code is.
    It expects to file an ini file called app_name.ini in that folder where application specific parameter settings can be held.
    It offers a logging mechanism for other code to use
    It accesses Azure KeyVault secret values if requested
    This class is designed as a singleton - meaning only one instance of this class may exist for an execution. 
    Any attempt to create a 2nd (or more) instance of this object will return the first instance created
'''
import sys
import os
from configparser import SafeConfigParser
from wllib2.env_lib import env_utils

'''
WL_PROJECT_ROOT_ENV_VARIABLE = 'WL_PROJECT_ROOT'
WL_ENV_INI_FILE = 'wl_lib/env_utils/wavelength_env.ini'
WL_ENV_PARAM_SET = 'ENV'
WL_ENV_PARAM_NAME = 'wl_environment_name'
WL_LIB_ROOT_PARAM_NAME = 'wl_lib_root'
'''
WL_KEY_VAULT_PARAM_NAME = 'KeyVaultName'

def _get_parameter_value(app_p, env_name, param_name):
    ''' get a value of an environment parameter for the current DEV/TEST/PROD environment
        precendent is application parameters win over enviroment ones

    Args:
        env_p (SafeConfigParser): the enviroment config parser
        app_p (SafeConfigParser): the app config parser
        param_name (str): the requested parameter name
        
    Returns:
        str: the value of the parameter found, None if not found
    '''  
    '''
    try:
        wl_lib_path_env = env_p.get('ENV', param_name)
    except:
        wl_lib_path_env = None
    '''

    try:
        wl_lib_path_app = app_p.get(env_name, param_name)
    except:
        wl_lib_path_app = None

    return  wl_lib_path_app


class WLAppEnv(object):
    _instance = None

    def __new__(self, app_ini_file):
        ''' for first call creat and return an instance of WLAppEnv - for all future calls return the same object
            Access the config parser .ini files
            Initialise the log stash
            Connect to the Azure Key Vault

        Args: n/a
            
        Returns: the instance 
        '''  
        if self._instance is None:
            #print('Creating the object')
            self._instance = super(WLAppEnv, self).__new__(self)

            self.env_name = env_utils.get_env_name()

            '''
            self.wl_project_root = os.environ.get(WL_PROJECT_ROOT_ENV_VARIABLE)
            self.using_azure_keyvault = using_azure_keyvault

            self.env_parser = SafeConfigParser()
            wl_env_file_name = self.wl_project_root + '/' + WL_ENV_INI_FILE
            self.env_parser.read(wl_env_file_name)
            self.env_name = self.env_parser.get(WL_ENV_PARAM_SET, WL_ENV_PARAM_NAME)
 
            app_ini_file = self.wl_project_root + '/' + app_name + '/' + app_name + '.ini'
            '''

            self.app_parser = SafeConfigParser()
            self.app_parser.read(app_ini_file)

            '''
            wl_lib_root = _get_parameter_value(self.app_parser,  self.env_name, WL_LIB_ROOT_PARAM_NAME)
            sys.path.append(wl_lib_root)
            '''

            self.app_log = ''
            self.env_log = f'Env = {self.env_name}; '

            key_vault_name = _get_parameter_value(self.app_parser,  self.env_name, WL_KEY_VAULT_PARAM_NAME)
            if key_vault_name:
                self.using_azure_keyvault = True
            else:
                self.using_azure_keyvault = False

            if self.using_azure_keyvault:
                from azure.identity import ClientSecretCredential
                from azure.keyvault.secrets import SecretClient
                tenant_id = self.app_parser.get(self.env_name, 'TenantID')
                client_id = self.app_parser.get(self.env_name, 'ClientID')
                client_secret = self.app_parser.get(self.env_name, 'ClientSecret')
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

            self.log_mode = 'LOG_AND_PRINT'
        return self._instance

    def get_env_name(self):
        ''' get the name of the environment one of DEV, TEST or PROD

        Args: n/a
            
        Returns:
            str: the name of the enviroment
        '''  
        return self.env_name

    def get_parameter(self, param_name):
        ''' get the vaue of a parameter - if directed get from Azure Key Vault

        Args: 
            param_name (str): the name of the parameter
            
        Returns:
            str: the value of the parameter
        '''  
        p_val = _get_parameter_value(self.app_parser,  self.env_name, param_name)
        if p_val == '$azkv.secret' and self.using_azure_keyvault:
            p_val = self.get_secret_value(param_name)
        return p_val

    def log_message(self, mess, print_mode = 'NO_PRINT'):
        ''' save a message in the log and print it if requested

        Args: 
            mess (str): log message
            print_mode (str): PRINT or NO_PRINT
            
        Returns:
            n/a
        '''  
        self.app_log += f'\n{mess};'
        if self.log_mode == 'LOG_AND_PRINT' and print_mode != 'NO_PRINT':
            print(mess)
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


    
