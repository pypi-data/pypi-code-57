from functools import partial
import itertools as it
import operator as op
import os
import random
import re
from typing import get_type_hints
import unittest

import numpy as np
import torch

from dipas.build import from_script, error_script, sequence_script, track_script, create_script
from dipas.elements import Parameter, tensor, Element, Drift, Kicker, HKicker, VKicker, Quadrupole, \
    ThinQuadrupole, Sextupole, ThinSextupole, SBend, Monitor, Marker, AlignmentError, LongitudinalRoll, Tilt, Offset, \
    BPMError, Aperture, ApertureCircle, ApertureEllipse, ApertureRectangle, ApertureRectEllipse, Segment, ThinElement, \
    CompoundElement, Utilities, elements
from dipas.madx import run_script


torch.set_default_dtype(torch.float64)

run_script = partial(run_script, madx=os.path.expanduser('~/bin/madx'))
columns = ['X', 'PX', 'Y', 'PY', 'T', 'PT']
e1_label = 'e1'
e1_allclose = partial(np.allclose, atol=1e-12, rtol=1e-9)


def sequence_script_from_list(elements):
    return sequence_script(Segment(elements))


def error_script_from_list(elements):
    return error_script(Segment(elements))


class TestElement(unittest.TestCase):
    def test_abc_methods(self):
        with self.assertRaises(NotImplementedError):
            Element(2.0, beam={}).exact(torch.zeros(6, 10))

    def test_makethin_deltas(self):
        expected = {2: {'edge': (0.0, 1.0), 'simple': (0.25, 0.50), 'teapot': (1/6, 2/3)},
                    3: {'edge': (0.0, 0.5), 'simple': (1/6, 1/3), 'teapot': (0.125, 0.375)},
                    4: {'edge': (0.0, 1/3), 'simple': (0.125, 0.25), 'teapot': (0.1, 4/15)}}
        for n in range(2, 5):
            for style in ('edge', 'simple', 'teapot'):
                with self.subTest(f'[{style}] n = {n}'):
                    self.assertTupleEqual(ThinElement.makethin_deltas[style](n), expected[n][style])


# noinspection PyUnresolvedReferences
class TestAperture(unittest.TestCase):
    def _check(self, element, x, outside_expected):
        t = torch.from_numpy(x)
        x1 = element.loss(t).numpy()
        x2 = element.aperture(t[[0, 2]]).numpy()
        self.assertTupleEqual(x1.shape, x.shape[1:])
        self.assertTrue(np.all(x1 == x2))
        self.assertSequenceEqual((x1 > 0).tolist(), outside_expected)

        # Check with MADX.
        beam = dict(beta=0.6, gamma=1.25)
        element = Marker(label=e1_label, aperture=element.aperture)
        track = track_script(x, [e1_label], aperture=True, recloss=True, maxaper=[1e3]*6)
        sequence = sequence_script_from_list([element, Drift(l=1, beam=beam)])
        script = create_script(beam, sequence=sequence, track=track)
        loss = run_script(script, ['trackloss'])['trackloss']
        self.assertTrue(np.array_equal(loss.loc[:, 'NUMBER'], np.arange(1, x.shape[1]+1)[outside_expected]))
        self.assertTrue(np.all(loss.loc[:, 'S'] == 0))

        # Check round-trip via script.
        element = from_script(script, beam=beam)[0]
        self.assertTupleEqual(x1.shape, element.loss(t).numpy().shape)
        self.assertTrue(np.all(x1 == element.loss(t).numpy()))

    def test_default(self):
        e = Element(0, beam={})
        self.assertIsNone(e.aperture)

    def test_elliptical(self):
        e = Element(0, beam={}, aperture=ApertureEllipse((3.0, 4.0)))
        x = np.zeros((6, 5), dtype=float)
        x[0] = [1.5, 3.000001, 0, 2.5, 5]
        x[2] = [-3, 0, 4.000001, 3.5, -5]
        self._check(e, x, [False, True, True, True, True])

    def test_rectangular(self):
        e = Element(0, beam={}, aperture=ApertureRectangle((3.0, 4.0)))
        x = np.zeros((6, 5), dtype=float)
        x[0] = [1.5, 3.000001, 0, 2.5, 5]
        x[2] = [-3, 0, 4.000001, 3.5, -5]
        self._check(e, x, [False, True, True, False, True])

    def test_rectangle_ellipse(self):
        e = Element(0, beam={}, aperture=ApertureRectEllipse((8.0, 4.0, 9.0, 5.0)))
        x = np.zeros((6, 6), dtype=float)
        x[0] = [-8.0, 0.0, 7.0, 9.0,  0.0, 7.5]
        x[2] = [ 0.0, 4.0, 0.5, 0.0, -5.0, 3.5]
        self._check(e, x, [False, False, False, True, True, True])

    def test_padding(self):
        e = Element(0, beam={}, aperture=ApertureRectangle(aperture=(3.0, 4.0), padding=(1.0, 1.0)))
        self.assertListEqual(e.aperture.aperture.numpy().tolist(), [3.0, 4.0])
        self.assertListEqual(e.aperture.padding.numpy().tolist(), [1.0, 1.0])
        x = np.zeros((6, 5), dtype=float)
        x[0] = [1.5, 2.000001, 0, 1.5, 4]
        x[2] = [-2.999, 0, 3.000001, 2.5, -4]
        self._check(e, x, [False, True, True, False, True])

        e = Element(0, beam={}, aperture=ApertureRectangle(aperture=(3.0, 4.0), padding=(1.0, 3.0)))
        self.assertListEqual(e.aperture.aperture.numpy().tolist(), [3.0, 4.0])
        self.assertListEqual(e.aperture.padding.numpy().tolist(), [1.0, 3.0])
        x = np.zeros((6, 6), dtype=float)
        x[0] = [0.0, 1.5, 2.000001, 0, 1.5, 4]
        x[2] = [0.0, -2.999, 0, 3.000001, 2.5, -4]
        self._check(e, x, [False, True, True, True, True, True])

    def test_aperture_offset(self):
        e = Element(0, beam={}, aperture=ApertureRectangle((2.0, 4.0), offset=(3.0, 1.0)))
        x = np.zeros((6, 5), dtype=float)
        x[0] = [5.1,  1.001, 4.999, 5.0, 2.5]
        x[2] = [5.0, -2.999, 4.999, 5.1, 4.5]
        self._check(e, x, [True, False, False, True, False])

    def test_abc_methods(self):
        with self.assertRaises(NotImplementedError):
            Aperture(1, 0).forward(torch.zeros(2, 10))


