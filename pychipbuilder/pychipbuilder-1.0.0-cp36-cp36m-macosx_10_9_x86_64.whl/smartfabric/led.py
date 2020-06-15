"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

SmartFabric functions for LED configuration
"""

from chipbuilder.smartfabric.host import SF_Host
from chipbuilder.smartfabric.util import IS_CLI_CMD, OPEN_HOST_ATTR



class SF_LED(SF_Host):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def led_enable(self, bitMask:int):
        """
        Enable ZIP's LED current sinks. The bitmask argument is a three bit integer 
        in which each LED is assigned a bit position. A 1b'1 will enable the LED from
        that respective position. This function is supported on the CLI script.

        ========== ========
         bitField   bitPos
        ========== ========
         LED3       2
         LED2       1
         LED1       0
        ========== ========

        e.g.::

            bitMask = 2 = 3b'010 = LED2;
            bitMask = 3 = 3b'011 = LED2 & LED1;

        Args:
            bitMask (int): Bit mask representing which of the LED's to turn on (bit0=LED1, bit1=LED2, bit2=LED3).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_enable_led(bitMask)

        return ret


    def led_disable(self, bitMask:int):
        """
        Disable ZIP's LED current sinks. The bitmask argument is a three bit integer 
        in which each LED is assigned a bit position. A 1b'1 will disable the LED from
        that respective position. This function is supported on the CLI script.

        ========== ========
         bitField   bitPos
        ========== ========
         LED3       2
         LED2       1
         LED1       0
        ========== ========

        e.g.::

            bitMask = 2 = 3b'010 = LED2;
            bitMask = 3 = 3b'011 = LED2 & LED1;

        Args:
            bitMask (int): Bit mask representing which of the LED's to turn off (bit0=LED1, bit1=LED2, bit2=LED3).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_disable_led(bitMask)

        return ret


    def led_config(self, ledId:int, dutyCycle:int, period:int, irange:int, bright:int, invert:int):
        """
        Configure ZIP's LED current sinks. This function is supported on the CLI script.

        Args:
            ledId (int): Index of LED current sink (LED1=1, LED2=2, LED3=3).
            dutyCycle (int): Percent of period to remain active (0=6.25% - 15=100%).
            period (int): Time in seconds for a complete PWM period (0=0.5s - 15=8s).
            irange (int): Current range for brightness parameter (0=OFF - 3=0.4mA-12.8mA).
            bright (int): Current sink selection for LED brightness (0=OFF - 31=irangeMax).
            invert (int): Invert PWM cycle (0=active high, 1=active low).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_write_led_config(ledId, dutyCycle, period, irange, bright, invert)

        return ret


    def led_configdef(self, ledId:int):
        """
        Configure ZIP's LED current sinks with default parameter values.
        This function is supported on the CLI script.

        Args:
            ledId (int): Index of LED current sink (LED1=1, LED2=2, LED3=3).

        Returns:
            int. A status code::

                0 = Success
                1 = Invalid handle
                2 = Device not found
                3 = Device not opened
        """

        ret = self._zip_write_led_config(ledId)

        return ret


    setattr(led_enable, IS_CLI_CMD, True)
    setattr(led_disable, IS_CLI_CMD, True)
    setattr(led_config, IS_CLI_CMD, True)
    setattr(led_configdef, IS_CLI_CMD, True)

    setattr(led_enable, OPEN_HOST_ATTR, True)
    setattr(led_disable, OPEN_HOST_ATTR, True)
    setattr(led_config, OPEN_HOST_ATTR, True)
    setattr(led_configdef, OPEN_HOST_ATTR, True)

