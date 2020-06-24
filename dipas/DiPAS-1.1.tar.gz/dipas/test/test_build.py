from dataclasses import dataclass
from functools import partial
from importlib import resources
import math
import operator as op
import os
import random
import re
import tempfile
import unittest

import numpy as np
import torch

from dipas.build import _from_sequence, from_file, from_script, from_twiss, from_device_data, update_from_twiss, \
    error_script, sequence_script, track_script, write_attribute_value, create_script, serialize_element, get_template, \
    SerializerError, BuildError, augment_beam, Lattice, collect_device_data, get_attribute_names
from dipas.elements import Drift, Monitor, Kicker, HKicker, VKicker, Quadrupole, SBend, Tilt, Offset, LongitudinalRoll, \
    BPMError, ApertureCircle, ApertureEllipse, ApertureRectEllipse, Segment, Parameter, elements, AlignmentError, Element, \
    CompoundElement, tensor
from dipas.external import Paramodi
from dipas.madx.parser import Command, Variable
from dipas.madx import run_script
# noinspection PyUnresolvedReferences
import dipas.test.sequences


def _dedent_script(script):
    script = script.strip(' \n')
    script = re.sub(r'^ *$(?=\n)', '', script, flags=re.MULTILINE)
    indentation = min(map(len, re.findall(r'^ +', script, flags=re.MULTILINE)))
    return re.sub(rf'^ {{{indentation}}}', '', script, flags=re.MULTILINE).strip('\n')


class _TestDedentScript(unittest.TestCase):
    def test(self):
        script = '''
            first line
                second line
            third line
        '''
        expected = 'first line\n    second line\nthird line'
        self.assertEqual(_dedent_script(script), expected)


class TestLattice(unittest.TestCase):
    def test(self):
        beam = {'particle': 'proton', 'beta': 0.6}
        a_beam = augment_beam(beam)
        with Lattice(beam) as lattice:
            lattice.Quadrupole(k1=0.1, l=2.0)
            lattice.SBend(angle=0.25, l=5.0)
        self.assertEqual(len(lattice), 2)
        self.assertIsInstance(lattice[0], Quadrupole)
        self.assertDictEqual(lattice[0].beam, a_beam)
        self.assertEqual(lattice[0].k1.item(), 0.1)
        self.assertEqual(lattice[0].l.item(), 2.0)
        self.assertIsInstance(lattice[1], SBend)
        self.assertDictEqual(lattice[1].beam, a_beam)
        self.assertEqual(lattice[1].angle.item(), 0.25)
        self.assertEqual(lattice[1].l.item(), 5.0)

        lattice += [lattice.Quadrupole(k1=0.1, l=2.0)]
        lattice += lattice.SBend(angle=0.25, l=5.0)
        self.assertEqual(len(lattice), 4)
        self.assertIsInstance(lattice[2], Quadrupole)
        self.assertDictEqual(lattice[2].beam, a_beam)
        self.assertEqual(lattice[2].k1.item(), 0.1)
        self.assertEqual(lattice[2].l.item(), 2.0)
        self.assertIsInstance(lattice[3], SBend)
        self.assertDictEqual(lattice[3].beam, a_beam)
        self.assertEqual(lattice[3].angle.item(), 0.25)
        self.assertEqual(lattice[3].l.item(), 5.0)

    def test_setattr(self):
        lattice = Lattice({'particle': 'proton', 'beta': 0.6})
        lattice[5.0] = lattice.Quadrupole(k1=0.125, l=1, label='q1')
        lattice['q1', 2.0] = lattice.Quadrupole(k1=0.25, l=2, label='q2')
        lattice[12.0] = lattice.Quadrupole(k1=0.5, l=4, label='q3')
        self.assertEqual(len(lattice), 6)
        self.assertIsInstance(lattice[0], Drift)
        self.assertEqual(lattice[0].l.item(), 5.0)
        self.assertIsInstance(lattice[1], Quadrupole)
        self.assertIs(lattice[1], lattice['q1'])
        self.assertEqual(lattice[1].label, 'q1')
        self.assertIsInstance(lattice[2], Drift)
        self.assertEqual(lattice[2].l.item(), 2.0)
        self.assertIsInstance(lattice[3], Quadrupole)
        self.assertIs(lattice[3], lattice['q2'])
        self.assertEqual(lattice[3].label, 'q2')
        self.assertIsInstance(lattice[4], Drift)
        self.assertEqual(lattice[4].l.item(), 2.0)
        self.assertIsInstance(lattice[5], Quadrupole)
        self.assertIs(lattice[5], lattice['q3'])
        self.assertEqual(lattice[5].label, 'q3')

    def test_negative_offset(self):
        lattice = Lattice({'particle': 'proton', 'beta': 0.6})
        lattice[2.0] = lattice.Quadrupole(k1=0, l=1)
        with self.assertRaises(BuildError):
            lattice[0.0] = lattice.Quadrupole(k1=0, l=1)