class TestMarker(unittest.TestCase):
    def test(self):
        m = Marker(l=0, beam=dict(particle='proton'))
        self.assertEqual(m.l, 0.)
        self.assertDictEqual(m.beam, dict(particle='proton'))
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        x1 = m.linear(torch.from_numpy(x0)).numpy()
        x2 = m.exact(torch.from_numpy(x0)).numpy()
        self.assertTrue(np.all(x1 == x0))
        self.assertTrue(np.all(x2 == x0))


class TestDrift(unittest.TestCase):
    def test_exact(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for l in np.logspace(-1, 3, 50):
            with self.subTest(l=l):
                drift = Drift(l, beam=beam_config, label=e1_label)
                sequence = sequence_script_from_list([drift])
                script = create_script(beam_config, sequence=sequence, track=track)
                result = run_script(script, ['trackone'])
                x1_ref = result['trackone'].loc[e1_label, columns].values.T
                x1 = drift.exact(torch.from_numpy(x0)).numpy()
                self.assertTrue(e1_allclose(x1, x1_ref))


class TestKicker(unittest.TestCase):
    kicker_cls = Kicker

    def test_linear_zero_length(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        drift = Drift(0.1, beam=beam_config)  # Need drift to create non-zero length sequence.
        for _kick in np.logspace(-4, -1, 25):
            for sign in (-1, 1):
                kick = _kick * sign
                with self.subTest(kick=kick):
                    config = {list(self.kicker_cls.__annotations__)[0]: kick, 'l': 0, 'beam': beam_config}
                    kicker = self.kicker_cls(**config, label=e1_label)
                    sequence = sequence_script_from_list([drift, kicker])
                    script = create_script(beam_config, sequence=sequence, track=track)
                    result = run_script(script, ['trackone'])
                    x1_ref = result['trackone'].loc[e1_label, columns].values.T
                    x1 = kicker.linear(drift.exact(torch.from_numpy(x0))).numpy()
                    self.assertTrue(e1_allclose(x1, x1_ref))


class TestHKicker(TestKicker):
    kicker_cls = HKicker


class TestVKicker(TestKicker):
    kicker_cls = VKicker


class TestQuadrupole(unittest.TestCase):
    def test_linear(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        # MADX considers non-linear effects for path length difference and influence of momentum error:
        # https://github.com/MethodicalAcceleratorDesign/MAD-X/blob/85dea91cb5ebca66963741840aa661cf033d224e/src/trrun.f90#L4390
        # https://github.com/MethodicalAcceleratorDesign/MAD-X/blob/85dea91cb5ebca66963741840aa661cf033d224e/src/trrun.f90#L4346
        x0[[4, 5], :] = 0
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for l in np.logspace(-1, 1, 5):
            for _k1 in np.logspace(-5, 0, 10):
                for sign in (-1, 1):
                    k1 = _k1 * sign
                    with self.subTest(l=l, k1=k1):
                        quadrupole = Quadrupole(k1, l, beam=beam_config, label=e1_label)
                        sequence = sequence_script_from_list([quadrupole])
                        script = create_script(beam_config, sequence=sequence, track=track)
                        result = run_script(script, ['trackone'])
                        x1_ref = result['trackone'].loc[e1_label, columns].values.T
                        x1_ref[4, :] = 0  # MADX considers non-linear effects for path length difference (see above).
                        x1 = quadrupole.linear(torch.from_numpy(x0)).numpy()
                        self.assertTrue(e1_allclose(x1, x1_ref))

    def test_zero_gradient(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        l = 5.
        x0 = torch.from_numpy(np.random.uniform(-0.001, 0.001, size=(6, 100)))
        self.assertTrue(np.all(Quadrupole(0., l, beam=beam_config).linear(x0).numpy()
                               == Drift(l, beam=beam_config).linear(x0).numpy()))

    def test_k1_as_parameter_cannot_go_to_zero(self):
        x0 = torch.zeros(6, 1, dtype=torch.get_default_dtype())
        with self.assertRaises(ValueError):
            Quadrupole(Parameter(tensor(0.)), 5.0, beam={'beta': 0.6, 'gamma': 1.25}).linear(x0)


class TestSextupole(unittest.TestCase):
    def test_linear(self):
        element = Sextupole(np.random.uniform(0.1, 0.5), 2.5, beam=dict(particle='proton', beta=0.6, gamma=1.25))
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        x1 = element.linear(torch.from_numpy(x0)).numpy()
        self.assertTrue(np.array_equal(x1, Drift(element.l.item(), beam=element.beam).linear(torch.from_numpy(x0)).numpy()))


class TestSBend(unittest.TestCase):
    def test_linear(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        # MADX considers non-linear effects for path length difference and influence of momentum error:
        # https://github.com/MethodicalAcceleratorDesign/MAD-X/blob/85dea91cb5ebca66963741840aa661cf033d224e/src/trrun.f90#L4390
        # https://github.com/MethodicalAcceleratorDesign/MAD-X/blob/85dea91cb5ebca66963741840aa661cf033d224e/src/trrun.f90#L4345
        x0[[4, 5], :] = 0
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for l in np.logspace(-1, 2, 5):
            for _angle in np.pi/4 * np.logspace(-5, 0, 10):
                for sign in (-1, 1):
                    angle = _angle * sign
                    with self.subTest(l=l, angle=angle):
                        sbend = SBend(angle, l, beam=beam_config, label=e1_label)
                        sequence = sequence_script_from_list([sbend])
                        script = create_script(beam_config, sequence=sequence, track=track)
                        result = run_script(script, ['trackone'])
                        x1_ref = result['trackone'].loc[e1_label, columns].values.T
                        x1_ref[4, :] = 0  # MADX considers non-linear effects for path length difference (see above).
                        x1 = sbend.linear(torch.from_numpy(x0)).numpy()
                        x1[4] = 0
                        self.assertTrue(e1_allclose(x1, x1_ref))

    def test_zero_angle(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        l = 5.
        x0 = torch.from_numpy(np.random.uniform(-0.001, 0.001, size=(6, 100)))
        self.assertTrue(np.all(SBend(0., l, beam=beam_config).linear(x0).numpy()
                               == Drift(l, beam=beam_config).linear(x0).numpy()))

    def test_pole_face_rotation(self):
        beam = dict(particle='proton', beta=0.6, gamma=1.25)
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        x0[[4, 5], :] = 0
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for angle in np.random.uniform(0, np.pi/2, size=3):
            for sign in (-1, 1):
                angle *= sign
                for e1, e2 in np.random.uniform(0, angle/2, size=(3, 2)):
                    for fint in (1/6, 0.4, 0.7, 0.45, True):
                        for fintx in (fint, None):
                            if fintx is True:  # Setting fintx to True is not defined.
                                continue
                            hgap = np.random.uniform(0.1, 1)
                            with self.subTest(angle=angle, e1=e1, e2=e2, fint=fint, fintx=fintx, hgap=hgap):
                                sbend = SBend(angle, 5.0, e1, e2, fint, fintx, hgap, beam=beam, label='sbend_1')
                                sequence = sequence_script_from_list([sbend, Marker(label=e1_label)])
                                script = create_script(beam, sequence=sequence, track=track)
                                script = script.replace('refer = entry',
                                                        'refer = centre').replace('at = 0.0',
                                                                                  'at = 2.5')
                                script = script.replace(
                                    'track,',
                                    'select, flag = makethin, range = "sbend_1", makedipedge = true, thick = true;'
                                    '\nmakethin, sequence = seq;'
                                    '\nuse, sequence = seq;'
                                    '\ntrack,'
                                )
                                result = run_script(script, ['trackone'])
                                x1_ref = result['trackone'].loc[e1_label, columns].values.T
                                x1_ref[4, :] = 0
                                x1 = sbend.linear(torch.from_numpy(x0)).numpy()
                                x1[4, :] = 0
                                self.assertTrue(e1_allclose(x1, x1_ref))


class TestMakethin(unittest.TestCase):
    @staticmethod
    def _compute_deltas(n: int):
        """Compute delta and Delta."""
        return (0.5 / (1 + n), n / (n**2 - 1)) if n > 1 else (0.5, 0)

    def test_drift(self):
        d = Drift(1.0, beam=dict(particle='proton', beta=0.6, gamma=1.25))
        self.assertIs(d, d.makethin(5))

    def test_kickers(self):
        beam = dict(beta=0.6, gamma=1.25, particle='proton')
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for n in range(1, 11):
            cls = Kicker
            with self.subTest(n=n, cls=cls):
                L, kick = 12.0, 0.0012
                kicker = cls(**dict(l=L, beam=beam, **{k: kick for k in cls.__annotations__}))
                segment = kicker.makethin(n, style='edge')
                self.assertSequenceEqual([type(x) for x in segment.elements],
                                         [Drift] + [cls, Drift] * (n-1) + [cls, Drift])
                d, D = (0, 1/(n-1)) if n >= 2 else (0.5, 0)
                self.assertSequenceEqual([e.l for e in segment.elements], [d*L] + [0., D*L] * (n-1) + [0., d*L])
                for val in [getattr(e, k) for e in segment.elements[1::2] for k in type(e).__annotations__]:
                    self.assertAlmostEqual(val, kick/n, delta=1e-12)
                self.assertSequenceEqual([e.label for e in segment.elements],
                                         [f'None__{d}{i}' for i in range(n+1) for d in ('d', '')][:-1])
                sequence = sequence_script_from_list([kicker, Marker(label=e1_label)])
                sequence = sequence.replace('entry', 'centre').replace('at = 0.0', f'at = {L/2}')
                script = create_script(beam, sequence=sequence, track=track)
                script = script.replace(
                    'track,',
                    f'select, flag = makethin, slice = {n}, class = "{cls.__name__.lower()}";\n'
                    f'makethin, sequence = "seq";\n'
                    f'use, sequence = "seq";\n'
                    f'track,'
                )
                result = run_script(script, ['trackone'])
                x1_ref = result['trackone'].loc[e1_label, columns].values.T
                x1 = segment.linear(torch.from_numpy(x0)).numpy()
                self.assertTrue(e1_allclose(x1, x1_ref))

    def test_quadrupole(self):
        beam = dict(beta=0.6, gamma=1.25, particle='proton')
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for n in range(1, 11):
            with self.subTest(n=n):
                L, k1 = 12.0, 0.0012
                quadrupole = Quadrupole(k1, L, beam=beam)
                segment = quadrupole.makethin(n)
                self.assertSequenceEqual(
                    [type(x) for x in segment.elements],
                    [Drift] + [ThinQuadrupole, Drift] * (n-1) + [ThinQuadrupole, Drift]
                )
                d, D = self._compute_deltas(n)
                self.assertSequenceEqual([e.l for e in segment.elements], [d*L] + [0., D*L] * (n-1) + [0., d*L])
                for val in [e.k1l for e in segment.elements if isinstance(e, ThinQuadrupole)]:
                    self.assertAlmostEqual(val.item(), k1*L/n, delta=1e-12)
                sequence = sequence_script_from_list([quadrupole, Marker(label=e1_label)])
                sequence = sequence.replace('entry', 'centre').replace('at = 0.0', f'at = {L/2}')
                script = create_script(beam, sequence=sequence, track=track)
                script = script.replace(
                    'track,',
                    f'select, flag = makethin, slice = {n}, thick = false, class = "quadrupole";\n'
                    f'makethin, sequence = "seq";\n'
                    f'use, sequence = "seq";\n'
                    f'track,'
                )
                result = run_script(script, ['trackone'])
                x1_ref = result['trackone'].loc[e1_label, columns].values.T
                x1 = segment.linear(torch.from_numpy(x0)).numpy()
                self.assertTrue(e1_allclose(x1, x1_ref))
        q = Quadrupole(1, 2, beam=dict(beta=0.6, gamma=1.25))
        self.assertIs(q.makethin(0), q)

    def test_sbend(self):
        with self.assertRaises(NotImplementedError):
            SBend(0.1, 5.0, beam=dict(beta=0.6, gamma=1.25, particle='proton')).makethin(3)

    def test_create_thin_sequence(self):
        with self.assertRaises(ValueError):
            ThinElement.create_thin_sequence(0, 1, Drift, ThinQuadrupole, '', 'teapot')
        thin_cls = partial(HKicker, 0.1)
        thick_cls = partial(Drift, beam=dict(beta=0.6, gamma=1.25))
        for n in range(1, 11):
            self.assertEqual(len(ThinElement.create_thin_sequence(n, 1.0, thick_cls, thin_cls, '', 'teapot')), 2*n + 1)

    def test_wrapped(self):
        element = Tilt(Offset(Quadrupole(0.1, 5.0, beam=dict(beta=0.6, gamma=1.25)), 1.0), 2.0)
        thin = element.makethin(1)
        self.assertIsNot(thin, element)
        self.assertIsNot(thin.target, element.target)
        self.assertIsNot(thin.element, element.element)
        self.assertIsInstance(element.element, Quadrupole)
        self.assertIsInstance(thin, Tilt)
        self.assertIsInstance(thin.target, Offset)
        self.assertIsInstance(thin.target.target, Segment)
        self.assertIs(thin.element, thin.target.target)
        self.assertEqual(thin.psi, 2.0)
        self.assertEqual(thin.target.dx, 1.0)
        self.assertEqual(thin.target.dy, 0.0)
        self.assertSequenceEqual([type(x) for x in thin.element.elements], [Drift, ThinQuadrupole, Drift])

    def test_special_cases(self):
        q = Quadrupole(2.0, 1.0, beam=dict(beta=0.6, gamma=1.25), label='test')
        self.assertIs(q.makethin(0), q)
        q = Quadrupole(2.0, 0.999e-6, beam=dict(beta=0.6, gamma=1.25), label='test')
        self.assertIs(q.makethin(3), q)
        k = HKicker(2.0, l=0.987e-6, beam=dict(beta=0.6, gamma=1.25), label='test')
        self.assertIs(k.makethin(3), k)
        k.makethin_min_length = 1e-7
        self.assertIsInstance(k.makethin(3), Segment)


class TestThinQuadrupole(unittest.TestCase):
    def test_makethin(self):
        with self.assertRaises(NotImplementedError):
            ThinQuadrupole(1.0, label='test').makethin(0)
        with self.assertRaises(NotImplementedError):
            ThinQuadrupole(1.0, label='test').makethin(3)

    def test_track(self):
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        beam = dict(particle='proton', beta=0.6, gamma=1.25)
        quad = Quadrupole(0.01, 5.0, beam=beam, label='test')
        for n in range(2, 8):
            thin = quad.makethin(n)

            sequence_thin = sequence_script_from_list(thin.elements + [Marker(label=e1_label)])
            script_thin = create_script(beam, sequence=sequence_thin, track=track)
            result_thin = run_script(script_thin, ['trackone'])
            x1_thin = result_thin['trackone'].loc[e1_label, columns].values.T

            x1 = thin.linear(torch.from_numpy(x0)).numpy()

            sequence_makethin = sequence_script_from_list([quad, Marker(label=e1_label)])
            sequence_makethin = sequence_makethin.replace('entry', 'centre').replace('at = 0.0', f'at = {quad.l / 2}')
            script_makethin = create_script(beam, sequence=sequence_makethin, track=track)
            script_makethin = script_makethin.replace(
                'track,',
                f'select, flag = makethin, slice = {n}, thick = false, class = "quadrupole";\n'
                f'makethin, sequence = "seq";\n'
                f'use, sequence = "seq";\n'
                f'track,'
            )
            result_makethin = run_script(script_makethin, ['trackone'])
            x1_ref = result_makethin['trackone'].loc[e1_label, columns].values.T

            self.assertTrue(e1_allclose(x1, x1_ref))
            self.assertTrue(e1_allclose(x1, x1_thin))
            self.assertTrue(e1_allclose(x1_thin, x1_ref))


class TestThinSextupole(unittest.TestCase):
    def test_makethin(self):
        with self.assertRaises(NotImplementedError):
            ThinSextupole(1.0, label='test').makethin(0)
        with self.assertRaises(NotImplementedError):
            ThinSextupole(1.0, label='test').makethin(3)


class TestAlignmentError(unittest.TestCase):
    def test_raise_attribute_error(self):
        a = AlignmentError(Quadrupole(2.0, 1.0, beam={'beta': 0.6, 'gamma': 1.25}, label='test'))
        with self.assertRaises(AttributeError):
            getattr(a, 'unknown_attr')
        with self.assertRaises(AttributeError):
            getattr(a, 'k1')

    def test_unwrap(self):
        a = Tilt(Offset(LongitudinalRoll(Marker(), 0.1), 0.2), 0.3)
        self.assertTrue(all(it.starmap(op.is_, it.zip_longest(a.unwrap(),
                                                              [a, a.target, a.target.target, a.target.target.target]))))

    def test_aperture_loss(self):
        x = torch.from_numpy(np.random.uniform(-0.05, 0.05, size=(6, 100)))
        d = Drift(1.0, beam=dict(beta=0.6, gamma=1.25), aperture=ApertureCircle(aperture=0.01))
        a = AlignmentError(d)
        self.assertTrue(np.array_equal(a.loss(x).numpy(), d.loss(x).numpy()))

    def test_enter_exit(self):
        a = AlignmentError(Quadrupole(2.0, 1.0, beam={'beta': 0.6, 'gamma': 1.25}, label='test'))
        x = np.random.random(size=(6, 100))
        self.assertTrue(np.array_equal(a.enter(torch.from_numpy(x)).numpy(), x))
        self.assertTrue(np.array_equal(a.exit(torch.from_numpy(x)).numpy(), x))


class TestOffset(unittest.TestCase):
    def test(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        elements = [Quadrupole(0.1, 2.0, beam=beam_config, label=e1_label)]
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        x0[[4, 5], :] = 0
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for dx, dy in np.random.uniform(-1e-2, 1e-2, size=(100, 2)):
            for element in elements:
                with self.subTest(dx=dx, dy=dy, element=element):
                    element = Offset(element, dx, dy)
                    script = create_script(beam_config, sequence=sequence_script_from_list([element]), track=track,
                                           errors=error_script_from_list([element]))
                    result = run_script(script, ['trackone'])
                    x1_ref = result['trackone'].loc[e1_label, columns].values.T
                    x1_ref[4, :] = 0  # MADX considers non-linear effects for path length difference (see above).
                    # Need to copy x0 because Offset .enter .exit modifies its argument in-place via slice assignment.
                    x1 = element.linear(torch.from_numpy(x0.copy())).numpy()
                    self.assertTrue(e1_allclose(x1, x1_ref))


class TestLongitudinalRoll(unittest.TestCase):
    cls = LongitudinalRoll

    def test_rotation(self):
        xy_0 = np.zeros((6, 4), dtype=float)
        xy_0[0] = [1, 0, -1, 0]
        xy_0[2] = [0, -1, 0, 1]
        roll_clockwise = self.cls(Drift(0., beam={'beta': 0.6, 'gamma': 1.25}), np.pi / 2)
        xy_1 = roll_clockwise.enter(torch.from_numpy(xy_0)).numpy()
        xy_1_ref = np.zeros((6, 4), dtype=float)
        xy_1_ref[0] = [0, -1, 0, 1]
        xy_1_ref[2] = [-1, 0, 1, 0]
        self.assertTrue(e1_allclose(xy_1, xy_1_ref))
        xy_2 = roll_clockwise.exit(torch.from_numpy(xy_1)).numpy()
        self.assertTrue(e1_allclose(xy_2, xy_0))

        roll_ccw = self.cls(Drift(0., beam={'beta': 0.6, 'gamma': 1.25}), -np.pi / 2)
        xy_1 = roll_ccw.enter(torch.from_numpy(xy_0)).numpy()
        xy_1_ref = np.zeros((6, 4), dtype=float)
        xy_1_ref[0] = [0, 1, 0, -1]
        xy_1_ref[2] = [1, 0, -1, 0]
        self.assertTrue(e1_allclose(xy_1, xy_1_ref))
        xy_2 = roll_ccw.exit(torch.from_numpy(xy_1)).numpy()
        self.assertTrue(e1_allclose(xy_2, xy_0))

    def test(self):
        beam_config = {'particle': 'proton', 'beta': 0.6, 'gamma': 1.25}
        elements = [Quadrupole(0.1, 2.0, beam=beam_config, label=e1_label), HKicker(0.01, label=e1_label),
                    VKicker(0.1, label=e1_label)]
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        x0[[4, 5], :] = 0
        track = track_script(x0, [e1_label], aperture=False, recloss=False)
        for psi in np.random.uniform(-np.pi, np.pi, size=25):
            for element in elements:
                with self.subTest(psi=psi, element=element):
                    sequence = []
                    if element.l == 0:  # Need to insert drift because MADX can't deal with zero-length sequences.
                        sequence.append(Drift(1.0, beam=beam_config))
                    element = self.cls(element, psi)
                    sequence.insert(0, element)
                    script = create_script(beam_config, sequence=sequence_script_from_list(sequence), track=track,
                                           errors=error_script_from_list([element]))
                    result = run_script(script, ['trackone'])
                    x1_ref = result['trackone'].loc[e1_label, columns].values.T
                    if isinstance(element.target, Quadrupole):
                        x1_ref[4, :] = 0  # MADX considers non-linear effects for path length difference (see above).
                    x1 = element.linear(torch.from_numpy(x0)).numpy()
                    self.assertTrue(e1_allclose(x1, x1_ref))


class TestTilt(TestLongitudinalRoll):
    cls = Tilt


class TestBPMError(unittest.TestCase):
    def test(self):
        err = BPMError(Monitor(0.0, beam=dict(beta=0.6, gamma=1.25)), 0.1, 0.2, 0.3, 0.4)
        x0 = np.random.uniform(-0.001, 0.001, size=(6, 100))
        self.assertTrue(np.array_equal(
            err.readout(torch.from_numpy(x0)).numpy(),
            [[1.3], [1.4]] * (x0[[0, 2]] + [[0.1], [0.2]])
        ))

    def test_enter_exit(self):
        err = BPMError(Monitor(0.0, beam=dict(beta=0.6, gamma=1.25)), 0.1, 0.2, 0.3, 0.4)
        x0 = torch.from_numpy(np.random.uniform(-0.001, 0.001, size=(6, 100)))
        self.assertIs(err.enter(x0), x0)
        self.assertIs(err.exit(x0), x0)


class TestSegment(unittest.TestCase):
    def test(self):
        s = Segment([HKicker(-0.5), HKicker(0.5)])
        x = np.random.uniform(-0.001, 0.001, size=(6, 100))
        self.assertTrue(e1_allclose(s.linear(torch.from_numpy(x)).numpy(), x))

    def test_flatten(self):
        beam = dict(beta=0.6, gamma=1.25)
        s = Segment([Quadrupole(2.0, 2.0, beam=beam, label='q1'), Segment([Quadrupole(4.0, 4.0, beam=beam, label='q2')])])
        f = s.flat()
        self.assertEqual(len(f.elements), 2)
        self.assertIs(f.elements[0], s.elements[0])
        self.assertIs(f.elements[1], s.elements[1].elements[0])
        f = s.makethin(2).flat()
        self.assertEqual(len(f.elements), 10)
        self.assertTrue(all(x.label.startswith('q1') for x in f.elements[:5]))
        self.assertTrue(all(x.label.startswith('q2') for x in f.elements[5:]))
        self.assertSequenceEqual([type(x) for x in f.elements],
                                 [Drift, ThinQuadrupole, Drift, ThinQuadrupole, Drift, Drift, ThinQuadrupole, Drift,
                                  ThinQuadrupole, Drift])

    def test_makethin(self):
        s = Segment([Drift(12.0, beam=dict(beta=0.6, gamma=1.25), label='drift_1'),
                     Quadrupole(120.0, 24.0, beam=dict(beta=0.6, gamma=1.25), label='q_1'),
                     HKicker(240.0, l=36.0, beam=dict(beta=0.6, gamma=1.25), label='h_kicker_1')])
        thin_variants = [s.makethin(3), s.makethin({None: 3}),
                         s.makethin({Element: 3, Quadrupole: 5, HKicker: 7, re.compile('.+'): 9}),
                         s.makethin({re.compile('.+'): 3, re.compile('.*'): 5, Element: 7, Quadrupole: 9, None: 11})]
        for thin in thin_variants:
            self.assertIs(thin.elements[0], s.elements[0])
            self.assertSequenceEqual([type(x) for x in thin.elements], [Drift, ThinElement, ThinElement])
            self.assertSequenceEqual([type(x) for x in thin.elements[1].elements],
                                     [Drift, ThinQuadrupole, Drift, ThinQuadrupole, Drift, ThinQuadrupole, Drift])
            self.assertSequenceEqual([type(x) for x in thin.elements[2].elements],
                                     [Drift, HKicker, Drift, HKicker, Drift, HKicker, Drift])
            self.assertSequenceEqual([x.l for x in thin.elements[1].elements[::2]], [3.0, 9.0, 9.0, 3.0])
            self.assertSequenceEqual([x.k1l for x in thin.elements[1].elements[1::2]], [120 * 24 / 3] * 3)
            self.assertSequenceEqual([x.l for x in thin.elements[2].elements[::2]], [4.5, 13.5, 13.5, 4.5])
            self.assertSequenceEqual([x.kick for x in thin.elements[2].elements[1::2]], [240 / 3] * 3)

        thin_variants = [s.makethin({Quadrupole: 2, HKicker: 3, VKicker: 4, None: 5}),
                         s.makethin({Quadrupole: 2, re.compile('[a-z_]+_1'): 3, HKicker: 4}),
                         s.makethin({re.compile('q_1'): 2, re.compile('[a-z_]+_1'): 3, HKicker: 4})]
        for thin in thin_variants:
            self.assertIs(thin.elements[0], s.elements[0])
            self.assertSequenceEqual([type(x) for x in thin.elements], [Drift, ThinElement, ThinElement])
            self.assertSequenceEqual([type(x) for x in thin.elements[1].elements],
                                     [Drift, ThinQuadrupole, Drift, ThinQuadrupole, Drift])
            self.assertSequenceEqual([type(x) for x in thin.elements[2].elements],
                                     [Drift, HKicker, Drift, HKicker, Drift, HKicker, Drift])
            self.assertSequenceEqual([x.l for x in thin.elements[1].elements[::2]], [4.0, 16.0, 4.0])
            self.assertSequenceEqual([x.k1l for x in thin.elements[1].elements[1::2]], [120 * 24 / 2] * 2)
            self.assertSequenceEqual([x.l for x in thin.elements[2].elements[::2]], [4.5, 13.5, 13.5, 4.5])
            self.assertSequenceEqual([x.kick for x in thin.elements[2].elements[1::2]], [240 / 3] * 3)

        thin = s.makethin({Quadrupole: 2})
        self.assertIsInstance(thin.elements[1], ThinElement)
        self.assertIs(thin.elements[2], s.elements[2])

        with self.assertRaises(TypeError):
            s.makethin({1: 2})

    def test_raise_attribute_error(self):
        with self.assertRaises(AttributeError):
            getattr(Segment([Drift(1.0, beam=dict(beta=0.6, gamma=1.25))]), 'unknown_attr')

    # noinspection PyTypeChecker,PyStatementEffect
    def test_getitem(self):
        s = Segment([Drift(12.0, beam=dict(beta=0.6, gamma=1.25), label='drift_1'),
                     Quadrupole(120.0, 24.0, beam=dict(beta=0.6, gamma=1.25), label='q_1'),
                     Offset(Drift(16.0, beam=dict(beta=0.6, gamma=1.25), label='drift_2'), dx=5.0),
                     HKicker(240.0, l=36.0, beam=dict(beta=0.6, gamma=1.25), label='h_kicker_1')])
        cases = [
            (0, s.elements[0]),
            (1, s.elements[1]),
            (2, s.elements[2]),
            (3, s.elements[3]),
            (re.compile('[a-z]+_1'), s.elements[:2]),
            ((re.compile('[a-z]+_1'), 0), s.elements[0]),
            ((re.compile('[a-z]+_1'), 1), s.elements[1]),
            (re.compile('.+_1'), s.elements[:2] + s.elements[-1:]),
            ('*_1', s.elements[:2] + s.elements[-1:]),
            (re.compile('^[a-z]+$'), []),
            ('drift_2', s.elements[2]),
            (Drift, s.elements[::2]),
            ('drift_*', s.elements[::2]),
            (Offset, s.elements[2:3]),
            (Tilt, []),
            (Quadrupole, s.elements[1:2]),
            (HKicker, s.elements[-1:]),
            ((HKicker, 0), s.elements[-1]),
            (Kicker, s.elements[-1:]),
            (VKicker, []),
            (slice(None, None), s.elements),
            (slice(1, None), s.elements[1:]),
            (slice(None, -1), s.elements[:-1]),
            (slice(1, -1), s.elements[1:-1]),
            (slice('q_1', -1), s.elements[1:-1]),
            (slice(None, 'drift_2'), s.elements[:-1]),
            (slice(None, (Offset, 0)), s.elements[:-1]),
            (slice(None, s.elements[-2]), s.elements[:-1]),
            (slice(s.elements[1], s.elements[-2]), s.elements[1:-1]),
        ]
        for selection, expected in cases:
            with self.subTest(selection=selection, expected=expected):
                elements = s[selection]
                if isinstance(selection, slice):
                    self.assertIsInstance(elements, Segment)
                    elements = elements.elements
                elif isinstance(expected, list):
                    self.assertIsInstance(elements, list)
                else:
                    self.assertIsInstance(elements, (Element, AlignmentError))
                if not isinstance(expected, list):
                    expected = [expected]
                    elements = [elements]
                self.assertSequenceEqual(elements, expected)
                self.assertTrue(all(it.starmap(op.is_, it.zip_longest(elements, expected))))
        with self.assertRaises(IndexError):
            s['unknown':]
        with self.assertRaises(IndexError):
            s[1:'illegal']
        with self.assertRaises(TypeError):
            s[1.0]
        with self.assertRaises(TypeError):
            s[object()]

    def test_forward(self):
        beam = dict(beta=0.6, gamma=1.25)
        x0 = np.zeros((6, 5), dtype=float)
        x0[0, :] = [0.0, 0.0  , 0.1, 0.007, 0.0   ]
        x0[1, :] = [0.0, 0.001, 0.0, 0.001, 0.0051]
        lattice = Segment([
            Drift(1.0, beam=beam, label='d1', aperture=ApertureCircle(0.01)),
            Drift(1.0, beam=beam, label='d2', aperture=ApertureCircle(0.01)),
            Drift(1.0, beam=beam, label='d3', aperture=ApertureEllipse((0.01, 0.05))),
            Drift(1.0, beam=beam, label='d4', aperture=ApertureRectangle((0.01, np.inf))),
            Drift(1.0, beam=beam, label='d5', aperture=ApertureCircle(0.01)),
        ])
        ret = lattice.exact(torch.from_numpy(x0))
        self.assertIsInstance(ret, torch.Tensor)
        self.assertTupleEqual(tuple(ret.shape), x0.shape)
        script = create_script(beam,
                               sequence=sequence_script_from_list(lattice.elements),
                               track=track_script(x0, ['d5'], aperture=False, recloss=False))
        result = run_script(script, ['trackone'])
        x1_ref = result['trackone'].loc['d5', columns].values.T
        self.assertTrue(e1_allclose(ret.numpy(), x1_ref))

        ret = lattice.exact(torch.from_numpy(x0), aperture=True)
        self.assertIsInstance(ret, torch.Tensor)
        self.assertTupleEqual(tuple(ret.shape), (6, 2))
        script = create_script(beam,
                               sequence=sequence_script_from_list(lattice.elements),
                               track=track_script(x0, ['d5'], aperture=True, recloss=False))
        result = run_script(script, ['trackone'])
        x1_ref = result['trackone'].loc['d5', columns].values.T
        self.assertTrue(e1_allclose(ret.numpy(), x1_ref))

        ret = lattice.exact(torch.from_numpy(x0), aperture=True, recloss='sum')
        self.assertIsInstance(ret, tuple)
        self.assertIsInstance(ret[0], torch.Tensor)
        self.assertIsInstance(ret[1], torch.Tensor)
        self.assertTupleEqual(tuple(ret[0].shape), (6, 2))
        self.assertTupleEqual(tuple(ret[1].shape), tuple())
        self.assertGreater(ret[1].item(), 0.)

        ret = lattice.exact(torch.from_numpy(x0), aperture=True, recloss=True)
        self.assertIsInstance(ret, tuple)
        self.assertIsInstance(ret[0], torch.Tensor)
        self.assertIsInstance(ret[1], dict)
        self.assertSequenceEqual(list(ret[1]), ['d1', 'd2', 'd3', 'd4', 'd5'])
        self.assertTupleEqual(tuple(ret[0].shape), (6, 2))
        self.assertSequenceEqual([tuple(x.shape) for x in ret[1].values()], [(5,), (4,), (4,), (3,), (2,)])

        ret = lattice.exact(torch.from_numpy(x0), aperture=True, recloss=[re.compile(r'd\d')],
                            loss_func=lambda x: (x > 0).double())
        self.assertIsInstance(ret, tuple)
        self.assertIsInstance(ret[0], torch.Tensor)
        self.assertIsInstance(ret[1], dict)
        self.assertSequenceEqual(list(ret[1]), ['d1', 'd2', 'd3', 'd4', 'd5'])
        self.assertTupleEqual(tuple(ret[0].shape), (6, 2))
        self.assertSequenceEqual([tuple(x.shape) for x in ret[1].values()], [(5,), (4,), (4,), (3,), (2,)])
        self.assertSequenceEqual([torch.sum(x).item() for x in ret[1].values()], [1.0, 0.0, 1.0, 1.0, 0.0])

        ret = lattice.exact(torch.from_numpy(x0), aperture=True, recloss='sum',
                            loss_func=lambda x: (x > 0).double().sum())
        self.assertIsInstance(ret, tuple)
        self.assertIsInstance(ret[0], torch.Tensor)
        self.assertIsInstance(ret[1], torch.Tensor)
        self.assertTupleEqual(tuple(ret[0].shape), (6, 2))
        self.assertEqual(ret[1].item(), 3.0)

        ret = lattice.exact(torch.from_numpy(x0), observe=['d1', 'd2', 'd3', 'd4', 'd5'])
        self.assertIsInstance(ret, tuple)
        self.assertIsInstance(ret[0], torch.Tensor)
        self.assertIsInstance(ret[1], dict)
        self.assertTupleEqual(tuple(ret[0].shape), x0.shape)
        self.assertTrue(np.array_equal(ret[0].numpy(), ret[1]['d5'].numpy()))
        script = create_script(beam,
                               sequence=sequence_script_from_list(lattice.elements),
                               track=track_script(x0, ['d1', 'd2', 'd3', 'd4', 'd5'], aperture=False, recloss=False))
        result = run_script(script, ['trackone'])
        for place in ['d1', 'd2', 'd3', 'd4', 'd5']:
            self.assertTrue(e1_allclose(ret[1][place].numpy(), result['trackone'].loc[place, columns].values.T))

    def test_forward_different_methods(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        lattice = Segment([
            Drift(l=1, beam=beam, label='drift_1'),
            Quadrupole(k1=0.1, l=2, beam=beam, label='quad_1'),
            Quadrupole(k1=0.1, l=2, beam=beam, label='quad_2'),
        ])
        x0 = torch.from_numpy(np.random.uniform(-0.01, 0.01, size=(6, 250)))
        expected = lattice.elements[2].linear(lattice.elements[1].second_order(lattice.elements[0].linear(x0))).numpy()
        x1 = lattice.forward(x0, method={Drift: 'linear',
                                         'quad_2': Quadrupole.linear,
                                         Quadrupole: Quadrupole.second_order}, exact_drift=False).numpy()
        x2 = lattice.forward(x0, method={re.compile('drift_[0-9]'): Drift.linear,
                                         re.compile('quad_[2-9]'): 'linear',
                                         re.compile('quad_[0-9]'): 'second_order'}, exact_drift=False).numpy()
        self.assertTrue(np.array_equal(x1, expected))
        self.assertTrue(np.array_equal(x2, expected))
        expected = lattice.linear(x0).numpy()
        x1 = lattice.forward(x0, method={None: 'linear'})
        x2 = lattice.forward(x0, method={'*_*': 'linear'})
        self.assertTrue(np.array_equal(x1, expected))
        self.assertTrue(np.array_equal(x2, expected))

    def test_forward_all_particles_lost_in_between(self):
        beam = {'beta': 0.6, 'gamma': 1.25}
        aperture = ApertureCircle(1)
        lattice = Segment([
            Drift(l=1, beam=beam, label='drift_1', aperture=aperture),
            Quadrupole(k1=0.1, l=2, beam=beam, label='quad_1', aperture=aperture),
            Quadrupole(k1=0.1, l=2, beam=beam, label='quad_2', aperture=aperture),
        ])
        x0 = torch.zeros(6, 1)
        x0[1, 0] = 2
        x1 = lattice.linear(x0, aperture=True)
        self.assertEqual(x1.shape, (6, 0))
        x1, history = lattice.linear(x0, observe=['*'], aperture=True)
        self.assertEqual(x1.shape, (6, 0))
        self.assertEqual(history['drift_1'].shape, (6, 1))
        self.assertEqual(history['quad_1'].shape, (6, 0))
        self.assertEqual(history['quad_2'].shape, (6, 0))


class TestUtilities(unittest.TestCase):
    def setUp(self):
        random.seed(12345)

    def test_symplectify(self):
        allclose = partial(np.allclose, atol=1e-15, rtol=1e-14)
        with self.subTest('test identity'):
            R = torch.eye(6)
            self.assertTrue(allclose(Utilities.symplectify(R).numpy(), R.numpy()))
        beam = {'beta': 0.6, 'gamma': 1.25}
        for name, cls in elements.items():
            attributes = {k: random.uniform(0.001, 1) for k in get_type_hints(cls) if k not in cls.field_errors.values()}
            if issubclass(cls, (HKicker, VKicker)):
                del attributes['hkick']
                del attributes['vkick']
            if issubclass(cls, Marker):
                attributes['l'] = 0.
            element = cls(beam=beam, **attributes)
            R = element.R
            if issubclass(cls, CompoundElement):
                R = Utilities.symplectify(R)
            with self.subTest(f'test symplecticity condition ({cls})'):
                self.assertTrue(allclose((torch.t(R) @ Utilities.S @ R).numpy(), Utilities.S.numpy()))
            with self.subTest(f'test symplectifying again does not change the matrix ({cls})'):
                self.assertTrue(allclose(Utilities.symplectify(R).numpy(), R.numpy()))


if __name__ == '__main__':
    unittest.main()
