"""
Dans_Diffraction tests
Test definition of gaussian
27/3/2020
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt # Plotting

sys.path.insert(0,r'C:\Users\dgpor\Dropbox\Python\Dans_Diffraction')
import Dans_Diffraction as dif

xtl = dif.structure_list.Ca2RuO4()

hkl = xtl.Cell.all_hkl(2.838)[1:]
tth = xtl.Cell.tth(hkl, 2.838)
inten = xtl.Scatter.intensity(hkl)

t,i = dif.fg.grid_intensity(tth, inten)

dif.fp.newplot(t, i)

xtl.Plot.simulate_powder(2.838, peak_width=0.001)
plt.plot(t, i)

plt.show()
