import atexit
import time
import logging
from datetime import datetime
from datetime import timedelta
import warnings
import threading
import random
from pathlib import Path
from typing import Dict, Union, List, Tuple
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from ftdi_serial import Serial
from hein_utilities.runnable import Runnable
from hein_utilities.datetime_utilities import datetimeManager
from ika.utilities.data_analysis_visualization import stable_against_known, \
    find_stable_against_known_custom_one_window, plot_axes, plot_plateau

# todo add errors

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MagneticStirrer(Runnable):
    """
    Establish a connection with an IKA magnetic stirrer
    Supported models:
        - C-MAG HS 7
        - RCT 5 digital

    Not inherent in the IKA hot plate, is the ability to wait and know when the temperature has stabilized. A custom
    way to know has been added, see the wait_until_temperature_stable function.

    Parameters for knowing when the temperature has stabilized
        :int, n: the number of most recent measurements used to determine if the temperature has been stabilized
        :float, std_max: maximum standard deviation the data can have to be determined as stable
        :float, sem_max: maximum standard error the data can have to be determined as stable
        :bool, relative_limits: if true, then the upper and lower limits, if their values are 0 < 1,
            will be relative to the range of all temperature measurements so far
        :float, upper_limit: if relative limits is False, it is the absolute temperature (C) that the mean
            and mode of the data can is allowed to be above than the plate target temperature, to determine if it
            has stabilized.
            if the value is above 0 and less than 1 and relative limits is True,  it is the percent of the range of all
            the temperature data gathered so far (range = max - min values) that will be converted into absolute
            temperature for use in this function
        :float, lower_limit: if relative limits is False, it is the absolute temperature (C) that the mean
            and mode of the data can is allowed to be below than the plate target temperature, to determine if it
            has stabilized.
            if the value is above 0 and less than 1 and relative limits is True,  it is the percent of the range of all
            the temperature data gathered so far (range = max - min values) that will be converted into absolute
            temperature for use in this function
        :float, r_min: minimum r when doing a linear regression on the data required for the data =to be
            determined as stable
        :float, slope_upper_limit: how much above zero the slope from doing a linear regression can be in order for
            the data to be determined as stable
        :float, slope_lower_limit: how much below zero the slope from doing a linear regression can be in order for
            the data to be determined as stable
    """

    # hex command characters for data transmission
    SP_HEX = "\x20"  # space or blank
    CR_HEX = "\x0d"  # carriage return
    LF_HEX = "\x0a"  # line feed or new line
    DOT_HEX = "\x2E"  # dot
    LINE_ENDING = CR_HEX + LF_HEX  # each individual command and each response are terminated CR LF
    LINE_ENDING_ENCODED = LINE_ENDING.encode()

    # default connection parameters
    CONNECTION_SETTINGS = dict(
        baudrate=9600,
        data_bits=Serial.DATA_BITS_7,
        stop_bits=Serial.STOP_BITS_1,  # todo check with someone because it seems like this is 0 even if it is called 1
        parity=Serial.PARITY_EVEN,
    )

    # constant names are the functions, and the values are the corresponding NAMUR commands
    READ_THE_DEVICE_NAME = "IN_NAME"
    READ_ACTUAL_EXTERNAL_SENSOR_VALUE = "IN_PV_1"
    READ_ACTUAL_HOTPLATE_SENSOR_VALUE = "IN_PV_2"
    READ_STIRRING_SPEED_VALUE = "IN_PV_4"
    READ_VISCOSITY_TREND_VALUE = "IN_PV_5"
    READ_RATED_TEMPERATURE_VALUE = "IN_SP_1"
    READ_RATED_SET_SAFETY_TEMPERATURE_VALUE = "IN_SP_3"
    READ_RATED_SPEED_VALUE = "IN_SP_4"
    ADJUST_THE_SET_TEMPERATURE_VALUE = "OUT_SP_1"
    SET_TEMPERATURE_VALUE = "OUT_SP_1 "  # requires a value to be appended to the end of the command
    ADJUST_THE_SET_SPEED_VALUE = "OUT_SP_4"
    SET_SPEED_VALUE = "OUT_SP_4 "  # requires a value to be appended to the end of the command
    START_THE_HEATER = "START_1"
    STOP_THE_HEATER = "STOP_1"
    START_THE_MOTOR = "START_4"
    STOP_THE_MOTOR = "STOP_4"
    SWITCH_TO_NORMAL_OPERATING_MODE = "RESET"
    SET_OPERATING_MODE_A = "SET_MODE_A"
    SET_OPERATING_MODE_B = "SET_MODE_B"
    SET_OPERATING_MODE_D = "SET_MODE_D"
    SET_WD_SAFETY_LIMIT_TEMPERATURE_WITH_SET_VALUE_ECHO = "OUT_SP_12@"  # requires a value to be appended to the end of
    # the command
    SET_WD_SAFETY_LIMIT_SPEED_WITH_SET_VALUE_ECHO = "OUT_SP_12@"  # requires a value to be appended to the end of
    # the command
    WATCHDOG_MODE_1 = "OUT_WD1@"   # requires a value (bw 20-1500) to be appended to the end of the command - this is
    # the watchdog time in seconds. this command launches the watchdog function and must be transmitted within the
    # set watchdog time. in watchdog mode 1, if event WD1 occurs, the heating and stirring functions are switched off
    #  and ER 2 is displayed
    WATCHDOG_MODE_2 = "OUT_WD2@"   # requires a value (bw 20-1500) to be appended to the end of the command - this is
    # the watchdog time in seconds. this command launches the watchdog function and must be transmitted within the
    # set watchdog time. the WD2 event can be reset with the command "OUT_WD2@0", and this also stops the watchdog
    # function.  in watchdog mode 2, if event WD2 occurs, the speed target value is changed to the WD safety speed
    # limit and the temperature target value is change to the WD safety temperature limit value

    human_readable_commands: Dict[str, str] = {
        ADJUST_THE_SET_TEMPERATURE_VALUE: 'adjust the set temperature value',
        SET_TEMPERATURE_VALUE: 'set target temperature',
        ADJUST_THE_SET_SPEED_VALUE: 'adjust the set stir rate value',
        SET_SPEED_VALUE: 'set target stir rate',
        START_THE_HEATER: 'start heating',
        STOP_THE_HEATER: 'stop heating',
        START_THE_MOTOR: 'start stirring',
        STOP_THE_MOTOR: 'stop stirring',
        SWITCH_TO_NORMAL_OPERATING_MODE: 'switch to normal operating mode',
        SET_OPERATING_MODE_A: 'set operating mode a',
        SET_OPERATING_MODE_B: 'set operating mode b',
        SET_OPERATING_MODE_D: 'set operating mode d',
    }

    _unit_seconds = datetimeManager._unit_seconds
    _unit_minutes = datetimeManager._unit_minutes
    _unit_hours = datetimeManager._unit_hours

    def __init__(self,
                 device_port: str,
                 save_folder: Path = None,
                 datetime_format: str = datetimeManager._default_datetime_format,
                 ):
        """

        :param device_port: port on computer to connect to the hotplate. For example, 'COM3'
        :param save_folder: path to folder to save data from running the hotplate
        :param str, datetime_format: string format for the time stamps
        """
        Runnable.__init__(self, logger=logger)
        self.ser: Serial = None
        self._lock = threading.Lock()
        self._device_port = device_port
        self._heating: bool = None  # true if hot plate is heating; used for tracking, does not control the ika
        self._stirring: bool = None  # true if hot plate is heating; used for tracking, does not control the ika
        self.datetime_format = datetime_format
        self.datetime_manager = datetimeManager(string_format=self.datetime_format)  # datetime format for data
        # recording
        self.datetime_manager_rounding = 4

        self.connect()

        if save_folder is None:
            save_folder = Path.cwd()
        self.save_path = save_folder
        self.temperature_csv_path = self.save_path.joinpath('ika_temperature_data.csv')
        self.command_csv_path = self.save_path.joinpath('ika_command_data.csv')
        self.temperature_data: pd.DataFrame = None
        self.command_data: pd.DataFrame = None
        self.set_up_data()

        self.monitor_temperature_thread = None
        self.save_temperature_data_interval = 200  # interval of number of data points to save the temperature csv file
        self.set_temperatures: List[float] = []  # list of the temperatures to go to

        self.stop_stirring()
        self.stop_heating()
        """
        Parameters for knowing when the temperature has stabilized
        :param n: the number of most recent measurements used to determine if the temperature has been stabilized
        :param float, std_max: maximum standard deviation the data can have to be determined as stable
        :param float, sem_max: maximum standard error the data can have to be determined as stable
        :param bool, relative_limits: if true, then the upper and lower limits, if their values are 0 < 1, 
            will be relative to the range of all temperature measurements so far 
        :param float, upper_limit: if relative limits is False, it is the absolute temperature (C) that the mean 
            and mode of the data can is allowed to be above than the plate target temperature, to determine if it 
            has stabilized. 
            if the value is above 0 and less than 1 and relative limits is True,  it is the percent of the range of all 
            the temperature data gathered so far (range = max - min values) that will be converted into absolute 
            temperature for use in this function
        :param float, lower_limit: if relative limits is False, it is the absolute temperature (C) that the mean 
            and mode of the data can is allowed to be below than the plate target temperature, to determine if it 
            has stabilized. 
            if the value is above 0 and less than 1 and relative limits is True,  it is the percent of the range of all 
            the temperature data gathered so far (range = max - min values) that will be converted into absolute 
            temperature for use in this function
        :param float, r_min: minimum r when doing a linear regression on the data required for the data =to be
            determined as stable
        :param float, slope_upper_limit: how much above zero the slope from doing a linear regression can be in order for
            the data to be determined as stable
        :param float, slope_lower_limit: how much below zero the slope from doing a linear regression can be in order for
            the data to be determined as stable
        """
        self._n: int = 120
        self._std_max: float = 0.05
        self._sem_max: float = 0.05
        self._relative_limits: bool = False
        self._upper_limit: float = 1
        self._lower_limit: float = 1
        self._r_min: float = None
        self._slope_upper_limit: float = None
        self._slope_lower_limit: float = None

    @property
    def stir_rate(self) -> float:
        """
        Plate actual stir rate

        :return:
        """
        return self.read_stirring_speed_value()

    @property
    def target_stir_rate(self) -> float:
        """
        Stir rate hotplate is set to go to

        :return:
        """
        return self.read_rated_speed_value()

    @target_stir_rate.setter
    def target_stir_rate(self,
                         value,
                         ):
        self.set_speed_value(value=value)

    def set_target_stir_rate(self,
                             value,
                             ):
        self.target_stir_rate = value

    @property
    def probe_temperature(self):
        """
        The temperature (degrees C) picked up by the temperature probe

        :return:
        """
        return self.read_actual_external_sensor_value()

    @property
    def target_temperature(self) -> float:
        """
        Temperature hotplate is set to go to

        :return:
        """
        return self.read_rated_temperature_value()

    @target_temperature.setter
    def target_temperature(self,
                           value,
                           ):
        self.set_temperature_value(value=value)

    def set_target_temperature(self,
                               value,
                               ):
        self.target_temperature = value

    @property
    def hotplate_sensor_temperature(self) -> float:
        """
        The value (degrees C) that the hotplate itself is at

        :return:
        """
        return self.read_actual_hotplate_sensor_value()

    @property
    def viscosity_trend(self):
        """
        The viscosity trend

        :return:
        """
        return self.read_viscosity_trend_value()

    @property
    def n(self) -> float:
        return self._n

    @n.setter
    def n(self,
          value: int,
          ):
        if isinstance(value, int) is False:
            raise TypeError('value must be of type int')
        self._n = value

    @property
    def std_max(self) -> float:
        return self._std_max

    @std_max.setter
    def std_max(self,
                value: float,
                ):
        self._std_max = value

    @property
    def sem_max(self) -> float:
        return self._sem_max

    @sem_max.setter
    def sem_max(self,
                value: float,
                ):
        self._sem_max = value

    @property
    def upper_limit(self) -> float:
        return self._upper_limit

    @upper_limit.setter
    def upper_limit(self,
                    value: float,
                    ):
        self._upper_limit = value

    @property
    def lower_limit(self) -> float:
        return self._lower_limit

    @lower_limit.setter
    def lower_limit(self,
                    value: float,
                    ):
        self._lower_limit = value

    @property
    def relative_limits(self) -> bool:
        return self._relative_limits

    @relative_limits.setter
    def relative_limits(self,
                        value: bool,
                        ):
        self._relative_limits = value

    @property
    def r_min(self) -> float:
        return self._r_min

    @r_min.setter
    def r_min(self,
              value: float,
              ):
        self._r_min = value

    @property
    def slope_upper_limit(self) -> float:
        return self._slope_upper_limit

    @slope_upper_limit.setter
    def slope_upper_limit(self,
                          value: float,
                          ):
        self._slope_upper_limit = value

    @property
    def slope_lower_limit(self) -> float:
        return self._slope_lower_limit

    @slope_lower_limit.setter
    def slope_lower_limit(self,
                          value: float,
                          ):
        self._slope_lower_limit = value

    def connect(self):
        try:
            if self.ser is None:
                cn = Serial(device_port=self._device_port,
                            **self.CONNECTION_SETTINGS,
                            )
                self.ser = cn
            else:
                self.ser.connect()

            logger.info(self.read_device_name())
            # Ensure that the serial port is closed on system exit
            atexit.register(self.disconnect)  # todo, does this work?
        except Exception as e:
            logger.warning("could not connect")
            raise e

    def disconnect(self):
        """
        Stop heating and stirring and close the serial port

        :return:
        """
        try:
            self.stop_the_heater()
            self.stop_the_motor()

            # disconnect
            self.ser.disconnect()
        except Exception as e:
            logger.warning("could not disconnect")
            raise e

    def set_up_data(self):
        start_time: str = self.datetime_manager.now_string()
        self.set_up_temperature_data(start_time=start_time)
        self.set_up_command_data(start_time=start_time)

    def set_up_temperature_data(self, start_time) -> None:
        """
        For the Time column, what's in the parenthesis is the datetime format set, and the values are strings,
        but for the rest, the values are floats or datetime objects

        Example table:

        +-----------------------------+----------+------------+-------------+-----------------+
        | Time (self.datetime_format) | Time (s) | Time (min) | Time (hour) | Temperature (C) |
        +-----------------------------+----------+------------+-------------+-----------------+
        |          datetime_1         |     0    |      0     |      0      |      TEMP_1     |
        +-----------------------------+----------+------------+-------------+-----------------+
        |          datetime_2         |    30    |     0.5    |    0.0083   |      TEMP_2     |
        +-----------------------------+----------+------------+-------------+-----------------+
        |          datetime_3         |    60    |      1     |    0.0167   |      TEMP_3     |
        +-----------------------------+----------+------------+-------------+-----------------+

        :return: None
        """
        columns = [f'Time ({self.datetime_format})', 'Time (s)', 'Time (min)', 'Time (hour)', 'Temperature (C)']
        df = pd.DataFrame(columns=columns)
        temperature = self.read_actual_external_sensor_value()
        add_data = {f'Time ({self.datetime_format})': start_time,
                    'Time (s)': 0,
                    'Time (min)': 0,
                    'Time (hour)': 0,
                    'Temperature (C)': temperature,
                    }
        df = df.append(add_data, ignore_index=True)
        self.temperature_data = df
        df.to_csv(self.temperature_csv_path, sep=',', index=False, mode='w')

    def set_up_command_data(self, start_time) -> None:
        """
        For the Time column, what's in the parenthesis is the datetime format set, and the values are strings,
        but for the rest of the time columns, the values are floats

        In the command column, put select commands that are through Python to the hot plate in human readable form

        Example table:

        +-----------------------------+----------+------------+-------------+-----------+
        | Time (self.datetime_format) | Time (s) | Time (min) | Time (hour) |  Command  |
        +-----------------------------+----------+------------+-------------+-----------+
        |          datetime_1         |     0    |      0     |      0      |   START   |
        +-----------------------------+----------+------------+-------------+-----------+
        |          datetime_2         |    30    |     0.5    |    0.0083   | COMMAND_2 |
        +-----------------------------+----------+------------+-------------+-----------+
        |          datetime_3         |    60    |      1     |    0.0167   | COMMAND_3 |
        +-----------------------------+----------+------------+-------------+-----------+

        :return: None
        """
        columns = [f'Time ({self.datetime_format})', 'Time (s)', 'Time (min)', 'Time (hour)', 'Command']
        df = pd.DataFrame(columns=columns)
        add_data = {f'Time ({self.datetime_format})': start_time,
                    'Time (s)': 0,
                    'Time (min)': 0,
                    'Time (hour)': 0,
                    'Command': 'START',
                    }
        df = df.append(add_data, ignore_index=True)
        self.command_data = df
        df.to_csv(self.command_csv_path, sep=',', index=False, mode='w')

    def save_csv_files(self):
        self.save_temperature_csv()
        self.save_command_csv()

    def save_temperature_csv(self):
        self.temperature_data.to_csv(self.temperature_csv_path, sep=',', index=False, mode='w')

    def save_command_csv(self):
        self.command_data.to_csv(self.command_csv_path, sep=',', index=False, mode='w')

    def register_temperature(self, temperature: float = None) -> None:
        current_time_str: str = self.datetime_manager.now_string()
        current_time: datetime = datetimeManager.str_to_datetime(current_time_str, datetime_format=self.datetime_format)[0]
        if temperature is None:
            temperature = self.probe_temperature
        first_row = self.temperature_data.head(1)
        start_time: str = first_row[f'Time ({self.datetime_format})'][0]
        start_time: datetime = datetimeManager.str_to_datetime(start_time,
                                                               datetime_format=self.datetime_format)[0]
        times = [start_time, current_time]

        relative_s = datetimeManager.relative_datetime(times,
                                                       units=self._unit_seconds,
                                                       rounding=self.datetime_manager_rounding)[1]
        relative_min = datetimeManager.relative_datetime(times,
                                                         units=self._unit_minutes,
                                                         rounding=self.datetime_manager_rounding)[1]
        relative_hour = datetimeManager.relative_datetime(times,
                                                          units=self._unit_hours,
                                                          rounding=self.datetime_manager_rounding)[1]

        add_data = {f'Time ({self.datetime_format})': current_time_str,
                    'Time (s)': relative_s,
                    'Time (min)': relative_min,
                    'Time (hour)': relative_hour,
                    'Temperature (C)': temperature,
                    }
        self.temperature_data = self.temperature_data.append(add_data, ignore_index=True)

        nrows = len(self.temperature_data)
        if nrows % self.save_temperature_data_interval == 0:
            self.save_temperature_csv()

    def register_command(self, command: str) -> None:
        current_time_str: str = self.datetime_manager.now_string()
        current_time: datetime = datetimeManager.str_to_datetime(current_time_str, datetime_format=self.datetime_format)[0]
        first_row = self.command_data.head(1)
        start_time: str = first_row[f'Time ({self.datetime_format})'][0]
        start_time: datetime = datetimeManager.str_to_datetime(start_time,
                                                               datetime_format=self.datetime_format)[0]
        times = [start_time, current_time]
        relative_s = datetimeManager.relative_datetime(times,
                                                       units=self._unit_seconds,
                                                       rounding=self.datetime_manager_rounding)[1]
        relative_min = datetimeManager.relative_datetime(times,
                                                         units=self._unit_minutes,
                                                         rounding=self.datetime_manager_rounding)[1]
        relative_hour = datetimeManager.relative_datetime(times,
                                                          units=self._unit_hours,
                                                          rounding=self.datetime_manager_rounding)[1]

        add_data = {f'Time ({self.datetime_format})': current_time_str,
                    'Time (s)': relative_s,
                    'Time (min)': relative_min,
                    'Time (hour)': relative_hour,
                    'Command': command,
                    }
        self.command_data = self.command_data.append(add_data, ignore_index=True)
        self.save_command_csv()

    def run(self):
        """function to monitor temperature in the background every second\
        """
        while self.running:
            time.sleep(1)
            self.register_temperature()

    def start_background_monitoring(self):
        """start the thread to monitor temperature in the background every second"""
        self.start()

    def stop_background_monitoring(self):
        """stop the thread to monitor temperature in the background every second"""
        self.stop()

    def stable(self,
               x,
               y,
               ) -> bool:
        """
        Definition of stability:
        Check if the temperature measurements mean and mode fall within set temperature value plus/minus the
        lower_limit and upper limits, and if the standard deviation is less than std_max, and the standard error is
        less than sem_max, and if the r value from doing a linear regression is less than r_min and the slope from
        doing a linear regression is plus/minus slope upper and lower limits.

        All of the properties that are used in this function must have been set beforehand

        :param x: 1d array of the x data; time data
        :param y: 1d array of the y data; temperature data

        :return: True if based on the data passed in, the temperature has stabilized to the temperature the hot plate
            was set to go to
        """
        temperatures = self.temperature_data['Temperature (C)'].tolist()
        y_max = max(temperatures)
        y_min = min(temperatures)
        total_range = y_max - y_min
        if self.upper_limit < 1 and self.relative_limits is True:
            upper_limit = self.upper_limit * total_range
        else:
            upper_limit = self.upper_limit
        if self.lower_limit < 1 and self.relative_limits is True:
            lower_limit = self.lower_limit * total_range
        else:
            lower_limit = self.lower_limit

        stable: bool = stable_against_known(x=x,
                                            y=y,
                                            known=self.target_temperature,
                                            upper_limit=upper_limit,
                                            lower_limit=lower_limit,
                                            std_max=self.std_max,
                                            sem_max=self.sem_max,
                                            r_min=self.r_min,
                                            slope_upper_limit=self.slope_upper_limit,
                                            slope_lower_limit=self.slope_lower_limit,
                                            )
        return stable

    def wait_until_temperature_stable(self,
                                      time_out: float = 1800,
                                      ) -> bool:
        """
        Check for when the temperature has stabilized, and pause code execution until this happes or when
        timeout number of seconds has passed. Every measurement takes about 1 second.

        :param float, time_out: every measurement takes roughly 1 second. The time_out value is the maximum number
            seconds after this function has been started that it can run for until it must return. This is to prevent
            the function from holding something up for too long

        :return:
        """
        n = self.n

        # self.stop_background_monitoring()
        start_time: str = self.datetime_manager.now_string()
        start_time: datetime = datetimeManager.str_to_datetime(start_time,
                                                               datetime_format=self.datetime_format)[0]
        while True:
            current_time: str = self.datetime_manager.now_string()
            current_time: datetime = datetimeManager.str_to_datetime(current_time,
                                                                     datetime_format=self.datetime_format)[0]
            seconds_passed: timedelta = datetimeManager.relative_datetime([start_time, current_time],
                                                                          units=datetimeManager._unit_seconds,
                                                                          rounding=1)[1]
            if seconds_passed > time_out:
                # self.start_background_monitoring()
                return False
            else:
                time.sleep(1)
                self.register_temperature()
                times = self.temperature_data['Time (min)'].tolist()
                temperatures = self.temperature_data['Temperature (C)'].tolist()
                if len(times) < n:
                    continue
                else:
                    last_n_x_values = times[-n:]
                    last_n_y_values = temperatures[-n:]
                    stable = self.stable(
                        x=last_n_x_values,
                        y=last_n_y_values,
                    )
                    if stable:
                        # self.start_background_monitoring()
                        return True
                    else:
                        continue

    def _send_and_receive(self,
                          command: str,
                          ):
        """
        Send a command, get a response back, and return the response
        :param str, command: a command that will give back a response - these will be:
            READ_THE_DEVICE_NAME
            READ_ACTUAL_EXTERNAL_SENSOR_VALUE
            READ_ACTUAL_HOTPLATE_SENSOR_VALUE
            READ_STIRRING_SPEED_VALUE
            READ_VISCOSITY_TREND_VALUE
            READ_RATED_TEMPERATURE_VALUE
            READ_RATE_SET_SAFETY_TEMPERATURE_VALUE
            READ_RATE_SPEED_VALUE

        :return:
        """
        with self._lock:
            # format the command to send so that it terminates with the line ending (CR LF)
            formatted_command: str = command + self.LINE_ENDING
            formatted_command_encoded = formatted_command.encode()
            # this is the response, and is returned
            return_string = self.ser.request(data=formatted_command_encoded,
                                             line_ending=self.LINE_ENDING_ENCODED,
                                             ).decode()
            # all the functions that would use this function, except when asking for the device name, returns a number.
            # however the return string type for all the other functions is a string of the type '#.# #', so we want to
            # change that into a float instead so it can be easily used
            if return_string == 'C-MAG HS7':
                return 'C-MAG HS7'
            elif return_string == 'RCT digital':
                return 'RCT digital'
            else:
                formatted_return_float = float(return_string.split()[0])  # return just the information we want as a float
            return formatted_return_float

    def _send(self,
              command: str,
              ):
        """
        Send a command
        :param str, command: a command with optional parameter's included if required (such as for setting temperature
            or stirring rate

        :return:
        """
        with self._lock:
            # format the command to send so that it terminates with the line ending (CR LF)
            formatted_command: str = command + self.LINE_ENDING
            formatted_command_encoded = formatted_command.encode()
            self.ser.write(data=formatted_command_encoded)  # commands need to be encoded when sent

    def read_device_name(self):
        return self._send_and_receive(command=self.READ_THE_DEVICE_NAME)

    def read_actual_external_sensor_value(self):
        """
        read and return the temperature (degrees C) picked up by the temperature probe

        :return:
        """
        return self._send_and_receive(command=self.READ_ACTUAL_EXTERNAL_SENSOR_VALUE)

    def read_actual_hotplate_sensor_value(self):
        """
        read and return the value (degrees C) that the hotplate itself is at

        :return:
        """
        return self._send_and_receive(command=self.READ_ACTUAL_HOTPLATE_SENSOR_VALUE)

    def read_stirring_speed_value(self):
        return self._send_and_receive(command=self.READ_STIRRING_SPEED_VALUE)

    def read_viscosity_trend_value(self):
        return self._send_and_receive(command=self.READ_VISCOSITY_TREND_VALUE)

    def read_rated_temperature_value(self):
        """
        read and return the temperature (degrees C) that the hotplate was set to maintain

        :return:
        """
        return self._send_and_receive(command=self.READ_RATED_TEMPERATURE_VALUE)

    def read_rated_set_safety_temperature_value(self):
        return self._send_and_receive(command=self.READ_RATED_SET_SAFETY_TEMPERATURE_VALUE)

    def read_rated_speed_value(self):
        return self._send_and_receive(command=self.READ_RATED_SPEED_VALUE)

    def adjust_the_set_temperature_value(self):
        self._send(command=self.ADJUST_THE_SET_TEMPERATURE_VALUE)

    def set_temperature_value(self,
                              value,
                              ):
        command = self.SET_TEMPERATURE_VALUE + str(value) + ' '
        self._send(command=command)
        command_str = self.human_readable_commands[self.SET_TEMPERATURE_VALUE] + f' to {str(value)}'
        self.register_command(command_str)
        self.set_temperatures.append(value)

    def adjust_the_set_speed_value(self):
        self._send(command=self.ADJUST_THE_SET_SPEED_VALUE)

    def set_speed_value(self,
                        value,
                        ):
        command = self.SET_SPEED_VALUE + str(value) + ' '
        self._send(command=command)
        command_str = self.human_readable_commands[self.SET_SPEED_VALUE] + f' to {str(value)}'
        self.register_command(command_str)

    def start_the_heater(self):
        self._send(command=self.START_THE_HEATER)
        self._heating = True
        command_str = self.human_readable_commands[self.START_THE_HEATER]
        self.register_command(command_str)

    def start_heating(self):
        self.start_the_heater()

    def stop_the_heater(self):
        self._send(command=self.STOP_THE_HEATER)
        self._heating = False
        command_str = self.human_readable_commands[self.STOP_THE_HEATER]
        self.register_command(command_str)

    def stop_heating(self):
        self.stop_the_heater()

    def start_the_motor(self):
        self._send(command=self.START_THE_MOTOR)
        self._stirring = True
        command_str = self.human_readable_commands[self.START_THE_MOTOR]
        self.register_command(command_str)

    def start_stirring(self):
        self.start_the_motor()

    def stop_the_motor(self):
        self._send(command=self.STOP_THE_MOTOR)
        self._stirring = False
        command_str = self.human_readable_commands[self.STOP_THE_MOTOR]
        self.register_command(command_str)

    def stop_stirring(self):
        self.stop_the_motor()

    def switch_to_normal_operating_mode(self):
        self._send(command=self.SWITCH_TO_NORMAL_OPERATING_MODE)
        command_str = self.human_readable_commands[self.SWITCH_TO_NORMAL_OPERATING_MODE]
        self.register_command(command_str)

    def set_operating_mode_a(self):
        self._send(command=self.SET_OPERATING_MODE_A)
        command_str = self.human_readable_commands[self.SET_OPERATING_MODE_A]
        self.register_command(command_str)

    def set_operating_mode_b(self):
        self._send(command=self.SET_OPERATING_MODE_B)
        command_str = self.human_readable_commands[self.SET_OPERATING_MODE_B]
        self.register_command(command_str)

    def set_operating_mode_d(self):
        self._send(command=self.SET_OPERATING_MODE_D)
        command_str = self.human_readable_commands[self.SET_OPERATING_MODE_D]
        self.register_command(command_str)

    def set_wd_safety_limit_temperature(self,
                                        value: str,
                                        ):
        command = self.SET_WD_SAFETY_LIMIT_TEMPERATURE_WITH_SET_VALUE_ECHO + value + ' '
        return self._send_and_receive(command=command)

    def set_wd_safety_limit_speed(self,
                                  value,
                                  ):
        command = self.SET_WD_SAFETY_LIMIT_SPEED_WITH_SET_VALUE_ECHO + str(value) + ' '
        return self._send_and_receive(command=command)

    def watchdog_mode_1(self,
                        value,
                        ):
        """
        This command launches the watchdog function and must be transmitted within the set watchdog time.
        in watchdog mode 1, if event WD1 occurs, the heating and stirring functions are switched off and ER 2 is
        displayed

        :param value: value between 20 and 1500 (units in seconds) - the watchdog time

        :return:
        """
        command = self.WATCHDOG_MODE_1 + str(value) + ' '
        self._send(command=command)

    def watchdog_mode_2(self,
                        value: str,
                        ):
        """
        This command launches the watchdog function and must be transmitted within the set watchdog time. the WD2
        event can be reset with the command "OUT_WD2@0", and this also stops the watchdog function.  in watchdog mode
        2, if event WD2 occurs, the speed target value is changed to the WD safety speed limit and the temperature
        target value is change to the WD safety temperature limit value

        :param value: value between 20 and 1500 (units in seconds) - the watchdog time

        :return:
        """
        command = self.WATCHDOG_MODE_2 + value + ' '
        self._send(command=command)


