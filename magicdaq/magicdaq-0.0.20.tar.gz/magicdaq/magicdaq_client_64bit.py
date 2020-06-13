###############################################
#*** 64 Bit Magic DAQ Client ***
#Client is used with a 32 bit server to allow 64 bit python to use the 32 bit MagicDAQ Python API
###############################################

###############################################
#*** Imports ***
###############################################

from loadlib import Client64

###############################################
#*** How to Use ***
###############################################

#This is how you use the client:
# https://msl-loadlib.readthedocs.io/en/latest/interprocess_communication.html

# >>> from my_client import MyClient
# >>> c = MyClient()
# >>> c.add(1, 2)

###############################################
#*** Server Class ***
###############################################

class MagicDAQClient64Bit(Client64):

    def __init__(self):
        # Specify the name of the Python module to execute on the 32-bit server (i.e., 'my_server')
        super(MagicDAQClient64Bit, self).__init__(module32='magicdaq_server_32bit')

    ###################################################
    # *** All PUBLIC DAQDevice Methods ***
    #Includeds doc strings as these methods will be directly used by customer's IDE

    ###################################################
    #*** easydaq.py Public Methods ***
    ###################################################

    def open_daq_device(self, daq_serial_num = None):
        '''
        Method opens a daq device for utilization.

        Returns: none

        Optional Arg:
            daq_serial_num : str : DAQ Serial Number. When supplied, open_daq_device connects to the specified device.

        *** Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        *** Example Usage, daq_serial_num = '7e18aa9b'***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device(daq_serial_num = '7e18aa9b')
        '''

        return self.request32('open_daq_device', daq_serial_num)

    def get_hardware_version(self) -> str:
        """
        Returns: str : the connected DAQ hardware version

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()
        print('This is Hardware Version: ',daq_one.get_hardware_version())

        ***Example Usage Output ***
        This is Hardware Version: 1.10
        """

        return self.request32('get_hardware_version')

    def get_serial_number(self) -> str:
        """
        Returns: str : the connected DAQ serial number

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()
        print('This is Serial Number: ',daq_one.get_serial_number())

        ***Example Usage Output ***
        This is Serial Number: 1.10
        """

        return self.request32('get_serial_number')

    def get_firmware_version(self) -> str:
        """
        Returns: str : the connected DAQ firmware version

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()
        print('This is Firmware Version: ',daq_one.get_firmware_version())

        ***Example Usage Output ***
        This is Firmware Version: 2.6
        """

        return self.request32('get_firmware_version')

    def get_bootloader_version(self) -> str:
        """
        Returns: str : the connected DAQ bootloader version

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()
        print('This is Bootloader Version: ',daq_one.get_bootloader_version())

        ***Example Usage Output ***
        This is Bootloader Version: 1.0
        """
        return self.request32('get_bootloader_version')

    def get_product_type(self) -> str:
        '''
        Returns: str : the Product Type of the connected DAQ device

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()
        print('This is Product Type: ',daq_one.get_product_type())

        ***Example Usage Output ***
        This is Product Type: 3
        '''

        return self.request32('get_product_type')

    def get_all_version_info(self):
        '''
        Returns: 2 Dimensional List: containing all DAQ version information:

        [
        ['Serial Number', str],
        ['Hardware Version', str],
        ['Firmware Version', str],
        ['Bootloader Version', str],
        ['Product Type', str],
        ]

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()
        print(daq_one.get_all_version_info())

        ***Example Usage Output ***
        [['Hardware Version', '1.10'], ['Serial Number', '7e18aa9b'], ['Firmware Version', '2.6'], ['Bootloader Version', '1.0'], ['Product Type', '3']]
        '''

        return self.request32('get_all_version_info')

    def close_daq_device(self):
        '''
        Method closes the DAQDevice. Call this method after you are finished using the DAQ device.
        In order to use the DAQ hardware again, you will have to call the open_daq_device() method.

        Returns: none

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Do useful operations with the DAQ here

        daq_one.close_daq_device()

        '''

        return self.request32('close_daq_device')

    #*** Former Functions, Now Methods of DAQDevice Class **

    def get_api_version(self) -> float:
        '''
        Returns: float : Version number of easy daq API

        Args: none

        *** Example Usage ***

        import easydaq
        print(easydaq.get_api_version())

        *** Example Usage Output ***

        1.0
        '''

        return self.request32('get_api_version')

    def get_driver_version(self) -> float:
        '''
        Returns: float : Installed DAQ driver version number

        Args: none

        *** Example Usage ***

        import easydaq
        print(easydaq.get_driver_version())

        *** Example Usage Output ***

        1.0
        '''

        return self.request32('get_driver_version')

    def list_all_daqs(self):
        '''
        Function returns a list of the serial numbers for all DAQs connected to the computer. If no DAQs are connected, an empty list [] is returned.

        Returns: [str,str] : list of serial numbers. Serial numbers are in string format.

        *** Example Usage ***
        print('All DAQ serial numbers: ',easydaq.list_all_daqs())
        '''

        return self.request32('list_all_daqs')


    ###################################################
    #*** digitalmethods.py Public Methods ***
    ###################################################

    def set_digital_output(self, channel: int, pin_state: int):
        '''
        Method makes a digital output pin either High or Low.

        Returns: none

        Args:
            channel: int : DAQ pin number. For example, channel 'P0.0' is pin number 0. Must be an integer 0 - 7.
            pin_state: int : State of digital output pin. 1 = High (5V) and 0 = Low (0V)

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Set pin zero (labeled P0.0 on the DAQ device) to High (5V)
        daq_one.set_digital_output(0,1)
        '''

        return self.request32('set_digital_output', channel, pin_state)

    def configure_counter_pwm(self, pwm_frequency: float, pwm_duty_cycle: float, total_cycle_count = 0):
        '''
        Method configures counter PWM output.

        IMPORTANT:
            -The PWM waveform is output on the channel labeled 'CTR0' on the DAQ.
            -The PWM waveform is 3.3V amplitude

        Returns: none

        Args:
            pwm_frequency: float : The frequency of the PWM waveform in Hz. Valid range from 1 Hz (1) to 100kHz (100000)
            pwm_duty_cycle: float : The duty cycle of the PWM waveform. Valid range from 0% (0) to 100% (100) duty cycle.

        Optional Arg:
            total_cycle_count: int : The total number of pulses you want the PWM to output after a single start_pwm_output() command.
                                     Valid range from 1 pulse (1) to 65535 pulses (65535).
                                     Omit this optional parameter if you want the PWM waveform to continue until stopped with a stop_pwm_output() command.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the PWM Output (100Hz, 50% Duty Cycle)
        daq_one.configure_counter_pwm(100,50)

        #Start the PWM output
        daq_one.start_counter_pwm()

        ***Example Usage, Optional total_cycle_count Argument Used***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the PWM Output (100Hz, 50% Duty Cycle, 500 total cycles)
        daq_one.configure_counter_pwm(100,50, total_cycle_count = 500)

        #Start the PWM output
        daq_one.start_counter_pwm()
        '''

        return self.request32('configure_counter_pwm', pwm_frequency, pwm_duty_cycle, total_cycle_count)

    def start_counter_pwm(self):
        '''
        Method starts the counter PWM output.

        IMPORTANT:
            -The PWM waveform is output on the channel labeled 'CTR0' on the DAQ.
            -The PWM waveform is 3.3V amplitude

        Returns: none

        Args: none

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the PWM Output (100Hz, 50% Duty Cycle)
        daq_one.configure_counter_pwm(100,50)

        #Start the PWM output
        daq_one.start_counter_pwm()
        '''

        return self.request32('start_counter_pwm')

    def stop_counter_pwm(self):
        '''
        Method stops the counter PWM output.

        IMPORTANT:
            -The PWM waveform is output on the channel labeled 'CTR0' on the DAQ.
            -The PWM waveform is 3.3V amplitude

        Returns: none

        Args: none

        ***Example Usage ***
        import time

        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the PWM Output (100Hz, 50% Duty Cycle)
        daq_one.configure_counter_pwm(100,50)

        #Start the PWM output
        daq_one.start_counter_pwm()

        #Sleep for 5 seconds
        time.sleep(5)

        #Stop the PWM output
        daq_one.stop_counter_pwm()
        '''

        return self.request32('stop_counter_pwm')

    def read_digital_input(self, channel: int):
        '''
        Method reads a digital input pin and returns either 1 (meaning High) or 0 (meaning Low).

        IMPORTANT:
            -The digital input pin has an internal pull-up resistor. As such, the pin defaults to High.

            -If the digital pin has previously been driven Low by a set_digital_output command, ensure that you run
            the read_digital_input command before applying external voltage. This prevents excessive current being
            shunted to GND, possibly damaging the DAQ.

        Returns:
            pin_status : int : 1 = High, 0 = Low

        Args:
            channel: int : DAQ pin number. For example, channel 'P0.0' is pin number 0. Must be an integer 0 - 7.

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Read state of digital pin 0 (labeled P0.0 on the DAQ device)
        print("This is pin 0 state: ", daq_one.read_digital_input(0))
        '''

        return self.request32('read_digital_input', channel)

    def enable_pulse_counter(self, edge_type = 0):
        '''
        Method enables the pulse counter.

        IMPORTANT:
            -When the pulse counter is enabled, the pulse count value is re-set to 0.

        Returns: none

        Optional Arg:
            edge_type: int : The pulse counter may be set for falling edge detection (edge_type = 0) or rising edge detection (edge_type = 1). By default, falling edge detection is set.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Enable the pulse counter
        daq_one.enable_pulse_counter()

        ***Example Usage: edge_type set***
        #Enable the pulse counter, setting edge detection to rising edge
        daq_one.enable_pulse_counter(edge_type = 1)
        '''

        return self.request32('enable_pulse_counter', edge_type)

    def read_pulse_counter(self) -> int:
        '''
        Method returns the number of pulses that have been counted.

        Returns: int : number of pulses that have been counted.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Enable the pulse counter
        daq_one.enable_pulse_counter()

        #Allow some time for pulses to be measured on the CTR0 pin
        print('Start applying pulses now')
        time.sleep(2)

        #Print out the number of pulses that have been counted
        print('This many pulses have been counted: ',daq_one.read_pulse_counter())
        '''

        return self.request32('read_pulse_counter')

    def clear_pulse_counter(self):
        '''
        Method re-sets pulse count to 0.

        Returns: none

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        print('This is the existing pulse count value: ',daq_one.read_pulse_counter())

        #Reset the pulse counter to 0
        daq_one.clear_pulse_counter()

        #Show that the new pulse counter value is now 0
        print('The pulse counter has now been cleared. New pulse count value: ',daq_one_read_pulse_counter())
        '''

        return self.request32('clear_pulse_counter')


    ###################################################
    #*** analogmethods.py Public Methods ***
    ###################################################

    def read_analog_input(self, channel: int, decimal_places = 2) -> float:
        '''
        Method reads an analog input pin and returns the voltage.

        IMPORTANT:
            -A 'single ended' measurement is performed, meaning voltage is measured between the analog input pin and ground (AGND).
            -The maximum input voltage for the analog input pins is +/- 10V (referenced to AGND)

        Returns:
            voltage: float : the voltage measured at the analog input pin specified.

        Args:
            channel: int : DAQ pin number. For example, channel 'AI0' is pin number 0. Must be an integer 0 - 7.

        Optional Args:
            decimal_places : int : Number of decimal places the reading is rounded to. decimal_places = 2 is default. Maximum suggested is 3.

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Read analog input pin 0
        print('This is voltage at analog pin 0: ',read_single_analog_input(0))
        '''

        return self.request32('read_analog_input', channel, decimal_places)

    def read_diff_analog_input(self, channel_p: int, channel_n: int, decimal_places = 2) -> float:
        '''
        Method reads the differential voltage between two analog input pins.

        IMPORTANT:
            -A 'differential' measurement is performed, meaning voltage is measured between two analog input pins.
            -The maximum input voltage for each analog input pins is +/- 10V (referenced to AGND)

        Returns:
            voltage: float : the voltage difference between the two analog input pins. Voltage = Vpositive input pin - Vnegative input pin.

        Args:
            channel_p: int : Positive analog input DAQ pin number. For example, channel 'AI0' is pin number 0. Must be an integer 0 - 7.
            channel_n: int : Negative analog input DAQ pin number. For example, channel 'AI0' is pin number 0. Must be an integer 0 - 7.

        Optional Args:
            decimal_places : int : Number of decimal places the reading is rounded to. decimal_places = 2 is default. Maximum suggested is 3.

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #This is the differential voltage between pin 1 and pin 0. Voltage = pin 1 voltage - pin 0 voltage.
        print('This is the differential voltage between pin 1 and pin 0: ',read_raw_diff_analog_input(1,0))
        '''

        return self.request32('read_diff_analog_input', channel_p, channel_n, decimal_places)

    def set_analog_output(self, channel: int, output_voltage: float):
        '''
        Method sets the output voltage of an Analog Output pin.

        Returns: none

        Args:
            channel: int : DAQ pin number. For example, channel 'AO0' is Analog Output pin 0. There are two channels: 0 and 1.
            output_voltage: float : Voltage to output. May be any voltage between 0 and 5.

        ***Example Usage ***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Set pin zero (labeled P0.0 on the DAQ device) to High (5V)
        daq_one.set_digital_output(0,1)
        '''

        return self.request32('set_analog_output', channel, output_voltage)

    def configure_analog_output_sine_wave(self, channel: int, sine_frequency: float, total_cycle_count=0, amplitude=5):
        '''
        Method configures analog output sine wave.

        Returns: none

        Args:
            channel: int : DAQ pin number. For example, channel 'AO0' is Analog Output pin 0. There are two channels: 0 and 1.
            sine_frequency: float : The frequency of the sine waveform in Hz. Valid range from 1 Hz (1) to 31.25kHz (31250)

        Optional Arg:
            total_cycle_count: int : The total number of cycles you want to output after a single start command.
                                     Valid range from 1 cycle (1) to 10000 cycles (10000).
                                     Omit this optional parameter if you want the PWM waveform to continue until stopped with a stop command.
            amplitude: float : The sine wave will range from 0V to the maximum amplitude you specify.
                             Valid range from 0.1V (0.1) to 5V (5).
                             Omitting this optional parameters will result in the sine wave ranging between 0 and 5 volts.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the analog output sine wave (channel 1, 1000Hz, 3.3V amplitude)
        daq_one.configure_analog_output_sine_wave(1,1000,amplitude=3.3)

        #Start the analog output wave on channel 1
        daq_one.start_analog_output_wave(1)

        #Sleep for 4 seconds to allow wave to observation on oscilloscope
        time.sleep(4)

        #Stop the analog output wave
        daq_one.stop_analog_output_wave(1)
        '''

        return self.request32('configure_analog_output_sine_wave', channel, sine_frequency, total_cycle_count, amplitude)

    def configure_analog_output_pwm_wave(self, channel: int, pwm_frequency: float, pwm_duty_cycle: float, total_cycle_count=0, amplitude=5):
        '''
        Method configures analog output PWM wave.

        Returns: none

        Args:
            channel: int : DAQ pin number. For example, channel 'AO0' is Analog Output pin 0. There are two channels: 0 and 1.
            pwm_frequency: float : The frequency of the PWM waveform in Hz. Valid range from 1 Hz (1) to 31.25kHz (31250)
            pwm_duty_cycle: float : The duty cycle of the PWM waveform. Valid range from 0% (0) to 100% (100) duty cycle.


        Optional Arg:
            total_cycle_count: int : The total number of cycles you want to output after a single start command.
                                     Valid range from 1 cycle (1) to 10000 cycles (10000).
                                     Omit this optional parameter if you want the PWM waveform to continue until stopped with a stop command.
            amplitude: float : The PWM wave will range from 0V to the maximum amplitude you specify.
                             Valid range from 0.1V (0.1) to 5V (5).
                             Omitting this optional parameters will result in the sine wave ranging between 0 and 5 volts.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the analog output PWM wave (channel 0, 100Hz, 50% duty cycle, 4V amplitude)
        daq_one.configure_analog_output_pwm_wave(0,100,50, amplitude=4)

        #Start the analog output wave on channel 0
        daq_one.start_analog_output_wave(0)

        #Sleep for 4 seconds to allow wave to observation on oscilloscope
        time.sleep(4)

        #Stop the analog output wave
        daq_one.stop_analog_output_wave(0)
        '''

        return self.request32('configure_analog_output_pwm_wave',channel,pwm_frequency,pwm_duty_cycle,total_cycle_count,amplitude)

    def start_analog_output_wave(self, channel: int):
        '''
        Method starts the analog output wave.

        IMPORTANT:
            -You must configure the analog output port for a wave before using this command to start the wave.
             See methods configure_analog_output_sine_wave() and configure_analog_output_pwm_wave()

        Returns: none

        Args:
            channel: int : DAQ pin number. For example, channel 'AO0' is Analog Output pin 0. There are two channels: 0 and 1.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the analog output sine wave (channel 1, 1000Hz, 3.3V amplitude)
        daq_one.configure_analog_output_sine_wave(1,1000,amplitude=3.3)

        #Start the analog output wave on channel 1
        daq_one.start_analog_output_wave(1)

        #Sleep for 4 seconds to allow wave to oscilloscoped on osiliscope
        time.sleep(4)

        #Stop the analog output wave
        daq_one.stop_analog_output_wave(1)
        '''

        return self.request32('start_analog_output_wave', channel)

    def stop_analog_output_wave(self, channel: int):
        '''
        Method stops the analog output wave.

        Returns: none

        Args:
            channel: int : DAQ pin number. For example, channel 'AO0' is Analog Output pin 0. There are two channels: 0 and 1.

        ***Example Usage***
        daq_one = easydaq.DAQDevice()
        daq_one.open_daq_device()

        #Configure the analog output sine wave (channel 1, 1000Hz, 3.3V amplitude)
        daq_one.configure_analog_output_sine_wave(1,1000,amplitude=3.3)

        #Start the analog output wave on channel 1
        daq_one.start_analog_output_wave(1)

        #Sleep for 4 seconds to allow wave to oscilloscoped on osiliscope
        time.sleep(4)

        #Stop the analog output wave
        daq_one.stop_analog_output_wave(1)
        '''

        return self.request32('stop_analog_output_wave', channel)


    ###################################################
    #*** streamingmethods.py Public Methods ***
    ###################################################


    def configure_analog_input_stream(self, channels: [int], measurement_frequency: float, decimal_places = 2):
        '''
        Method configures single ended analog input stream.

        Returns: none

        Args:
            channels: [int] : List of analog input pin numbers to stream from. For example, to stream from channel 0 only enter [0]. To stream from channels 0-2 enter [0,1,2].
            measurement_frequency: float : Measurement frequency. Valid range from 1 Hz (1) to 48kHz (48000).
                                           The maximum measurement_frequency possible is contingent on the number of channels being streamed. Expressed as an equation:
                                           measurement_frequency X # of channels being streamed <= 48000
        Optional Arg:
            decimal_places : int : Number of decimal places the readings are rounded to. decimal_places = 2 is default. Maximum suggested is 3.

        ***Example Usage***
        TODO: complete
        '''

        return self.request32('configure_analog_input_stream', channels, measurement_frequency, decimal_places)

    def start_analog_input_stream(self) -> float:
        '''
        Method starts the analog input stream.

        Returns: float : Actual sampling frequency. The actual sample frequency may differ slightly from what is specified by
                       the measurement_frequency parameter used with the configure_analog_input_stream() method
                       due to DAQ hardware timer functionality.

        ***Example Usage***
        TODO: complete
        '''

        return self.request32('start_analog_input_stream')

    def set_streaming_data_buffer_max_rows(self, max_rows: int):
        """
        Method sets the maximum number of rows allowed in the streaming data storage buffer. The default (if this function is not used) is
        480000 (roughly 0.8Gb if all 8 channels are streamed and the buffer is full). Each row is 192 bytes maximum.

        Returns: none

        Args:
            max_rows : int : Maximum number of rows allowed for the streaming data buffer. Valid entries between 1000 and 10000000 inclusive.

        ***Example Usage ***
        #TODO: put something here
        """

        return self.request32('set_streaming_data_buffer_max_rows', max_rows)

    def get_last_n_streaming_data_samples(self, n_samples:int):
        '''
        Method returns the most recently acquired n_samples of streamed data. This function does not clear or delete the streaming data buffer.
        As such, the same data will be returned by the function if no new streaming data has been acquired since the last time this function has been called.

        Returns: [[float]] : Last n_samples of streamed data.

        Args:
            n_samples : int : Number of samples to return. If n_samples is greater than the length of the streaming_data_buffer, all available data points will be returned.
            n_samples must be >= 1.

        ***Example Usage***
        TODO: complete
        '''

        return self.request32('get_last_n_streaming_data_samples', n_samples)

    def get_full_streaming_data_buffer(self, only_new_data = True, read_and_delete =False):
        '''
        Method returns all data available in the streaming data buffer.

        Returns: [[float]] :

        Args: None.

        Optional Arg:
            only_new_data: bool : When only_new_data is set to True, this function will only return streaming data acquired since the last time this function was called.
                                  In other words, only 'new' data is returned. Default is only_new_data = True.
            read_and_delete: bool: When read_and_delete is set to True, the data returned by this function will be deleted from the underlying streaming data buffer.
                                   Setting read_and_delete to True reduces the total amount of memory used. However, get_last_n_streaming_data_samples()
                                   will not be able to return and data that has been previously deleted from the streaming data buffer by this function.
                                   Default is read_and_delete = False.

        ***Example Usage***
        TODO: complete
        '''

        return self.request32('get_full_streaming_data_buffer', only_new_data, read_and_delete)

    def delete_streaming_data_buffer(self):
        '''
        Method deletes the streaming_data_buffer. This is will reduce the memory being used.

        Returns: None.

        Args: None.

        ***Example Usage***
        TODO: complete
        '''

        return self.request32('delete_streaming_data_buffer')

    def stop_analog_input_stream(self):
        '''
        Method stops the analog input stream.

        Returns: None.

        Args: None.

        ***Example Usage***
        TODO: complete
        '''

        return self.request32('stop_analog_input_stream')