class TestFromFile(unittest.TestCase):
    def test(self):
        script = _dedent_script('''
        BEAM, particle = proton, energy = 2;
        
        q1_k1 = 0.5;  // [flow] variable
        q2_k1 = 0.1;  // [flow] variable
        q3_k1 = 0.2;  // [flow] variable
        
        Q: QUADRUPOLE, l = 2;
        seq: SEQUENCE, l = 36, refer = entry;
            q1: Q, k1 := q1_k1, at = 4;
            m1: MONITOR, at = 8;
            q2: Q, k1 := q2_k1, at = q1->l/2 + 4, from = "q1";
            m2: MONITOR, at = 14;
            q3: Q, l = 4, k1 := q3_k1, at = q2->l/2 + 4, from = "q2";
            s1: SBEND, angle = 0.125, l = 4, at = q3->l/2 + 4, from = "q3";
            h1: HKICKER, kick = 0.5, at = 29;
            v1: VKICKER, kick = 0.5, at = 30;
            q4: QUADRUPOLE, l = 2, k1 = 0.5, tilt = -0.1, at = 32;
        ENDSEQUENCE;
        
        eoption, seed = 0, add = true;
        select, flag = error, clear;
        select, flag = error, class = Q;
        q_dx := ranf() - 0.5;  // [flow] variable
        ealign, dx = q_dx;
        select, flag = error, clear;
        select, flag = error, range = "q3";
        ealign, dy = 0.1;
        select, flag = error, clear;
        select, flag = error, range = "q4";
        q4_dy = 0.25;  // [flow] variable
        q4_dpsi = 0.50;  // [flow] variable
        ealign, dy := q4_dy, dpsi := q4_dpsi;
        select, flag = error, clear;
        select, flag = error, range = m2;
        ealign, mrex = 0.25, mscaly = 0.50;
        ''')
        lattice_1 = from_script(script)
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'test')
            with open(f_name, 'w') as fh:
                fh.write(script)
            lattice_2 = from_file(f_name).elements
        for func, lattice in zip([from_script, from_file], [lattice_1, lattice_2]):
            with self.subTest(func=func):
                np.random.seed(0)  # Reset RNG seed for following comparisons.
                self.assertEqual(len(lattice), 19)  # Including implicit drifts.
                element_types = [
                    Drift, Offset, Drift, Monitor, Drift, Offset, Drift, BPMError, Drift, Offset, Drift, SBend, Drift,
                    HKicker, Drift, VKicker, Drift, Offset, Drift
                ]
                for i, (e, t) in enumerate(zip(lattice, element_types)):
                    with self.subTest(i=i, e=e, t=t):
                        self.assertIsInstance(e, t)

                # Check drifts.
                self.assertEqual(lattice[0].l, 4.)
                self.assertEqual(lattice[2].l, 2.)
                self.assertEqual(lattice[4].l, 2.)
                self.assertEqual(lattice[6].l, 2.)
                self.assertEqual(lattice[8].l, 2.)
                self.assertEqual(lattice[10].l, 4.)
                self.assertEqual(lattice[12].l, 1.)
                self.assertEqual(lattice[14].l, 1.)
                self.assertEqual(lattice[16].l, 2.)
                self.assertEqual(lattice[18].l, 2.)

                # Check quadrupoles 1 - 3.
                self.assertIsInstance(lattice[1].target, Quadrupole)
                self.assertIsInstance(lattice[1].target.k1, Parameter)
                self.assertEqual(lattice[1].target.k1.item(), 0.5)
                self.assertEqual(lattice[1].target.l, 2.)
                self.assertIsInstance(lattice[5].target, Quadrupole)
                self.assertIsInstance(lattice[5].target.k1, Parameter)
                self.assertEqual(lattice[5].target.k1.item(), 0.1)
                self.assertEqual(lattice[5].target.l, 2.)
                self.assertIsInstance(lattice[9].target, Quadrupole)
                self.assertIsInstance(lattice[9].target.k1, Parameter)
                self.assertEqual(lattice[9].target.k1.item(), 0.2)
                self.assertEqual(lattice[9].target.l, 4.)

                # Check offsets.
                self.assertIsInstance(lattice[1].dx, Parameter)
                self.assertEqual(lattice[1].dx.item(), np.random.random() - 0.5)
                self.assertEqual(lattice[1].dy, 0.)
                self.assertIsInstance(lattice[5].dx, Parameter)
                self.assertEqual(lattice[5].dx.item(), np.random.random() - 0.5)
                self.assertEqual(lattice[5].dy, 0.)
                self.assertIsInstance(lattice[9].dx, Parameter)
                self.assertEqual(lattice[9].dx.item(), np.random.random() - 0.5)
                self.assertEqual(lattice[9].dy, 0.1)

                # Check 4th quadrupole.
                self.assertIsInstance(lattice[17].target, LongitudinalRoll)
                self.assertIsInstance(lattice[17].target.target, Tilt)
                self.assertIsInstance(lattice[17].target.target.target, Quadrupole)
                self.assertNotIsInstance(lattice[17].dx, Parameter)
                self.assertEqual(lattice[17].dx, 0.)
                self.assertIsInstance(lattice[17].dy, Parameter)
                self.assertEqual(lattice[17].dy.item(), 0.25)
                self.assertIsInstance(lattice[17].target.psi, Parameter)
                self.assertEqual(lattice[17].target.psi.item(), 0.5)
                self.assertNotIsInstance(lattice[17].target.target.psi, Parameter)
                self.assertEqual(lattice[17].target.target.psi, -0.1)

                # Check BPMError, Monitor.
                self.assertIsInstance(lattice[7], BPMError)
                self.assertEqual(lattice[7].ax, 0.25)
                self.assertEqual(lattice[7].ay, 0.00)
                self.assertEqual(lattice[7].rx, 0.00)
                self.assertEqual(lattice[7].ry, 0.50)
                self.assertIsInstance(lattice[7].target, Monitor)
                self.assertIs(lattice[7].target, lattice[7].element)

    def test_errors_from_madx(self):
        script = _dedent_script('''
        BEAM, particle = proton, energy = 2;

        q1_k1 = 0.5;  // [flow] variable
        q2_k1 = 0.1;  // [flow] variable
        q3_k1 = 0.2;  // [flow] variable

        Q: QUADRUPOLE, l = 2;
        seq: SEQUENCE, l = 36, refer = entry;
            q1: Q, k1 := q1_k1, at = 4;
            m1: MONITOR, at = 8;
            q2: Q, k1 := q2_k1, at = q1->l/2 + 4, from = "q1";
            m2: MONITOR, at = 14;
            q3: Q, l = 4, k1 := q3_k1, at = q2->l/2 + 4, from = "q2";
            s1: SBEND, angle = 0.125, l = 4, at = q3->l/2 + 4, from = "q3";
            h1: HKICKER, kick = 0.5, at = 29;
            v1: VKICKER, kick = 0.5, at = 30;
            q4: QUADRUPOLE, l = 2, k1 = 0.5, tilt = -0.1, at = 32;
        ENDSEQUENCE;
        
        use, sequence = seq;

        eoption, seed = 0, add = true;
        select, flag = error, clear;
        select, flag = error, class = Q;
        q_dx := 0.5;  // [flow] variable
        ealign, dx = q_dx;
        select, flag = error, clear;
        select, flag = error, range = "q3";
        ealign, dy = 0.1;
        select, flag = error, clear;
        select, flag = error, range = "q4";
        q4_dy = 0.25;  // [flow] variable
        q4_dpsi = 0.50;  // [flow] variable
        ealign, dy := q4_dy, dpsi := q4_dpsi;
        select, flag = error, clear;
        select, flag = error, range = m2;
        ealign, mrex = 0.25, mscaly = 0.50;
        select, flag = error, full;
        esave, file = "test_errors";
        ''')
        original_errors = run_script(script, ['test_errors'], madx=os.path.expanduser('~/bin/madx'))['test_errors']
        test_errors = original_errors.set_index('NAME')
        test_errors.index = test_errors.index.str.lower()
        test_errors.columns = test_errors.columns.str.lower()
        self.assertDictEqual({k: v for k, v in test_errors.loc['q1', :].items() if v != 0}, {'dx': 0.5})
        self.assertDictEqual({k: v for k, v in test_errors.loc['q2', :].items() if v != 0}, {'dx': 0.5})
        self.assertDictEqual({k: v for k, v in test_errors.loc['q3', :].items() if v != 0}, {'dx': 0.5, 'dy': 0.1})
        self.assertDictEqual({k: v for k, v in test_errors.loc['q4', :].items() if v != 0}, {'dy': 0.25, 'dpsi': 0.5})
        self.assertDictEqual({k: v for k, v in test_errors.loc['m2', :].items() if v != 0},
                             {'mrex': 0.25, 'mscaly': 0.5})
        for errors in [original_errors, original_errors.set_index('NAME')]:
            lattice_1 = from_script(script, errors=errors)
            with tempfile.TemporaryDirectory() as td:
                f_name = os.path.join(td, 'test')
                with open(f_name, 'w') as fh:
                    fh.write(script)
                lattice_2 = from_file(f_name, errors=errors).elements
            for func, lattice in zip([from_script, from_file], [lattice_1, lattice_2]):
                with self.subTest(func=func):
                    np.random.seed(0)  # Reset RNG seed for following comparisons.
                    self.assertEqual(len(lattice), 19)  # Including implicit drifts.
                    element_types = [
                        Drift, Offset, Drift, Monitor, Drift, Offset, Drift, BPMError, Drift, Offset, Drift, SBend,
                        Drift, HKicker, Drift, VKicker, Drift, Offset, Drift
                    ]
                    for i, (e, t) in enumerate(zip(lattice, element_types)):
                        with self.subTest(i=i, e=e, t=t):
                            self.assertIsInstance(e, t)

                    # Check drifts.
                    self.assertEqual(lattice[0].l, 4.)
                    self.assertEqual(lattice[2].l, 2.)
                    self.assertEqual(lattice[4].l, 2.)
                    self.assertEqual(lattice[6].l, 2.)
                    self.assertEqual(lattice[8].l, 2.)
                    self.assertEqual(lattice[10].l, 4.)
                    self.assertEqual(lattice[12].l, 1.)
                    self.assertEqual(lattice[14].l, 1.)
                    self.assertEqual(lattice[16].l, 2.)
                    self.assertEqual(lattice[18].l, 2.)

                    # Check quadrupoles 1 - 3.
                    self.assertIsInstance(lattice[1].target, Quadrupole)
                    self.assertEqual(lattice[1].target.k1.item(), 0.5)
                    self.assertEqual(lattice[1].target.l, 2.)
                    self.assertIsInstance(lattice[5].target, Quadrupole)
                    self.assertEqual(lattice[5].target.k1.item(), 0.1)
                    self.assertEqual(lattice[5].target.l, 2.)
                    self.assertIsInstance(lattice[9].target, Quadrupole)
                    self.assertEqual(lattice[9].target.k1.item(), 0.2)
                    self.assertEqual(lattice[9].target.l, 4.)

                    # Check offsets.
                    self.assertEqual(lattice[1].dx.item(), 0.5)
                    self.assertEqual(lattice[1].dy, 0.)
                    self.assertEqual(lattice[5].dx.item(), 0.5)
                    self.assertEqual(lattice[5].dy, 0.)
                    self.assertEqual(lattice[9].dx.item(), 0.5)
                    self.assertEqual(lattice[9].dy, 0.1)

                    # Check 4th quadrupole.
                    self.assertIsInstance(lattice[17].target, LongitudinalRoll)
                    self.assertIsInstance(lattice[17].target.target, Tilt)
                    self.assertIsInstance(lattice[17].target.target.target, Quadrupole)
                    self.assertEqual(lattice[17].dx, 0.)
                    self.assertEqual(lattice[17].dy, 0.25)
                    self.assertEqual(lattice[17].target.psi, 0.5)
                    self.assertEqual(lattice[17].target.target.psi, -0.1)

                    # Check BPMError, Monitor.
                    self.assertIsInstance(lattice[7], BPMError)
                    self.assertEqual(lattice[7].ax, 0.25)
                    self.assertEqual(lattice[7].ay, 0.00)
                    self.assertEqual(lattice[7].rx, 0.00)
                    self.assertEqual(lattice[7].ry, 0.50)
                    self.assertIsInstance(lattice[7].target, Monitor)
                    self.assertIs(lattice[7].target, lattice[7].element)


