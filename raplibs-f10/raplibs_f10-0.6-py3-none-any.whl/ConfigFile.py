
def flashData_Creator(HV_Val,DAC_Val,T_Val):
    flashData = [
    3,      # board number/ID
    '4v1 ', # board version
    'v10 ', # hardware version
    'v8  ', # software version (Microblaze)
    hex(HV_Val),   # high voltage
    hex(DAC_Val),  # DAC
    T_Val,     # Temperature in Celsius
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    0xFFFFFFFF,
    'HAMA', # detector S1, manufacturer
    'MATS',
    'U   ',
    'S133', # type no
    '60-1',
    '350P',
    'E   ',
    '4826', # serial no
    '3   ',
    '53.9', # Vop
    '9V  ',
    '0.03', # Id
    '1uA ',
    'HAMA', # detector S2, manufacturer
    'MATS',
    'U   ',
    'S133', # type no
    '60-3',
    '050P',
    'E   ',
    '7080', # serial no
    '8   ',
    '54.9', # Vop
    '8V  ',
    '0.12', # Id
    '3uA '
    ]
