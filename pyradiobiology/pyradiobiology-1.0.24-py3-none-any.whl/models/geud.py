#  MIT License
#
#  Copyright (c) 2020. Medical Innovation and Technology P.C. (MIT)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
import numpy as np

from ..primitives import DoseArray, DoseType


class Geud():
    def __init__(self, a_volume_effect) -> None:
        self._validate_positive_or_throw_exception(a_volume_effect, "m must be a positive number")
        self.a_volume_effect = a_volume_effect

    def _validate_positive_or_throw_exception(self, value, message):
        if value < 0:
            raise ValueError(message)

    def calculate(self, dose_array_in_eqd2: DoseArray, volume_array):
        if not isinstance(volume_array, type(np.array)):
            volume_array = np.array(volume_array)

        if dose_array_in_eqd2.dose_type != DoseType.EQD2:
            raise ValueError("dose_array_inEQD2 must be in EQD2 DoseType")

        volume_array = np.array(volume_array)
        totalVolume = np.sum(volume_array)
        fractionalVolume = volume_array / totalVolume
        geud = np.sum(fractionalVolume * (dose_array_in_eqd2.data ** self.a_volume_effect))
        return geud**(1/self.a_volume_effect)
