''' 
    WL_Az_http_func_handler is a class intended to be used by Azure Serverless Functions
    When invoked an Azure function will create an object of this class, pass
    to it the HttpRequest & HttpContext it has been passed.
    Then call the exec_request() method and return a composed result
'''  
import sys, traceback
import os
from importlib import reload
import pandas as pd
from datetime import date, datetime
import json
from wllib2.env_lib import WLAzAppEnv

def _proccess_request_inputs(http_req):
    ''' Takes an Azure function HttpRequest as an argument and extracts out all the parameters (get or post or json)
        and extracts the binary file if there is one.

    Args:
        http_req (Azure function HttpRequest): The HTTP request data

    Returns:
        req_params (Dictionary), req_file (binary file bytes): The data extracted from the request.
    '''
    req_params = {}
    req_file = None

    req_get_params = http_req.params
    for req_key in req_get_params:
        req_val = req_get_params.get(req_key)
        req_params[req_key] = req_val

    try:
        req_body = http_req.get_json()
    except ValueError:
        pass
    else:
        for req_key in req_body:
            req_val = req_body.get(req_key)
            req_params[req_key] = req_val

    try:
        file_bytes = http_req.get_body()
    except ValueError:
        pass
    else:
        req_file = file_bytes

    return req_params, req_file

def _dict_to_html(r, d, nametag="<strong>%s: </strong>", itemtag='<li>%s</li>',
             valuetag="%s", blocktag=('<ul>', '</ul>')):
    ''' Recursive function which takes a python dictionary type and converts it into a list of strings containing HTML which 
       , if joined together, will display the dictionary data on a web page.

    Args:
        r (list): the list of HTML strings
        d (dictionary): the dictionary source data
        nametag (str): html styling for nametags
        itemtag (str): html styling for itemtags
        valuetag (str): html styling for valuetags
        blocktag (str): html styling for blocktags
        
    Returns:
        nothing returned - the output is in the r list argument.
    '''   
    if isinstance(d, dict):
        r.append(blocktag[0])
        for k in d:
            v = d[k]
            name = nametag % k
            if isinstance(v, dict) or isinstance(v, list):
                r.append(itemtag % name)
                _dict_to_html(r, v)
            else:
                if isinstance(v, pd.DataFrame):
                    value = v.to_html()
                else:
                    value = valuetag % v
                r.append(itemtag % (name + value))
        r.append(blocktag[1])
    elif isinstance(d, list):
        r.append(blocktag[0])
        for i in d:
            if isinstance(i, dict) or isinstance(i, list):
                r.append(itemtag % " - ")
                _dict_to_html(r, i)
            else:
                r.append(itemtag % i)
    r.append(blocktag[1])
    return

def _json_serialize(obj):
    ''' JSON serializer for objects not serializable by default json code

    Args:
        obj (any python type): the thing to be serialised
        
    Returns:
        a serializable version of obj.
    '''
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    if isinstance(obj, pd.DataFrame):
        serial = obj.to_dict()
        return serial

    if isinstance(obj, pd.Series):
        serial = obj.to_dict()
        return serial

    return obj.__dict__



