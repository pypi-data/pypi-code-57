#!/usr/bin/env python3

import requests
import json
import base64

import logging

import sys, getopt

#from . import __version__

#from requests_oauthlib import OAuth2Session
#from requests.auth import HTTPBasicAuth
#from oauthlib.oauth2 import BackendApplicationClient

from inforion.ionapi.basic import load_config,login,header
from inforion.ionapi.MMS import AddItmBasic,MMS021

def main():
    print ('Main')
    method =''
    argv = sys.argv[1:]
    print (argv)
    help_string = "Usage:\n./%s -u URL -f IONFile -m method"
    try:
        opts, args = getopt.getopt(argv, "h:u:f:m:i:o:", ["url", "ionfile","method","inputfile","outputfile"])

    except getopt.GetoptError:
        print (help_string)
        sys.exit(2)

    for opt, arg in opts:

        if arg == ("-h", "help"):
            print (help_string)
            return help_string
            sys.exit(2)
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-f", "--ionfile"):
            ionfile = arg
        elif opt in ("-m", "--method"):
            method = arg   
        elif opt in ("-i", "--inputfile"):
            inputfile = arg 
        elif opt in ("-o", "--outputfile"):
            outputfile = arg 

    if method == "checklogin":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
          
        if "Bearer" in headers['Authorization']:
            return "InforION Login is working"
    elif method == "MMS200MI":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return AddItmBasic(url,headers,inputfile,'out.xslx')
    elif method == "MMS021":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return MMS021(url,headers,inputfile,'out.xslx')
    else:
        return ('Sorry you need to define a method plese use inforion -h')

if __name__ == "__main__":
    #sys.exit(run("-h"))
    main()

