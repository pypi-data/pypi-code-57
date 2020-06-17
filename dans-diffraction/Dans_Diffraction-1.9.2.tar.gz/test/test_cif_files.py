"""
Dans_Diffraction Tests
Check reading of cif files
"""

import sys, os, re, time
import Dans_Diffraction as dif

# 0) Check python version
print('Dans_Diffraction Unit Tests')
print('Python Version:')
print(sys.version)
print('re version: %s' % re.__version__)
print('Dans_Diffraction version: %s' % dif.__version__)
print('  classes_crystal: %s' % dif.classes_crystal.__version__)
print('  functions_crystallography: %s' % dif.fc.__version__)
print('  functions_general: %s' % dif.fg.__version__)

#files = list(dif.classes_structures.cif_list())
#files += [r"C:\Users\grp66007\Downloads\1000175.cif"]#
cifdir = os.path.expanduser('~/OneDrive - Diamond Light Source Ltd/CIF_Files')
files = [os.path.join(cifdir, nm) for nm in os.listdir(cifdir) if 'cif' in nm[-5:]]

t1 = time.time()
n = 0
m = 0
for file in files:
    print(' ')
    print(file)
    xtl = dif.Crystal(file)
    A = len(xtl.Atoms.type)
    S = len(xtl.Symmetry.symmetry_operations)
    N = len(xtl.Structure.type) # atoms in unit cell
    I = xtl.Scatter.intensity([[1,0,0],[2,0,0],[3,3,3]]) # intensity of reflection
    n += 1
    if xtl.Structure.ismagnetic():
        mag = '(magnetic)'
        m+=1
    else:
        mag = '          '
    print('%s: %s %s' % (xtl.name, xtl.Properties.molname(), mag))
    print('Atoms=%3.0f, Symmetries=%3.0f, P1=%3.0f' %(A, S, N))
    print('I(100)=%8.2f, I(200)=%8.2f, I(333)=%8.2f' % (I[0],I[1],I[2]))
t2 = time.time()

print('\n%d files (%d magnetic) parsed succesfully in %1.1fs!' % (n, m, t2-t1))