class TestFromTwiss(unittest.TestCase):
    def test(self):
        beam = dict(particle='proton', energy=1)
        with resources.path('dipas.test.sequences', 'cryring.seq') as f_path:
            lattice_ref = from_file(f_path, beam=beam)
        script_ref = create_script(sequence=lattice_ref, beam=beam)
        lattice_test = from_twiss(run_script(script_ref, twiss=True, madx=os.path.expanduser('~/bin/madx'))['twiss'][0],
                                  beam=beam)
        for e1, e2 in zip(lattice_test, lattice_ref):
            with self.subTest(e1=e1, e2=e2):
                self.assertEqual(type(e1), type(e2))
                self.assertEqual(e1.label, e2.label)
                self.assertDictEqual(e1.beam, e2.beam)
                self.assertDictEqual({k: getattr(e1, k).item() for k in get_attribute_names(e1)},
                                     {k: getattr(e1, k).item() for k in get_attribute_names(e2)})


class TestUpdateFromTwiss(unittest.TestCase):
    def test(self):
        beam = dict(particle='proton', energy=1)
        with resources.path('dipas.test.sequences', 'cryring.seq') as f_path:
            lattice_ref = from_file(f_path, beam=beam)
            lattice_test = from_file(f_path, beam=beam)
        for element in lattice_test:
            for name in get_attribute_names(element):
                getattr(element, name).data = tensor(0.)
        script_ref = create_script(sequence=lattice_ref, beam=beam)
        twiss_ref = run_script(script_ref, twiss=True, madx=os.path.expanduser('~/bin/madx'))['twiss'][0]
        update_from_twiss(lattice_test, twiss_ref)
        for e1, e2 in zip(lattice_test, lattice_ref):
            with self.subTest(e1=e1, e2=e2):
                self.assertEqual(type(e1), type(e2))
                self.assertEqual(e1.label, e2.label)
                self.assertDictEqual(e1.beam, e2.beam)
                self.assertDictEqual({k: getattr(e1, k).item() for k in get_attribute_names(e1)},
                                     {k: getattr(e1, k).item() for k in get_attribute_names(e2)})


