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
from inforion.ionapi.MMS import AddItmBasic,MMS021,MMS021bulk,MMS021bulk2,CRS610bulk,CRS610,CRS610bulk2,bulk

from inforion.helper.urlsplit import spliturl
def main():
    print ('Main')
    method =''
    argv = sys.argv[1:]
    print (argv)
    help_string = "Usage:\n./%s -u URL -f IONFile -m method"
    try:
        opts, args = getopt.getopt(argv, "h:u:f:p:m:i:o:s:e:", ["url", "ionfile","program""method","inputfile","outputfile","start","end"])

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
        elif opt in ("-p", "--program"):
            program = arg   
        elif opt in ("-i", "--inputfile"):
            inputfile = arg 
        elif opt in ("-o", "--outputfile"):
            outputfile = arg 
        elif opt in ("-s", "--start"):
            start = int(arg)
        elif opt in ("-e", "--end"):
            end = int(arg)
   
    result = spliturl(url)

    if "Call" in result:
        if len(result["Call"]) > 0:
            if result["Call"] == "execute":

                config = load_config(ionfile)
                token=login(url,config)
                
                headers = header(config,token)
                if "Bearer"  not in headers['Authorization']:
                    return "InforION Login is not working"
                #return CRS610bulk(url,headers,inputfile,'CRS610MI',outputfile,start,end)
                return bulk(url,headers,program,method,inputfile,outputfile,start,end)  

    if method == "checklogin":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
          
        if "Bearer" in headers['Authorization']:
            return "InforION Login is working"
    
    
    '''
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
    elif method == "MMS021bulk":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return MMS021bulk(url,headers,inputfile,'out.xslx')
    elif method == "MMS021bulk2":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return MMS021bulk2(url,headers,inputfile,'out.xslx')
    elif method == "CRS610bulk":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return CRS610bulk(url,headers,inputfile,'CRS610MI',outputfile,start,end)
    elif method == "CRS610bulk2":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return CRS610bulk2(url,headers,inputfile,'CRS610MI',outputfile)
    elif method == "CRS610":
        config = load_config(ionfile)
        token=login(url,config)
        headers = header(config,token)
        return CRS610(url,headers,inputfile,'out.xslx')
    
    else:
        return ('Sorry you need to define a method plese use inforion -h')
    '''

if __name__ == "__main__":
    #sys.exit(run("-h"))
    main()

