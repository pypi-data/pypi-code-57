import os
import tempfile
import unittest
import warnings

from dipas.external import Paramodi
from dipas.madx.parser import Command, sequence_to_data_frame, data_frame_to_sequence


class TestParamodi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('default')

    def test_parse(self):
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'paramodi')
            with open(f_name, 'w') as fh:
                fh.write('# Version: 1.0\n'
                         '# Comment: ParamModi Export at 29.02.2019 00:00:01\n'
                         '# Context: THEFILENAME.C1\n'
                         '# Columns: PARAMETERNAME,VALUE,UNIT,BEAMPROCESSPURPOSE\n'
                         'DEVICE1/HKICK,0.0,rad,TRANSFER_INJECTION_MTI\n'
                         'LONG_DEVICE_NAME_2/CURVATURE,[0, 0],s,TRANSFER_INJECTION_MTI\n'
                         'LONG_DEVICE_NAME_2/THE_ATTRIBUTE,[[0, 0]],1/m,THE_PURPOSE\n'
                         'THE_DEVICE_NR_3/ACTIVE,false,---,RING_INJECTION')
            paramodi = Paramodi.parse(f_name)
        self.assertListEqual(paramodi.index.get_level_values(0).to_list(),
                             ['device1', 'long_device_name_2', 'long_device_name_2', 'the_device_nr_3'])
        self.assertListEqual(paramodi.index.get_level_values(1).to_list(),
                             ['hkick', 'curvature', 'the_attribute', 'active'])
        self.assertListEqual(paramodi.index.get_level_values(2).to_list(),
                             ['transfer_injection_mti', 'transfer_injection_mti', 'the_purpose', 'ring_injection'])
        self.assertEqual(paramodi['value'].to_list()[0], '0.0')
        self.assertEqual(paramodi['value'].to_list()[1], ['0', '0'])
        self.assertEqual(paramodi['value'].to_list()[2], ['0', '0'])
        self.assertEqual(paramodi['value'].to_list()[3], 'false')
        self.assertListEqual(paramodi['unit'].to_list(), ['rad', 's', '1/m', '---'])
        self.assertListEqual(paramodi['parameter_name'].to_list(),
                             ['DEVICE1/HKICK', 'LONG_DEVICE_NAME_2/CURVATURE', 'LONG_DEVICE_NAME_2/THE_ATTRIBUTE',
                              'THE_DEVICE_NR_3/ACTIVE'])
        self.assertListEqual(paramodi['original_value'].to_list(), ['0.0', '[0, 0]', '[[0, 0]]', 'false'])

    def test_update_madx_device_data(self):
        sequence = [
            Command('quadrupole', {'k1': 0.1, 'l': 2.0}, label='q1'),
            Command('s1', {'angle': 1.0, 'l': 4.0}, label='e2', base=Command('sbend', label='s1')),
            Command('hkicker', {'kick': 0.0}, label='hk1'),
            Command('vkicker', {'kick': 0.0}, label='vk1'),
        ]
        devices = sequence_to_data_frame(sequence)
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'paramodi')
            with open(f_name, 'w') as fh:
                fh.write('Q1/KL,4.0,1/m,THE_PURPOSE\n'
                         'E2/HKICK,2.0,rad,THE_PURPOSE\n'
                         'HK1/HKICK,4.0,rad,THE_PURPOSE\n'
                         'VK1/VKICK,8.0,rad,THE_PURPOSE')
            paramodi = Paramodi.parse(f_name)
        updated = data_frame_to_sequence(Paramodi.update_madx_device_data(devices, paramodi)[0])
        self.assertListEqual([c.label for c in updated], [c.label for c in sequence])
        self.assertDictEqual(updated[0].attributes, {**sequence[0].attributes, 'k1': 2.0})
        self.assertDictEqual(updated[1].attributes, {**sequence[1].attributes, 'angle': 3.0, 'dk0': 0.5})
        self.assertDictEqual(updated[2].attributes, {**sequence[2].attributes, 'kick': 4.0})
        self.assertDictEqual(updated[3].attributes, {**sequence[3].attributes, 'kick': 8.0})

    def test_apply_units(self):
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'paramodi')
            with open(f_name, 'w') as fh:
                fh.write('Q1/KL,4.0,1/m,THE_PURPOSE\n'
                         'E2/HKICK,2.0,rad,THE_PURPOSE\n'
                         'HK1/HKICK,4.0,rad,THE_PURPOSE\n'
                         'VK1/VKICK,8.0,rad,THE_PURPOSE')
            paramodi = Paramodi.parse(f_name)
        self.assertIsInstance(Paramodi.apply_units(paramodi), list)


if __name__ == '__main__':
    unittest.main()