class WL_Az_http_func_handler():

    def __init__(self, proj_root_path, http_request, function_context):
        ''' Instanciate a AZ Function handler object

        Args:
            proj_root_path (str): the root folder for the function where it is being run from
            http_request (azure function HttpRequest): the request data involved in the function call
            function_context (azure function HttpContext): the request context of the function call
            
        Returns:
            n/a
        '''
        func_name = function_context.function_name
        self.env = WLAzAppEnv.WLAzAppEnv(proj_root_path, func_name)

        self.funcdef_well_formed = False
        self.response_status = 500
        self.response_wrapper = {}

        if self.env:
            self.env.clear_app_log_messages()

            self.request_params, self.request_file = _proccess_request_inputs(http_request)

            if len(self.request_params):
                self.func_def = self.request_params.get('FuncDef')
                if self.func_def and len(self.func_def.split('.')) == 4:
                    f_parts =  self.func_def.split('.')
                    self.func_lib = f_parts[0]
                    self.func_classes = f_parts[1]
                    self.func_class = f_parts[2]
                    self.func_method = f_parts[3]
                    self.funcdef_well_formed = True

                if self.funcdef_well_formed: 
                    self.response_mode = self.request_params.get('ResponseMode')
                    self.response_wrapper['Handler'] = 'WL_Az_http_func_handler'    
                    self.response_wrapper['Function'] = self.func_def
                    self.response_wrapper['ResponseMode'] = self.response_mode

                    if self.request_file:
                        self.response_wrapper['FileUpload'] = True
                        self.response_wrapper['FileSize'] = len(self.request_file)
                    
                    self.exec_response = {}

                    self.request_method_args = {}
                    for key in self.request_params:
                        if key != 'FuncDef' and key != 'ResponseMode' and key != 'code':
                            self.request_method_args[key] = self.request_params.get(key)

                    readable_method_args = {}
                    for key in self.request_method_args:
                        val = self.request_method_args.get(key)
                        if not isinstance(val,bytes):
                            if sys.getsizeof(val) < 300:
                                readable_method_args[key] = val
                            else:
                                readable_method_args[key] = 'Long variables not included.'
                        else:
                            readable_method_args[key] = 'File binary contents not included.'

                    self.response_wrapper['FuncArgs'] = readable_method_args
                    self.env.log_message('FuncArgs: '+ json.dumps(readable_method_args))
                else:
                    mess = f'Function definition [{self.func_def}] was empty or malformed. Should be [Library_directory.Library_file.Class.Method].'
                    self.env.log_message('Error: '+ mess)
                    self.response_wrapper = {'Status':'Error','Message':mess}
                    self.response_mode = 'application/json'
                    self.response_status = 500
            else:
                mess = f'Failed to handle Function request - the request parameters are incorrectly formed.'
                self.env.log_message('Error: '+ mess)                
                self.response_wrapper = {'Status':'Error','Message':mess}
                self.response_mode = 'application/json'
                self.response_status = 500                
        else:
            mess = f'Failed to create instance of Function Handler Environment object.'
            self.env.log_message('Error: '+ mess)
            self.response_wrapper = {'Status':'Error','Message':mess}
            self.response_mode = 'application/json'
            self.response_status = 500
        return

    def exec_request(self):
        ''' Execute the Azure Function requested

        Args:
            n/a
            
        Returns:
            response_str (str): a json string containing the function response
        '''
        if self.funcdef_well_formed:
            str_func = f'from wllib2.{self.func_lib} import {self.func_classes}'
            str_func += f'\nreload({self.func_classes})'
            str_func += f'\nfunc_obj = {self.func_classes}.{self.func_class}(self.env,self.request_method_args,self.request_file)'
            str_func += f'\nself.exec_response = func_obj.{self.func_method}()'
            self.env.log_message(str_func)
            
            try:
                exec(str_func)
                self.response_status = 200
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                line_number = exc_traceback.tb_lineno
                traceback.clear_frames(exc_traceback)
                em = exc_type(exc_value).with_traceback(exc_traceback)

                str_err_mess = f'Function definition [{self.func_def}] could not be found or executed. '
                
                if self.env.get_env_name() != 'PROD':
                    str_err_mess += f'Error of type {exc_type} on line number {line_number} : message = [{em}]'
                    str_err_mess += f'Env log : {self.env.get_log_messages()}'

                self.env.log_message('Error: '+ str_err_mess)
                self.exec_response = {'Status':'Error','Message':str_err_mess}
                self.response_status = 500

            if self.response_mode == 'HTML':
                self.response_wrapper['ResponseData'] = self.exec_response
                html_response_list = []
                _dict_to_html(html_response_list, self.response_wrapper)
                response_str ='\n'.join(html_response_list)
            else:
                self.response_wrapper['ResponseData'] = self.exec_response
                response_str = json.dumps(self.response_wrapper, default=_json_serialize)
        else:
            response_str = json.dumps(self.response_wrapper)

        return response_str

    def response_mime_type(self):
        ''' Get the mime-type for the most recent call of exec_request()

        Args:
            n/a
            
        Returns:
            mime_type (str): the mime-type string for the most recent call of exec_request()
        '''
        if self.response_mode == 'HTML':
            mime_type = 'text/html'
        else:
            mime_type = 'application/json'
        return mime_type
    
    def get_response_status(self):
        ''' Get the status for the most recent call of exec_request()

        Args:
            n/a
            
        Returns:
            mime_type (int): the status number (200=ok, 500=fail) for the most recent call of exec_request()
        '''
        return self.response_status

    def get_request_params(self):
        ''' Get the request parameters (non-structural)

        Args:
            n/a
            
        Returns:
            request_params (dict): the request parameters passed to the function
        '''      
        return self.request_params

    def get_request_file(self):
        ''' Get the request file (if there is one)

        Args:
            n/a
            
        Returns:
            request_file (bytes): the request file passed to the function
        '''      
        return self.request_file

    def get_env(self):
        ''' Get the request environment object

        Args:
            n/a
            
        Returns:
            env (WLAzAppEnv(object)): the environment object created when this handler object was instanciated
        '''      
        return self.env