class MagneticStirrerVisual(MagneticStirrer):
    """
    Subclass with additional functions to plot temperature over time graphs
    """
    _unit_seconds = datetimeManager._unit_seconds
    _unit_minutes = datetimeManager._unit_minutes
    _unit_hours = datetimeManager._unit_hours

    def __init__(self,
                 device_port: str,
                 save_folder: Path = None,
                 datetime_format: str = datetimeManager._default_datetime_format,
                 ):
        super().__init__(
            device_port=device_port,
            save_folder=save_folder,
            datetime_format=datetime_format,
        )
        self.figure, self.axes = plt.subplots(nrows=1, ncols=1)

    def graph_temperature_time(self,
                               x_axis_units: Union[_unit_seconds, _unit_minutes, _unit_hours] = _unit_minutes,
                               scatter: bool = False,
                               line: bool = True,
                               ) -> Figure:
        graph_title = 'Temperature over time'

        # axis names
        x_axis_name = None
        if x_axis_units == self._unit_seconds:
            x_axis_name = 'Time (s)'
        elif x_axis_units == self._unit_minutes:
            x_axis_name = 'Time (min)'
        elif x_axis_units == self._unit_hours:
            x_axis_name = 'Time (hour)'
        y_axis_name = 'Temperature (C)'

        times = self.temperature_data[x_axis_name].tolist()
        temperatures = self.temperature_data['Temperature (C)'].tolist()

        axes = self.axes
        figure = self.figure
        axes = plot_axes(axes=axes,
                         x=times,
                         y=temperatures,
                         axes_name=graph_title,
                         x_axis_label=x_axis_name,
                         y_axis_label=y_axis_name,
                         scatter=scatter,
                         line=line,
                         )
        return figure

    def graph_temperature_time_stable_visualization(self,
                                                    x_axis_units: Union[_unit_seconds, _unit_minutes, _unit_hours] = _unit_minutes,
                                                    scatter: bool = False,
                                                    line: bool = True,
                                                    ):
        n = self.n
        std_max = self.std_max
        sem_max = self.sem_max
        upper_limit = self.upper_limit
        lower_limit = self.lower_limit
        r_min = self.r_min
        slope_upper_limit = self.slope_upper_limit
        slope_lower_limit = self.slope_lower_limit

        figure = self.graph_temperature_time(x_axis_units=x_axis_units,
                                             scatter=scatter,
                                             line=line,
                                             )

        # axis names
        x_axis_name = None
        if x_axis_units == self._unit_seconds:
            x_axis_name = 'Time (s)'
        elif x_axis_units == self._unit_minutes:
            x_axis_name = 'Time (min)'
        elif x_axis_units == self._unit_hours:
            x_axis_name = 'Time (hour)'

        times = self.temperature_data[x_axis_name].tolist()
        x_values = times
        temperatures = self.temperature_data['Temperature (C)'].tolist()
        y_values = temperatures

        axes = figure.axes[0]
        y_max = max(temperatures)
        y_min = min(temperatures)

        total_range = y_max - y_min
        if upper_limit < 1 and self.relative_limits is True:
            upper_limit = self.upper_limit * total_range
        if lower_limit < 1 and self.relative_limits is True:
            lower_limit = self.lower_limit * total_range

        for temperature in self.set_temperatures:
            plateau_points: List[Tuple] = find_stable_against_known_custom_one_window(
                x=x_values,
                y=y_values,
                window_size=n,
                known=temperature,
                upper_limit=upper_limit,
                lower_limit=lower_limit,
                std_max=std_max,
                sem_max=sem_max,
                r_min=r_min,
                slope_upper_limit=slope_upper_limit,
                slope_lower_limit=slope_lower_limit,
            )
            axes = plot_plateau(
                axes=axes,
                plateau_points=plateau_points,
                y_min=y_min,
                y_max=y_max
            )

        return figure

    def save_graph_stable_visualized(self,
                                     file_name: str = None,
                                     ):
        figure = self.graph_temperature_time_stable_visualization()
        self.save_graph(figure=figure, file_name=file_name)

    def save_graph(self,
                   figure: Figure = None,
                   file_name: str = None,
                   ) -> Path:
        """
        Save the graph as a png

        :param matplotlib.figure.Figure, figure:
        :param str, file_name: title for the graph file

        :return:
        """
        if figure is None:
            figure = self.graph_temperature_time()
        if file_name is None:
            file_name = 'ika_temperature_time_graph.png'
        if file_name[-4:] != '.png':
            file_name += '.png'
        graph_save_path: Path = self.save_path.joinpath(file_name)
        figure.savefig(f'{str(graph_save_path)}', bbox_inches='tight')
        return graph_save_path


