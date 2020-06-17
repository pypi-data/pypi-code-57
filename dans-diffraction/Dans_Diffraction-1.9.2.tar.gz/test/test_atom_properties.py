"""
Dans_Diffraction Tests
Check speed of different methods of reading atom_properties.txt file
"""

import os, time
import numpy as np
import Dans_Diffraction as dif

ATOMFILE = dif.fc.ATOMFILE

def atom_properties(elements=None, fields=None):
    """Old version"""

    try:
        data = np.genfromtxt(ATOMFILE, skip_header=6, dtype=None, names=True, encoding='ascii')
    except TypeError:
        # Numpy version < 1.14
        data = np.genfromtxt(ATOMFILE, skip_header=6, dtype=None, names=True)

    if elements is not None:
        # elements must be a list e.g. ['Co','O']
        elements = np.char.lower(np.asarray(elements).reshape(-1))
        indx = [None] * len(elements)
        for n in range(len(data)):
            d = data[n]
            fileelement = d['Element'].lower()
            if fileelement in elements:
                for m in range(len(elements)):
                    if fileelement == elements[m]:
                        indx[m] = n
        data = data[indx]

    if fields is None:
        return data

    return data[fields]


def atom_properties2(elements=None, fields=None):
    """Test"""

    try:
        data = np.genfromtxt(ATOMFILE, skip_header=6, dtype=None, names=True, encoding='ascii')
    except TypeError:
        # Numpy version < 1.14
        data = np.genfromtxt(ATOMFILE, skip_header=6, dtype=None, names=True)

    if elements is not None:
        # elements must be a list e.g. ['Co','O']
        elements = np.char.lower(np.asarray(elements).reshape(-1))
        all_elements = [el.lower() for el in data['Element']]
        # This will error if the required element doesn't exist
        index = [all_elements.index(el) for el in elements]
        data = data[index]

    if fields is None:
        return data

    return data[fields]


elements = ['Co','Mn','Cm']
fields = 'Z'

t1 = time.time()
for n in range(1000):
    out1 = atom_properties(elements, fields)
t2 = time.time()
for n in range(1000):
    out2 = atom_properties2(elements, fields)
t3 = time.time()

print(out1)
print(out2)

print('Method 1: %s s'%(t2-t1))
print('Method 2: %s s'%(t3-t2))

