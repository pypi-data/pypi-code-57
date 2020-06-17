"""
Dans_Diffraction Tests
Test accuracy of different methods of readstfm
5/5/2020
"""

import os, time, re
import numpy as np
import Dans_Diffraction as dif


def readstfm(string):
    """
    Read numbers written in standard form: 0.01(2), return value and error
    Read numbers from string with form 0.01(2), returns floats 0.01 and 0.02

    E.G.
    readstfm('0.01(2)') = (0.01, 0.02)
    readstfm('1000(300)') = (1000.,300.)
    """

    values = re.findall('[-0-9.]+', string)

    if values[0] == '.':
        values[0] = '0'
    value = float(values[0])
    error = 0.

    if len(values) > 1:
        error = float(values[1])

        # Determine decimal place
        idx = values[0].find('.')  # returns -1 if no decimal
        if idx > -1:
            pp = idx - len(values[0]) + 1
            error = error * 10 ** pp
    return value, error

def readstfm2(string):
    """
    Read numbers written in standard form: 0.01(2), return value and error
    Read numbers from string with form 0.01(2), returns floats 0.01 and 0.02

    E.G.
    readstfm('0.01(2)') = (0.01, 0.02)
    readstfm('1000(300)') = (1000.,300.)
    """

    values = re.findall('[-0-9.]+|\([-0-9.]+\)', string)
    if len(values) > 0 and '(' not in values[0]:
        value = values[0]
    else:
        value = '0'

    # Determine number of decimal places for error
    idx = value.find('.') # returns -1 if . not found
    if idx > -1:
        pp = idx - len(value) + 1
    else:
        pp = 0
    value = float(value)

    error = re.findall('\([-0-9.]+\)', string)
    if len(error) > 0:
        error = abs(float(error[0].strip('()')))
        error = error * 10 ** pp
    else:
        error = 0.

    power = re.findall('(?:[eE]|x10\^|\*10\^|\*10\*\*)([+-]?\d*\.?\d+)', string)
    if len(power) > 0:
        power = float(power[0])
        value = value * 10 ** power
        error = error * 10 ** power
    return value, error



values = [
    '1.2(1)', '452.2(3)', '0.00123(2)', '-3.245(23)', '4577.1(11)', '0.001(30)',
    '1.2', '(0.1)', '000(0.1)', '1.2e5', '1.2(3)E-2', '123.312(1231)E-0.23',
    '0', '?'
]

for value in values:
    out = 'Value: %30s  ' % value
    try:
        val, err = readstfm(value)
        out += 'readstfm: %10s %10s  ' % (val, err)
    except:
        out += 'readstfm:  %20s  ' % 'FAIL'

    try:
        val, err = readstfm2(value)
        out += 'readstfm2: %10s %10s  ' % (val, err)
    except:
        out += 'readstfm2:  %20s  ' % 'FAIL'

    print(out)

