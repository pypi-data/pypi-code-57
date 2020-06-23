from qcodes.instrument_drivers.Keysight.KeysightAgilent_33XXX import WaveformGenerator_33XXX


class Ks33510b(WaveformGenerator_33XXX):
    def __init__(self, ip_address):
        # set pyvisa backend to pyvisa-py, no more NI
        super().__init__('Ks33510b_', f'TCPIP0::{ip_address}::inst0::INSTR', visalib='@py')


if __name__ == '__main__':
    SIG_ADDRESS = '192.168.153.180'
    sig_inst = Ks33510b(SIG_ADDRESS)
    setattr(sig_inst, 'ch1.function_type', 'PLUS')
    # sig_inst.ch1.function_type('PULS')
    # sig_inst.ch1.amplitude_unit('VPP')
    # sig_inst.ch1.amplitude(5)
    # sig_inst.ch1.pulse_width(5e-6)
    # sig_inst.ch1.offset(2.5)
    # sig_inst.ch1.frequency(25)
    # sig_inst.ch1.output('ON')
    # sig_inst.sync.source(1)
    # sig_inst.error()
