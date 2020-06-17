"""
Test functions_scattering.pu

"""

import Dans_Diffraction as dif
from Dans_Diffraction import functions_scattering as fs

en = 2.838 # keV
aziref = [0,0,1]

xtl = dif.structure_list.Ca2RuO4()
xtl.Atoms.changeatom(1,mxmymz=[0,3,0.3])
xtl.generate_structure()

hkl = xtl.Cell.all_hkl(en, 120)
q = xtl.Cell.calculateQ(hkl)
qmag = dif.fg.mag(q)

uvw, type, label, occupancy, uiso, mxmymz = xtl.Structure.get()
r = xtl.Cell.calculateR(uvw)
moment = xtl.Cell.calculateR(mxmymz)
scatlength = dif.fc.neutron_scattering_length(type)
ff = dif.fc.xray_scattering_factor(type, qmag)
ffmag = dif.fc.magnetic_form_factor(type, qmag)
z = dif.fc.element_z(type)

class_inten = {
    'neutron': xtl.Scatter.neutron(hkl),
    'xray': xtl.Scatter.x_ray(hkl),
    'xfast': xtl.Scatter.x_ray_fast(hkl),
    'neutron_magnetic': xtl.Scatter.magnetic_neutron(hkl),
    'xray_magnetic': xtl.Scatter.xray_magnetic(hkl),
    #'xray_nonresonant_magnetic': xtl.Scatter.xray_nonresonant_magnetic(hkl, energy_kev=en, azim_zero=aziref, psi=0),
    #'xray_resonant': xtl.Scatter.xray_resonant(hkl, energy_kev=en, F0=0, F1=1, F2=0, azim_zero=aziref, psi=0),
    #'xray_resonant_magnetic': xtl.Scatter.xray_resonant_magnetic(hkl, energy_kev=en, F0=0, F1=1, F2=0, azim_zero=aziref, psi=0),
}

func_inten = {
    'neutron': fs.intensity(fs.sf_neutron(hkl, uvw, occupancy, scatlength, uiso)),
    'xray': fs.intensity(fs.sf_xray(hkl, uvw, occupancy, ff, uiso)),
    'xfast': fs.intensity(fs.sf_xray_fast(hkl, uvw, occupancy, z, uiso)),
    'neutron_magnetic': fs.intensity(fs.sf_magnetic_neutron(q, r, occupancy, moment, ffmag, uiso)),
    'xray_magnetic': fs.intensity(fs.sf_magnetic_xray(q, r, occupancy, moment, ffmag)),
    #'xray_nonresonant_magnetic': 0,
    #'xray_resonant': fs.intensity(fs.sf_re),
    #'xray_resonant_magnetic':
}

for key in class_inten.keys():
    difrat = 200*np.abs(class_inten[key] - func_inten[key])/np.abs(class_inten[key] + func_inten[key])
    print('%s %6.2f% %%'%(key, difrat))
