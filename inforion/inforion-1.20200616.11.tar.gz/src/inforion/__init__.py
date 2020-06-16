

import sys

#from inforion.ionapi.ionbasic import ionbasic

#from ionbasic import load_config


from inforion.ionapi.basic import load_config,login,header



import validators
import os.path



def main(url,IONFile,method=None):
        
    if validators.url(url) != True:
        return ("Error: URL is not valid")
    
    if os.path.exists(IONFile) == False:
        return ("Error: File does not exist")
    else:
        config = load_config(IONFile)

    if method == "checklogin":
        token=login(url,config)
        headers = header(config,token)
        return (headers['Authorization'])





