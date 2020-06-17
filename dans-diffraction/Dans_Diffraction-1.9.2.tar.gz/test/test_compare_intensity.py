"""
Compare diffracted intensities from Dans_Diffraction and Federica's Crystal
*Should be run in cctbx python
"""

import sys, os
import numpy as np
import matplotlib.pyplot as plt # Plotting
# Location of Dans_Diffraction
df='C:/Users/grp66007/Dropbox/Python/Dans_Diffraction'
if df not in sys.path: sys.path.insert(0,df)
import Dans_Diffraction as dif
# Location of Crystal.py
ff='C:/Users/grp66007/Dropbox/Python/Federica'
if ff not in sys.path: sys.path.insert(0,ff)
from Crystal import Crystal

cf=os.path.dirname(__file__)
#f = cf+'/../Dans_Diffraction/Structures/Diamond.cif'
f="C:\Users\grp66007\Dropbox\Python\Dans_Diffraction\Dans_Diffraction\Structures\Diamond.cif" # same results
f="C:\Users\grp66007\Dropbox\Python\Dans_Diffraction\Dans_Diffraction\Structures\Na0.8CoO2_P63mmc.cif" # very different!
#f="C:\Users\grp66007\Dropbox\Python\Dans_Diffraction\Dans_Diffraction\Structures\Ca2RuO4.cif" # 

xtl = dif.Crystal(f)
mycr = Crystal()
mycr.load_cif(f)

energy_kev=8.0

xtl.Scatter.setup_scatter(type='x-ray', energy_kev=energy_kev)
#print("Dan's Diffraction Reflections")
#print(xtl.Scatter.print_all_reflections(print_symmetric=False, min_intensity=0.01))
#print("Extinctions")
#print(xtl.Scatter.print_all_reflections(print_symmetric=False, min_intensity=None, max_intensity=0.01))

# Generate reflection list
refs = mycr.reflection_list(energy_keV, 'sym', print_list=False)

#print 'Crystal Reflections:'
#refs.sortlist()
#refs.printlist()

for n in range(len(refs.reflections['ind'])):
    hkl = refs.reflections['ind'][n]
    ref = refs.ref(hkl)
    Ftth = ref['two_theta']
    FI = ref['Bragg']
    Dtth = xtl.Cell.tth(hkl,energy_kev)
    DI = xtl.Scatter.intensity(hkl)
    print('(%2.0f,%2.0f,%2.0f) %7.3f %7.3f   %12.6g %12.6g'%(hkl[0],hkl[1],hkl[2],Ftth,Dtth,np.sqrt(FI),np.sqrt(DI)))