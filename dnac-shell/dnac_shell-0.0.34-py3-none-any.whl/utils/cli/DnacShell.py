from dnac.utils.cli.CliSession import CliSession
from dnac.DnacCluster import DnacCluster
import requests


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

def main():
    clis = CliSession()
    clis.start()


if __name__ == "__main__":
    main()

         
