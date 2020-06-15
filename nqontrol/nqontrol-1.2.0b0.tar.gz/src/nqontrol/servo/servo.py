"""Servo class."""
# pylint: disable=too-many-lines
import json
import logging as log
import multiprocessing as mp
from math import copysign
from time import sleep, time
from typing import Optional

import jsonpickle
import numpy as np
from ADwin import ADwinError
from matplotlib import pyplot as plt
from openqlab.analysis.servo_design import ServoDesign
from pandas import DataFrame
from scipy.signal import find_peaks

from nqontrol.general import helpers, settings
from nqontrol.general.errors import (
    AutoLockAnalysisError,
    Bug,
    ConfigurationError,
    DeviceError,
    UserInputError,
)
from nqontrol.general.helpers import (
    convertFloat2Volt,
    convertFrequency2Stepsize,
    convertStepsize2Frequency,
    convertVolt2Float,
    rearrange_filter_coeffs,
)

from .feedbackController import FeedbackController


class Servo:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    Servo object that communicates with a control channel of the ADwin.

    `readFromFile` overwrites all other parameters.

    Parameters
    ----------
    channel: :obj:`int`
        Channel used vor the Servo.
        Possible is `1..8`
        Channel number is used for input,
        output and process number
    adw: :obj:`ADwin`
        For all servos of a :obj:`ServoDevice` to use the same
        :obj:`ADwin` object,
        it is necessary to pass an ADwin object.
    applySettings: :obj:`str` or `dict`
        Apply settings directly from file or dict.
    offset: :obj:`offset`
        Overall offset.
    gain: :obj:`float`

    filters: 5 * 5 :obj:`list`
        Filter coefficient matrix. Default is a 0.0 matrix.
    name: :obj:`str`
        Choose an optional name for this servo.

    """

    _DONT_SERIALIZE = [
        "_manager",
        "_adw",
        "_subProcess",
        "_fifoBuffer",
        "_tempFeedback",
    ]
    REALTIME_DICTS = ["realtime", "_fifo"]
    _JSONPICKLE = ["servoDesign"]
    _MIN_REFRESH_TIME = 0.02
    _DEFAULT_FILTERS = [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ]
    DEFAULT_COLUMNS = ["input", "aux", "output"]
    _manager = mp.Manager()
    realtime = _manager.dict(
        {"enabled": False, "ydata": DEFAULT_COLUMNS, "ylim": None, "refreshTime": 0.1}
    )
    DEFAULT_FIFO_STEPSIZE = 10
    """
    Control realtime plotting.

    .. code:: python

        realtime = {
            'enabled': False,
            'ydata': ['input', 'aux', 'output'],
            'ylim': None,
            'refreshTime': 0.1,
        }
    """

    ########################################
    # Predefined methods
    ########################################
    def __init__(  # pylint: disable=too-many-arguments
        self,
        channel,
        adw,
        applySettings=None,
        offset=0.0,
        gain=1.0,
        filters=None,
        name=None,
    ):
        """
        Create the servo object, also on ADwin.

        `readFromFile` overwrites all other parameters.

        Parameters
        ----------
        deviceNumber: Number of the ADwin-Pro device.
        channel:      Channel used for the Servo.
                      Possible is `1..8`
                      Channel number is used for input,
                      output and process number
        offset=0.0:   Overall offset
        filters:      Filter coefficient matrix. Default is a 0.0 matrix.

        """
        MAX_CHANNELS = 8

        if not 1 <= channel <= MAX_CHANNELS:
            raise ValueError(f"There are max {MAX_CHANNELS} channels.")
        self._channel = channel
        if name is None:
            self.name = "Servo " + str(channel)
        else:
            self.name = name
        if filters is None:
            filters = self._DEFAULT_FILTERS

        # State dictionaries
        self._state = dict(
            {
                # Control parameters
                "offset": offset,
                "gain": gain,
                "filters": filters,
                "inputSensitivity": 0,
                "auxSensitivity": 0,
                # Control flags
                "filtersEnabled": [False] * 5,
                "auxSw": False,
                "offsetSw": False,
                "outputSw": False,
                "inputSw": False,
                # 'snapSw': False,
            }
        )
        self._autolock = dict(
            {
                "search": 0,
                "locked": 0,
                "relock": 0,
                "greater": 1,
                "rampmode": 0,
                "threshold": 0,
                "threshold_break": 0,
                "amplitude": 10,
                "offset": 0,
                "stepsize": convertFrequency2Stepsize(30),
            }
        )
        self._fifo = self._manager.dict({"stepsize": self.DEFAULT_FIFO_STEPSIZE})
        if settings.FIFO_MAXLEN * 2 > settings.FIFO_BUFFER_SIZE:
            raise ConfigurationError(
                "FIFO_BUFFER_SIZE must be at least twice as big as _fifo['maxlen']."
            )
        self._fifoBuffer = None
        self._subProcess = None

        # has to be initalized as None / could maybe include in the loading?
        self._tempFeedback = None
        self._tempFeedbackSettings = self._manager.dict(
            {"dT": None, "mtd": None, "update_interval": 1, "voltage_limit": 5}
        )

        # ServoDesign object
        self.servoDesign: ServoDesign = ServoDesign()

        # Use adwin object
        self._adw = adw

        # initialize lock values

        try:
            if applySettings:
                # loadSettings calls `_sendAllToAdwin()`
                self.loadSettings(applySettings)
            else:
                self._sendAllToAdwin()
                self._sendLockControl()
                self._initLockValues()
        except ADwinError as e:
            log.error(f"{e} Servo {self._channel}: Couldn't write to ADwin.")

    def __repr__(self):
        """Name of the object."""
        return f"Name: {self.name}, channel: {self._channel}"

    ########################################
    # Help methods
    ########################################

    def _sendAllToAdwin(self):
        """Write all settings to ADwin."""
        # Control parameters
        self.offset = self._state["offset"]
        self.gain = self._state["gain"]
        self.filters = self._state["filters"]
        self.inputSensitivity = self._state["inputSensitivity"]
        self.auxSensitivity = self._state["auxSensitivity"]

        self._sendLockControl()
        # Control flags
        self._sendFilterControl()

    def _readAllFromAdwin(self):
        self._readFilterControl()
        _ = self.offset
        _ = self.gain
        _ = self.filters
        _ = self.inputSensitivity
        _ = self.auxSensitivity

    def _triggerReload(self):
        """Trigger bit to trigger reloading of parameters."""
        par = self._adw.Get_Par(settings.PAR_RELOADBIT)
        # only trigger if untriggered
        if not helpers.readBit(par, self._channel - 1):
            par = helpers.changeBit(par, self._channel - 1, True)
            self._adw.Set_Par(settings.PAR_RELOADBIT, par)
        else:
            raise DeviceError(
                "ADwin has been triggered to reload the shared RAM within 10µs or the realtime program doesn't run properly."
            )

    def _readFilterControl(self):
        c = self._adw.Get_Par(settings.PAR_FCR + self._channel)
        # read control bits
        self._state["auxSw"] = helpers.readBit(c, 9)
        for i in range(5):
            bit = helpers.readBit(c, 4 + i)
            self._state["filtersEnabled"][i] = bit
            assert (
                list(self._state["filtersEnabled"])[i] == bit
            ), f'dict: {list(self._state["filtersEnabled"])[i]}, bit: {bit}'
        # self._state['snapSw'] = helpers.readBit(c, 3)
        self._state["offsetSw"] = helpers.readBit(c, 2)
        self._state["outputSw"] = helpers.readBit(c, 1)
        self._state["inputSw"] = helpers.readBit(c, 0)

    def _sendFilterControl(self):
        # read current state
        c = self._adw.Get_Par(settings.PAR_FCR + self._channel)

        # set control bits
        c = helpers.changeBit(c, 9, self._state["auxSw"])
        for i in range(5):
            c = helpers.changeBit(c, 4 + i, self._state["filtersEnabled"][i])
        # c = helpers.changeBit(c, 3, self._state['snapSw'])
        c = helpers.changeBit(c, 2, self._state["offsetSw"])
        c = helpers.changeBit(c, 1, self._state["outputSw"])
        c = helpers.changeBit(c, 0, self._state["inputSw"])

        self._adw.Set_Par(settings.PAR_FCR + self._channel, c)

    @property
    def channel(self):
        return self._channel

    ########################################
    # Change servo state
    ########################################

    @property
    def filterStates(self):
        """
        List of all filter states.

        :getter: Return the filter states.
        :setter: Set all filter states.
        :type: :obj:`list` of :code:`5*`:obj:`bool`.
        """
        self._readFilterControl()
        return self._state["filtersEnabled"]

    @filterStates.setter
    def filterStates(self, filtersEnabled):
        self._state["filtersEnabled"] = filtersEnabled
        self._sendFilterControl()

    def filterState(self, id_, enabled):
        """Enable or disable the SOS filter with number `id_`.

        Parameters
        ----------
        id_: :obj:`int` index from 0 to 4
            Index of the filter to control.
        enabled: :obj:`bool`
            :obj:`True` to enable.

        """
        filtersEnabled = self._state["filtersEnabled"]
        filtersEnabled[id_] = enabled
        self._state["filtersEnabled"] = filtersEnabled
        self._sendFilterControl()

    @property
    def auxSw(self):
        """
        Switch for mixing the aux signal to the output.

        :getter: Return the state of aux mixing.
        :setter: Enable or disable the aux mixing.
        :type: :obj:`bool`
        """
        self._readFilterControl()
        return self._state["auxSw"]

    @auxSw.setter
    def auxSw(self, enabled):
        self._state["auxSw"] = enabled
        self._sendFilterControl()

    @property
    def offsetSw(self):
        """
        Enable or disable offset switch.

        :getter: Return the state of the switch.
        :setter: Enable or disable the offset.
        :type: :obj:`bool`
        """
        self._readFilterControl()
        return self._state["offsetSw"]

    @offsetSw.setter
    def offsetSw(self, enabled):
        self._state["offsetSw"] = enabled
        self._sendFilterControl()

    @property
    def outputSw(self):
        """
        Enable or disable output switch.

        :getter: Return the state of the switch.
        :setter: Enable or disable the output.
        :type: :obj:`bool`
        """
        self._readFilterControl()
        return self._state["outputSw"]

    @outputSw.setter
    def outputSw(self, enabled):
        self._state["outputSw"] = enabled
        self._sendFilterControl()

    @property
    def inputSw(self):
        """
        Enable or disable input switch.

        :getter: Return the state of the switch.
        :setter: Enable or disable the input.
        :type: :obj:`bool`
        """
        self._readFilterControl()
        return self._state["inputSw"]

    @inputSw.setter
    def inputSw(self, enabled):
        self._state["inputSw"] = enabled
        self._sendFilterControl()

    @property
    def offset(self):
        """
        Offset value in volt. (-10 to 10)

        :getter: Return the offset value.
        :setter: Set the offset.
        :type: :obj:`float`
        """
        index = self._channel + 8
        data = self._adw.GetData_Double(settings.DATA_OFFSETGAIN, index, 1)[0]
        offset = convertFloat2Volt(data, self.inputSensitivity, signed=True)
        self._state["offset"] = offset

        return offset

    @offset.setter
    def offset(self, offset: float):
        limit = round(10 / pow(2, self.inputSensitivity), 2)
        if abs(offset) > limit:
            offset = copysign(limit, offset)
            log.warning(
                f"With the selected mode the offset must be in the limits of ±{limit}V. Adjusting to {offset}V..."
            )
        self._state["offset"] = offset
        index = self._channel + 8
        offsetInt = convertVolt2Float(offset, self.inputSensitivity, signed=True)
        self._adw.SetData_Double([offsetInt], settings.DATA_OFFSETGAIN, index, 1)

    @property
    def gain(self):
        """
        Overall gain factor.

        :getter: Return the gain value.
        :setter: Set the gain.
        :type: :obj:`float`
        """
        index = self._channel
        data = self._adw.GetData_Double(settings.DATA_OFFSETGAIN, index, 1)[0]
        gain = data * pow(2, self.inputSensitivity)
        self._state["gain"] = gain

        return gain

    @gain.setter
    def gain(self, gain):
        self._state["gain"] = gain
        index = self._channel
        effectiveGain = gain / pow(2, self.inputSensitivity)
        self._adw.SetData_Double([effectiveGain], settings.DATA_OFFSETGAIN, index, 1)

    @property
    def inputSensitivity(self):
        r"""
        Input sensitivity mode (0 to 3).

        The input voltage is amplified by :math:`2^\mathrm{mode}`.

        +------+---------------+------------+
        | mode | amplification | limits (V) |
        +======+===============+============+
        | 0    | 1             | 10         |
        +------+---------------+------------+
        | 1    | 2             | 5          |
        +------+---------------+------------+
        | 2    | 4             | 2.5        |
        +------+---------------+------------+
        | 3    | 8             | 1.25       |
        +------+---------------+------------+

        :getter: Return the sensitivity mode.
        :setter: Set the mode.
        :type: :obj:`int`
        """
        data = self._adw.Get_Par(settings.PAR_SENSITIVITY)
        mask = 3
        # bit shifting backwards
        mode = data >> self._channel * 2 - 2 & mask
        self._state["inputSensitivity"] = mode

        return mode

    @inputSensitivity.setter
    def inputSensitivity(self, mode):
        if not 0 <= mode <= 3:
            raise ValueError("Choose a mode between 0 and 3")
        gain = self.gain
        offset = self.offset

        self._state["inputSensitivity"] = mode

        currentRegister = self._adw.Get_Par(settings.PAR_SENSITIVITY)
        register = helpers.clearBit(currentRegister, self._channel * 2 - 2)
        register = helpers.clearBit(register, self._channel * 2 - 1)

        # bit shifting
        register += mode << self._channel * 2 - 2

        self._adw.Set_Par(settings.PAR_SENSITIVITY, register)

        # Update gain to correct gain change from input sensitivity
        self.gain = gain
        self.offset = offset

    @property
    def auxSensitivity(self):
        r"""
        Aux sensitivity mode (0 to 3).

        The input voltage is amplified by :math:`2^\mathrm{mode}`.

        +------+---------------+------------+
        | mode | amplification | limits (V) |
        +======+===============+============+
        | 0    | 1             | 10         |
        +------+---------------+------------+
        | 1    | 2             | 5          |
        +------+---------------+------------+
        | 2    | 4             | 2.5        |
        +------+---------------+------------+
        | 3    | 8             | 1.25       |
        +------+---------------+------------+

        :getter: Return the sensitivity mode.
        :setter: Set the mode.
        :type: :obj:`int`
        """

        data = self._adw.Get_Par(settings.PAR_SENSITIVITY)
        mask = 3
        # bit shifting backwards
        mode = data >> self._channel * 2 + 14 & mask
        self._state["auxSensitivity"] = mode

        return mode

    @auxSensitivity.setter
    def auxSensitivity(self, mode):
        if not 0 <= mode <= 3:
            raise ValueError(f"Choose a mode between 0 and 3, was {mode}.")

        # saving old lock parameters
        threshold = self.lockThreshold
        threshold_break = self.lockThresholdBreak

        self._state["auxSensitivity"] = mode

        currentRegister = self._adw.Get_Par(settings.PAR_SENSITIVITY)
        register = helpers.clearBit(currentRegister, self._channel * 2 + 14)
        register = helpers.clearBit(register, self._channel * 2 + 15)

        register += mode << self._channel * 2 + 14

        self._adw.Set_Par(settings.PAR_SENSITIVITY, register)

        # setting lock parameters with new sensitivity
        self.lockThreshold = threshold
        self.lockThresholdBreak = threshold_break

    @property
    def filters(self):
        """
        All second order sections (SOS) of all filters.

        A neutral filter matrix looks like:

        .. code:: python

            [ [1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0] ]

        Use :obj:`ServoDesign` from :obj:`openqlab.analysis` to create your filters.
        That object you can simply pass to a servo using :obj:`applyServoDesign`.

        :getter: Return all filter values.
        :setter: Write all 5 filters to ADwin and trigger reloading.
        :type: :code:`(5, 5)` matrix with filter values (:obj:`float`).
        """
        startIndex = (
            self._channel - 1
        ) * settings.NUMBER_OF_FILTERS * settings.NUMBER_OF_SOS + 1

        data = self._adw.GetData_Double(
            settings.DATA_FILTERCOEFFS,
            startIndex,
            settings.NUMBER_OF_FILTERS * settings.NUMBER_OF_SOS,
        )

        for i in range(settings.NUMBER_OF_FILTERS):
            for j in range(settings.NUMBER_OF_SOS):
                self._state["filters"][i][j] = data[i * settings.NUMBER_OF_FILTERS + j]

        return list(self._state["filters"])

    @filters.setter
    def filters(self, filters):
        if not len(filters) == settings.NUMBER_OF_FILTERS:
            raise IndexError(
                f"A servo must have exactly {settings.NUMBER_OF_FILTERS} filters!"
            )
        for filter_ in filters:
            if not len(filter_) == settings.NUMBER_OF_SOS:
                raise IndexError(
                    f"A servo must have exactly {settings.NUMBER_OF_FILTERS} filters with {settings.NUMBER_OF_SOS} SOS!"
                )

        self._state["filters"] = filters

        startIndex = (
            self._channel - 1
        ) * settings.NUMBER_OF_FILTERS * settings.NUMBER_OF_SOS + 1

        data = []
        for filter_ in filters:
            for i in filter_:
                data.append(i)
        self._adw.SetData_Double(
            data, settings.DATA_FILTERCOEFFS, startIndex, len(data)
        )
        self._triggerReload()

    def applyServoDesign(self, servoDesign=None):
        """
        Apply filters from a :obj:`ServoDesign` object.

        Parameters
        ----------
        servoDesign: :obj:`openqlab.analysis.ServoDesign`
            Object to apply filters from.
        """
        if servoDesign is None:
            servoDesign = self.servoDesign
        else:
            self.servoDesign = servoDesign
        discreteServoDesign = servoDesign.discrete_form(
            sampling_frequency=settings.SAMPLING_RATE
        )
        filters6 = discreteServoDesign["filters"]  # returns a list of dicts
        filters = [[1.0, 0, 0, 0, 0]] * servoDesign.MAX_FILTERS
        filtersEnabled = [False] * servoDesign.MAX_FILTERS

        for f in filters6:
            j = f["index"]
            filters[j] = rearrange_filter_coeffs(f["sos"])
            filtersEnabled[j] = f["enabled"]

        self.gain = discreteServoDesign["gain"]
        self.filters = filters
        self.filterStates = filtersEnabled

    ##############################################################
    #####################   Autolock   ###########################
    ##############################################################

    ###################   Lock helpers   #########################

    def _lockIter(self):
        # just a helper method to expose the lockIterator for testing

        lockIter = self._adw.GetData_Double(settings.DATA_LOCK_ITER, self._channel, 1)[
            0
        ]
        return lockIter

    def _testLockOutput(self):
        # a helper to expose the last output used in locking
        # specifically, when locked this is the output value added to the lockIter of where the lock was found, meaning the new output is set as
        # out_new = lockIter + out_old
        # it is this out_old we wish to expose
        testOutput = self._adw.GetData_Long(
            settings.DATA_LOCK_OUTPUT, self._channel, 1
        )[0]
        testOutput = convertFloat2Volt(testOutput, self.auxSensitivity, signed=False)
        return testOutput

    ###################   Lock control   #########################

    def _readLockControl(self):
        # boolean values
        lcr = self._adw.Get_Par(settings.PAR_LCR)
        gcr = self._adw.Get_Par(settings.PAR_GCR)
        log.debug(bin(lcr))
        bitoffset = self._channel - 1
        self._autolock["search"] = helpers.readBit(lcr, bitoffset)
        self._autolock["locked"] = helpers.readBit(lcr, bitoffset + 8)
        self._autolock["relock"] = helpers.readBit(lcr, bitoffset + 16)
        self._autolock["greater"] = helpers.readBit(gcr, self._channel - 1)
        self._autolock["rampmode"] = helpers.readBit(gcr, 8 + self._channel - 1)
        log.debug(
            f"Read out lock pars on servo {self._channel}: lcr {bin(lcr)} and {bin(gcr)}."
        )

    def _sendLockControl(self):
        # this send the control register and greater boolean
        lcr = self._adw.Get_Par(settings.PAR_LCR)
        gcr = self._adw.Get_Par(settings.PAR_GCR)
        bitoffset = self._channel - 1
        # search bit
        lcr = helpers.changeBit(lcr, bitoffset, self._autolock["search"])
        # locked bit
        lcr = helpers.changeBit(lcr, bitoffset + 8, self._autolock["locked"])
        # relock bit
        lcr = helpers.changeBit(lcr, bitoffset + 16, self._autolock["relock"])
        # greater bit
        gcr = helpers.changeBit(gcr, (self._channel - 1), self._autolock["greater"])
        # rampmode bit
        gcr = helpers.changeBit(
            gcr, 8 + (self._channel - 1), self._autolock["rampmode"]
        )
        log.debug(
            f"Sending lock pars on servo {self._channel}: lcr {bin(lcr)} and gcr {bin(gcr)}."
        )
        self._adw.Set_Par(settings.PAR_LCR, lcr)
        self._adw.Set_Par(settings.PAR_GCR, gcr)

    @property
    def lockSearch(self):
        """Return the lock search state. Don't confuse with `locked`.

        `0`: off
        `1`: search

        :getter: Trigger a read from ADwin. Return current value.
        :setter: Set new lock state. Will convert given value to bool and then back to int.
        :type: :obj:`int`

        """
        self._readLockControl()
        return self._autolock["search"]

    @lockSearch.setter
    def lockSearch(self, search):
        if not isinstance(search, (int, bool)):
            raise TypeError("Must be given as either an integer or a boolean.")
        search = int(bool(search))
        if search:
            # disabling input, output and aux while searching
            self.outputSw = False
            self.inputSw = False
            self.auxSw = False
            self._autolock["locked"] = 0
        self._autolock["search"] = search
        self._sendLockControl()

    @property
    def locked(self):
        """Return the locked state. Whether the servo is currently in locked state.

        `0`: not locked
        `1`: locked

        :getter: Trigger a read from ADwin. Return current value.
        :setter: Set new locked state. Will convert given value to bool and then back to int. Really only makes sense to turn this off manually, not on. Still, when manually switching on, will make sure to turn off lock search.
        :type: :obj:`int`

        """
        self._readLockControl()
        return self._autolock["locked"]

    @locked.setter
    def locked(self, locked):
        if not isinstance(locked, (int, bool)):
            raise TypeError(
                f"Must be given as either an integer or a boolean, was {locked}."
            )
        locked = int(bool(locked))
        if locked:
            self._autolock["search"] = 0
        self._autolock["locked"] = locked
        self._sendLockControl()

    @property
    def relock(self):
        """
        Set the lock to trigger a relock automatically when falling below or above threshold (according to `greater` setting). The `relock` parameter is either 0 or 1, can also be passed as a boolean.

        :getter: Return the current value.
        :setter: Set the condition.
        :type: :obj:`int`
        """
        self._readLockControl()
        return self._autolock["relock"]

    @relock.setter
    def relock(self, relock):
        if not isinstance(relock, (int, bool)):
            raise TypeError(
                f"Must be given as either an integer or a boolean, was {relock}."
            )
        relock = int(bool(relock))
        self._autolock["relock"] = relock
        self._sendLockControl()

    @property
    def lockGreater(self):
        """
        Set the lock direction to either greater (True) or lesser (False) than the threshold.

        :getter: Return the current value.
        :setter: Set the condition.
        :type: :obj:`bool`
        """
        self._readLockControl()
        return self._autolock["greater"]

    @lockGreater.setter
    def lockGreater(self, greater):
        if not isinstance(greater, (int, bool)):
            raise TypeError(
                f"Must be given as either an integer or a boolean, was {greater}."
            )
        greater = int(bool(greater))
        self._autolock["greater"] = greater
        self._sendLockControl()

    @property
    def lockRampmode(self):
        """Enable rampmode bit for lock function. If in ramp mode, the autolock will keep searching even if a lock is found. This replaces the previous ramp.

        :getter: Return current rampmode bit.
        :setter: Set rampmode bit True or False.
        :type: :obj:`bool`
        """
        self._readLockControl()
        return self._autolock["rampmode"]

    @lockRampmode.setter
    def lockRampmode(self, ramp):
        if not isinstance(ramp, (int, bool)):
            raise TypeError(
                f"Must be given as either an integer or a boolean, was {ramp}."
            )
        ramp = int(bool(ramp))
        self._autolock["rampmode"] = ramp
        self._sendLockControl()

    ###################   Lock values   #########################

    def _initLockValues(self):
        # split from _sendLockControl to avoid recursion
        # voltage values for the lock parameters
        self.lockThreshold = self._autolock["threshold"]
        self.lockThresholdBreak = self._autolock["threshold_break"]
        self.lockStepsize = self._autolock["stepsize"]
        self.lockAmplitude = self._autolock["amplitude"]
        self.lockOffset = self._autolock["offset"]

    @property
    def lockThreshold(self):
        """Get or set the autolock threshold.

        :getter: Trigger a read from ADwin. Return the threshold.
        :setter: Set the threshold.
        :type: :obj:`float`
        """
        # voltage values
        self._autolock["threshold"] = convertFloat2Volt(
            self._adw.GetData_Double(settings.DATA_LOCK, self._channel, 1)[0],
            self.auxSensitivity,
            signed=False,
        )
        return self._autolock["threshold"]

    @lockThreshold.setter
    def lockThreshold(self, threshold):
        try:
            threshold = float(threshold)
        except (ValueError, TypeError):
            raise TypeError(f"threshold must be a float or int, was {type(threshold)}.")
        self._autolock["threshold"] = threshold
        threshold = convertVolt2Float(threshold, self.auxSensitivity, signed=False)
        # Sending values to ADwin
        # threshold
        self._adw.SetData_Double([threshold], settings.DATA_LOCK, self._channel, 1)

    @property
    def lockThresholdBreak(self):
        """Get or set the autolock threshold break. This is the tolerance value for falling out of lock.

        :getter: Trigger a read from ADwin. Return the threshold break.
        :setter: Set the threshold break value.
        :type: :obj:`float`
        """
        # voltage values
        self._autolock["threshold_break"] = convertFloat2Volt(
            self._adw.GetData_Double(settings.DATA_LOCK, self._channel + 8, 1)[0],
            self.auxSensitivity,
            signed=False,
        )
        return self._autolock["threshold_break"]

    @lockThresholdBreak.setter
    def lockThresholdBreak(self, threshold):
        try:
            threshold = float(threshold)
        except (ValueError, TypeError):
            raise TypeError(
                f"threshold break must be a float or int, was {type(threshold)}."
            )
        self._autolock["threshold_break"] = threshold
        threshold = convertVolt2Float(threshold, self.auxSensitivity, signed=False)
        # Sending values to ADwin
        # threshold_break, same as threshold for now
        self._adw.SetData_Double([threshold], settings.DATA_LOCK, self._channel + 8, 1)

    @property
    def lockAmplitude(self):
        """Get or set the autolock ramp amplitude. A floating point number from 0 to 10 which will be multiplied to the normalized (-1 to 1 V) ramp.

        ramp_position = amplitude * iterator + offset

        :getter: Trigger a read from ADwin. Return the amplitude.
        :setter: Set the amplitude.
        :type: :obj:`float`
        """
        # voltage values
        self._autolock["amplitude"] = self._adw.GetData_Double(
            settings.DATA_LOCK, 16 + self._channel, 1
        )[0]
        return self._autolock["amplitude"]

    @lockAmplitude.setter
    def lockAmplitude(self, amplitude):
        try:
            amplitude = float(amplitude)
        except (ValueError, TypeError):
            raise TypeError(f"Amplitude must be a float or int, was {type(amplitude)}.")
        if not 0 <= amplitude <= 10:
            raise ValueError(
                f"Amplitude should be positive and in the range of 0 to 10 V, was {amplitude}."
            )
        self._autolock["amplitude"] = amplitude
        # amplitude is transferred directly and does not have to be converted
        self._adw.SetData_Double([amplitude], settings.DATA_LOCK, self._channel + 16, 1)

    @property
    def lockOffset(self):
        """Get or set the autolock ramp offset. A floating point number from -10 to 10 V which will be added to the ramp.

        ramp_position = amplitude * iterator + offset

        :getter: Trigger a read from ADwin. Return the offset.
        :setter: Set the offset.
        :type: :obj:`float`
        """
        # voltage values
        self._autolock["offset"] = convertFloat2Volt(
            self._adw.GetData_Double(settings.DATA_LOCK, 24 + self._channel, 1)[0],
            signed=False,
        )
        return self._autolock["offset"]

    @lockOffset.setter
    def lockOffset(self, offset):
        try:
            offset = float(offset)
        except (ValueError, TypeError):
            raise TypeError(f"Offset must be a float or int, was {type(offset)}.")
        if not -10 <= offset <= 10:
            raise ValueError(f"Offset can't be outside -10 and 10 volts, was {offset}.")
        self._autolock["offset"] = offset
        offset = convertVolt2Float(offset, signed=False)
        # Sending values to ADwin
        self._adw.SetData_Double([offset], settings.DATA_LOCK, self._channel + 24, 1)

    @property
    def lockStepsize(self):
        """Read out the autolock stepsize.

        Returns
        -------
        :obj:`int`
            Stepsize value.
        """
        self._autolock["stepsize"] = self._adw.GetData_Double(
            settings.DATA_LOCK_STEPSIZE, self._channel, 1
        )[0]
        return self._autolock["stepsize"]

    @lockStepsize.setter
    def lockStepsize(self, stepsize):
        if not isinstance(stepsize, (float)):
            raise TypeError(
                f"Ideally, pass the stepsize as a float, was {type(stepsize)}."
            )
        if (
            not convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)
            <= stepsize
            <= convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MAX)
        ):
            raise ValueError(
                f"Please make sure the stepsize is in the correct range of {convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)} to {convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MAX)}, was {stepsize}."
            )
        self._autolock["stepsize"] = stepsize
        self._adw.SetData_Double(
            [stepsize], settings.DATA_LOCK_STEPSIZE, self._channel, 1
        )
        self._updateFifoStepsize()

    @property
    def lockFrequency(self):
        """Rough frequency of the ramp, might contain rounding errors. Calculates the frequency from the stepsize and search range of the lock. If possible, use the stepsize directly!

        :getter: Set the frequency.
        :setter: Get the frequency.
        :type: :obj:`float`
        """
        return convertStepsize2Frequency(self.lockStepsize)

    @lockFrequency.setter
    def lockFrequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError(
                f"Please pass the frequency as a float (ideally) or integer, was {type(frequency)}."
            )
        if not settings.RAMP_FREQUENCY_MIN <= frequency <= settings.RAMP_FREQUENCY_MAX:
            raise ValueError(
                f"Please make sure the frequency is in the correct range of {settings.RAMP_FREQUENCY_MIN} to {settings.RAMP_FREQUENCY_MAX} Hz, was {frequency}."
            )
        self.lockStepsize = convertFrequency2Stepsize(frequency)

    ############   Autolock command line tools   ##############

    def autolock(  # pylint: disable=too-many-arguments
        self,
        search=True,
        relock=None,
        rampmode=None,
        amplitude=None,
        offset=None,
        frequency=None,
        analysis=True,
        **args,
    ):
        """Autolock activation for command line use. The user may pass options as additional arguments. For valid options see the signature of :obj:`Servo.autolockOptions`.

        Parameters
        ----------
        search : :obj:`bool`, optional
            Will trigger a new autolock search. If an integer is passed, it will be interpreted as a boolean value, by default True
        relock : :obj:`bool`, optional
            Whether relock feature should be active or inactive. Also see the documentation for :obj:`Servo.relock`, by default None
        rampmode : :obj:`bool`, optional
            Whether lock search should be in rampmode (won't snap to a lock point).
        amplitude : :obj:`float`, optional
            Autolock ramp amplitude, 0 to 10 V.
        offset : :obj:`float`, optional
            Autolock ramp offset, -10 to 10 V.
        frequency : obj:`int`, optional
            Lock ramp frequency. From {0} to {1}.
        analysis: :obj:`bool`, optional
            Whether to run the threshold analysis, by default True

        Returns
        -------
        :obj:`String`
            Information string as feedback.

        Raises
        ------
        TypeError
            The `search` keyword should be an integer (which translates to boolean) or boolean value.
        """.format(
            settings.RAMP_FREQUENCY_MIN, settings.RAMP_FREQUENCY_MAX
        )
        if not isinstance(search, (bool, int)):
            raise TypeError(
                f"Please make sure the search keyword is an integer or boolean, indicating whether to turn lock searching on or off. {search} was given."
            )
        search = int(bool(search))
        s = ""
        s += self._autolockOptions(
            relock, rampmode, amplitude, offset, frequency, **args
        )
        if analysis:
            self.lockAnalysis()
        self.lockSearch = search
        s += f"\nLOCK SEARCH STATUS: {self.lockSearch}."
        return s

    def _autolockOptions(  # pylint: disable=too-many-arguments
        self,
        relock=None,
        rampmode=None,
        amplitude=None,
        offset=None,
        frequency=None,
        **args,
    ):
        s = ""
        if relock is not None:
            self.relock = relock
            s += f"Set relock option: {self.relock}. "
        if rampmode is not None:
            self.lockRampmode = rampmode
            s += f"Set lock rampmode: {self.lockRampmode}. "
        if amplitude is not None:
            self.lockAmplitude = amplitude
            s += f"Changed lock amplitude: {self.lockAmplitude}. "
        if offset is not None:
            self.lockOffset = offset
            s += f"Changed lock offset: {self.lockOffset}. "
        if frequency is not None:
            self.lockFrequency = frequency
            s += f"Changed lock ramp frequency: {self.lockFrequency}. "
        if s == "":
            s += "No options changed. "
        if args:
            s += f"Additional arguments were passed that had no effect: {args}. "
        return s

    def enableRamp(self, amplitude=None, offset=None, frequency=None, enableFifo=True):
        """
        Enable the lock ramp on this servo. Intended for command line use.

        Parameters
        ----------
        amplitude : :obj:`float`, optional
            Ramp amplitude from 0 to 10 V. (0 does not make too much sense, though.) Default 1.
        offset : :obj:`float`, optional
            Ramp offset from -10 to 10 V. Default 0.
        frequency : :obj:`float`, optional
            Ramp frequency from 1 to 100 Hz. (Can be changed in settings.)
        enableFifo: :obj:`bool`
            Defaults to :obj:`True`.
            Possible not to enable the FIFO buffering for this servo.

        """
        self._readLockControl()

        if amplitude is not None:
            self.lockAmplitude = amplitude

        if offset is not None:
            self.lockOffset = offset

        if frequency is not None:
            self.lockFrequency = frequency

        self._autolock["rampmode"] = 1
        self._autolock["search"] = 1

        self._sendLockControl()

        if enableFifo:
            self.enableFifo(self._calculateFifoStepsize())

    def disableRamp(self):
        """Disable the ramp on this channel. Counterpart to `enableRamp`."""
        self._readLockControl()
        self._autolock["search"] = 0
        self._autolock["rampmode"] = 0
        self._sendLockControl()

    ##############   Autolock analysis tools   ################

    def _prepareLockData(self):
        self._readLockControl()
        # preserve old state
        old_search = self._autolock["search"]
        old_rampmode = self._autolock["rampmode"]
        old_ydata = self.realtime["ydata"]
        # turn everything off in case it's still running
        self.lockSearch = 0
        self.locked = 0
        # turn on the ramp and search again
        self.lockRampmode = 1
        # make sure aux is included
        self.realtime["ydata"] = self.DEFAULT_COLUMNS
        self.lockSearch = 1
        data = self.takeData()
        # set old values again
        self.lockSearch = old_search
        self.lockRampmode = old_rampmode
        self.realtime["ydata"] = old_ydata
        return data

    def lockAnalysis(self, testdata=None, raiseErrors: bool = False, tries: int = 10):
        """Analyze the threshold and direction to be used in the autolock feature. Takes in data or reads out automatically if None was provided. Determines the correct peak by analyzing median value of the AUX channel and comparing it to the signal's maxima and minima. A peak is deemed valid if it is sufficiently different from the median value. Generally, one would expect good peaks to be much bigger than white noise, thus we deem the analysis valid using a 3 sigma criteria.

        You can also use this in conjunction with the `autolock` command line method, e.g.

        ```python
        s = DEVICE.servo(1)
        s.lockAmplitude = 3
        s.lockOffset = -4
        s.lockFrequency = 3
        s.lockAnalysis()
        s.autolock()
        ```

        Parameters
        ----------
        testdata : :obj:`pandas.DataFrame`, optional
            For testing purposes one can provide a pandas DataFrame to be analyzed. Please make sure it contains a 'aux' column. If no data is provided, it will be read out from ADwin. (by default None)
        raiseErrors : bool, optional
            Can raise errors instead of logs for testing purposes. (by default False)
        """
        for n in range(tries):
            # take in new data
            if testdata is None:
                data = self._prepareLockData()
            else:
                data = testdata

            log.info(f"data columns {data.columns}")

            if data.empty:
                if n == tries - 1:
                    w = "Could not take data. Something might be wrong!"
                    if raiseErrors:
                        raise DeviceError(w)
                    log.warning(w)
                    return
                continue

            aux = data["aux"]
            # how do we check whether there is a meaningful peak?
            # if there is one as we expect it should be pretty simple
            # most values are going to be similar, except for peaks, therefore we use the median:
            median = aux.median()
            # now check the absolute differences of minima and maxima to find peaks
            absmin = np.abs(median - aux.min())
            absmax = np.abs(median - aux.max())
            # in any good signal there should be a significant difference between these distances
            # if not, you're probably looking at white noise
            if np.abs(absmin - absmax) > 5 * aux.std():
                break

            log.warning(f"Try {n+1}...")
            if n == tries - 1:
                log.warning("ABORTING: Could not find reasonable peak in 10 tries.")
                w = f"""Could not find a reasonable threshold, as distances of minimum and maximum are very close (within five standard deviations).
                    Values of last try:
                    Distance of minimum to median: {absmin:3f}
                    Distance of maximum to median: {absmax:3f}
                    Difference of the two: {np.abs(absmin - absmax):3f}
                    5 Std: {5*aux.std():3f}
                    Values remain unchanged: treshold {self._autolock["threshold"]} break {self._autolock["threshold_break"]} greater {self._autolock["greater"]}
                    """
                log.warning(w)
                if raiseErrors:
                    raise AutoLockAnalysisError(w)
                return

        # check peak direction
        if absmin > absmax:  # the peaks are minima
            # use the minimum as threshold, add some low percentage tolerance to the values
            self.lockGreater = 0
            self.lockThreshold = np.round(
                aux.min() + (1 - settings.LOCK_THRESHOLD) * absmin, 3
            )
            self.lockThresholdBreak = np.round(
                aux.min() + (1 - settings.LOCK_THRESHOLD_BREAK) * absmin, 3
            )
        else:  # the peaks are maxima
            self.lockGreater = 1
            self.lockThreshold = np.round(
                aux.max() - (1 - settings.LOCK_THRESHOLD) * absmax, 3
            )
            self.lockThresholdBreak = np.round(
                aux.max() - (1 - settings.LOCK_THRESHOLD_BREAK) * absmax, 3
            )
        w = f"""
            Found greater {self._autolock["greater"]} with threshold {self._autolock["threshold"]:3f}.
            Median was {median:3f} with min/max {aux.min():3f} and {aux.max():3f}.
            """
        log.warning(w)

    #########################################
    # Realtime plotting and fifo
    #########################################

    def _calculateFifoStepsize(self):
        # in ramp mode, we would like the monitor output to match at least one ramp cycle
        # in reality we will need 2 to make sure it always finds minima
        # so: what fifo stepsize is required for given ramp settings
        factor = 2.2
        fifoStepsize = int(
            factor * 4 / self._autolock["stepsize"] / settings.FIFO_MAXLEN
        )
        if fifoStepsize == 0:
            fifoStepsize = 1
        log.debug(
            (
                "Calculated new fifo stepsize",
                fifoStepsize,
                "with lock step",
                self._autolock["stepsize"],
            )
        )
        return fifoStepsize

    def _updateFifoStepsize(self):
        if self.fifoEnabled and self._autolock["search"]:
            self.enableFifo(self._calculateFifoStepsize())

    def _calculateRefreshTime(self):
        bufferFillingLevel = 0.5
        if self._autolock["search"]:
            bufferFillingLevel = 1

        refreshTime = (
            self._fifo["stepsize"]
            / settings.SAMPLING_RATE
            * bufferFillingLevel
            * settings.FIFO_MAXLEN
        )

        if refreshTime < self._MIN_REFRESH_TIME:
            refreshTime = self._MIN_REFRESH_TIME
        self.realtime["refreshTime"] = refreshTime

    @property
    def _fifoBufferSize(self) -> int:
        """Get the current size of the fifo buffer on ADwin."""
        return self._adw.Fifo_Full(settings.DATA_FIFO)

    @property
    def fifoStepsize(self) -> int:
        """
        Setter DEPRECATED: Use :obj:`nqontrol.Servo.enableFifo()`

        Trigger ADwin to write the three channels of this servo to the FIFO buffer to read it with the PC over LAN.

        :code:`input`, :code:`aux` and :code:`output` will be sent.

        :getter: Number of program cycles between each data point.
        :setter: Set the number or choose `None` to disable the FiFo output.
        :type: :obj:`int`
        """
        return self._fifo["stepsize"]

    @property
    def realtimeEnabled(self) -> bool:
        if self.realtime["enabled"] and self.fifoEnabled:
            return True

        return False

    @property
    def fifoEnabled(self) -> bool:
        if self._adw.Get_Par(settings.PAR_ACTIVE_CHANNEL) == self._channel:
            return True

        return False

    def enableFifo(self, fifo_stepsize: Optional[int] = None):
        """
        Trigger ADwin to write the three channels of this servo to the
        FIFO buffer to read it with the PC over LAN.

        :code:`input`, :code:`aux` and :code:`output` will be sent.

        Parameters
        ----------
            fifo_stepsize: :obj:`int`
                Number of program cycles between each data point.
                If unset it will stay the same or use the default ({})

        """.format(
            self.DEFAULT_FIFO_STEPSIZE
        )
        if fifo_stepsize is None:
            fifo_stepsize = self._fifo["stepsize"]
        if not isinstance(fifo_stepsize, int) or fifo_stepsize < 1:
            raise ValueError(
                f"The stepsize must be a positive integer, but it was: {fifo_stepsize}"
            )

        self._fifo["stepsize"] = fifo_stepsize
        # Enable on adwin
        self._adw.Set_Par(settings.PAR_ACTIVE_CHANNEL, self._channel)
        # stepsize will never be None
        self._adw.Set_Par(settings.PAR_FIFOSTEPSIZE, fifo_stepsize)
        # set refresh time
        self._calculateRefreshTime()
        # Create local buffer
        self._createDataFrame()

    def disableFifo(self):
        """Disable the FiFo output if it is enabled on this channel."""
        if self.fifoEnabled:
            # Disable on adwin only if this channel is activated
            self._adw.Set_Par(settings.PAR_ACTIVE_CHANNEL, 0)
            self._adw.Set_Par(settings.PAR_FIFOSTEPSIZE, 0)
            # Destroy local buffer
            self._fifoBuffer = None

    def _readoutNewData(self, n: int) -> DataFrame:
        m: int = self._fifoBufferSize
        if n > m:
            n = m

        newData: DataFrame = DataFrame(columns=self.DEFAULT_COLUMNS)

        if n == 0:
            log.warning("I should readout 0 data.")
            return newData

        # Saving 3 16bit channels in a 64bit long variable
        # Byte    | 7 6 | 5 4   | 3 2 | 1 0    |
        # Channel |     | input | aux | output |
        combined = np.array(
            self._adw.GetFifo_Double(settings.DATA_FIFO, n)[:], dtype="int"
        )

        def extractValue(combined, offset=0):
            shifted = np.right_shift(combined, offset)
            return np.bitwise_and(shifted, 0xFFFF)

        log.debug(extractValue(combined[0], 32))
        log.debug(extractValue(combined[0], 16))
        log.debug(extractValue(combined[0]))

        newData["input"] = convertFloat2Volt(
            extractValue(combined, 32), self._state["inputSensitivity"]
        )
        newData["aux"] = convertFloat2Volt(
            extractValue(combined, 16), self._state["auxSensitivity"]
        )
        newData["output"] = convertFloat2Volt(extractValue(combined))

        log.debug(newData["input"][0])
        log.debug(newData["aux"][0])
        log.debug(newData["output"][0])

        return newData

    def _prepareContinuousData(self) -> None:
        n: int = self._fifoBufferSize
        if n == 0:
            return

        maxLen: int = settings.FIFO_MAXLEN
        buf: DataFrame = DataFrame()

        if n >= maxLen:
            n = maxLen
        else:
            # local copy of the `maxlen-n` newest entries.
            if settings.FIFO_MAXLEN < len(buf) + n:
                raise Bug(
                    f"That check should not fail. maxlen = {settings.FIFO_MAXLEN}, "
                    "len(buf) = {len(DataFrame(self._fifoBuffer[n:]))}, "
                    "lenBefore = {len(self._fifoBuffer)}, n = {n}"
                )

        # Read new data
        newData: DataFrame = self._readoutNewData(n)
        # Append to the local DataFrame
        self._fifoBuffer = buf.append(newData, sort=False)

        newLen: int = len(self._fifoBuffer)
        if newLen > settings.FIFO_MAXLEN:
            raise Bug(
                f"That is a bug. Please report it. "
                "len(newData): {len(newData)}, len(buf): {len(buf)}"
            )

        dt: float = self._timeForFifoCycles(1)
        self._fifoBuffer.index = np.arange(0, newLen * dt, dt)[:newLen]

    def _prepareRampData(self, tries: int = 3) -> None:
        if tries < 1:
            log.warning("tries must be at least 1.")
            tries = 1

        found_min = False

        for _ in range(tries):
            # we used some calculations here before, better to just use a fixed value
            n_data_buffer = settings.FIFO_MAXLEN
            log.debug(f"Buffer points: {n_data_buffer}")
            self._waitForBufferFilling(n=n_data_buffer)
            # Take data
            newData = self._readoutNewData(n_data_buffer)
            log.debug(f"length of readout ramp data {len(newData)}")
            # Find the first minimum
            try:
                minima, _ = find_peaks(-newData["output"])
                log.debug(f"Minima: {minima}")
                _ = minima[0]
                found_min = True
                break
            except IndexError:
                log.warning("Could not find a ramp minimum.")

        if not found_min:
            log.warning(
                f"Unable to find the ramp minimum in {tries} tries. Giving up..."
            )
            return

        try:
            second_min = minima[1]
        except IndexError:
            log.warning("No second minimum found.")
            # in case you want to test this:

            # newData.to_csv("test123")
            second_min = None
        # Copy data from the first minimum untill the end
        localBuffer = DataFrame(newData[minima[0] : second_min])
        log.debug(f"Local buffer length {len(localBuffer)}")

        # Calculate times for the index
        length = len(localBuffer)
        dt = self._timeForFifoCycles(1)
        localBuffer.index = np.arange(0, length * dt, dt)[:length]

        self._fifoBuffer = DataFrame(localBuffer)

    def _timeForFifoCycles(self, n):
        log.debug((n, self._fifo["stepsize"]))
        return n * self._fifo["stepsize"] / settings.SAMPLING_RATE

    def _waitForBufferFilling(self, n: int = None, refill: bool = True):
        if n is None:
            n = settings.FIFO_MAXLEN
        if refill:
            cycles = n
        else:
            bufferSize = self._fifoBufferSize
            if bufferSize < n:
                cycles = n - bufferSize
            else:
                return
        sleep(self._timeForFifoCycles(cycles))

    def _createDataFrame(self):
        data = {"input": [], "aux": [], "output": []}
        self._fifoBuffer = DataFrame(data=data)

    def takeData(self) -> DataFrame:
        """Take data from ADwin.

        It will return a DataFrame containing the columns input, aux and output.

        Returns
        -------

        returnVar : DataFrame
        """
        self._readLockControl()
        if not self.fifoEnabled:
            log.warning("The FiFo output was not activated. Enabling now...")
            self.enableFifo()
        if self._autolock["search"] and self._autolock["amplitude"] > 0:
            self._prepareRampData()
        else:
            self._prepareContinuousData()
        return self._fifoBuffer[self.realtime["ydata"]]

    def _realtimeLoop(self):
        try:
            gui_breaks = (KeyboardInterrupt,)
            from tkinter import TclError  # pylint: disable=import-outside-toplevel

            gui_breaks += (TclError,)
        except ImportError:
            pass

        # plotting loop
        assert (
            self.realtimeEnabled
        ), "Realtime should be enabled when starting the loop."

        # generate plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.ion()  # interactive mode

        try:
            while self.realtimeEnabled:
                timeStart = time()
                ax.clear()
                if self.realtime["ylim"] is None:
                    ax.set_ylim(auto=True)
                else:
                    ax.set_ylim(self.realtime["ylim"])
                ax.plot(self.takeData())
                ax.legend(self.realtime["ydata"], loc=1)

                timePause = self.realtime["refreshTime"] - time() + timeStart
                if timePause <= 0:
                    timePause = 1e-6

                plt.pause(timePause)
        except gui_breaks:
            plt.close("all")
            log.info("Plot closed")
        finally:
            # Ensure that `realtime` is disabled if the plot is closed
            log.info("Stop plotting...")
            self.realtime["enabled"] = False
            self._subProcess = None

    def stopRealtimePlot(self):
        """Stop the realtime plot."""
        self.realtime["enabled"] = False
        if self._subProcess is not None:
            self._subProcess.join()
        else:
            log.warning("No subprocess had been started.")
            return
        assert not self._subProcess.is_alive(), "The subprocess should be finished!"

    def realtimePlot(self, ydata=None, refreshTime=None, multiprocessing=True):
        """
        Enable parallel realtime plotting.

        To stop the running job call `stopRealtimePlot()`.

        Parameters
        ----------
        ydata: :obj:`list` of :obj:`str`
            Choose the data to be plotted: :code:`['input', 'aux', 'output']`.
        refreshTime: :obj:`float`
            Sleeping time (s) between plot updates.

        """
        if self._subProcess is not None and self._subProcess.is_alive():
            raise UserInputError(
                "Do you really want more than one plot of the same data? It is not implemented..."
            )
        if self._fifoBuffer is None:
            log.info(
                "Enabling the FiFo buffer with a default step size of {}...".format(
                    self.DEFAULT_FIFO_STEPSIZE
                )
            )
            self.enableFifo()

        # Update local parameters
        self.realtime["enabled"] = True
        if ydata:
            self.realtime["ydata"] = ydata
        if refreshTime:
            self.realtime["refreshTime"] = refreshTime

        # Start plotting process
        if multiprocessing:
            self._subProcess = mp.Process(target=self._realtimeLoop)
            self._subProcess.start()
        else:
            self._realtimeLoop()

    ########################################
    # Temperature feedback
    ########################################
    @property
    def tempFeedback(self):
        """Return or set temperature feedback server associated with the servo.

        :getter: Return the :obj:`FeedbackController`.
        :setter: Set a new :obj:`FeedbackController`.
        :type: :obj:`FeedbackController`.
        """
        return self._tempFeedback

    def tempFeedbackStart(  # pylint: disable=too-many-arguments
        self,
        dT=None,
        mtd=None,
        voltage_limit=None,
        server=settings.DEFAULT_TEMP_HOST,
        port=settings.DEFAULT_TEMP_PORT,
        update_interval=None,
    ):
        """Start the temperature feedback server. Setup a server if it hasn't been previously set.

        Parameters
        ----------
        dT : :obj:`float`
            Description of parameter `dT`.
        mtd : :obj:`tuple`
            (1, 1)
        voltage_limit : :obj:`float`
            The maximum voltage to which one can go using the temperature control (the default is 5).
        server : type
            Description of parameter `server` (the default is settings.DEFAULT_TEMP_HOST).
        port : type
            Description of parameter `port` (the default is settings.DEFAULT_TEMP_PORT).
        update_interval : :obj:`float`
            Description of parameter `update_interval` (the default is 1).

        """
        if dT is None:
            dT = self._tempFeedbackSettings["dT"]
        if mtd is None:
            mtd = self._tempFeedbackSettings["mtd"]
        if voltage_limit is None:
            voltage_limit = self._tempFeedbackSettings["voltage_limit"]
        if update_interval is None:
            update_interval = self._tempFeedbackSettings["update_interval"]

        self._tempFeedback = FeedbackController(
            self, dT, mtd, voltage_limit, server, port, update_interval
        )
        self.tempFeedback.start()

    def tempFeedbackStop(self):
        """Stop the tempFeedback server."""
        self.tempFeedback.enabled = False
        self.tempFeedback.join()
        self._tempFeedback = None

    ########################################
    # Save and load settings
    ########################################
    def _applySettingsDict(self, data):
        # Don't import the channel because it isn't possible to change it.
        DONT_SERIALIZE = self._DONT_SERIALIZE + ["_channel"] + ["name"]
        # overwrite name from save file only if no other name has been set specifically in settings
        if (
            data.get("name") is not None
            and data.get("name") != f"Servo {self._channel}"
        ):
            self.name = data.get("name")
        for d in self.__dict__:
            value = data.get(d.__str__())
            if (d.__str__() not in DONT_SERIALIZE) and (value is not None):
                if d.__str__() in self._JSONPICKLE:
                    self.__dict__[d.__str__()] = jsonpickle.decode(value)
                elif isinstance(value, dict):
                    self.__dict__[d.__str__()].update(value)
                else:
                    self.__dict__[d.__str__()] = value

    def getSettingsDict(self):
        """
        Get a dict with all servo settings.

        Returns
        -------
        :obj:`dict`
            Return all important settings for the current servo state.
        """
        # load state from adwin
        self._readAllFromAdwin()

        # save settings
        data = {}
        for d in self.__dict__:
            if d.__str__() not in self._DONT_SERIALIZE:
                value = self.__dict__[d.__str__()]
                # Convert dicts from multiprocessing
                if isinstance(value, (dict, mp.managers.DictProxy)):
                    value = dict(value)
                elif d.__str__() in self._JSONPICKLE:
                    value = jsonpickle.encode(value)
                data[d.__str__()] = value
        return data

    def saveJsonToFile(self, filename):
        """
        Save this single servo as json to a file.

        Parameters
        ----------
        filename: :obj:`str`
            Filename to save the json file.

        """
        data = {self.__class__.__name__: self.getSettingsDict()}
        with open(filename, "w+") as file:
            json.dump(data, file, indent=2)

    def loadSettings(self, applySettings):
        """
        Load settings from file or dict.

        Not reading the channel, it can only be set on creating a servo object.

        Parameters
        ----------
        applySettings: :obj:`str` or :obj:`dict`
            Settings to load for this servo.

        """
        if isinstance(applySettings, dict):
            load_settings = applySettings
        elif isinstance(applySettings, str):
            load_settings = self._readJsonFromFile(applySettings)
        else:
            raise ValueError("You can only apply settings from a file or a dict.")

        self._applySettingsDict(load_settings)
        self._sendAllToAdwin()

    def _readJsonFromFile(self, filename):
        """
        Read settings from a single servo file.

        return: dict with only the servo settings
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            raise e

        if not data.get(self.__class__.__name__):
            raise SyntaxError("Invalid file.")

        return data[self.__class__.__name__]
