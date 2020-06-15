"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

SmartFabric functions for OTP configuration
"""

from chipbuilder.smartfabric.host import SF_Host
from chipbuilder.smartfabric.util import log_performance
from chipbuilder.smartfabric.util import IS_CLI_CMD, OPEN_HOST_ATTR


SCAN_OTP_FI_NAME    = 'otp_scan.log'

# OTP signature status
SIG_VALID     = 0
SIG_EMPTY     = 1
SIG_INVALID   = 2
SIG_CORRUPTED = 3


class SF_OTP(SF_Host):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def otp_sigcheck(self):
        """
        Test OTP Boot Signature. Use this command to confirm
        that the OTP signature is valid.

        Returns:
            int. OTP signature status::

                0 - OTP SIG Valid
                1 - OTP SIG Empty
                2 - OTP SIG Invalid
                3 - OTP SIG Corrupted
        """

        ret = self._zip_test_otpsig()
        print("OTP Sig Status: %s" % ret)

        return ret


    def otp_blankcheck(self, addr:int = 0):
        """
        Blankcheck OTP memory. Use this command to confirm
        that the OTP memory is initialized to all 8h'00.

        Returns:
            int. OTP blankcheck result::

                0 - Blankcheck passed
                1 - Blankcheck failed
        """

        ret = self._zip_test_otpblankcheck(addr)
        print("OTP Blankcheck result: %s" % ret)

        return ret



    @log_performance
    def otp_scan(self, oFiName:str = None, isRegFormat:int = 0):
        """
        Scan zGlue's ZIP OTP memory space until next available address.
        The data will be saved in the file specified by oFiName.
        If ``None`` is passed, the file ``otp_scan.log`` will be saved in the current working directory.
        This function is supported on the CLI script.

        Args:
            oFiName (str, optional): File name to save OTP scan.
            isRegFormat (int, optional): Format OTP scan as "0xRegAddr,0xRegData"; otherwise, save as "addr:0xOTPaddr,data:0xOTPdata".

        Returns:
            int. The next available OTP address.
        """

        ret = self._zip_scan_otp()

        if oFiName == None:
            oFiName = SCAN_OTP_FI_NAME

        print("Next available OTP address: 0x%04x" % self.nxtOtpAddr)
        ret |= self._zip_save_otp_scan(oFiName=oFiName, isRegFormat=isRegFormat)
        print("OTP scan saved")
                
        return self.nxtOtpAddr


    @log_performance
    def otp_program(self, rFiName:str, pgmZeros:int = 0):
        """
        Program a specified routing file into zGlue's ZIP OTP.
        This command should only be used if the OTP is empty. After intitial
        programming, otp_patch should be used instead.
        This function is supported on the CLI script.

        Args:
            rFiName (str): File name of routing file to program in OTP.
                To download a routing file for your specific ZIP, 
                click ``Menu > Outputs > Routing`` on that system's ChipBuilder page.
            pgmZeros (int, optional): Program entries that clear registers. 
                A '1' programs the cleared registers. They're skipped otherwise.

        Returns:
            list. List of the OTP address values that were just programmed.
        """

        numBytes = self._zip_program_otp(rFiName=rFiName, otpAddr=0, isPatch=0, pgmZeros=pgmZeros)
        print("%d bytes written to OTP." % numBytes)
        self.idle()
        mmdrVal = numBytes
        rdAddr = self.nxtOtpAddr - numBytes + 6

        # try:
        #     mmdrVal = self._zip_read_otp(rdAddr, numBytes)

        #     for idx, val in enumerate(mmdrVal):
        #         curAddr = rdAddr + 2*idx
        #         print("addr:0x%04x,mmdr:%04x" % (curAddr, val))
        
        # except AttributeError:
        #    pass

        return mmdrVal


    @log_performance
    def otp_patch(self, rFiName:str, stAddr:int = 0, pgmZeros:int = 0):
        """
        Patch a ZIP's OTP with a specified routing file.
        Command scans OTP space until a DONE or empty OTP entry is found, and appends
        the routing file's programming to the next available OTP address.
        To bypass the scan, specify a starting OTP address.
        This function is supported on the CLI script.

        Args:
            rFiName (str): File name of routing file to patch in OTP.
                To download a routing file for your specific ZIP, 
                click ``Menu > Outputs > Routing`` on that system's ChipBuilder page.
            stAddr (int, optional): Start OTP address for programming. OTP scan is bypassed if stAddr != 0.
            pgmZeros (int, optional): Program entries that clear registers.
                A ‘1’ programs the cleared registers. They’re skipped otherwise.

        Returns:
            list. List of the OTP address values that were just programmed.
        """

        numBytes = self._zip_program_otp(rFiName=rFiName, otpAddr=stAddr, isPatch=1, pgmZeros=pgmZeros)
        print("%d bytes written to OTP." % numBytes)
        self.idle()
        mmdrVal = numBytes
        rdAddr = self.nxtOtpAddr - numBytes + 6

        # try:
        #     mmdrVal = self._zip_read_otp(rdAddr, numBytes)

        #     for idx, val in enumerate(mmdrVal):
        #         curAddr = rdAddr + 2*idx
        #         print("addr:0x%04x,mmdr:%04x" % (curAddr, val))
        
        # except AttributeError:
        #    pass

        return mmdrVal


    setattr(otp_scan, IS_CLI_CMD, True)
    setattr(otp_program, IS_CLI_CMD, True)
    setattr(otp_patch, IS_CLI_CMD, True)
    setattr(otp_sigcheck, IS_CLI_CMD, True)
    setattr(otp_blankcheck, IS_CLI_CMD, True)

    setattr(otp_sigcheck, OPEN_HOST_ATTR, True)
    setattr(otp_blankcheck, OPEN_HOST_ATTR, True)
    setattr(otp_scan, OPEN_HOST_ATTR, True)
    setattr(otp_program, OPEN_HOST_ATTR, True)
    setattr(otp_patch, OPEN_HOST_ATTR, True)

