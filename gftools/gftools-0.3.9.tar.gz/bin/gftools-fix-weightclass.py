#!/usr/bin/env python3
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
A Python script to set a font's OS/2 usWeightClass value so it conforms to
the Google Fonts specification. The font's filename is used to determine
the correct value.
"""
from __future__ import print_function
from fontTools.ttLib import TTFont
import sys
import os


# TODO (M Foley) support VFs
WEIGHTS = {
    "Thin": 250,
    "ExtraLight": 275,
    "Light": 300,
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
    "ExtraBold": 800,
    "Black": 900
}


def is_variable(ttfont):
    return "fvar" in ttfont


def main(font_path):
    font = TTFont(font_path)
    filename = os.path.basename(font_path)[:-4]
    if is_variable(font):
        stylename = font['name'].getName(17, 3, 1, 1033) or font['name'].getName(2, 3, 1, 1033)
        stylename = stylename.toUnicode()
        weight_names = sorted(WEIGHTS, key=lambda k: len(k), reverse=True)
        found_weight = None
        for name in weight_names:
            print(stylename)
            if name in stylename:
                found_weight = name
                break
        if found_weight:
            print(f"changing usWeightClass to {WEIGHTS[found_weight]}")
            font['OS/2'].usWeightClass = WEIGHTS[found_weight]

        font.save(font_path + ".fix")
        return

    if not "-" in filename:
        raise Exception("Font filename is not canonical. Filename should "
                        "be structured as FamilyName-StyleName.ttf "
                        "e.g Montserrat-Regular.ttf")
    family_name, style_name = filename.split("-")
    current_weight_class = font["OS/2"].usWeightClass
    if current_weight_class != WEIGHTS[style_name]:
        print("{}: Updating weightClass to {}".format(filename,
                                                      WEIGHTS[style_name]))
        font['OS/2'].usWeightClass = WEIGHTS[style_name]
        font.save(font_path + ".fix")
    else:
        print("{}: Skipping. Current WeightClass is correct".format(filename))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please include a path to a font")
    else:
        main(sys.argv[1])

