"""utility class for parsing and manipulating datetime objects"""
from datetime import datetime
from datetime import timedelta
from typing import List, Union
import warnings


class datetimeManager:
    _unit_seconds = 'seconds'
    _unit_minutes = 'minutes'
    _unit_hours = 'hours'
    _time_units = {0: _unit_seconds,
                   1: _unit_minutes,
                   2: _unit_hours,
                   }

    _reverse_time_units = dict((v, k) for k, v in _time_units.items())
    _default_datetime_format = '%Y_%m_%d_%H_%M_%S'  # to add in milliseconds, add %f

    def __init__(self,
                 string_format: str = _default_datetime_format,
                 ):
        """
        utility class for parsing and manipulating datetime objects

        :param string_format: datetime string format to use for parsing
        """
        self._string_format = string_format

    @property
    def string_format(self) -> str:
        return self._string_format

    @string_format.setter
    def string_format(self,
                      value: str,
                      ):
        if isinstance(value, str) is False:
            raise TypeError('value must be of type string')
        self._string_format = value

    @string_format.deleter
    def string_format(self) -> None:
        self._string_format = None

    @classmethod
    def str_to_datetime(cls,
                        *string_values: str,
                        datetime_format: str = None,
                        ) -> List[datetime]:
        """
        Convert a list of string values, back into datetime objects with a specific format; in this case, the string has
        to have been a datetime object that was converted into a string with the datetime_format that is passed in this
        function.

        Main use has previously been when files where timestamped, and when the file names need to be converted back
        into datetime objects in order to do calculations

        :param string_values: one or more (a list) of strings that can be converted into datetime objects
        :param str, datetime_format: a string to represent the datetime format the string should be converted into; it
            should also have been the format that the strings already are in
        :return:
        """
        if datetime_format is None:
            datetime_format = cls._default_datetime_format
        return [datetime.strptime(value, datetime_format) for value in string_values]

    @classmethod
    def relative_datetime(cls,
                          datetime_objects: List[datetime],
                          units: Union[_unit_seconds, _unit_minutes, _unit_hours] = None,
                          rounding: int = None,
                          ) -> List[timedelta]:
        """
        Convert an array of datetime objects that are absolute times, and return an array where all the times in the
        array are relative to the first time in the array. The relativity can be in seconds, minutes, or hours.

        :param datetime_objects: a list of datetime objects
        :param units: one of _unit_seconds, _unit_minutes, or _unit_hours
        :param int, rounding: the number of decimal places to round to
        :return:
        """
        # takes a list of datetime objects, and makes all the values relative to the first object in the list
        if units not in list(cls._time_units.values()):
            raise Exception(f'units must be one of: {list(cls._time_units.values())}')

        if units is None:
            units = cls._unit_seconds

        # make an array of timedelta objects where each value is the difference between the actual time relative to
        # the first time point
        array_of_datetime_timedelta = [datetime_value - datetime_objects[0] for datetime_value in
                                       datetime_objects]

        # convert the relative timedeltas to floats, where the float number is the number of seconds since the first
        # time point
        array_of_relative_x_in_seconds = [array_of_datetime_timedelta[index].total_seconds() for index
                                          in range(len(array_of_datetime_timedelta))]

        if units == cls._unit_seconds:
            array_of_relative_datetime_objects = array_of_relative_x_in_seconds
        elif units == cls._unit_minutes:
            array_of_relative_x_in_minutes = [array_of_relative_x_in_seconds[index] / 60.0 for index in
                                              range(len(array_of_relative_x_in_seconds))]
            array_of_relative_datetime_objects = array_of_relative_x_in_minutes
        elif units == cls._unit_hours:
            array_of_relative_x_in_hours = [array_of_relative_x_in_seconds[index] / 3600.0 for index in
                                            range(len(array_of_relative_x_in_seconds))]
            array_of_relative_datetime_objects = array_of_relative_x_in_hours

        if rounding is not None:
            array_of_relative_datetime_objects = [round(datetime_obj, rounding) for datetime_obj in
                                                  array_of_relative_datetime_objects]

        return array_of_relative_datetime_objects

    def now_string(self) -> str:
        """
        Get the current time from datetime.now() formatted as as a string according to the string_format property
        :return:
        """
        return datetime.now().strftime(self.string_format)


def array_of_str_to_array_of_datetime_objects(list_of_string_values,
                                              datetime_format: str = '%Y_%m_%d_%H_%M_%S',
                                              ) -> List[datetime]:
    """
    Legacy passthrough for deprecated function. Use the datetimeManager class method instead.
    """
    warnings.warn(  # v3.7.1
        'This method has been deprecated, use the class method in the datetimeManager class; use that instead',
        DeprecationWarning,
        stacklevel=2,
    )


def array_of_datetime_objects_to_array_of_relative_datetime_objects(array_of_datetime_objects,
                                                                    units,
                                                                    ) -> List[timedelta]:
    """
    Legacy passthrough for deprecated function. Use the datetimeManager class method instead.
    """
    warnings.warn(  # v3.7.1
        'This method has been deprecated, use the class method in the datetimeManager class; use that instead',
        DeprecationWarning,
        stacklevel=2,
    )







