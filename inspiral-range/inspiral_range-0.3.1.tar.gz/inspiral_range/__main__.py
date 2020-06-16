import os
import argparse
import numpy as np

from . import __version__
from . import logger
from . import waveform
from . import inspiral_range

logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))

##################################################

description = """Calculate GW detector inspiral range from ASD/PSD

Strain spectra data should be two-column ASCII, (freq, strain), and
may be given in amplitude or power (ASD or PSD).

Inspiral waveform parameters are specified as PARAM=VALUE pairs.  Mass
('m1'/'m2') parameters are assumed to be in solar masses (Msolar)
Default: m1 = m2 = 1.4 Msolar.

"""

def parse_params(clparams):
    params = {}
    for param in clparams:
        try:
            k, v = param.split('=')
        except ValueError:
            raise ValueError("Could not parse parameter: {}".format(param))
        try:
            params[k] = float(v)
        except ValueError:
            params[k] = v
    return params


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
)


class FileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'file', values)
        setattr(namespace, 'stype', self.dest)
        delattr(namespace, 'asd')
        delattr(namespace, 'psd')


class ParamsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            params = parse_params(values)
        except ValueError as e:
            parser.error(e)
        setattr(namespace, self.dest, params)


igroup = parser.add_mutually_exclusive_group(required=True)
igroup.add_argument(
    '-a', '--asd', action=FileAction,
    help="assume noise spectrum is ASD")
igroup.add_argument(
    '-p', '--psd', action=FileAction,
    help="assume noise spectrum is PSD")
ogroup = parser.add_mutually_exclusive_group()
ogroup.add_argument(
    '-f', '--format', dest='fmt', choices=['txt', 'json', 'yaml'], default='txt',
    help="output format (default: txt)")
ogroup.add_argument(
    '-s', '--single', metavar='FUNC',
    help="print output from single function only")
parser.add_argument(
    '--plot', action='store_true',
    help="plot the spectrum and the waveform")
parser.add_argument(
    '-v', '--version', action='version', version=__version__,
    help="output value of specific calculation only (from available inspiral_range functions)")
parser.add_argument(
    'params', metavar='PARAM=VALUE', nargs='*', action=ParamsAction,
    help="waveform parameters")


def main():
    args = parser.parse_args()

    data = np.loadtxt(args.file)
    freq = data[1:, 0]
    psd = data[1:, 1]
    if args.stype == 'asd':
        psd **= 2

    metrics, H = inspiral_range.all_ranges(freq, psd, **args.params)

    if args.single:
        print(metrics[args.single][0])
    elif args.fmt == 'txt':
        print('waveform:')
        fmt = '  {:18} {}'
        for p, v in H.params.items():
            print(fmt.format(p+':', v))
        print('metrics:')
        fmt = '  {:18} {:.6f} {}'
        for r, v in metrics.items():
            print(fmt.format(r+':', v[0], v[1]))
    else:
        out = {'metrics': dict(metrics), 'waveform': dict(H.params)}
        if args.fmt == 'json':
            import json
            print(json.dumps(out))
        elif args.fmt == 'yaml':
            import yaml
            print(yaml.safe_dump(out, default_flow_style=False))
        else:
            parser.error("Unknown output format: {}".format(args.fmt))

    if args.plot:
        import matplotlib.pyplot as plt
        dlum = metrics['horizon'][0]
        z = inspiral_range.horizon_redshift(freq, psd, H=H)
        hf, ha = H.z_scale(z)
        label = '{} {}/{} M_sun\nhorizon = {:.3f} Mpc'.format(
            H.params['approximant'],
            H.params['m1'], H.params['m2'],
            dlum,
        )
        plt.loglog(freq, np.sqrt(psd), label="{} ASD".format(args.file))
        plt.loglog(hf, ha, label=label)
        plt.xlabel("frequency [Hz]")
        plt.ylabel("characteristic strain")
        plt.legend()
        plt.show()

##################################################

if __name__ == '__main__':
    main()
