import os, sys, requests,argparse,configparser
from .util import * 
from . import *

if __name__ == "__main__": 
    main()
def main():
    parser = argparse.ArgumentParser(description="Process arguments for status_cofc_edu job execution")
    # Parse the arguments, turn them into variables
    # Endpoint argument, one value -> nargs=? 
    parser.add_argument('endpoint', metavar='e', type=str, nargs='?',
                    help='an endpoint to hit, e.g. {}<endpoint>'.format(base_url))
    parser.add_argument('method', metavar='m', type=str, nargs='?',
                    help='HTTP Method to use (GET, POST, PUT, or DELETE)')
    parser.add_argument('payload', metavar='p', type=str, nargs='+',
                    help='data payload formatted as \'{"key1":"value1","key2":"value2"}\'')
    parser.add_argument('queryargs', metavar='q', type=str, nargs='+',
                    help='Comma-separated list of query args formatted as q1=A,q2=B,q3=C...')

    args = parser.parse_args()
    if not (args.endpoint and args.method): 
        print("At least one statuscast API endpoint and corresponding method is required. Use python status_cofc_edu -h for help with arguments.")
        sys.exit(1)
    else:
        e = "{}{}".format(base_url,args.endpoint,data)
        hit_endpoint(e,args.method)
