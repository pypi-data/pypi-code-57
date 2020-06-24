from functools import partial, wraps
from importlib import resources
import inspect
import itertools as it
import math
import os
import os.path
from pathlib import Path
import random
import re
from typing import List
import unittest
import warnings

import numpy as np
import torch

from dipas.build import from_file, from_script, create_script, sequence_script, error_script, write_attribute_value
from dipas.compute import closed_orbit, linear_closed_orbit, orm, transfer_maps, twiss, InitialLatticeParameters
from dipas.elements import Kicker, HKicker, HMonitor, Monitor, ThinQuadrupole, elements
from dipas.madx import run_orm, run_script
from dipas.madx.parser import replace_dots_in_variable_names

from dipas.test.mocks import MockMADXConstants


path_to_madx = os.path.expanduser('~/bin/madx')
path_to_madx_linear = os.path.expanduser('~/bin/madx-linear-twiss')

skip_unless_madx_linear_exists = unittest.skipUnless(
    os.path.exists(path_to_madx_linear),
    'Requires custom MAD-X build which performs linear Twiss computations')

WORKING_DIRECTORY = os.getenv('DIPAS_TEST_COMPUTE_WDIR')


def autofill_wdir(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.wdir_base is not None:
            wdir = Path(self.wdir_base) / self.__class__.__name__ / func.__name__
            wdir.mkdir(parents=True, exist_ok=True)
            kwargs['wdir'] = str(wdir)
        else:
            kwargs['wdir'] = None
        return func(self, *args, **kwargs)
    return wrapper


class Bases:
    class Base(unittest.TestCase):
        wdir_base = WORKING_DIRECTORY
        mock_madx_constants = MockMADXConstants()

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.mock_madx_constants.apply()

        @classmethod
        def tearDownClass(cls):
            super().tearDownClass()
            cls.mock_madx_constants.restore()

        def setUp(self):
            super().setUp()
            warnings.simplefilter('error')
            random.seed(123456)
            np.random.seed(123456)

    class TestORM(Base):
        kicks = (-0.005, 0.005)
        tolerance = 1e-6
        madx = None
        order = None
        allclose = partial(np.allclose, atol=1e-10/(kicks[1] - kicks[0]), rtol=1e-6)

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            for e_type in elements.values():
                if hasattr(e_type, 'transfer_map_order'):
                    e_type.transfer_map_order = cls.order

        @classmethod
        def tearDownClass(cls):
            super().tearDownClass()
            for e_type in elements.values():
                if hasattr(e_type, 'transfer_map_order'):
                    e_type.transfer_map_order = 2

        def _test(self, lattice, script, kickers, monitors):
            k_labels = [k.label for k in kickers]
            m_labels = [m.label for m in monitors]
            orm_ref = run_orm(script, kickers=k_labels, monitors=m_labels, kicks=self.kicks, twiss_args={'tolerance': self.tolerance}, madx=self.madx)
            orm_x, orm_y = orm(lattice, kickers=k_labels, monitors=m_labels, kicks=self.kicks, order=self.order, co_args={'tolerance': self.tolerance})
            with self.subTest('zero kickers'):
                self.assertTupleEqual(orm_x.numpy().shape, orm_ref.loc['X'].values.shape)
                self.assertTrue(self.allclose(orm_x.numpy(), orm_ref.loc['X'].values))
                self.assertTupleEqual(orm_y.numpy().shape, orm_ref.loc['Y'].values.shape)
                self.assertTrue(self.allclose(orm_y.numpy(), orm_ref.loc['Y'].values))
            for kicker in kickers:
                kicker.kick = random.uniform(-0.002, 0.002)
            orm_ref = run_orm(self._prepare_script(create_script(lattice[0].beam, sequence=sequence_script(lattice))),
                              kickers=k_labels, monitors=m_labels, kicks=self.kicks, twiss_args={'tolerance': self.tolerance},
                              madx=self.madx)
            orm_x, orm_y = orm(lattice, kickers=k_labels, monitors=m_labels, kicks=self.kicks, order=self.order, co_args={'tolerance': self.tolerance})
            with self.subTest('non-zero kickers'):
                self.assertTupleEqual(orm_x.numpy().shape, orm_ref.loc['X'].values.shape)
                self.assertTrue(self.allclose(orm_x.numpy(), orm_ref.loc['X'].values))
                self.assertTupleEqual(orm_y.numpy().shape, orm_ref.loc['Y'].values.shape)
                self.assertTrue(self.allclose(orm_y.numpy(), orm_ref.loc['Y'].values))

        def test_single_kicker(self):
            with resources.path('dipas.test.sequences', 'cryring.seq') as path:
                lattice = from_file(path)
            script = self._prepare_script(resources.read_text('dipas.test.sequences', 'cryring.seq'))
            h_kickers = lattice[HKicker][0:1]
            h_monitors = lattice[HMonitor]
            self._test(lattice, script, h_kickers, h_monitors)

        def test_all_kickers(self):
            with resources.path('dipas.test.sequences', 'cryring.seq') as path:
                lattice = from_file(path)
            script = self._prepare_script(resources.read_text('dipas.test.sequences', 'cryring.seq'))
            h_kickers = lattice[HKicker]
            h_monitors = lattice[HMonitor]
            self._test(lattice, script, h_kickers, h_monitors)

        @classmethod
        def _prepare_script(cls, script):
            return script

    class TestClosedOrbit(Base):
        sequence = None
        tolerance = 1e-6
        allclose = partial(np.allclose, atol=1e-10, rtol=1e-6)
        madx = None
        order = None
        _d_indices = [f"K{i}" for i in range(1, 7)]
        _r_indices = [f"R{i}{j}" for i in range(1, 7) for j in range(1, 7)]
        _t_indices = [f"T{i}{j}{k}" for i in range(1, 7) for j in range(1, 7) for k in range(1, 7)]

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            for e_type in elements.values():
                if hasattr(e_type, 'transfer_map_order'):
                    e_type.transfer_map_order = cls.order

        @classmethod
        def tearDownClass(cls):
            super().tearDownClass()
            for e_type in elements.values():
                if hasattr(e_type, 'transfer_map_order'):
                    e_type.transfer_map_order = 2

        @autofill_wdir
        def test_closed_orbit(self, *, wdir):
            script = self._get_script()
            co_ref = self._get_co_ref(script, wdir=wdir).loc[f'{self.sequence}$start', :].values
            lattice = self._customize_lattice(from_script(script))
            co = closed_orbit(lattice, order=self.order, tolerance=self.tolerance).numpy().ravel()[:4]

            script_ref = create_script(dict(particle='proton', energy=1),
                                       sequence=sequence_script(lattice, label=self.sequence),
                                       errors=error_script(lattice))
            co_lattice_ref = self._get_co_ref(self._augment_script(script_ref), wdir=wdir).loc[f'{self.sequence}$start', :].values

            with self.subTest('Compare closed orbit from MADX vs. closed orbit from lattice dump'):
                self.assertTrue(self.allclose(co_ref, co_lattice_ref))
            with self.subTest('Compare closed orbit search vs. MADX reference'):
                self.assertTrue(self.allclose(co_ref, co))

            for co_val, msg in [(co, 'custom'), (co_ref, 'MADX')]:
                x0 = torch.zeros(6, 1)
                x0[:4, 0] += torch.from_numpy(co_val)
                co_one_turn = lattice.transfer_maps('reduce', order=self.order, symplectify=False, d0=x0)[0].numpy()[:4, 0]
                with self.subTest(f'Check invariance of closed orbit under one turn tracking ({msg})'):
                    self.assertTrue(self.allclose(co_val, co_one_turn))

            co_ref_everywhere = self._get_co_ref(script, wdir=wdir)
            x0 = torch.zeros(6, 1)
            x0[:4, 0] += torch.from_numpy(co_ref_everywhere.loc[f'{self.sequence}$start', :].values)
            co_propagated = lattice.transfer_maps('accumulate', order=self.order, symplectify=False, d0=x0)
            co_propagated = np.array([x[0].numpy().ravel()[:4].tolist() for x in co_propagated])
            with self.subTest('Check closed orbit propagation vs. MADX reference'):
                self.assertTrue(self.allclose(co_ref_everywhere.iloc[1:-1].values, co_propagated))

            return lattice, co, co_ref

        @autofill_wdir
        def test_transfer_maps_accumulated(self, *, wdir):
            script = self._get_script()
            sm_ref = self._get_transfer_maps_ref(script, wdir=wdir)
            sm_ref = zip(*sm_ref[1])
            lattice = self._customize_lattice(from_script(script))
            sm = transfer_maps(lattice, method='accumulate', order=self.order, labels=True)
            for (label, value), ref in zip(sm, sm_ref):
                with self.subTest(f'[{label!r}] Accumulated first order vs. MADX reference'):
                    self.assertTrue(self.allclose(value[1].numpy(), ref[1]))
                if self.order >= 2:
                    with self.subTest(f'[{label!r}] Accumulated second order vs. MADX reference'):
                        self.assertTrue(self.allclose(value[2].numpy(), ref[2]))

        @autofill_wdir
        def test_twiss(self, *, wdir):
            self._test_twiss(wdir=wdir)

        @autofill_wdir
        def test_twiss_init_beta_alpha(self, *, wdir):
            init = InitialLatticeParameters(beta_x=random.uniform(10, 100), beta_y=random.uniform(10, 100),
                                            alpha_x=random.uniform(0.1, 1.0), alpha_y=random.uniform(0.1, 1.0))
            self._test_twiss(init=init, wdir=wdir)

        @autofill_wdir
        def test_twiss_init_beta_alpha_mu(self, *, wdir):
            init = InitialLatticeParameters(beta_x=random.uniform(10, 100), beta_y=random.uniform(10, 100),
                                            alpha_x=random.uniform(0.1, 1.0), alpha_y=random.uniform(0.1, 1.0),
                                            mu_x=random.uniform(0, 1), mu_y=random.uniform(0, 1))
            self._test_twiss(init=init, wdir=wdir)

        @autofill_wdir
        def test_twiss_init_dispersion(self, *, wdir):
            init = InitialLatticeParameters(beta_x=10, beta_y=20,
                                            dx=random.uniform(1, 10), dy=random.uniform(1, 10),
                                            dpx=random.uniform(0.1, 1.0), dpy=random.uniform(0.1, 1.0))
            self._test_twiss(init=init, wdir=wdir)

        @autofill_wdir
        def test_twiss_init_orbit(self, *, wdir):
            init = InitialLatticeParameters(beta_x=10, beta_y=20,
                                            x=random.uniform(1e-3, 1e-2), y=random.uniform(1e-3, 1e-2),
                                            px=random.uniform(1e-4, 1e-3), py=random.uniform(1e-4, 1e-3))
            self._test_twiss(init=init, wdir=wdir)

        def _test_twiss(self, *, init=None, wdir):
            script = self._get_script()
            lattice = self._customize_lattice(from_script(script))
            data = twiss(lattice, order=self.order, initial=init)
            ref = run_script(self._augment_script(script, b0=init), {'twiss': True}, madx=self.madx, wdir=wdir)['twiss']
            ref[0]['NAME'] = ref[0]['NAME'].str.lower()
            ref[0].set_index('NAME', inplace=True)
            self.assertEqual(data['lattice'].index.tolist()[0], '#s')
            self.assertTrue(ref[0].index.tolist()[0].endswith('$start'))
            self.assertTrue(np.allclose(data['coupling_matrix'].detach().numpy(),
                                        ref[0].iloc[0][['R11', 'R12', 'R21', 'R22']].values.reshape(2, 2)))
            for (l1, r1), (l2, r2) in zip(data['lattice'].iterrows(), ref[0].iterrows()):
                with self.subTest(l1=l1, r1={k: v.item() for k, v in r1.to_dict().items()}, l2=l2, r2=r2.to_dict()):
                    if l1 == '#s':
                        if init is None:  # In case initial Twiss parameters are given no one turn matrix is returned.
                            self.assertTrue(np.allclose(
                                data['one_turn_matrix'].numpy().ravel(),
                                r2[[f'RE{i}{j}' for i, j in it.product(range(1, 7), repeat=2)]]
                            ))
                    else:
                        self.assertEqual(l1, replace_dots_in_variable_names(l2))
                    assert_almost_equal = lambda x, y: self.assertTrue(np.isclose(x, y, atol=1e-6, rtol=1e-5))
                    assert_almost_equal(r1['x' ].item(), r2['X'])
                    assert_almost_equal(r1['px'].item(), r2['PX'])
                    assert_almost_equal(r1['y' ].item(), r2['Y'])
                    assert_almost_equal(r1['py'].item(), r2['PY'])
                    assert_almost_equal(r1['bx'].item(), r2['BETX'])
                    assert_almost_equal(r1['ax'].item(), r2['ALFX'])
                    assert_almost_equal(r1['mx'].item(), r2['MUX'])
                    assert_almost_equal(r1['by'].item(), r2['BETY'])
                    assert_almost_equal(r1['ay'].item(), r2['ALFY'])
                    assert_almost_equal(r1['my'].item(), r2['MUY'])
                    assert_almost_equal(r1['dx'].item(), r2['DX'])
                    assert_almost_equal(r1['dpx'].item(), r2['DPX'])
                    assert_almost_equal(r1['dy'].item(), r2['DY'])
                    assert_almost_equal(r1['dpy'].item(), r2['DPY'])
            self.assertAlmostEqual(data['Q1'].item(), ref[1]['Q1'], delta=1e-6)
            self.assertAlmostEqual(data['Q2'].item(), ref[1]['Q2'], delta=1e-6)

        def _customize_lattice(self, lattice):
            return lattice

        def _get_co_ref(self, script, *, wdir):
            twiss = run_script(script, ['twiss'], madx=self.madx, wdir=wdir)['twiss']
            twiss['NAME'] = twiss['NAME'].str.lower()
            twiss.set_index('NAME', inplace=True)
            return twiss.loc[:, ['X', 'PX', 'Y', 'PY']]

        def _get_transfer_maps_ref(self, script, *, wdir):
            results = run_script(script, ['sectormap.tfs', 'sectormap_acc.tfs'], madx=self.madx, wdir=wdir)
            s_maps = results['sectormap.tfs']
            s_maps_acc = results['sectormap_acc.tfs']
            return_list = []
            for sm in [s_maps, s_maps_acc]:
                sm['NAME'] = sm['NAME'].str.lower()
                sm.set_index('NAME', inplace=True)
                sm = sm.iloc[1:-1, :]  # Skip "seq$start" and "seq$end".
                return_list.append((sm.loc[:, self._d_indices].values.reshape(-1, 6, 1),
                                    sm.loc[:, self._r_indices].values.reshape(-1, 6, 6),
                                    sm.loc[:, self._t_indices].values.reshape(-1, 6, 6, 6)))
            return return_list

        def _get_script(self):
            script = self._get_base_script()
            if not script.lstrip().lower().startswith('beam'):
                script = 'beam, particle = proton, beta = 0.6;\n' + script
            return self._augment_script(script)

        def _augment_script(self, script, *, b0: InitialLatticeParameters = None):
            if b0 is not None:
                x, px, y, py, t, pt = b0.orbit.numpy().ravel()
                dx, dpx, dy, dpy = b0.dispersion.numpy().ravel()[:4]
                beta0 = (
                    f'beta0, x = {x:.9f}, px = {px:.9f}, y = {y:.9f}, py = {py:.9f}, t = {t:.9f}, pt = {pt:.9f}, '
                    f'betx = {b0.beta_x:.9f}, alfx = {b0.alpha_x:.9f}, mux = {b0.mu_x:.9f}, '
                    f'bety = {b0.beta_y:.9f}, alfy = {b0.alpha_y:.9f}, muy = {b0.mu_y:.9f}, '
                    f'dx = {dx:.9f}, dpx = {dpx:.9f}, dy = {dy:.9f}, dpy = {dpy:.9f}'
                )
                beta0 = f'\ninitial: {beta0};'
                beta0_twiss = ', beta0 = initial'
            else:
                beta0 = beta0_twiss = ''
            return script + (
                f'\n{self._use_sequence()}'
                f'{beta0}'
                f'\nselect, flag = twiss, full, column = name, s, x, px, y, py, t, pt, betx, alfx, mux, bety, alfy, muy, dx, dpx, dy, dpy, r11, r12, r21, r22, re;'
                f'\ntwiss{beta0_twiss}, tolerance = {self.tolerance}, rmatrix = true, save, file = "twiss";'
                f'\ntwiss, tolerance = 1e-16, sectormap = true, sectorpure = true, sectoracc = false, sectorfile = "sectormap.tfs";'
                f'\ntwiss, tolerance = 1e-16, sectormap = true, sectorpure = false, sectoracc = true, sectorfile = "sectormap_acc.tfs";'
            )

        def _use_sequence(self):
            return f'use, sequence = {self.sequence};'

        def _get_base_script(self):
            raise NotImplementedError

    @skip_unless_madx_linear_exists
    class TestLinearClosedOrbit(TestClosedOrbit):
        order = 1
        madx = path_to_madx_linear

        def _customize_lattice(self, lattice):
            # MADX uses 2 slices with "edge" style but for linear optics neither number of slices nor slicing style matters.
            return lattice.makethin({Kicker: 1})

        def test_closed_orbit(self):
            lattice, co, co_ref = super().test_closed_orbit()
            co2 = linear_closed_orbit(lattice).numpy().ravel()[:4]
            with self.subTest('Compare closed orbit search vs. linear closed orbit'):
                self.assertTrue(self.allclose(co, co2))
            with self.subTest('Compare linear closed orbit vs. MADX reference'):
                self.assertTrue(self.allclose(co_ref, co2))
            for co_val, msg in [(co, 'custom'), (co_ref, 'MADX')]:
                x0 = torch.zeros(6, 1)
                x0[:4, 0] += torch.from_numpy(co_val)
                co_one_turn = lattice.transfer_maps('reduce', order=self.order, symplectify=False, d0=x0)[0].numpy()[:4, 0]
                co_one_turn_acc = lattice.transfer_maps('accumulate', order=self.order, symplectify=False, d0=x0)[-1][0].numpy()[:4, 0]
                co_tracked = lattice.linear(x0, exact_drift=False).numpy()[:4, 0]
                with self.subTest(f'Check equivalence of "reduce" and "accumulate" for linear optics ({msg})'):
                    self.assertTrue(np.allclose(co_one_turn_acc, co_one_turn, atol=1e-16, rtol=1e-16))
                with self.subTest(f'Check equivalence of tracking methods for linear optics ({msg})'):
                    self.assertTrue(np.allclose(co_tracked, co_one_turn, atol=1e-16, rtol=1e-16))

    class TestSecondOrderClosedOrbit(TestClosedOrbit):
        order = 2
        madx = path_to_madx

        def _customize_lattice(self, lattice):
            # MADX uses 2 slices with "edge" style for Twiss computations, i.e. `| --- drift --- |` ("|" == slice).
            return lattice.makethin({Kicker: 2}, style={Kicker: 'edge'})

    class WithFieldErrors(unittest.TestCase):
        def generate_field_errors(self, labels: List[str], order: int, base_strength: float, fraction: float = 0.01,
                                  selector: str = 'range'):
            errors = [random.choice((-1, 1)) * random.uniform(0.8, 1.2) * fraction * base_strength for __ in labels]
            field_errors = np.zeros((len(labels), order+1))
            for i, error in enumerate(errors):
                field_errors[i, order] = error
            return '\n' + '\n'.join([
                f'select, flag = error, clear;\n'
                f'select, flag = error, {selector} = "{label}";\n'
                f'efcomp, dkn = {write_attribute_value(error)};\n'
                for label, error in zip(labels, field_errors)
            ])

        def setUp(self):
            super().setUp()
            random.seed(3247253)
            np.random.seed(4589145)

        def _use_sequence(self):  # Will be used as a mixin together with `TestClosedOrbit`.
            return ''


class Lattices:
    class ToyLattice(unittest.TestCase):
        N = 60  # Number of FODO cells.
        L = 13.45  # Length of FODO cell.
        f = 7.570366  # Focal length of quadrupoles.

        sequence = 'test'
        kick_max = 1e-4
        rand_func = None

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            elements['multipole'] = lambda knl, l, beam, label, **kwargs: ThinQuadrupole(k1l=knl[1], label=label)

        @classmethod
        def tearDownClass(cls):
            del elements['multipole']

        def _get_base_script(self):
            N, L, f = self.N, self.L, self.f
            dipole = f'sbend, l = {L / 4}, angle = 2*pi / {4 * N}, at = {{at}};'  # Four dipoles per cell.
            q_foc = f'multipole, knl = {{{{0, {1 / f}}}}}, at = {{at}};'
            q_def = f'multipole, knl = {{{{0, {-1 / f}}}}}, at = {{at}};'
            h_kicker = f'hkicker, kick = {{kick}}, at = {{at}};'
            v_kicker = f'vkicker, kick = {{kick}}, at = {{at}};'

            seq = []
            for i in range(N):
                seq.extend([
                    f'e{i:02d}_01: ' + q_foc.format(at=i * L),
                    f'e{i:02d}_02: ' + dipole.format(at=i * L),
                    f'e{i:02d}_03: ' + h_kicker.format(kick=self.rand_func(), at=i * L + L / 4),
                    f'e{i:02d}_04: ' + dipole.format(at=i * L + L / 4),
                    f'e{i:02d}_05: ' + q_def.format(at=i * L + L / 2),
                    f'e{i:02d}_06: ' + dipole.format(at=i * L + L / 2),
                    f'e{i:02d}_07: ' + v_kicker.format(kick=self.rand_func(), at=i * L + 0.75 * L),
                    f'e{i:02d}_08: ' + dipole.format(at=i * L + 0.75 * L),
                ])
            seq = '\n'.join(seq)
            return f'{self.sequence}: sequence, refer=entry, l={N * L};\n{seq}\nendsequence;'

    class ToyLattice2(ToyLattice):
        def _get_base_script(self):
            N, L, f = self.N, self.L, self.f
            dipole = f'sbend, l = {L / 8}, angle = 2*pi / {4 * N}, at = {{at}};'  # Four dipoles per cell.
            q_foc = f'quadrupole, l = {L / 8}, k1 = {1 / (f * L / 8)}, at = {{at}};'
            q_def = f'quadrupole, l = {L / 8}, k1 = {-1 / (f * L / 8)}, at = {{at}};'
            h_kicker = f'hkicker, l = {L / 8}, kick = {{kick}}, at = {{at}};'
            v_kicker = f'vkicker, l = {L / 8}, kick = {{kick}}, at = {{at}};'

            seq = []
            for i in range(N):
                seq.extend([
                    f'e{i:02d}_01: ' + q_foc.format(at=i * L),
                    f'e{i:02d}_02: ' + dipole.format(at=i * L + 0.125 * L),
                    f'e{i:02d}_03: ' + h_kicker.format(kick=self.rand_func(), at=i * L + 0.250 * L),
                    f'e{i:02d}_04: ' + dipole.format(at=i * L + 0.375 * L),
                    f'e{i:02d}_05: ' + q_def.format(at=i * L + 0.500 * L),
                    f'e{i:02d}_06: ' + dipole.format(at=i * L + 0.625 * L),
                    f'e{i:02d}_07: ' + v_kicker.format(kick=self.rand_func(), at=i * L + 0.750 * L),
                    f'e{i:02d}_08: ' + dipole.format(at=i * L + 0.875 * L),
                ])
            seq = '\n'.join(seq)
            return f'{self.sequence}: sequence, refer=entry, l={N * L};\n{seq}\nendsequence;'

    class ToyLattice2WithFieldErrors(ToyLattice2, Bases.WithFieldErrors):
        def _get_base_script(self):
            script = super()._get_base_script()
            script += f'\nuse, sequence = {self.sequence};'
            script += self.generate_field_errors(  # Quadrupole errors
                labels=[f'e{i:02d}_{random.choice((1, 5)):02d}' for i in random.sample(range(self.N), 10)],
                order=1,
                base_strength=1/self.f
            )
            script += self.generate_field_errors(  # Dipole errors
                labels=[f'e{i:02d}_{random.choice((2, 4, 6, 8)):02d}' for i in random.sample(range(self.N), 10)],
                order=0,
                base_strength=0.5*math.pi / self.N
            )
            return script

    class ToyLattice3(ToyLattice):
        def _get_base_script(self):
            N, L, f = self.N, self.L, self.f
            dipole = f'sbend, l = {L / 10}, angle = 2*pi / {4 * N}, at = {{at}};'  # Four dipoles per cell.
            q_foc = f'quadrupole, l = {L / 10}, k1 = {1 / (f * L / 10)}, at = {{at}};'
            q_def = f'quadrupole, l = {L / 10}, k1 = {-1 / (f * L / 10)}, at = {{at}};'
            drift_quad = f'quadrupole, l = {L / 10}, k1 = 0, at = {{at}};'
            h_kicker = f'hkicker, l = {L / 10}, kick = {{kick}}, at = {{at}};'
            v_kicker = f'vkicker, l = {L / 10}, kick = {{kick}}, at = {{at}};'
            sextupole = f'sextupole, l = {L / 10}, k2 = 0.001, at = {{at}};'
            marker = f'marker, at = {{at}};'

            seq = []
            for i in range(N):
                seq.extend([
                    f'e{i:02d}_01: ' + q_foc.format(at=i * L + 0.05 * L),
                    f'e{i:02d}_02: ' + dipole.format(at=i * L + 0.15 * L),
                    f'e{i:02d}_03: ' + h_kicker.format(kick=self.rand_func(), at=i * L + 0.25 * L),
                    f'e{i:02d}_04: ' + dipole.format(at=i * L + 0.35 * L),
                    f'e{i:02d}_05: ' + sextupole.format(at=i * L + 0.45 * L),
                    f'e{i:02d}_06: ' + marker.format(at=i * L + 0.50 * L),
                    f'e{i:02d}_07: ' + q_def.format(at=i * L + 0.55 * L),
                    f'e{i:02d}_08: ' + dipole.format(at=i * L + 0.65 * L),
                    f'e{i:02d}_09: ' + v_kicker.format(kick=self.rand_func(), at=i * L + 0.75 * L),
                    f'e{i:02d}_10: ' + dipole.format(at=i * L + 0.85 * L),
                    f'e{i:02d}_11: ' + drift_quad.format(at=i * L + 0.95 * L),
                    f'e{i:02d}_12: ' + marker.format(at=i * L + 1.00 * L),
                ])
            seq = '\n'.join(seq)
            return f'{self.sequence}: sequence, l={N * L};\n{seq}\nendsequence;'

    class ToyLattice3WithFieldErrors(ToyLattice3, Bases.WithFieldErrors):
        def _get_base_script(self):
            script = super()._get_base_script()
            script += f'\nuse, sequence = {self.sequence};'
            script += self.generate_field_errors(  # Sextupole errors
                labels=[f'e{i:02d}_{random.choice((5,)):02d}' for i in random.sample(range(self.N), 20)],
                order=2,
                base_strength=1e-4*self.L
            )
            script += self.generate_field_errors(  # Quadrupole errors
                labels=[f'e{i:02d}_{random.choice((1, 7)):02d}' for i in random.sample(range(self.N), 20)],
                order=1,
                base_strength=1/self.f
            )
            script += self.generate_field_errors(  # Dipole errors
                labels=[f'e{i:02d}_{random.choice((2, 4, 8, 10)):02d}' for i in random.sample(range(self.N), 20)],
                order=0,
                base_strength=0.5*math.pi / self.N
            )
            return script

    class ToyLatticeWithInactiveDipoles(ToyLattice):
        def _get_base_script(self):
            N, L, f = self.N, self.L, self.f
            dipole = f'sbend, l = {L / 8}, angle = 2*pi / {4*N}, at = {{at}};'  # Four dipoles per cell.
            dipole_off = f'sbend, l = {L / 8}, angle = 0, at = {{at}};'  # Four dipoles per cell.
            q_foc = f'multipole, knl = {{{{0, {1 / f}}}}}, at = {{at}};'
            q_def = f'multipole, knl = {{{{0, {-1 / f}}}}}, at = {{at}};'
            h_kicker = f'hkicker, kick = {{kick}}, at = {{at}};'
            v_kicker = f'vkicker, kick = {{kick}}, at = {{at}};'

            seq = []
            for i in range(N):
                seq.extend([
                    f'e{i:02d}_01: ' + q_foc.format(at=i * L),
                    f'e{i:02d}_02: ' + dipole.format(at=i * L),
                    f'e{i:02d}_03: ' + dipole_off.format(at=i * L + L / 8),
                    f'e{i:02d}_04: ' + h_kicker.format(kick=self.rand_func(), at=i * L + L / 4),
                    f'e{i:02d}_05: ' + dipole.format(at=i * L + L / 4),
                    f'e{i:02d}_06: ' + dipole_off.format(at=i * L + L / 4 + L / 8),
                    f'e{i:02d}_07: ' + q_def.format(at=i * L + L / 2),
                    f'e{i:02d}_08: ' + dipole.format(at=i * L + L / 2),
                    f'e{i:02d}_09: ' + dipole_off.format(at=i * L + L / 2 + L / 8),
                    f'e{i:02d}_10: ' + v_kicker.format(kick=self.rand_func(), at=i * L + 0.75 * L),
                    f'e{i:02d}_11: ' + dipole.format(at=i * L + 0.75 * L),
                    f'e{i:02d}_12: ' + dipole_off.format(at=i * L + 0.75 * L + L / 8),
                ])
            seq = '\n'.join(seq)
            return f'{self.sequence}: sequence, refer=entry, l={N * L};\n{seq}\nendsequence;'

    class ToyLatticeWithInactiveDipolesAndFieldErrors(ToyLatticeWithInactiveDipoles, Bases.WithFieldErrors):
        def _get_base_script(self):
            script = super()._get_base_script()
            script += f'\nuse, sequence = {self.sequence};'
            script += self.generate_field_errors(  # Inactive dipole errors
                labels=[f'e{i:02d}_{random.choice((3, 6, 9, 12)):02d}' for i in random.sample(range(self.N), 20)],
                order=0,
                base_strength=math.pi / self.N
            )
            return script

    class RealLattice(unittest.TestCase):
        sequence = 'cryring'
        kick_max = 0.005
        rand_func = None

        def _add_kicks(self, script):
            return re.sub(
                r'(k\d{2}k[hv])\s*:?=\s*0\s*;',
                lambda m: f'{m.group(1)} = {self.rand_func()};',
                script
            )

        def _get_base_script(self):
            with open(os.path.join('sequences', f'{self.sequence}.seq')) as fh:
                return fh.read()

        def _get_script(self):
            # `_get_script` is provided by mixin class.
            # noinspection PyUnresolvedReferences
            return self._add_kicks(super()._get_script())

    class RealLatticeWithFieldErrors(RealLattice, Bases.WithFieldErrors):
        d_labels = [
            'yr01mh',
            'yr02mh',
            'yr03mh',
            'yr04mh',
            'yr05mh',
            'yr06mh',
            'yr07mh',
            'yr08mh',
            'yr09mh',
            'yr10mh',
            'yr11mh',
            'yr12mh',
        ]
        q_foc_labels = [
            'yr02qs1', 'yr02qs3',
            'yr04qs1', 'yr04qs3',
            'yr06qs1', 'yr06qs3',
            'yr08qs1', 'yr08qs3',
            'yr10qs1', 'yr10qs3',
            'yr12qs1', 'yr12qs3',
        ]
        q_def_labels = ['yr02qs2', 'yr04qs2', 'yr06qs2', 'yr08qs2', 'yr10qs2', 'yr12qs2']

        def _get_base_script(self):
            # noinspection PyUnresolvedReferences
            script = super()._get_base_script()
            script += self.generate_field_errors(  # Focusing quadrupole errors
                labels=self.q_foc_labels,
                order=1,
                base_strength=0.5086546699,
                selector='class'
            )
            script += self.generate_field_errors(  # Defocusing quadrupole errors
                labels=self.q_def_labels,
                order=1,
                base_strength=-0.6511149282,
                selector='class'
            )
            script += self.generate_field_errors(  # Dipole errors
                labels=self.d_labels,
                order=0,
                base_strength=2*math.pi / len(self.d_labels),
                selector='class'
            )
            select_all = '\n'.join(f'select, flag = error, class = "{x}";' for x in self.d_labels + self.q_foc_labels + self.q_def_labels)
            script += (f'\nselect, flag = error, clear;'
                       f'\n{select_all}'
                       f'\nesave, file = "errors";\n')
            # noinspection PyUnresolvedReferences
            errors = run_script(script, results=['errors'], madx=self.madx)['errors']
            errors['NAME'] = errors['NAME'].str.lower()
            errors.set_index('NAME', inplace=True)
            assert set(self.d_labels) & set(errors.index.tolist()) == set(self.d_labels)
            assert set(self.q_foc_labels) & set(errors.index.tolist()) == set(self.q_foc_labels)
            assert set(self.q_def_labels) & set(errors.index.tolist()) == set(self.q_def_labels)
            return script


class TestKickerFieldErrors(unittest.TestCase):
    def setUp(self):
        elements['multipole'] = lambda *args, beam=None, label=None, **kwargs: Monitor(l=0, beam=beam, label=label)

    def tearDown(self):
        del elements['multipole']

    def test(self):
        def _co_from_script(_script):
            lattice = from_script(_script, errors=True)
            lattice.apply_unique_labels()
            co = twiss(lattice)['lattice'].loc[:, ['x', 'px', 'y', 'py']].to_numpy()
            co = np.vectorize(lambda x: x.item())(co).astype(float)
            co_ref = run_script(_script, twiss=True, madx=os.path.expanduser('~/bin/madx'))['twiss'][0].loc[:, ['X', 'PX', 'Y', 'PY']].to_numpy()
            co_ref = co_ref[:-1, :]  # drop 'end of lattice' marker
            return co, co_ref

        script = resources.read_text('dipas.test.sequences', 'sis18.seq')
        marker = 'USE, sequence=sis18lattice;'
        script = script[:script.index(marker)+len(marker)]
        assert script.endswith(marker)
        co, co_ref = _co_from_script(script)
        self.assertTrue(np.all(co == 0))
        self.assertTrue(np.all(co_ref == 0))

        with self.subTest(msg='dkn'):
            e_script = script + (
                '\nselect, flag=error, clear;'
                '\nselect, flag=error, range=cov_kick1;'
                '\nefcomp, dkn = {0.001};'
            )
            co, co_ref = _co_from_script(e_script)
            self.assertTrue(np.allclose(co, co_ref, atol=1e-6, rtol=1e-5))

        with self.subTest(msg='dks'):
            e_script = script + (
                '\nselect, flag=error, clear;'
                '\nselect, flag=error, range=cov_kick1;'
                '\nefcomp, dks = {0.001};'
            )
            co, co_ref = _co_from_script(e_script)
            self.assertTrue(np.allclose(co, co_ref, atol=1e-6, rtol=1e-5))


@skip_unless_madx_linear_exists
class TestORMLinear(Bases.TestORM):
    madx = path_to_madx_linear
    order = 1


class TestORMSecondOrder(Bases.TestORM):
    madx = path_to_madx
    order = 2


# noinspection PyUnusedLocal
def load_tests(loader, tests, pattern):
    compute_classes = [Bases.TestLinearClosedOrbit, Bases.TestSecondOrderClosedOrbit]
    lattice_classes = [x for x in vars(Lattices).values() if inspect.isclass(x) and issubclass(x, unittest.TestCase)]
    kicker_configs = {'ZeroKickers': lambda *args: 0., 'NonZeroKickers': random.uniform}
    for compute_class, lattice_class, kicker_config in it.product(compute_classes, lattice_classes, kicker_configs):
        test_class = type(f'{compute_class.__name__}{lattice_class.__name__}{kicker_config}',
                          (lattice_class, compute_class),
                          {'rand_func': partial(kicker_configs[kicker_config], -lattice_class.kick_max, lattice_class.kick_max)})
        tests.addTests(loader.loadTestsFromTestCase(test_class))
    return tests


if __name__ == '__main__':
    unittest.main()