class MockMagneticStirrer(MagneticStirrer):
    """
    A mock class of the magnetic stirrer class to test things out without having to connect to one. All commands
    will now instead log
    """

    def __init__(self):
        logger.debug(f'created a mock IKA magnetic stirrer')

        self._heating: bool = False  # true if hot plate is heating
        self._stirring: bool = False  # true if hot plate is heating

    @property
    def heating(self) -> bool:
        return self._heating

    @heating.setter
    def heating(self, value: bool) -> None:
        if isinstance(value, bool) is False:
            raise TypeError('value must be of type bool')
        self._heating = value

    @property
    def stirring(self) -> bool:
        return self._stirring

    @stirring.setter
    def stirring(self, value: bool) -> None:
        if isinstance(value, bool) is False:
            raise TypeError('value must be of type bool')
        self._stirring = value

    def wait_until_temperature_stabilized(self):
        logger.debug('wait_until_temperature_stabilized')

    def read_device_name(self):
        logger.debug(f'read device name command sent, get back a string')

    def read_actual_external_sensor_value(self):
        logger.debug(f'read actual external sensor value command sent, get back a number')
        return random.randint(20, 25)

    def read_actual_hotplate_sensor_value(self):
        logger.debug(f'read actual hotplate sensor command sent, got back a number')
        return random.randint(20, 25)

    def read_stirring_speed_value(self):
        logger.debug(f'read stirring speed value command sent, got back a number')
        return random.randint(20, 25)

    def read_viscosity_trend_value(self):
        logger.debug(f'read viscosity trend value command sent, got back a number')
        return random.randint(20, 25)

    def read_rated_temperature_value(self):
        logger.debug(f'read rated temperature value command sent, got back a number')
        return random.randint(20, 25)

    def read_rated_set_safety_temperature_value(self):
        logger.debug(f'read rate set safety temperature value command sent, got back a number')
        return random.randint(20, 25)

    def read_rated_speed_value(self):
        logger.debug(f'read rate speed value command sent, got back a number')
        return random.randint(20, 25)

    def adjust_the_set_temperature_value(self):
        logger.debug(f'adjust the set temperature value command sent')

    def set_temperature_value(self,
                              value,
                              ):
        logger.debug(f'set temperature value to {value} command sent')

    def adjust_the_set_speed_value(self):
        logger.debug(f'adjust the set speed value command sent')

    def set_speed_value(self,
                        value,
                        ):
        logger.debug(f'set speed to {value} value command sent')

    def start_the_heater(self):
        logger.debug(f'start the heater command sent')
        self._heating = True

    def stop_the_heater(self):
        logger.debug(f'stop the heater command sent')
        self._heating = False

    def start_the_motor(self):
        logger.debug(f'start the motor command sent')
        self._stirring = True

    def stop_the_motor(self):
        logger.debug(f'stop the motor command sent')
        self._stirring = False

    def switch_to_normal_operating_mode(self):
        logger.debug(f'switch to normal operating mode command sent')

    def set_operating_mode_a(self):
        logger.debug(f'switch to a operating mode command sent')

    def set_operating_mode_b(self):
        logger.debug(f'switch to b operating mode command sent')

    def set_operating_mode_d(self):
        logger.debug(f'switch to d operating mode command sent')

    def set_wd_safety_limit_temperature(self,
                                        value: str,
                                        ):
        logger.debug(f'set wd safety limit temperature to {value} command sent')

    def set_wd_safety_limit_speed(self,
                                  value,
                                  ):
        logger.debug(f'set wd safety limit speed to {value} command sent')

    def watchdog_mode_1(self,
                        value,
                        ):
        """
        This command launches the watchdog function and must be transmitted within the set watchdog time.
        in watchdog mode 1, if event WD1 occurs, the heating and stirring functions are switched off and ER 2 is
        displayed

        :param value: value between 20 and 1500 (units in seconds) - the watchdog time

        :return:
        """
        logger.debug(f'set watchdog mode 1 with value {value} command sent')

    def watchdog_mode_2(self,
                        value: str,
                        ):
        """
        This command launches the watchdog function and must be transmitted within the set watchdog time. the WD2
        event can be reset with the command "OUT_WD2@0", and this also stops the watchdog function.  in watchdog mode
        2, if event WD2 occurs, the speed target value is changed to the WD safety speed limit and the temperature
        target value is change to the WD safety temperature limit value

        :param value: value between 20 and 1500 (units in seconds) - the watchdog time

        :return:
        """
        logger.debug(f'set watchdog mode 2 with value {value} command sent')


