"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

SmartFabric functions for PMIC configuration
"""

import time
from chipbuilder.smartfabric.util import FAIL, SUCCESS
from chipbuilder.smartfabric.host import SF_Host
from chipbuilder.smartfabric.util import IS_CLI_CMD, OPEN_HOST_ATTR



class SF_PMIC(SF_Host):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def power_off(self):
        """
        Power off SmartFabric TileGrid over TTM. Note that this
        function does not power off the Smart Fabric controller.
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_pwr_off()

        return ret


    def power_on(self):
        """
        Power on SmartFabric over TTM. Note that this
        function does not affect the Smart Fabric controller.
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_pwr_on()

        return ret


    def power_cycle(self):
        """
        Power cycle the SmartFabric over TTM. Note that this
        function does not power cycle the Smart Fabric controller.
        This function is supported on the CLI script.

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_pwr_off()
        time.sleep(0.5)
        ret |= self._zip_pwr_on()

        return ret


    def pmic_boost(self, vout: int, bypMode:int, ilim:int):
        """
        Configure ZIP's BOOST regulator. This function is supported on the CLI script.

        Args:
            vout (int): BOOST output voltage (0=2.5V - 15=4.5V).
            bypMode (int): Bypass mode for BOOST (1=force bypass, 2=auto bypass).
            ilim (int): Set current limit (0=300mA, 1=200mA, 2=500mA, 3=400mA).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_write_boost_config(vout, bypMode, ilim)

        return ret


    def pmic_sysldo(self, vout:int, bypMode:int, ilim:int):
        """
        Configure ZIP's SYSLDO regulator. This function is supported on the CLI script.

        Args:
            vout (int): SYSLDO output voltage (0=0.5V - 31=3.6V).
            bypMode (int): Bypass SYSLDO (1=bypass).
            ilim (int): Enable current limit (1=ilim enabled).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_write_sysldo_config(vout, bypMode, ilim)

        return ret


    def pmic_ldo_enable(self, bitMask:int):
        """
        Enable ZIP's LDOs from bitmask. The bitmask argument is a three bit integer 
        in which each LDO is assigned a bit position. A 1b'1 will enable the LDO from
        that respective position. This function is supported on the CLI script.

        ========== ========
         bitField   bitPos
        ========== ========
         LDO3       2
         LDO2       1
         LDO1       0
        ========== ========

        e.g.::

            bitMask = 2 = 3b'010 = LDO2;
            bitMask = 3 = 3b'011 = LDO2 & LDO1;

        Args:
            bitMask (int): Bit mask representing which of the LDO's to enable (bit0=LDO1, bit1=LDO2, bit2=LDO3).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """ 

        ret = self._zip_enable_ldo(bitMask)

        return ret


    def pmic_ldo_disable(self, bitMask:int):
        """
        Disable ZIP's LDOs from bitmask. The bitmask argument is a three bit integer 
        in which each LDO is assigned a bit position. A 1b'1 will disable the LDO from
        that respective position. This function is supported on the CLI script.

        ========== ========
         bitField   bitPos
        ========== ========
         LDO3       2
         LDO2       1
         LDO1       0
        ========== ========

        e.g.::

            bitMask = 2 = 3b'010 = LDO2;
            bitMask = 3 = 3b'011 = LDO2 & LDO1;

        Args:
            bitMask (int): Bit mask representing which of the LDO's to disable (bit0=LDO1, bit1=LDO2, bit2=LDO3).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_disable_ldo(bitMask)

        return ret


    def pmic_ldo_config(self, ldoId:int, bypMode:int, ilim:int):
        """
        Configure ZIP's LDOx. This function is supported on the CLI script.

        Args:
            ldoId (int): LDOx index (LDO1=1, LDO2=2, LDO3=3).
            bypMode (int): Bypass LDOx (1=bypass).
            ilim (int): Enable current limit (1=ilim enabled).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_write_ldo_config(ldoId, bypMode, ilim)

        return ret


    def pmic_ldo_vout_get(self, ldoId:int):
        """
        Get ZIP's LDOx output voltage. This function is supported on the CLI script.

        Args:
            ldoId (int): LDOx index (LDO1=1, LDO2=2, LDO3=3).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        vout = self._zip_read_ldo_vout(ldoId)
        print("LDO%d vout: %0.1fV" % (ldoId, vout))

        return vout


    def pmic_ldo_vout_set(self, ldoId:int, vout:int):
        """
        Set ZIP's LDOx output voltage. This function is supported on the CLI script.

        Args:
            ldoId (int): LDOx index (LDO1=1, LDO2=2, LDO3=3).
            vout (int): LDOx output voltage (0=0.5V - 31=3.6V).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_write_ldo_vout(ldoId, vout)
        vout = self.pmic_ldo_vout_get(ldoId)

        if ret == SUCCESS:
            return vout
        else:
            return FAIL


    setattr(power_off, IS_CLI_CMD, True)
    setattr(power_on, IS_CLI_CMD, True)
    setattr(power_cycle, IS_CLI_CMD, True)
    setattr(pmic_boost, IS_CLI_CMD, True)
    setattr(pmic_sysldo, IS_CLI_CMD, True)
    setattr(pmic_ldo_enable, IS_CLI_CMD, True)
    setattr(pmic_ldo_disable, IS_CLI_CMD, True)
    setattr(pmic_ldo_config, IS_CLI_CMD, True)
    setattr(pmic_ldo_vout_get, IS_CLI_CMD, True)
    setattr(pmic_ldo_vout_set, IS_CLI_CMD, True)

    setattr(power_off, OPEN_HOST_ATTR, True)
    setattr(power_on, OPEN_HOST_ATTR, True)
    setattr(power_cycle, OPEN_HOST_ATTR, True)
    setattr(pmic_boost, OPEN_HOST_ATTR, True)
    setattr(pmic_sysldo, OPEN_HOST_ATTR, True)
    setattr(pmic_ldo_enable, OPEN_HOST_ATTR, True)
    setattr(pmic_ldo_disable, OPEN_HOST_ATTR, True)
    setattr(pmic_ldo_config, OPEN_HOST_ATTR, True)
    setattr(pmic_ldo_vout_get, OPEN_HOST_ATTR, True)
    setattr(pmic_ldo_vout_set, OPEN_HOST_ATTR, True)

