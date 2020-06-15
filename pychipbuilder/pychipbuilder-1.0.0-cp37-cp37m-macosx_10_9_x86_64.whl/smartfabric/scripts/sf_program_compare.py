"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

PyChipBuilder Program/Compare Script

Description:
    Program and compare a given routing file to the
    Smart Fabric register space. The differences will
    be stored on the provided <logFile>. Replace DEV_SN
    and DEV_VNP_ID according to the FTDI device connected
    to your PC.
"""

import sys
from chipbuilder.smartfabric.exceptions import FTDIError
import chipbuilder.smartfabric as sf


DEV_VNP_ID = 0x4036014
DEV_SN     = "FT15J6Y4"


def main():

    if len(sys.argv) < 2:
        print("Missing arguments")
        print("usage> python sf_program_compare.py <routeFile> <logFile>")
        exit()

    routeFile = sys.argv[1]

    try:
        logFile = sys.argv[2]

    except IndexError:
        logFile = None

    sfabric = sf.SmartFabric()
    devDict = sfabric.get_devs()
    sfabric.print_dev_info(devDict)

    try:
        ftDevId = sfabric.select_device(sn = DEV_SN, vnpId = DEV_VNP_ID)

    except FTDIError:
        print("No FTDI device matched vnpId:0x%x, SN:%s!" % (DEV_VNP_ID, DEV_SN))
        exit()

    print("DevID %d: Matched vnpId=0x%x, SN=%s!" % (ftDevId, DEV_VNP_ID, DEV_SN))
    sfabric.open()
    
    sfabric.reg_program(routeFile)

    if logFile:
        diffs = sfabric.reg_compare(routeFile, logFile)
        print("Differences are found in: %s" % logFile)

    else:
        diffs = sfabric.reg_compare(routeFile)
        print("Differences are found in: %s" % sf.tgrid.COMPARE_TG_FINAME)

    sfabric.close()

    return diffs


if __name__ == '__main__':
    main()