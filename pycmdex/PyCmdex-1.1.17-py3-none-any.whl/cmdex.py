"""
# ************************************************************
# File:     cmdex.py
# Version:  1.1.17 (24 Jun 2020)
# Author:   Asst.Prof.Dr.Santi Nuratch
#           Embedded Computing and Control Laboratory
#           ECC-Lab, INC, KMUTT, Thailand
# Update:   20:47:50, 24 Jun 2020
# ************************************************************
# 
# 
# Copyright 2020 Asst.Prof.Dr.Santi Nuratch
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
"""


"""
#************************************************************
#* File:    Cmdex.py                                        *
#* Author:  Asst.Prof.Dr.Santi Nuratch                      *
#*          Embedded Computing and Control Laboratory       *
#*          ECC-Lab, INC, KMUTT, Thailand                   *
#* Update:  27 May 2020                                     *
#************************************************************
"""

from PyCmdex.cmdex_mcu  import CmdexMcu
from PyCmdex.cmdex_core import CmdexCore

import sys

class Cmdex(CmdexMcu):
    """
    Cmdex class provides all APIs for the mcu-cmdex interfacing.
    """

    def __init__(self, port=None, baudrate=115200, **kwargs):
        """
        Opens communication port and performs the handshake openration.

            - port: port name, e.g., COM1, COM2,...
            - baudrate: UART baudrate (bits per second).
        """

        super().__init__(port, baudrate, **kwargs)


    def led_set(self, id, callback=None):
        """
        Turns the LED<id> ON.

            - id: LED Id (0, 1, 2, 3).
            - callback: Callback function executed when received response from MCU.
        """
        super().psw_get(id, callback)
        return self


    def led_clr(self, id, callback=None):
        """
        Turns the LED<id> OFF.

            - id: LED Id (0, 1, 2, 3).
            - callback: Callback function executed when received response from MCU.
        """
        super().led_clr(id, callback)
        return self


    def led_inv(self, id, callback=None):
        """
        Inverts status of the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - callback: Callback function executed when received response from MCU.
        """
        super().led_inv(id, callback)
        return self


    def led_wrt(self, id, status, callback=None):
        """
        Writes status (True/False) to the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - status: Boolean data, True is ON, False is OFF.
            - callback: Callback function executed when received response from MCU.
        """
        super().led_wrt(id, status, callback)
        return self


    def led_get(self, id, callback=None):
        """
        Reads status of the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - callback: Callback function executed when received response from MCU.
        """
        super().led_get(id, callback)
        return self


    def led_fls(self, id, interval, callback=None):
        """
        Flashes the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - interval: Time of LED-ON in milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().led_fls(id, interval, callback)
        return self


    def flash(self, id, interval, callback=None):
        """
        Flashes the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - interval: Time of LED-ON in milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().flash(id, interval, callback)
        return self


    def led_blk(self, id, delay, interval, callback=None):
        """
        Blinks the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - delay: Delay time before LED-ON in milliseconds.
            - interval: Time of LED-ON in milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().led_blk(id, delay, interval, callback)
        return self


    def blink(self, id, delay, interval, callback=None):
        """
        Blinks the LED<id>.

            - id: LED Id (0, 1, 2, 3).
            - delay: Delay time before LED-ON in milliseconds.
            - interval: Time of LED-ON in milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().blink(id, delay, interval, callback)
        return self


    def led_cps(self, id, delay, width, period, callback=None):
        """
        Controls the LED<id> with the continuous clock pulse.

            - id: LED Id (0, 1, 2, 3).
            - delay: Delay time before LED-ON in milliseconds.
            - period: Total time in a cycle.
            - interval: Time of LED-ON in milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().led_cps(id, delay, width, period, callback)
        return self


    def pulse(self, id, delay, width, period, callback=None):
        """
        Controls the LED<id> with the continuous clock pulse.

            - id: LED Id (0, 1, 2, 3).
            - delay: Delay time before LED-ON in milliseconds.
            - period: Total time in a cycle.
            - interval: Time of LED-ON in milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().pulse(id, delay, width, period, callback)
        return self


    def buzzer(self, interval, frequency=500, power=50, callback=None, **kwargs):
        """
        Generates beep sound.

            - interval: Beep interval in millisconds.
            - frequency: Bepp frequency in Hertz.
            - power: Beep power (%).
            - callback: Callback function executed when received response from MCU.
        """
        super().buzzer(interval, frequency, power, **kwargs)
        return self


    def buz(self, interval, frequency=500, power=50, callback=None, **kwargs):
        """
        Generates beep sound.

            - interval: Beep interval in millisconds.
            - frequency: Bepp frequency in Hertz.
            - power: Beep power (%).
            - callback: Callback function executed when received response from MCU.
        """
        super().buzzer(interval, frequency, power, **kwargs)
        return self


    def beep(self, interval, frequency=500, power=50, callback=None, **kwargs):
        """
        Generates beep sound.

            - interval: Beep interval in millisconds.
            - frequency: Bepp frequency in Hertz.
            - power: Beep power (%).
            - callback: Callback function executed when received response from MCU.
        """
        super().buzzer(interval, frequency, power, **kwargs)
        return self


    def adc_get(self, id, callback=None):
        """
        Reads 10-bit data of the ADC<id>.

            - id: ADC Id (0, 1, 2, 3).
            - callback: Callback function executed when received response from MCU.
        """
        super().adc_get(id, callback)
        return self


    def adc_auto_detection(self, id, threshold, interval, callback=None):
        """
        Configures the auto-detection behaviors of the ADC<id>.

            - id: ADC Id (0, 1, 2, 3).
            - threshold: Threahold value used as detection sensitivity.
            - interval: Detection interval in millisconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().adc_get(id, threshold, interval, callback)
        return self


    def psw_get(self, id, callback=None):
        """
        Reads status of the PSW<id>.

            - id: PSW Id (0, 1, 2, 3).
            - callback: Callback function executed when received response from MCU.
        """
        super().psw_get(id, callback)
        return self


    def pwm(self, id, function, value, callback=None):
        """
        Controls properties of the PWM<id>.

            - id: PWM Id (0, 1, 2, 3).
            - function:
                * 0: Set frequency.
                * 1: Set duty ratio.
                * 2: Set phase-shift.
                * 3: Stop if value=0, otherwise start.
            - value: Desired value or the the function.
            - callback: Callback function executed when received response from MCU.
        """
        super().pwm(id, function, value, callback)
        return self


    def get_clock(self, type, callback=None):
        """
        Reads dydtem clock/time.

            - type:
                * 0: HH:MM:SS:xxx.
                * 1: Microseconds.
                * 2: Milliseconds.
            - callback: Callback function executed when received response from MCU.
        """
        super().clock(type, callback)
        return self


    def get_cmdex_version(self, type=1, callback=None):
        """
        Reads version of the Cmdex firmware.

            - type:
                * 0: Reads version from the MCU firmware.
                * 1: Reads version from the CmdexApis class.
            - callback: Callback function executed when received response from MCU.
        """
        super().get_cmdex_version(type, callback)
        return self



    def set_interval(self, callback, interval):
        """
        Creats an interval timer. Returns an Id of the timer.

            - callback: Callback function executed when timeout.
            - interval: time in milliseconds.
        """
        return super().set_interval(callback, interval)


    def set_timeout(self, callback, interval):
        """
        Creats an timeout termer. Returns an Id of the timer.

            - callback: Callback function executed when timeout.
            - interval: time in milliseconds.
        """
        return super().set_timeout(callback, interval)


    def clr_interval(self, id):
        """
        Stops the interval timer<id>.

            - id: Id of the interval timer.
        """
        return super().clr_interval(id)


    def clr_timeout(self, id):
        """
        Stops the timeout timer<id>.

            - id: Id of the timeout timer.
        """
        return super().clr_timeout(id)


    def add_callback(self, type, callback):
        """
        Adds a callback function into the callback system.

            - type (event name):
                * line: Cmdex-line event data received.
                * psw: PSW event data received.
                * adc: ADC event data received.
                * led: LED event data received.
            - callback: Callback function executed when the event is emitted.
        """
        return super().add_callback(type, callback)



    def get_date_time(self):
        """
        Returns current datatime in the format of "yyyy-mm-dd HH:MM:SS.xxxxxx".
        """

        return super().get_date_time()


    def get_date(self):
        """
        Returns current date in the format of "yyyy-mm-dd".
        """
        return super().get_date()


    def get_time(self):
        """
        Returns current time in the format of "HH:MM:SS.xxxxxx".
        """
        return super().get_time()


    @staticmethod
    def detect_mcu():
        return CmdexCore.detect_mcu()


    @staticmethod
    def open_mcu_port(port):
        return CmdexCore.open_mcu_port(port)

    #
    # END OF Cmdex Class #
    #




def main():

    print('\r\nPyCmdex is working...\r\n')

    if len(sys.argv) > 1:
        if(sys.argv[1] == 'web'):
            CmdexCore.goto_github();
        else:
            url = 'https://github.com/drsanti/PyCmdex'
            print(f'Go to the {url} for more information\r\n')

if __name__ == '__main__':
    main()
