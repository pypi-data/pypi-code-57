"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

Sigilent DMM Integration with SmartFabric

Description: 
    This script demonstrates how
    to integrate an SDM3045X DMM from Sigilent
    to measure output voltage offset of the 
    SmartFabric LDO at different output voltages.
    Replace DEV_SN and DEV_VNP_ID according to 
    the FTDI device connected to your PC.
"""

import random
import statistics
import os, sys, time
import pyvisa as visa

from chipbuilder.smartfabric.exceptions import FTDIError
import chipbuilder.smartfabric as sf


DEV_VNP_ID = 0x4036014
DEV_SN     = "FT15J6Y4"
SF_LDO_VOUT_OFFSET = 0.01


# General VISA device
class generalDevice:
    def __init__(self):
        self.device = False
        self.isOpen = False

          
    def __del__(self):
        if self.isOpen:
            self.close()
            self.isOpen = False


    def close(self):
        if self.isOpen:
            self.device.close()
            self.isOpen = False


    def openDevice(self, toOpen, address=-1):
        self.rm = visa.ResourceManager()
        self.deviceAddresses = self.rm.list_resources()
        if address != -1:
            self.deviceAddress = address
            return self.rm.open_resource(address)
        else:
            for i in self.deviceAddresses:
                try:
                    self.dummy = self.rm.open_resource(i)
                    self.dummy.write('*IDN?')
                    time.sleep(.1)
                    self.name = self.dummy.read().split(',')[1]
                    self.dummy.close()

                    if ((self.name == 'SDM3045X') and (toOpen == 'dmm')):
                        self.deviceAddress = i
                        return self.rm.open_resource(i)

                except:
                    pass

            print("opening " + toOpen + " failed")


    # generic get ID from VISA device function            
    def getID(self):
        if (self.device):
            self.device.write('*IDN?')
            time.sleep(.25)
            return self.device.read()
        else:
            return 'device not found'



# DMM
class dmm(generalDevice):

    def __init__(self, address=-1):
        self.isOpen = False
        self.device = self.openDevice('dmm',address)

        if self.device:
            print("Opening dmm.")
            self.isOpen = True


    # set the dmm to trigger immediately
    def setTrigImmediate(self, samples):
        scpiStr = 'TRIG:SOUR IMM'
        self.device.write(scpiStr)
        scpiStr = 'TRIG:COUN ' + str(samples)
        self.device.write(scpiStr)
        scpiStr = 'INIT'
        self.device.write(scpiStr)


    # set DMM to take a single measurement
    def setTrigSingle(self):
        self.setTrigImmediate(1)


    # read a dc voltage from the dmm
    def readV(self):
        scpiStr = 'CONF:VOLT:DC'
        self.device.write(scpiStr)
        self.setTrigSingle()
        time.sleep(.25)
        scpiStr = 'READ?'

        return float(self.device.query(scpiStr).strip())


    # read a dc current from the DMM
    def readI(self):
        scpiStr = 'CONF:CURR:DC'
        self.device.write(scpiStr)
        self.setTrigSingle()
        time.sleep(.25)
        scpiStr = 'READ?'
        measuredI = float(self.device.query(scpiStr).strip())
        self.device.write('CONF:CURR:DC 60')

        return measuredI



class pseudo_dmm():
    """
    DMM Emulator to test script without
    physical equipment.
    """

    def __init__(self, errMaxPercent):

        self.voutRegPercent = errMaxPercent
        self.open()


    def open(self):
        print("Opening DMM.")


    def set_vout(self, voutExp):
        self.vout = voutExp


    def read_vout(self):
        maxErr = self.voutRegPercent*self.vout
        return random.uniform(self.vout - maxErr, self.vout + maxErr)


    def close(self):
        print("Closing DMM.")



def main():

    if len(sys.argv) < 2:
        print("Missing arguments")
        print("usage> python sf_program_compare.py <ldoID>")
        exit()

    ldoID = int(sys.argv[1])
    sfabric = sf.SmartFabric()
    devDict = sfabric.get_devs()
    sfabric.print_dev_info(devDict)

    try:
        ftDevId = sfabric.select_device(sn = DEV_SN, vnpId = DEV_VNP_ID)

    except FTDIError:
        exit("No FTDI device matched vnpId:0x%x, SN:%s!" % (DEV_VNP_ID, DEV_SN))

    print("DevID %d: Matched vnpId=0x%x, SN=%s!" % (ftDevId, DEV_VNP_ID, DEV_SN))
    sfabric.open()

    # Initialize the DMM resource
    # Uncomment Equipment emulator lines to test without equipment
    sdm3045x = dmm() # Physical equipment
    # sdm3045x = pseudo_dmm(SF_LDO_VOUT_OFFSET) # Equipment emulator
    print("Sigilent DMM connected.")
    deltaVoutList = []

    for vout in range(13, 29):
        # Test Vout = 1.8V - 3.3V
        voutExpected = sfabric.pmic_ldo_vout_set(ldoID, vout)
        # sdm3045x.set_vout(voutExpected) # Equipment emulator

        for meas in range(0, 32):
            # Measure Vout 32 times per voltage
            voutMeasured = sdm3045x.readV()
            # voutMeasured = sdm3045x.read_vout() # Equipment emulator
            # Measuring delta in % to normalize
            curDelta = (voutExpected - voutMeasured) / voutExpected
            deltaVoutList.append(curDelta)

    print("LDO%d Output Offset Summary:" % ldoID)
    print("Vout_offset_max   = {:0.2f}%".format(100 * max(deltaVoutList)))
    print("Vout_offset_avg   = {:0.2f}%".format(100 * statistics.mean(deltaVoutList)))
    print("Vout_offset_min   = {:0.2f}%".format(100 * min(deltaVoutList)))
    print("Vout_offset_stdev = {:0.2f}%".format(100 * statistics.stdev(deltaVoutList)))

    sdm3045x.close()
    sfabric.close()


if __name__ == '__main__':
    main()