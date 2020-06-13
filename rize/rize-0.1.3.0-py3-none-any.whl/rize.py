import os
from os import listdir
from os.path import isfile, join
import simplejson
import shutil
import sys
import time
import subprocess

# -----------------------------------. getPath --------------------------------
def getPath(variable_name):
    """
    Get system variable path

    Parameters
    ----------

    variable_name : string
        Name of the variable

    Returns:
    ----------
    
    path: string
        Path of the system varaible
    """
    path = os.environ[variable_name]
    print ("System variable <" + variable_name + "> with path: " +  path)
    return path

# -----------------------------------. setPath --------------------------------
def setPath(new_path, variable_name):
    """
    Set system variable path

    Parameters
    ----------

    new_path : string
        Path of the new folder of the variable

    variable_name : string
        Name of the system variable
    """
    if os.environ.get('OS','') == 'Windows_NT':
        from subprocess import Popen
        from subprocess import CREATE_NEW_CONSOLE
        command = 'setx ' + variable_name + ' "' + new_path + "/" + '"'
        Popen(command, creationflags=CREATE_NEW_CONSOLE)
    os.environ[variable_name] = new_path


# -----------------------------------. createFolder --------------------------------
# Create a new folder
def createFolder(path, name_folder):
    """
    Create a new folder

    Parameters
    ----------

    path : string
        Path of the folder

    name_folder : string
        Name of the folder
    """
    if not os.path.exists(path + "/" + name_folder):
        os.makedirs(path + "/" + name_folder)



# -----------------------------------. saveJSON --------------------------------
# Save JSON file
def saveJSON(path, name, json_code):
    """
    Save JSON file

    Parameters
    ----------

    path : string
        Path of the folder

    name : string
        Name of the file without .json (non extension)

    json_code : dictionary
        Json in a dictionary format

    """

    file_save = open(path +  "/" +  name + ".json" , "w")
    file_save.write(simplejson.dumps(json_code, separators=(',', ':'), sort_keys=True,  indent=4))
    file_save.close()

# -----------------------------------. saveFile --------------------------------
# Save txt file
def saveFile(path, name, code):
    """
    Save file

    Parameters
    ----------

    path : string
        Path of the folder

    name : string
        Name of the file + extension

    code : string
        Text to save

    """

    file_save = open(path +  "/" +  name , "w")
    file_save.write(code.encode('utf8'))
    file_save.close()


        
# -------------------------------------  json2dict  --------------------------------
def json2dict(s, **kwargs):
    """ Convert JSON to python dictionary
     
        Parameters
        ----------
        s: string
            string with the content of the json data

        Returns:
        ----------
        dict: dictionary
            dictionary with the content of the json data
    """

    import sys
    if sys.version_info[0] == 3:
        return simplejson.loads(s, **kwargs)

    else:
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
    
    return simplejson.loads(s, **kwargs)

# -------------------------------------  dict2json  -------------------------------
def dict2json(o, **kwargs ):
    """ Convert python dictionary to a JSON value 
     
        Parameters
        ----------
        o: dictionary
            dictionary to convert
            

        Returns:
        ----------
        d: string
            string in json format

    """
        
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
        
    s = simplejson.dumps(o, **kwargs)

    import sys
    if sys.version_info[0] == 3:
        if isinstance(s, str):
            s = s.encode('utf8')

    else:
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
    return s


# -------------------------------------  readJSON  -------------------------------
def readJSON(json_file):
    """ Read a json file and return an string 
        
        Parameters
        ----------
        json file:string
            Path +  name + extension of the json file

        Returns:
        ----------
        json_data: string
            string with the content of the json data

    """
    json_data = open (json_file).read()
    return json_data

# -------------------------------------  getFiles  -------------------------------
def getFiles(path):
    """ Get a list of files that are inside a folder
        
        Parameters
        ----------
        path: string
            path of the folder

        Returns:
        ----------
        onlyfiles: list 
            list of strings with the name of the files in the folder

    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print ("Available files:" +  str(onlyfiles))
    return onlyfiles


# ------------------------------------ seeIP -----------------------------------
def seeIP():
    """ Get current IP value

        Returns:
        ----------
        result: string 
            current IP value
    """

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    cw_ip = s.getsockname()[0]
    s.close()
    result = {'ip': str(cw_ip)}
    return result


