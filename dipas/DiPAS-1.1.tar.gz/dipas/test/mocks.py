import copy

import dipas.madx.parser as madx_parser


class MockMADXConstants:
    def __init__(self):
        self.backup = {
            'special_names': madx_parser.special_names.copy(),
            'particle_dict': copy.deepcopy(madx_parser.particle_dict)
        }

    def __enter__(self):
        self.apply()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

    def apply(self):
        madx_parser.special_names['emass'] = 0.5109989461e-3
        madx_parser.special_names['pmass'] = 0.9382720813
        madx_parser.special_names['nmass'] = 0.9314940954
        madx_parser.special_names['mumass'] = 0.1056583745
        madx_parser.special_names['clight'] = 299792458
        madx_parser.special_names['qelect'] = 1.6021766208e-19
        madx_parser.special_names['hbar'] = 6.582119514e-25
        madx_parser.special_names['erad'] = 2.8179403227e-15
        madx_parser.special_names['prad'] = (
                madx_parser.special_names['erad'] * madx_parser.special_names['emass']
                / madx_parser.special_names['pmass']
        )
        madx_parser.particle_dict['positron']['mass'] = madx_parser.special_names['emass']
        madx_parser.particle_dict['electron']['mass'] = madx_parser.special_names['emass']
        madx_parser.particle_dict['proton']['mass'] = madx_parser.special_names['pmass']
        madx_parser.particle_dict['antiproton']['mass'] = madx_parser.special_names['pmass']
        madx_parser.particle_dict['posmuon']['mass'] = madx_parser.special_names['mumass']
        madx_parser.particle_dict['negmuon']['mass'] = madx_parser.special_names['mumass']
        madx_parser.particle_dict['ion']['mass'] = madx_parser.special_names['nmass']

    def restore(self):
        madx_parser.special_names.update(self.backup['special_names'])
        madx_parser.particle_dict.update(copy.deepcopy(self.backup['particle_dict']))
