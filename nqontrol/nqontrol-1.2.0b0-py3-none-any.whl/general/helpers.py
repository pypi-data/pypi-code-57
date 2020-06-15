import logging as log
from typing import List, Union

import numpy as np

from . import settings


def setBit(x, offset):
    mask = 1 << offset
    return x | mask


def clearBit(x, offset):
    mask = ~(1 << offset)
    return x & mask


def testBit(x, offset):
    mask = 1 << offset
    if x & mask:
        return 1
    return 0


def changeBit(x, offset, enabled):
    if enabled:
        return setBit(x, offset)
    return clearBit(x, offset)


def readBit(x, offset):
    if testBit(x, offset):
        return True
    return False


def convertVolt2Float(
    value: Union[list, np.number, np.ndarray], mode: int = 0, signed=False
) -> Union[float, np.ndarray]:
    """Converts a volt scala value (in case of ADwin e.g. volt range from -10 to 10, because the outputs are limited) to a Float value. The supported range is divided onto the whole 16-bit float, so -10 Volt would e.g. correspond with 0, 10 V with 65535 for unsigned or -32768 to 32767 when signed.

    Parameters
    ----------
    value: :obj:`list`, :obj:`numpy.number`, :obj:`numpy.ndarray`
        The value(s) to be converted.
    mode: :obj:`int`
        Integer from 0 to 3, sensitivity mode. Decides how the bins are divided. See :obj:`nqontrol.servo.inputSensitivity` or `auxSensitivity` for more info.
    signed: :obj:`bool`
        Whether the Integer is supposed to have a sign or not, see above.

    Returns
    -------
    :obj:`list`, :obj:`numpy.number`, :obj:`numpy.ndarray`
        Converted value. Exact type depends on input type.
    """
    if isinstance(value, list):
        value = np.array(value)
    result = 0.1 * value * 0x8000 * pow(2, mode)

    upper_limit = 0x7FFF
    lower_limit = -0x8000
    if isinstance(result, (float, np.float64, np.float32)):
        if result > upper_limit:
            result = upper_limit
        if result < lower_limit:
            result = lower_limit
    elif isinstance(result, np.ndarray):
        result[result > upper_limit] = upper_limit
        result[result < lower_limit] = lower_limit
    else:
        raise TypeError("The type {} is not supported.".format(type(value)))

    if not signed:
        result += 32768
    return result


def convertVolt2Int(
    value: Union[list, np.number, np.ndarray], mode: int = 0, signed=False
) -> Union[int, np.ndarray]:
    """[DEPRECATED] Converts a volt scala value (in case of ADwin e.g. volt range from -10 to 10, because the outputs are limited) to an Integer value. There is an equivalent function for Floats. The supported range is divided onto the whole 16-bit integer, so -10 Volt would e.g. correspond with 0, 10 V with 65535 for unsigned or -32768 to 32767 when signed.

    Parameters
    ----------
    value: :obj:`list`, :obj:`numpy.number`, :obj:`numpy.ndarray`
        The value(s) to be converted.
    mode: :obj:`int`
        Integer from 0 to 3, sensitivity mode. Decides how the bins are divided. See :obj:`nqontrol.servo.inputSensitivity` or `auxSensitivity` for more info.
    signed: :obj:`bool`
        Whether the Integer is supposed to have a sign or not, see above.

    Returns
    -------
    :obj:`list`, :obj:`numpy.number`, :obj:`numpy.ndarray`
        Converted value. Exact type depends on input type.
    """
    log.warning(
        DeprecationWarning(
            "This method is deprecated, please use `convertVolt2Float` for higher accuracy."
        )
    )
    result = convertVolt2Float(value, mode, signed)
    if isinstance(result, (float, np.float64, np.float32)):
        return int(round(result, 0))
    if isinstance(result, np.ndarray):
        return result.astype(int)
    return result


