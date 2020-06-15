"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

PyChipBuilder Optimized OTP Programming Script

Description:
    This script optimizes OTP programming a ZIP by 
    validating the input file, minimizing required programming,
    and validating correct programming format. Replace DEV_VNP_ID and
    DEV_SN according to the FTDI device connected to your PC.
"""

import os, sys
import ntpath
import chipbuilder.smartfabric.otp as otp
from chipbuilder.smartfabric.exceptions import FTDIError
import chipbuilder.smartfabric as sf


DEV_VNP_ID = 0x4036014
DEV_SN     = "FT15J6Y4"


def close_and_exit(sfInst, msg):

    sfInst.close()
    exit(msg)


def create_route_diff(sfInst, rFiName):

    # Create diff file name
    fiPath = os.path.dirname(rFiName)
    fiName = ntpath.basename(rFiName).split(".")[0]

    # Compare routing
    difs = sfInst.reg_compare(rFiName)
    print(difs)

    # Create difference file
    regDiffs = []
    diffFiName = os.path.join(fiPath, fiName + "_diff.txt")

    for difReg in difs.keys():
        line = "0x%x,0x%x" % (difReg, difs[difReg]["expected"])
        regDiffs.append(line)

    difFi = open(diffFiName, "w")
    difFi.write("\n".join(regDiffs))
    difFi.close()

    return diffFiName


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
        exit("No FTDI device matched vnpId:0x%x, SN:%s!" % (DEV_VNP_ID, DEV_SN))

    print("DevID %d: Matched vnpId=0x%x, SN=%s!" % (ftDevId, DEV_VNP_ID, DEV_SN))
    sfabric.open()

    # Blank Check
    bchkFailed = sfabric.otp_blankcheck()

    if bchkFailed:
        # OTP memory not empty
        # Check OTP signature
        sigStat = sfabric.otp_sigcheck()

        if sigStat == otp.SIG_VALID:
            try:
                diffFile = create_route_diff(sfabric, routeFile)
                # Patch everything in diff file, including cleared registers
                sfabric.otp_patch(diffFile, pgmZeros=1)

            except Exception as e:
                # Catch all to guarantee close() runs
                close_and_exit(sfabric, e)
        else:
            close_and_exit(sfabric, "OTP signature invalid, empty or corrupted. Use debug build to fix OTP signature.")

    else:
        # OTP memory empty
        try:
            diffFile = create_route_diff(sfabric, routeFile)
            # Program everything in diff file, including cleared registers
            sfabric.otp_program(diffFile, pgmZeros=1)

        except Exception as e:
            # Catch all to guarantee close() runs
            close_and_exit(sfabric, e)

    # Delete temp file
    os.remove(diffFile)
    # Prompt user to power cycle
    pwrCycleIssued = input("Power cycled the board [y/n]: ")
    pwrCycleIssued = True if pwrCycleIssued.lower() == "y" else False

    if pwrCycleIssued:
        # Compare programming with original routing file
        if logFile:
            diffs = sfabric.reg_compare(routeFile, logFile)

        else:
            diffs = sfabric.reg_compare(routeFile)
    
    else:
        diffs = {}

    sfabric.close()

    return diffs


if __name__ == '__main__':
    main()