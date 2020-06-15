# pylint: disable=missing-function-docstring
import logging as log
import os
from time import time

import numpy as np
from ADwin import ADwinError
from scipy import signal

from . import helpers, settings


class MockADwin:  # pylint: disable=too-many-instance-attributes
    """Mock class for testing and demonstration of nqontrol"""

    NUM_SERVOS = 8

    def __init__(self, DeviceNo=0, raiseError=False):
        self.DeviceNo = DeviceNo
        self._par = [0] * 80
        self._fpar = [0] * 80
        self._running = [0] * 10
        self._data_double = [[]] * 200
        self._data_long = [[]] * 200
        self.ADwindir = "mock"
        self._boot_time = time()
        self._last_read = 0
        self._n_last = 0

        self._raiseError = False
        self.reset_trigger = True
        self._raiseError = raiseError

        # init offset and gain
        self._data_double[settings.DATA_OFFSETGAIN - 1] = [1.0] * self.NUM_SERVOS + [
            0.0
        ] * self.NUM_SERVOS
        # init filter coefficients
        self._data_double[settings.DATA_FILTERCOEFFS - 1] = (
            [1.0, 0.0, 0.0, 0.0, 0.0]
            * settings.NUMBER_OF_FILTERS
            * settings.NUMBER_OF_SOS
        )
        self._data_long[settings.DATA_LAST_OUTPUT - 1] = [0] * self.NUM_SERVOS
        self._data_long[settings.DATA_MONITORS - 1] = [0] * self.NUM_SERVOS
        # autolock parameters
        self._data_double[settings.DATA_LOCK - 1] = [0.0] * (self.NUM_SERVOS * 3)
        self._data_double[settings.DATA_LOCK - 1][0:8] = [0.0] * 8  # thresholds
        self._data_double[settings.DATA_LOCK - 1][8:16] = [0.0] * 8  # threshold breaks
        self._data_double[settings.DATA_LOCK - 1][16:24] = [1.0] * 8  # amplitudes
        self._data_double[settings.DATA_LOCK - 1][24:32] = [0x8000] * 8  # offsets
        # helper field, exposes the lockIterator
        self._data_double[settings.DATA_LOCK_ITER - 1] = [0] * self.NUM_SERVOS
        # helper field, exposes recent lock output as test value
        self._data_long[settings.DATA_LOCK_OUTPUT - 1] = [0] * self.NUM_SERVOS
        self._data_double[settings.DATA_LOCK_STEPSIZE - 1] = [
            helpers.convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)
        ] * self.NUM_SERVOS
        # internal field, direction of the lock step, either +1 or -1
        self._lockStepSign = [1] * self.NUM_SERVOS
        self._lockPosition = [0.0] * self.NUM_SERVOS
        self._lockBuffer = [0.0] * self.NUM_SERVOS
        # time difference
        self.Set_Par(settings.PAR_TIMEDIFF, 3000)
        self.Set_Par(settings.PAR_FIFOSTEPSIZE, 1)

    def Boot(self, file_):  # pylint: disable=unused-argument
        self._boot_time = time()

    def Workload(self):  # pylint: disable=no-self-use
        return 42

    def Process_Status(self, no):
        return self._running[no - 1]

    def Load_Process(self, process):  # pylint: disable=no-self-use
        assert os.path.isfile(
            process
        ), f"The ADwin process file '{process}' has to exist."

    def Start_Process(self, no):
        self._running[no - 1] = 1

    def Set_FPar(self, index, par):
        self._fpar[index - 1] = float(par)

    def Set_Par(self, index, par):
        if self._raiseError:
            raise ADwinError("test", "Test Error", 13)

        if index == 3 and par != 0:
            self._last_read = time()
        self._par[index - 1] = int(par)

    def Get_Par(self, index):
        self._par_special_functions()
        return self._par[index - 1]

    def Get_FPar(self, index):
        self._fpar_special_functions()
        return self._fpar[index - 1]

    def GetData_Double(self, DataNo, Startindex, Count):
        self._data_double_special_functions(DataNo)
        try:
            if DataNo == settings.DATA_LOCK:
                log.debug(
                    f"lock data values where accessed, are: {self._data_double[settings.DATA_LOCK - 1]}"
                )
            return list(
                self._data_double[DataNo - 1][Startindex - 1 : Startindex + Count - 1]
            )
        except IndexError as e:
            raise IndexError(
                f"An index error occured: {e}. The relevant indices were startindex {Startindex} and DataNo {DataNo}. The length of the target array was {len(self._data_double[DataNo - 1])}."
            )

    def _data_double_special_functions(self, no):
        if no == settings.DATA_LOCK_ITER:
            lcr = self._par[settings.PAR_LCR - 1]
            for i in range(1, 9):
                indexoffset = i - 1
                search = helpers.readBit(lcr, indexoffset)
                locked = helpers.readBit(lcr, indexoffset + 8)
                if not search and not locked:
                    self.SetData_Double([-2.0], settings.DATA_LOCK_ITER, i, 1)
                else:
                    # lock stuff
                    overshoot = self._data_double[settings.DATA_LOCK_STEPSIZE - 1][
                        i - 1
                    ]
                    out = np.random.uniform(-1 - overshoot, 1 + overshoot)
                    self.SetData_Double([out], settings.DATA_LOCK_ITER, i, 1)

    def SetData_Double(self, Data, DataNo, Startindex, Count):
        try:
            self._data_double[DataNo - 1][
                Startindex - 1 : Startindex + Count - 1
            ] = Data
        except IndexError as e:
            raise IndexError(
                f"An index error occured: {e}. The relevant indices were startindex {Startindex} and DataNo {DataNo}. The length of the target array was {len(self._data_double[DataNo - 1])}."
            )

    def GetData_Long(self, DataNo, Startindex, Count):
        self._data_long_special_functions(DataNo)
        try:
            return list(
                self._data_long[DataNo - 1][Startindex - 1 : Startindex - 1 + Count]
            )
        except IndexError as e:
            raise IndexError(
                f"An index error occured: {e}. The relevant indices were startindex {Startindex} and DataNo {DataNo}. The length of the target array was {len(self._data_long[DataNo - 1])}."
            )

    def SetData_Long(self, Data, DataNo, Startindex, Count):
        try:
            self._data_long[DataNo - 1][Startindex - 1 : Startindex + Count - 1] = Data
        except IndexError as e:
            raise IndexError(
                f"An index error occured: {e}. The relevant indices were startindex {Startindex} and DataNo {DataNo}. The length of the target array was {len(self._data_long[DataNo - 1])}."
            )

    def _data_long_special_functions(self, no):
        if no == settings.DATA_LAST_OUTPUT:
            for i in range(1, 9):
                if self._isRamp(i):
                    out = np.random.randint(
                        0, 2 ** 16
                    )  # some arbitrary number in the correct range, only for temp feedback
                else:
                    out = 2 ** 15
                self.SetData_Long([out], settings.DATA_LAST_OUTPUT, i, 1)

    def Fifo_Full(self, index):  # pylint: disable=unused-argument
        diff = time() - self._last_read
        fifoStepsize = self.Get_Par(6)
        n = int(diff * settings.SAMPLING_RATE / fifoStepsize)
        n = n + self._n_last
        if n > settings.FIFO_BUFFER_SIZE:
            n = settings.FIFO_BUFFER_SIZE
        self._n_last = n
        return int(n)

    def _isRamp(self, i):
        lcr = self._par[settings.PAR_LCR - 1]
        indexoffset = i - 1
        search = helpers.readBit(lcr, indexoffset)
        return bool(search)

    def _readSwitches(self, channel):
        c = self.Get_Par(10 + channel)
        # read control bits
        auxSw = helpers.readBit(c, 9)
        offsetSw = helpers.readBit(c, 2)
        outputSw = helpers.readBit(c, 1)
        inputSw = helpers.readBit(c, 0)
        return inputSw, offsetSw, auxSw, outputSw

    @staticmethod
    def _limitOutput(output):
        # Limit the output to 16bit
        output[output > 0xFFFF] = 0xFFFF
        output[output < 0] = 0
        return output

    def _frequency(self, channel):
        return helpers.convertStepsize2Frequency(
            self._data_double[settings.DATA_LOCK_STEPSIZE - 1][channel - 1]
        )

    @staticmethod
    def _sawtooth(amp, freq, amount):
        # due to how the sawtooth signal is constructed, it's normally going from -1 to 1
        # so we got to divide by 2 so we can cleanly multiply by amplitude!
        # we also want it to start at 0, thus the +1
        # and in order to get upwards and downwards, the sawtooth function needs to be passed the 0.5 as extra parameter
        # the - 0.1 in the sawtooth is just a little phase offset
        t = np.linspace(0, amount / 1000 * 1, amount)
        return amp * (signal.sawtooth(2 * np.pi * freq * (t - 0.1), 0.5))

    def _constructOutput(self, amount, input_, aux):
        channel = self.Get_Par(settings.PAR_ACTIVE_CHANNEL)
        inputSw, offsetSw, auxSw, outputSw = self._readSwitches(channel)

        # lock stuff
        lock = helpers.readBit(self._par[settings.PAR_LCR - 1], (channel - 1))
        locked = helpers.readBit(self._par[settings.PAR_LCR - 1], (channel - 1) + 8)

        amplitude = self._data_double[settings.DATA_LOCK - 1][channel - 1 + 16]
        offset = self._data_double[settings.DATA_LOCK - 1][channel - 1 + 24]
        if lock and not locked:
            # apply possible overflows on search start and search end (if iterator stepsize is bigger than +-1)
            log.debug(
                f"amplitude {amplitude} freq {self._frequency(channel)} amount {amount}"
            )
            output = self._sawtooth(amplitude, self._frequency(channel), amount)
            # uncomment for testing: np.savetxt("foo.csv", output, delimiter=",")
            # for some reason python cannot find peaks
            log.debug(f"constructed output of search state {output}")
            log.debug(
                f"minimum and maximum in volts {np.min(output)}, {np.max(output)}"
            )
            output = helpers.convertVolt2Float(output, signed=False) + offset - 0x8000
            log.debug(
                f"minimum and maximum as float {np.min(output)}, {np.max(output)}"
            )
            log.debug(f"offset in search state (as float) {offset}")
        elif locked:
            output = np.full(amount, self._lockPosition[channel - 1]).astype(int)
        else:
            output = np.full(amount, 0x8000).astype(int)
            if inputSw:
                output = input_
            if offsetSw:
                offset = self.GetData_Double(settings.DATA_OFFSETGAIN, channel + 8, 1)
                output = output + offset
            if outputSw:
                output = (output - 0x8000) * self.GetData_Double(
                    settings.DATA_OFFSETGAIN, channel, 1
                ) + 0x8000
            else:
                output = np.full(amount, 0x8000).astype(int)
            if auxSw:
                output = output + (aux - 0x8000)
            return output

        return self._limitOutput(output)

    @staticmethod
    def _extract_value(par, offset=0):
        shifted = np.right_shift(par, offset)
        return np.bitwise_and(shifted, 0xFF)

    def GetFifo_Double(self, index, amount):
        """GetFifo_Double returns a list of the fifo buffer.

        Parameters
        ----------

        index :
            index of the list
        amount :
            number of entries

        Returns
        -------
        list
        """
        assert index == settings.DATA_FIFO, f"Index has to be {settings.DATA_FIFO}."

        amount = int(amount)
        # Creating random data
        input_ = np.random.normal(0x8000, 10, size=amount).astype(int)
        aux = np.random.normal(0x8000, 10, size=amount).astype(int)

        output = self._constructOutput(amount, input_, aux)
        # concatenating bits
        crunch = np.left_shift(input_, 32)
        crunch = np.add(crunch, np.left_shift(aux, 16))
        crunch = np.add(crunch, output)
        # setting last readout time to current
        self._last_read = time()
        self._n_last = self._n_last - amount
        return crunch

    def Get_Processdelay(self, index):  # pylint: disable=no-self-use,unused-argument
        return 1e9 / settings.SAMPLING_RATE

    def _par_special_functions(self):
        self._par[0] = time() - self._boot_time  # Timestamp
        if self.reset_trigger:
            self._par[1] = 0  # Resetting trigger
        else:
            self._par[1] = 0xFFFF  # Not resetting trigger

        self._auto_lock()

    def _auto_lock(
        self,
    ):  # pylint: disable=too-many-statements, too-many-locals, too-many-branches
        # locking emulation
        aux = 0x8000
        data = self._data_double[settings.DATA_LOCK - 1]
        for servo in range(1, 9):
            indexoffset = servo - 1

            lcr = self._par[settings.PAR_LCR - 1]
            gcr = self._par[settings.PAR_GCR - 1]

            search = helpers.readBit(lcr, servo - 1)
            locked = helpers.readBit(lcr, servo - 1 + 8)
            relock = helpers.readBit(lcr, servo - 1 + 16)
            greater = helpers.readBit(gcr, (servo - 1))
            rampmode = helpers.readBit(gcr, self.NUM_SERVOS + (servo - 1))

            threshold = data[servo - 1]
            threshold_break = data[servo - 1 + 8]
            amplitude = data[servo - 1 + 16]
            offset = data[servo - 1 + 24]

            if self._lockBuffer[servo - 1] > 0:
                self._lockBuffer[
                    servo - 1
                ] = 0  # we dont really have a cycle counting down as on ADwin, where this line is just lockBuffer -= 1 basically

            if not search and not locked:
                # not searching, lock iter
                self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] = -2.0

            if search:
                log.debug(
                    f"using aux {helpers.convertFloat2Volt(aux, self._par[settings.PAR_SENSITIVITY - 1] >> servo * 2 + 14 & 3, False)}"
                )
                # ensure locked is 0 when searching
                self._par[settings.PAR_LCR - 1] = helpers.clearBit(
                    self._par[settings.PAR_LCR - 1], indexoffset + 8
                )
                if self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] == -2.0:
                    self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] = 0.0
                    # turn off input, output, aux
                    c = self._par[10 + (servo - 1)]
                    # clear control bits
                    c = helpers.clearBit(c, 0)  # input
                    c = helpers.clearBit(c, 1)  # output
                    c = helpers.clearBit(c, 9)  # aux
                    self._par[10 + (servo - 1)] = c
                    # technically filter history is cleared here, but its not implemented on mockADwin

                # a lock is found
                if not rampmode and (
                    (greater and aux > threshold) or ((aux < threshold) and not greater)
                ):
                    log.warning("found lock ")
                    log.debug(
                        f"lcr {self._par[settings.PAR_LCR - 1]} gcr {self._par[settings.PAR_GCR - 1]} offset {indexoffset}"
                    )
                    # set locked
                    self._par[settings.PAR_LCR - 1] = helpers.setBit(
                        self._par[settings.PAR_LCR - 1], indexoffset + 8
                    )
                    # set not searching (search = 0)
                    self._par[settings.PAR_LCR - 1] = helpers.clearBit(
                        self._par[settings.PAR_LCR - 1], indexoffset
                    )
                    c = self._par[10 + (servo - 1)]
                    c = helpers.setBit(c, 0)  # enable input
                    c = helpers.setBit(c, 1)  # enable output
                    # set the lockBuffer to 10000 cycles (on ADwin this is .1 seconds)
                    # please note this wont really work, we just reset this to 0 right away whenever we invoke this function
                    self._lockBuffer[servo - 1] = 10000
                    self._par[10 + (servo - 1)] = c
                else:  # searching for lock
                    if self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] <= -1:
                        self._lockStepSign[servo - 1] = 1
                    elif self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] >= 1:
                        self._lockStepSign[servo - 1] = -1

                    # iter = iter + stepsign * step
                    self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] = (
                        self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1]
                        + self._lockStepSign[servo - 1]
                        * self._data_double[settings.DATA_LOCK_STEPSIZE - 1][servo - 1]
                    )
                    c = self._par[10 + (servo - 1)]
                    # clear control bits
                    c = helpers.clearBit(c, 0)  # input
                    c = helpers.clearBit(c, 1)  # output
                    self._par[10 + (servo - 1)] = c

                self._lockPosition[servo - 1] = (
                    amplitude
                    * self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1]
                    * 0x8000
                    / 10
                    + offset
                )

            if locked:
                # if lock fails, set locked to 0, but only if the buffer phase is already over
                # we know this isnt pretty, but it's the same on ADwin because ADbasic is terrible, so shut up PYLINT!
                if (  # pylint: disable=too-many-boolean-expressions
                    (greater and (aux < threshold_break))
                    or (not greater and (aux > threshold_break))
                    and self._lockBuffer[servo - 1] == 0
                ) or rampmode:
                    log.warning("breaking lock")
                    if relock or rampmode:
                        self._par[settings.PAR_LCR - 1] = helpers.setBit(
                            self._par[settings.PAR_LCR - 1], indexoffset
                        )  # activate lock search again
                    else:
                        self._data_double[settings.DATA_LOCK_ITER - 1][servo - 1] = -2.0
                    # clear locked bit
                    self._par[settings.PAR_LCR - 1] = helpers.clearBit(
                        self._par[settings.PAR_LCR - 1], indexoffset + 8
                    )
                # normally the actual output signal would be added, but in test mode we always get perfect lock, eh
                self._data_long[settings.DATA_LOCK_OUTPUT - 1][
                    servo - 1
                ] = self._lockPosition[servo - 1]

    def _fpar_special_functions(self):
        pass