def convertFloat2Volt(
    value: Union[List[float], np.array, float], mode: int = 0, signed=False
) -> Union[float, np.ndarray]:
    """Convert float to volt.

    For details see :obj:`convertVolt2Float`.

    Parameters
    ----------

    value : Union[List[float], np.array, float]
        value is a 16 bit number
    mode : int
        mode is the input amplification mode
    signed :

    Returns
    -------

    returnVar : Union[float, np.ndarray]
    """
    if isinstance(value, list):
        value = np.array(value)
    if signed:
        value += 32768
    return 10.0 * (value / 0x8000 - 1) / pow(2, mode)


def rearrange_filter_coeffs(inputFilter: List[float]) -> List[float]:
    """Rearrage coefficients from `a, b` to `c`."""
    b = inputFilter[0:3]
    a = inputFilter[3:6]
    return [b[0], a[1], a[2], b[1] / b[0], b[2] / b[0]]


def convertStepsize2Frequency(stepsize: float) -> float:
    """Convert stepsize to frequency for the autolock ramp.

    The stepsize is a float and has the following relation to the ramp. Internally, ADwin uses a normalized ramp from -1 to 1 Volts, which is then multiplied by an amplitude and added to some offset value.

    Thus, we get a fixed ratio of frequency to stepsize, given by

    f = s * 200kHz / 4

    where the 200kHz is the ADwin sampling rate. The 4 derives from the fact, that the total steps needed for a given stepsize of one ramp cycle is 4 / s, when 1 is the amplitude, since we want to go from minimum to maximum and back.

    It makes sense to introduce some minimum frequency, e.g. {0} Hz, which correlates with a minimum stepsize of 2e-05. For UI purposes it also makes sense to have a reasonable maximum frequency, which can be found in `settings.py` under RAMP_FREQUENCY_MAX (currently {1}).

    As these are supposed to be general conversion methods, we do not enforce the given boundaries here, but on the `servo.py` level.

    Parameters
    ----------

    stepsize : float
        stepsize of the ramp

    Returns
    -------

    returnVar : float
        frequency in Hz
    """.format(
        settings.RAMP_FREQUENCY_MIN, settings.RAMP_FREQUENCY_MAX
    )

    if (
        not convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)
        <= stepsize
        <= convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MAX)
    ):
        log.warning(
            f"We recommend using stepsizes between {convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MIN)} Hz and {convertFrequency2Stepsize(settings.RAMP_FREQUENCY_MAX)} Hz. Input was {stepsize}."
        )

    return stepsize * settings.SAMPLING_RATE / 4


def convertFrequency2Stepsize(frequency: float) -> float:
    """Convert frequency to stepsize for the autolock ramp.

    The stepsize is a float and has the following relation to the ramp. Internally, ADwin uses a normalized ramp from -1 to 1 Volts, which is then multiplied by an amplitude and added to some offset value.

    Thus, we get a fixed ratio of frequency to stepsize, given by

    f = s * 200kHz / 4

    where the 200kHz is the ADwin sampling rate. The 4 derives from the fact, that the total steps needed for a given stepsize of one ramp cycle is 4 / s, when 1 is the amplitude, since we want to go from minimum to maximum and back.

    It makes sense to introduce some minimum frequency, e.g. {0} Hz, which correlates with a minimum stepsize of 2e-05. For UI purposes it also makes sense to have a reasonable maximum frequency, which can be found in `settings.py` under RAMP_FREQUENCY_MAX (currently {1}).

    As these are supposed to be general conversion methods, we do not enforce the given boundaries here, but on the `servo.py` level.

    Parameters
    ----------

    frequency : float
        frequency in Hz

    Returns
    -------

    returnVar : float
        stepsize
    """.format(
        settings.RAMP_FREQUENCY_MIN, settings.RAMP_FREQUENCY_MAX
    )
    if not settings.RAMP_FREQUENCY_MIN <= frequency <= settings.RAMP_FREQUENCY_MAX:
        log.warning(
            f"We recommend using frequencies between {settings.RAMP_FREQUENCY_MIN} Hz and {settings.RAMP_FREQUENCY_MAX} Hz. Input was {frequency}."
        )

    stepsize = frequency * 4 / settings.SAMPLING_RATE

    return stepsize
