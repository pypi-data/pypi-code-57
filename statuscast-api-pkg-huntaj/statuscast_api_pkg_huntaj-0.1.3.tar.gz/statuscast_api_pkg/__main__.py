import os, sys, requests,configparser
from . import driver

def main():
    # If you want use to be command-line driven, force arguments endpoint and method to be passed.
    # Otherwise, set endpoint, method and data in this script and then pass to route().

    # args are imported from __init__
    # Force endpoint and method arguments to be passed.
    if not (driver.args.endpoint and driver.args.method):
        print("At least one statuscast API endpoint and corresponding method is required. Use python status_cofc_edu -h for help with arguments.")
        sys.exit(1)
    else:
        endpoint = driver.args.endpoint[0]
        method = driver.args.method[0]
        data = None
        if method.lower() == "get" and driver.args.queryargs:
            data = driver.args.queryargs[0]
        elif method.lower() == "post" and driver.args.payload:
            data = driver.args.payload[0]

        endpoint = "{}{}".format(driver.base_url,endpoint)
        driver.route(endpoint,method,data)

if __name__ == "__main__":
    main()