class TestFromDeviceData(unittest.TestCase):
    def test(self):
        script = _dedent_script('''
        BEAM, particle = proton, energy = 2;

        q1_k1 = 0;
        q2_k1 = 0.1;
        q3_k1 = 0.2;

        Q: QUADRUPOLE, l = 2;
        seq: SEQUENCE, l = 36, refer = entry;
            q1: Q, k1 := q1_k1, at = 4;
            m1: MONITOR, at = 8;
            q2: Q, k1 := q2_k1, at = q1->l/2 + 4, from = "q1";
            m2: MONITOR, at = 14;
            q3: Q, l = 4, k1 := q3_k1, at = q2->l/2 + 4, from = "q2";
            s1: SBEND, angle = 0.125, l = 4, at = q3->l/2 + 4, from = "q3";
            h1: HKICKER, kick = 0.5, at = 29;
            v1: VKICKER, kick = 0.5, at = 30;
            q4: QUADRUPOLE, l = 2, k1 = 0.5, tilt = -0.1, at = 32;
        ENDSEQUENCE;

        use, sequence = seq;
        ''')
        lattice = from_script(script)
        devices = collect_device_data(lattice)
        lattice2 = from_device_data(devices, beam={'particle': 'proton', 'energy': 2})
        for e1, e2 in zip(lattice, lattice2):
            self.assertIs(type(e1), type(e2))
            self.assertEqual(e1.label, e2.label)
            for attr in get_attribute_names(e1):
                self.assertEqual(getattr(e1, attr), getattr(e2, attr))
            if isinstance(e1, (Element, CompoundElement)):
                self.assertTrue(torch.all(e1.d == e2.d))
                self.assertTrue(torch.all(e1.R == e2.R))
                self.assertTrue(torch.all(e1.T == e2.T))
            elif isinstance(e1, AlignmentError):
                self.assertTrue(torch.all(e1.d_enter == e2.d_enter))
                self.assertTrue(torch.all(e1.R_enter == e2.R_enter))
                self.assertTrue(torch.all(e1.T_enter == e2.T_enter))
                self.assertTrue(torch.all(e1.d_exit == e2.d_exit))
                self.assertTrue(torch.all(e1.R_exit == e2.R_exit))
                self.assertTrue(torch.all(e1.T_exit == e2.T_exit))
            else:
                self.fail(f'Illegal element type: {type(e1)}')


