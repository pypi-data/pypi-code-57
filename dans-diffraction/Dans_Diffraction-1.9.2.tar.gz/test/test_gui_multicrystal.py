"""
Test multicrystal gui

"""

import Dans_Diffraction as dif
from Dans_Diffraction.tkgui import multi_crystal

xtl1 = dif.structure_list.Diamond()
xtl2 = dif.structure_list.Aluminium()
xtls = xtl1 + xtl2

multi_crystal.MultiCrystalGui([xtl1])