class TestBuildLattice(unittest.TestCase):
    def test_single_element(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        attributes = {'l': 1.0, 'kick': 0, 'hkick': 0, 'vkick': 0, 'k1': 0, 'k2': 0, 'angle': 0, 'h': 0, 'e1': 0,
                      'e2': 0, 'fint': 0, 'fintx': 0, 'hgap': 0, 'h1': 0, 'h2': 0, 'dk0': 0, 'dk1': 0, 'dk1l': 0,
                      'dk2': 0, 'dk2l': 0}
        for name, cls in elements.items():
            attributes['l'] = 0. if name == 'marker' else 1.0
            cmd = Command(name, {k: attributes[k] for k in get_attribute_names(cls)}, name)
            if name in ('hkicker', 'vkicker'):
                del cmd['hkick']
                del cmd['vkick']
            lattice = _from_sequence(beam, [cmd]).elements
            self.assertEqual(len(lattice), 1)
            self.assertIsInstance(lattice[0], cls)
            self.assertEqual(lattice[0].label, name)

    def test_multiple_elements(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        attributes = {'l': 1.0, 'kick': 0, 'hkick': 0, 'vkick': 0, 'k1': 0, 'k2': 0, 'angle': 0, 'h': 0, 'e1': 0,
                      'e2': 0, 'fint': 0, 'fintx': 0, 'hgap': 0, 'h1': 0, 'h2': 0, 'dk0': 0, 'dk1': 0, 'dk1l': 0,
                      'dk2': 0, 'dk2l': 0}
        elements_ = {name: (name, Command(name, {k: attributes[k] for k in get_attribute_names(cls)}, name), cls)
                     for name, cls in elements.items() if name != 'marker'}
        for name in ('hkicker', 'vkicker'):
            del elements_[name][1]['hkick']
            del elements_[name][1]['vkick']
        elements_ = list(elements_.values())
        for i in range(10):  # Run 10 distinct tests.
            with self.subTest(nr=i):
                k = random.randint(5, 50)
                indices = random.choices(range(len(elements_)), k=k)
                lattice = _from_sequence(beam, map(op.itemgetter(1), (elements_[j] for j in indices))).elements
                self.assertEqual(len(lattice), k)
                for j, element in zip(indices, lattice):
                    with self.subTest(element_nr=j, element=element):
                        self.assertIsInstance(element, elements_[j][2])
                        self.assertEqual(element.label, elements_[j][0])
                        for attr in get_attribute_names(element):
                            self.assertIsInstance(getattr(element, attr), torch.Tensor)

    def test_derived_commands(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        base = Command('quadrupole', {'l': 1.0, 'k1': 2.0}, label='q1')
        derived = Command('q1', {'k1': 4.0}, base=base)
        lattice = _from_sequence(beam, [base, derived]).elements
        self.assertEqual(len(lattice), 2)
        self.assertIsInstance(lattice[0], elements['quadrupole'])
        self.assertIsInstance(lattice[1], elements['quadrupole'])
        self.assertEqual(lattice[0].label, 'q1')
        self.assertIs(lattice[1].label, None)
        self.assertEqual(lattice[0].l, 1.0)
        self.assertEqual(lattice[0].k1, 2.0)
        self.assertEqual(lattice[1].l, 1.0)
        self.assertEqual(lattice[1].k1, 4.0)

    # noinspection PyShadowingNames
    def test_wrapper(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        commands = [
            Command('quadrupole', dict(l=1.0, k1=0.5), label='q1'),
            Command('quadrupole', dict(l=1.0, k1=1.0, tilt=Variable(0.25)), label='q2'),
            Command('quadrupole', dict(l=1.0, k1=2.0, tilt=1.5), label='q3'),
        ]
        elements = _from_sequence(beam, commands).elements
        self.assertEqual(len(elements), 3)
        self.assertIsInstance(elements[0], Quadrupole)
        self.assertEqual(elements[0].k1.detach().item(), 0.5)
        self.assertEqual(elements[0].l, 1.0)
        self.assertEqual(elements[0].label, 'q1')
        self.assertIsInstance(elements[1], Tilt)
        self.assertIsInstance(elements[1].psi, Parameter)
        self.assertEqual(elements[1].psi, 0.25)
        self.assertIsInstance(elements[1].target, Quadrupole)
        self.assertEqual(elements[1].target.k1.detach().item(), 1.0)
        self.assertEqual(elements[1].target.l, 1.0)
        self.assertEqual(elements[1].target.label, 'q2')
        self.assertIsInstance(elements[2], Tilt)
        self.assertEqual(elements[2].psi, 1.5)
        self.assertIsInstance(elements[2].target, Quadrupole)
        self.assertEqual(elements[2].target.k1.detach().item(), 2.0)
        self.assertEqual(elements[2].target.l, 1.0)
        self.assertEqual(elements[2].target.label, 'q3')

    def test_variable_indicators(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        base = Command('quadrupole', {'l': 1.0, 'k1': Variable(2.0)}, label='q1')
        derived = Command('q1', {'l': 4.0}, base=base)
        lattice = _from_sequence(beam, [base, derived]).elements
        self.assertEqual(lattice[0].l, 1.0)
        self.assertIsInstance(lattice[0].k1, Parameter)
        self.assertEqual(lattice[0].k1.item(), 2.0)
        self.assertEqual(lattice[1].l, 4.0)
        self.assertIsInstance(lattice[1].k1, Parameter)
        self.assertEqual(lattice[1].k1.item(), 2.0)

    # noinspection PyUnresolvedReferences
    def test_aperture(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        element = _from_sequence(beam,
                                 [Command('drift', dict(l=1.0, apertype='ellipse', aperture=[1.0, 2.0]))]).elements[0]
        self.assertIsInstance(element.aperture, ApertureEllipse)
        self.assertListEqual(element.aperture.aperture.numpy().tolist(), [1.0, 2.0])
        element = _from_sequence(beam, [Command('drift', dict(l=1.0))]).elements[0]
        self.assertIsInstance(element.aperture, ApertureCircle)
        self.assertEqual(element.aperture.aperture.numpy().tolist(), np.inf)

    # noinspection PyUnresolvedReferences
    def test_padding(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        element = _from_sequence(beam, [Command('drift', dict(l=1.0, aperture=4.0))], padding=1.0).elements[0]
        self.assertIsInstance(element.aperture, ApertureCircle)
        self.assertEqual(element.aperture.aperture.numpy().tolist(), 4.0)
        self.assertEqual(element.aperture.padding.tolist(), 1.0)

    def test_unknown_element(self):
        with self.assertWarns(UserWarning):
            _from_sequence({'beta': 0.6, 'gamma': 1.25}, [Command('unknown')])


class TestAugmentBeam(unittest.TestCase):
    def test(self):
        base_attrs = dict(mass=1, charge=1)
        for attrs in (dict(energy=2.0), dict(gamma=2.0), dict(beta=math.sqrt(0.75)), dict(pc=math.sqrt(3)),
                      dict(brho=math.sqrt(3) / 0.299792458)):
            with self.subTest(beam_parameters=attrs):
                beam = augment_beam(dict(base_attrs, **attrs))
                self.assertAlmostEqual(beam['beta'], math.sqrt(0.75))
                self.assertAlmostEqual(beam['gamma'], 2.0)
                self.assertAlmostEqual(beam['energy'], 2.0)
                self.assertAlmostEqual(beam['pc'], math.sqrt(3))
                self.assertAlmostEqual(beam['brho'], math.sqrt(3) / 0.299792458)

    def test_unknown_particle_type(self):
        with self.assertRaises(ValueError):
            augment_beam(dict(particle='unknown'))

    def test_incomplete_beam_command(self):
        with self.assertRaises(ValueError):
            augment_beam(dict(mass=1.0))
        with self.assertRaises(ValueError):
            augment_beam(dict(charge=1.0))
        with self.assertRaises(ValueError):
            augment_beam(dict(particle='proton'))


class TestFieldErrors(unittest.TestCase):
    def test(self):
        script = _dedent_script('''
        BEAM, particle = proton, energy = 2;

        seq: SEQUENCE, l = 9, refer = entry;
            Q1: QUADRUPOLE, l = 2, k1 = 0.1, tilt = 0.2, at = 0;
            Q2: QUADRUPOLE, l = 3, k1 = 0.2            , at = 2;
            Q3: QUADRUPOLE, l = 4, k1 = 0.3            , at = 5;
        ENDSEQUENCE;

        use, sequence = seq;

        select, flag = error, clear;
        select, flag = error, range = "q1";
        efcomp, dkn = {0, 1.0};
        
        select, flag = error, clear;
        select, flag = error, range = "q3";
        efcomp, dkn := {0, 20};
        
        select, flag = error, full;
        esave, file = "test_errors";
        ''')
        errors = run_script(script, ['test_errors'], madx=os.path.expanduser('~/bin/madx'))['test_errors']
        lattice_1 = from_script(script, errors=errors)
        lattice_2 = from_script(script, errors=True)
        lattice_3 = from_script(create_script(beam=dict(particle='proton', energy=2), sequence=lattice_2, errors=True),
                                errors=True)
        for errors_arg, lattice in zip([type(errors), True, 'round_trip'], [lattice_1, lattice_2, lattice_3]):
            with self.subTest(errors=errors_arg):
                self.assertIsInstance(lattice[0], Tilt)
                self.assertIsInstance(lattice[0].target, Quadrupole)
                self.assertEqual(lattice[0].target.k1.item(), 0.1)
                self.assertEqual(lattice[0].target.dk1.item(), 0.5)
                self.assertIsInstance(lattice[1], Quadrupole)
                self.assertEqual(lattice[1].k1.item(), 0.2)
                self.assertEqual(lattice[1].dk1.item(), 0.0)
                self.assertIsInstance(lattice[2], Quadrupole)
                self.assertEqual(lattice[2].k1.item(), 0.3)
                self.assertEqual(lattice[2].dk1.item(), 5.0)

    def test_kickers(self):
        script = _dedent_script('''
        BEAM, particle = proton, energy = 2;

        seq: SEQUENCE, l = 1, refer = entry;
            KH: HKicker, kick = 0.0, at = 0;
            KV: VKicker, kick = 0.0, at = 0;
            K: Kicker, hkick = 0.0, vkick = 0.0, at = 0;
        ENDSEQUENCE;

        use, sequence = seq;

        select, flag = error, clear;
        select, flag = error, range = "KH";
        efcomp, dkn = {1.0}, dks = {2.0};
        
        select, flag = error, clear;
        select, flag = error, range = "KV";
        efcomp, dkn = {4.0}, dks = {8.0};
        
        select, flag = error, clear;
        select, flag = error, range = "K";
        efcomp, dkn = {0.25}, dks = {0.50};

        select, flag = error, full;
        esave, file = "test_errors";
        ''')
        errors = run_script(script, ['test_errors'], madx=os.path.expanduser('~/bin/madx'))['test_errors']
        lattice_1 = from_script(script, errors=errors)
        lattice_2 = from_script(script, errors=True)
        lattice_3 = from_script(create_script(beam=lattice_2[0].beam, sequence=lattice_2, errors=True), errors=True)
        for errors_arg, lattice in zip([type(errors), True, 'round_trip'], [lattice_1, lattice_2, lattice_3]):
            with self.subTest(errors=errors_arg):
                self.assertIs(type(lattice[0]), HKicker)
                self.assertEqual(lattice[0].hkick.item(), 0.0)
                self.assertEqual(lattice[0].vkick.item(), 0.0)
                self.assertEqual(lattice[0].dkh.item(), 1.0)
                self.assertEqual(lattice[0].dkv.item(), 2.0)

                self.assertIs(type(lattice[1]), VKicker)
                self.assertEqual(lattice[1].hkick.item(), 0.0)
                self.assertEqual(lattice[1].vkick.item(), 0.0)
                self.assertEqual(lattice[1].dkh.item(), 4.0)
                self.assertEqual(lattice[1].dkv.item(), 8.0)

                self.assertIs(type(lattice[2]), Kicker)
                self.assertEqual(lattice[2].hkick.item(), 0.0)
                self.assertEqual(lattice[2].vkick.item(), 0.0)
                self.assertEqual(lattice[2].dkh.item(), 0.25)
                self.assertEqual(lattice[2].dkv.item(), 0.50)


# noinspection PyTypeChecker
class TestWriteElement(unittest.TestCase):
    class _Test:
        aperture = ApertureCircle()
        field_errors = {}

        @property
        def element(self):
            return self

    def setUp(self):
        self.maxDiff = None

    def _write_element(self, element):
        return get_template('command.madx.j2').render(command=serialize_element(element))

    def test_float_attributes(self):
        @dataclass
        class Test(self._Test):
            a: float
            b: float
        self.assertEqual(self._write_element(Test(1., 2.)), 'test, a = 1.0, b = 2.0')

    def test_string_attributes(self):
        @dataclass
        class Test(self._Test):
            a: str
        self.assertEqual(self._write_element(Test('should be quoted')), 'test, a = "should be quoted"')

    def test_list_attributes(self):
        @dataclass
        class Test(self._Test):
            a: list
            b: list
        self.assertEqual(self._write_element(Test([1], [2, 3])), 'test, a = {1}, b = {2, 3}')
        self.assertEqual(self._write_element(Test([[1]], [2, [3, 4]])), 'test, a = {{1}}, b = {2, {3, 4}}')

    def test_flag_attributes(self):
        @dataclass
        class Test(self._Test):
            a: bool
            b: bool
        self.assertEqual(self._write_element(Test(True, False)), 'test, a = true, b = false')

    def test_aperture(self):
        @dataclass
        class Test(self._Test):
            aperture = ApertureCircle(1)
        self.assertEqual(self._write_element(Test()), 'test, aperture = 1.0, apertype = "circle"')

    def test_wrapped(self):
        element = Tilt(SBend(0.2, 1.0, beam={'beta': 0.6, 'gamma': 1.25}), 0.1)
        self.assertTrue(hasattr(element, 'target'))
        self.assertIsInstance(element.target, SBend)
        self.assertEqual(
            self._write_element(element),
            'sbend, angle = 0.2, e1 = 0.0, e2 = 0.0, fint = 0.0, fintx = 0.0, h1 = 0.0, h2 = 0.0, hgap = 0.0, l = 1.0, tilt = 0.1'
        )

    # noinspection PyShadowingNames
    def test_elements(self):
        beam_config = {'beta': 0.6, 'gamma': 1.25}
        attributes = {'l': 0.125, 'kick': 0.25, 'k1': 0.375, 'angle': 0.5}
        elements = (Drift, HKicker, VKicker, Quadrupole, SBend)
        expected = ('drift, l = {l}', 'hkicker, kick = {kick}, l = {l}', 'vkicker, kick = {kick}, l = {l}',
                    'quadrupole, k1 = {k1}, l = {l}',
                    'sbend, angle = {angle}, e1 = 0.0, e2 = 0.0, fint = 0.0, fintx = 0.0, h1 = 0.0, h2 = 0.0, hgap = 0.0, l = {l}')
        for element, output in zip(elements, expected):
            with self.subTest(element=element.__name__):
                with self.assertWarns(UserWarning):
                    instance = element(beam=beam_config, **attributes)
                self.assertEqual(self._write_element(instance), output.format(**attributes))

    def test_drift(self):
        self.assertEqual(self._write_element(Drift(1.0, beam={'beta': 0.6, 'gamma': 1.25})), 'drift, l = 1.0')
        self.assertEqual(self._write_element(Drift(1.0, beam={'beta': 0.6, 'gamma': 1.25}, aperture=ApertureCircle(1.0))),
                         'quadrupole, aperture = 1.0, apertype = "circle", k1 = 0.0, l = 1.0')
        self.assertEqual(self._write_element(Drift(1.0, beam={'beta': 0.6, 'gamma': 1.25}, aperture=ApertureEllipse([1.0, 2.0]))),
                         'quadrupole, aperture = {1.0, 2.0}, apertype = "ellipse", k1 = 0.0, l = 1.0')


class TestWriteAttributeValue(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_bool(self):
        for b in (True, False):
            with self.subTest(b=b):
                self.assertEqual(write_attribute_value(b), str(b).lower())

    def test_string(self):
        self.assertEqual(write_attribute_value('test string'), '"test string"')

    def test_integer(self):
        for i in range(101):
            with self.subTest(i=i):
                self.assertEqual(write_attribute_value(i), f'{i}')

    def test_float(self):
        for x in 2. ** np.arange(-10, 11):
            with self.subTest(x=x):
                self.assertEqual(write_attribute_value(x), f'{x}')

    def test_sequence(self):
        for i in range(1, 11):
            for t in (tuple, list):
                with self.subTest(i=i, t=t):
                    self.assertEqual(write_attribute_value(t(range(i))), '{' + ', '.join(map(str, range(i))) + '}')

    def test_numpy_array(self):
        self.assertEqual(write_attribute_value(np.arange(5)), '{0, 1, 2, 3, 4}')

    def test_torch_tensor(self):
        self.assertEqual(write_attribute_value(torch.from_numpy(np.arange(5))), '{0, 1, 2, 3, 4}')

    # noinspection PyArgumentList
    def test_torch_parameter(self):
        self.assertEqual(write_attribute_value(torch.nn.Parameter(torch.tensor(1.0))), '1.0')
        self.assertEqual(write_attribute_value(torch.nn.Parameter(torch.from_numpy(1.*np.arange(2)))), '{0.0, 1.0}')


class TestSequenceToScript(unittest.TestCase):
    beam_config = {'beta': 0.6, 'gamma': 1.25}

    def setUp(self):
        self.maxDiff = None

    def test_single_element(self):
        label = 'test_seq'
        sequence = [Drift(10., beam=self.beam_config, label='test_label')]
        output = sequence_script(Segment(sequence), label)
        expected = _dedent_script(f'''
            {label}: sequence, l = {sequence[0].l}, refer = entry;
                {sequence[0].label}: drift, l = {sequence[0].l}, at = 0.0;
            endsequence;
        ''')
        self.assertEqual(output, expected)

    def test_multiple_elements(self):
        label = 'test_seq'
        sequence = [Drift(10., beam=self.beam_config, label='drift_1'),
                    Quadrupole(0.25, 5., beam=self.beam_config, label='quad_1'),
                    Drift(8., beam=self.beam_config, label='drift_2'),
                    SBend(0.125, 2.5, beam=self.beam_config, label='sbend_1'),
                    Drift(5., beam=self.beam_config, label='drift_3')]
        output = sequence_script(Segment(sequence), label)
        expected = _dedent_script('''
        test_seq: sequence, l = 30.5, refer = entry;
            drift_1: drift, l = 10.0, at = 0.0;
            quad_1: quadrupole, k1 = 0.25, l = 5.0, at = 10.0;
            drift_2: drift, l = 8.0, at = 15.0;
            sbend_1: sbend, angle = 0.125, e1 = 0.0, e2 = 0.0, fint = 0.0, fintx = 0.0, h1 = 0.0, h2 = 0.0, hgap = 0.0, l = 2.5, at = 23.0;
            drift_3: drift, l = 5.0, at = 25.5;
        endsequence;
        ''')
        self.assertEqual(output, expected)


class TestTrackToScript(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_recloss(self):
        expected_template = _dedent_script('''
            track, aperture = true, recloss = %(recloss)s, onepass = true, dump = true, onetable = true;
                start, x = 0, px = 1, y = 2, py = 3, t = 4, pt = 5;
                start, x = 6, px = 7, y = 8, py = 9, t = 10, pt = 11;
                start, x = 12, px = 13, y = 14, py = 15, t = 16, pt = 17;
                start, x = 18, px = 19, y = 20, py = 21, t = 22, pt = 23;
                start, x = 24, px = 25, y = 26, py = 27, t = 28, pt = 29;
                
                observe, place = p1;
                observe, place = somewhere_else;
                observe, place = here_as_well;
                
                run, turns = 1, maxaper = {0.1, 0.01, 0.1, 0.01, 1.0, 0.1};
                
                write, table = trackloss, file;
            endtrack;
        ''')
        track_script_partials = [
            partial(track_script, np.arange(30).reshape(5, 6).T, ['p1', 'somewhere_else', 'here_as_well']),
            partial(track_script, torch.from_numpy(np.arange(30).reshape(5, 6).T),
                    ['p1', 'somewhere_else', 'here_as_well']),
        ]
        for track_script_2 in track_script_partials:
            for recloss in (True, False):
                with self.subTest(recloss=recloss):
                    script = track_script_2(recloss=recloss)
                    expected = expected_template % {'recloss': str(recloss).lower()}
                    if not recloss:
                        expected = expected.replace('\n    write, table = trackloss, file;\n', '')
                    self.assertEqual(script, expected)


class TestErrorToScript(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test(self):
        sequence = [
            Tilt(
                Offset(
                    LongitudinalRoll(
                        Quadrupole(0, 1, beam={'beta': 0.6, 'gamma': 1.25}, label='q1'),
                        0.1),
                    0.2, 0.3),
                0.4),
            Tilt(SBend(0, 1, beam={'beta': 0.6, 'gamma': 1.25}, label='s1'), 0.5),
            Offset(Quadrupole(0, 1, beam={'beta': 0.6, 'gamma': 1.25}, label='q2'), 0.6, 0.7),
            LongitudinalRoll(Quadrupole(0, 1, beam={'beta': 0.6, 'gamma': 1.25}, label='q3'), 0.8),
        ]
        expected = _dedent_script('''
            eoption, add = true;
            select, flag = error, clear = true;
            select, flag = error, range = "q1";
            ealign, dx = 0.2, dy = 0.3;
            ealign, dpsi = 0.1;
            select, flag = error, clear = true;
            select, flag = error, range = "q2";
            ealign, dx = 0.6, dy = 0.7;
            select, flag = error, clear = true;
            select, flag = error, range = "q3";
            ealign, dpsi = 0.8;
        ''')
        self.assertEqual(error_script(Segment(sequence)), expected)

    def test_missing_label(self):
        with self.assertRaises(SerializerError):
            error_script(Segment([Offset(Quadrupole(0, 1, beam={'beta': 0.6, 'gamma': 1.25}))]))
        self.assertEqual(
            error_script(Segment([Tilt(Quadrupole(0, 1, beam={'beta': 0.6, 'gamma': 1.25}, label='q1'))])),
            'eoption, add = true;'
        )


class TestCreateScript(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        sequence = sequence_script(Segment([
            Drift(10., beam=beam_config, label='drift_1'),
            Quadrupole(0.25, 5., beam=beam_config, label='quad_1'),
            Drift(8., beam=beam_config, label='drift_2'),
            SBend(0.125, 2.5, beam=beam_config, label='sbend_1'),
            Drift(5., beam=beam_config, label='drift_3')
        ]), label='test_seq')
        track = track_script(np.arange(30).reshape(5, 6).T, ['drift_1', 'quad_1', 'drift_2', 'sbend_1', 'drift_3'])
        script = create_script(beam_config, sequence=sequence, track=track)
        expected = _dedent_script('''
        beam, particle = proton, gamma = 1.25;
        
        test_seq: sequence, l = 30.5, refer = entry;
            drift_1: drift, l = 10.0, at = 0.0;
            quad_1: quadrupole, k1 = 0.25, l = 5.0, at = 10.0;
            drift_2: drift, l = 8.0, at = 15.0;
            sbend_1: sbend, angle = 0.125, e1 = 0.0, e2 = 0.0, fint = 0.0, fintx = 0.0, h1 = 0.0, h2 = 0.0, hgap = 0.0, l = 2.5, at = 23.0;
            drift_3: drift, l = 5.0, at = 25.5;
        endsequence;
        
        use, sequence = test_seq;
        
        track, aperture = true, recloss = true, onepass = true, dump = true, onetable = true;
            start, x = 0, px = 1, y = 2, py = 3, t = 4, pt = 5;
            start, x = 6, px = 7, y = 8, py = 9, t = 10, pt = 11;
            start, x = 12, px = 13, y = 14, py = 15, t = 16, pt = 17;
            start, x = 18, px = 19, y = 20, py = 21, t = 22, pt = 23;
            start, x = 24, px = 25, y = 26, py = 27, t = 28, pt = 29;
            
            observe, place = drift_1;
            observe, place = quad_1;
            observe, place = drift_2;
            observe, place = sbend_1;
            observe, place = drift_3;
            
            run, turns = 1, maxaper = {0.1, 0.01, 0.1, 0.01, 1.0, 0.1};
            
            write, table = trackloss, file;
        endtrack;
        ''')
        self.assertEqual(script, expected)

    def test_with_alignment_errors(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        sequence = Segment([
            Tilt(Offset(Quadrupole(0.25, 1., beam=beam_config, label='q1'), 0.25), 0.5),
            Tilt(Quadrupole(0.25, 1., beam=beam_config, label='q2'), 2.0),
            Offset(Quadrupole(0.25, 1., beam=beam_config, label='q3'), dy=4.0),
        ])
        script = create_script(beam_config, sequence=sequence_script(sequence, label='test'),
                               errors=error_script(sequence))
        expected = _dedent_script('''
            beam, particle = proton, gamma = 1.25;

            test: sequence, l = 3.0, refer = entry;
                q1: quadrupole, k1 = 0.25, l = 1.0, tilt = 0.5, at = 0.0;
                q2: quadrupole, k1 = 0.25, l = 1.0, tilt = 2.0, at = 1.0;
                q3: quadrupole, k1 = 0.25, l = 1.0, at = 2.0;
            endsequence;
            
            use, sequence = test;
            
            eoption, add = true;
            select, flag = error, clear = true;
            select, flag = error, range = "q1";
            ealign, dx = 0.25, dy = 0.0;
            select, flag = error, clear = true;
            select, flag = error, range = "q3";
            ealign, dx = 0.0, dy = 4.0;
        ''')
        self.assertEqual(script, expected)

    def test_missing_sequence_label(self):
        with self.assertRaises(SerializerError):
            create_script({}, sequence='sequence;', track='')


class TestParamodi(unittest.TestCase):
    def test(self):
        script = _dedent_script('''
        BEAM, particle = proton, energy = 2;

        Q: QUADRUPOLE, l = 2;
        seq: SEQUENCE, l = 36, refer = entry;
            q1: Q, k1 := 1.0, at = 4;
            m1: MONITOR, at = 8;
            q2: Q, k1 := 2.0, at = q1->l/2 + 4, from = "q1";
            m2: MONITOR, at = 14;
            q3: Q, l = 4, k1 := 4.0, at = q2->l/2 + 4, from = "q2";
            s1: SBEND, angle = 0.5, l = 4, at = q3->l/2 + 4, from = "q3";
            h1: HKICKER, kick = 1.0, at = 29;
            v1: VKICKER, kick = 2.0, at = 30;
            q4: QUADRUPOLE, l = 2, k1 = 0.5, tilt = -0.1, at = 32;
        ENDSEQUENCE;
        ''')
        paramodi = Paramodi.parse('q1/kl,4,1/m,the_purpose\n'
                                  'q3/kl,32.0,1/m,more_purpose\n'
                                  's1/hkick,0.5,rad,no_purpose\n'
                                  'h1/vkick,5.0,rad,should_be_ignored\n'
                                  'v1/vkick,1.0,rad,important')
        lattice_1 = from_script(script)
        lattice_2 = from_script(script, paramodi=paramodi)
        self.assertEqual(lattice_1['q1'].k1, 1.0)
        self.assertEqual(lattice_2['q1'].k1, 2.0)
        self.assertEqual(lattice_1['q2'].k1, 2.0)
        self.assertEqual(lattice_2['q2'].k1, 2.0)
        self.assertEqual(lattice_1['q3'].k1, 4.0)
        self.assertEqual(lattice_2['q3'].k1, 8.0)
        self.assertEqual(lattice_1['s1'].angle, 0.5)
        self.assertEqual(lattice_2['s1'].angle, 1.0)
        self.assertEqual(lattice_1['h1'].kick, 1.0)
        self.assertEqual(lattice_2['h1'].kick, 1.0)
        self.assertEqual(lattice_1['v1'].kick, 2.0)
        self.assertEqual(lattice_2['v1'].kick, 1.0)


class TestParametrization(unittest.TestCase):
    def test_aperture(self):
        aperture = ApertureCircle(Parameter(tensor(0.)))
        self.assertIsInstance(aperture.aperture, Parameter)
        aperture = ApertureRectEllipse(Parameter(torch.zeros(4)))
        self.assertIsInstance(aperture.aperture, Parameter)

    def test_aperture_from_script(self):
        lattice = from_script(_dedent_script('''
            beam, particle = proton, energy = 1;
            a = {1, 2, 3, 4};  // [flow] variable
            test: sequence, l = 1, refer = entry;
                q: quadrupole, k1 = 0, l = 1, aperture = a, apertype = rectellipse, at = 0;
            endsequence;
        '''))
        self.assertIsInstance(lattice[0].aperture, ApertureRectEllipse)
        self.assertIsInstance(lattice[0].aperture.aperture, Parameter)

    def test_quadrupole_from_script(self):
        lattice = from_script(_dedent_script('''
            beam, particle = proton, energy = 1;
            k1 = 0.5;  // [flow] variable
            test: sequence, l = 1, refer = entry;
                q: quadrupole, k1 = k1, l = 1, at = 0;
            endsequence;
        '''))
        self.assertIsInstance(lattice[0].k1, Parameter)
        self.assertEqual(lattice[0].k1.data.item(), 0.5)

    def test_kicker_from_script(self):
        lattice = from_script(_dedent_script('''
            beam, particle = proton, energy = 1;
            hk = 0.5;  // [flow] variable
            vk = 2.0;  // [flow] variable
            test: sequence, l = 2, refer = entry;
                h: hkicker, kick = hk, l = 1, at = 0;
                v: vkicker, kick = vk, l = 1, at = 1;
            endsequence;
        '''))
        self.assertIsInstance(lattice[0].kick, Parameter)
        self.assertEqual(lattice[0].kick.data.item(), 0.5)
        self.assertIsInstance(lattice[1].kick, Parameter)
        self.assertEqual(lattice[1].kick.data.item(), 2.0)


if __name__ == '__main__':
    unittest.main()
