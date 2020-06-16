import os
import sys
import json
import shutil
import logging
import argparse
import subprocess
import numpy as np
try:
    from termcolor import cprint
except ImportError:
    def cprint(text, **kwargs):
        print(text)

logging.basicConfig(
    format='%(message)s',
    level=os.getenv('LOG_LEVEL', 'WARNING'))

from .. import all_ranges

##################################################

PD_THRESHOLD = 1
IFOS = ['2G', 'O2', 'O3', 'CE']

##################################################

def test_path(*args):
    """Return path to package file."""
    return os.path.join(os.path.dirname(__file__), *args)


def git_cmd(*args, **kwargs):
    """Exec git command."""
    try:
        return subprocess.run(
            ['git'] + list(args),
            capture_output=True, universal_newlines=True,
            check=True,
            **kwargs,
        )
    except FileNotFoundError:
        raise SystemExit("Could not find git executable.")
    except subprocess.CalledProcessError as e:
        logging.error(e.stderr.split('\n')[0])


def git_find_upstream_name():
    """Find name of git upstream."""
    proc = git_cmd('remote', '-v')
    if not proc:
        return
    for remote in proc.stdout.strip().split('\n'):
        name, url, fp = remote.split()
        if 'gwinc/inspiral-range.git' in url:
            return name


def git_rev_resolve_hash(git_rev):
    """Resolve a git revision into its hash string."""
    proc = git_cmd('show', '-s', '--format=format:%H', git_rev)
    if proc:
        return proc.stdout
    else:
        return


def git_extract_hash(git_hash, path):
    """Extract code for git hash into specified directory."""
    hash_path = os.path.join(path, '.hash-{}'.format(git_hash))
    if os.path.exists(hash_path):
        return
    if os.path.exists(path):
        shutil.rmtree(path)
    logging.info("extracting code from git hash {}...".format(git_hash))
    os.makedirs(path)
    try:
        subprocess.check_call(
            'git archive {} | tar -x -C {}'.format(
                git_hash, path),
            shell=True)
    except subprocess.CalledProcessError:
        raise SystemExit("Could not extract code from git.")
    with open(hash_path, 'w') as f:
        f.write('')


def ranges_git(gitpath, ifopath, **kwargs):
    """Exec inspiral_range in subprocess from checkout of code."""
    params = ['{}={}'.format(*kv) for kv in kwargs.items()]
    try:
        proc = subprocess.run(
            [sys.executable, '-m', 'inspiral_range', '-a', ifopath, '--format=json'] + params,
            cwd=gitpath,
            capture_output=True, universal_newlines=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logging.error(e.stderr.split('\n')[0])
        raise
    return json.loads(proc.stdout)


def ranges_dt(ifopath, **kwargs):
    """Load cached output from distance_tool [ref]""" 
    import yaml
    with open(test_path('compare.yaml')) as f:
        compare = yaml.load(f, Loader=yaml.SafeLoader)
    rd = compare[os.path.basename(ifopath)]
    m1 = kwargs['m1']
    m2 = kwargs['m2']
    assert m1 == m2
    dt = rd[m1]
    params = {
        'approximant': dt['approximant'],
        'm1': m1, 'm2': m2,
    }
    del dt['approximant']
    metrics = {k: (v, 'Mpc') for k, v in dt.items()}
    return {'metrics': metrics, 'waveform': params}


def check_diff(ir0, ir1, fmt=''):
    """Compare calculations"""
    ok = True
    for t in ir0:
        val0 = ir0[t][0]
        val1 = ir1[t][0]
        pd = ((val1 - val0) / max(val0, val1)) * 100
        color = None
        if abs(pd) > PD_THRESHOLD:
            ok = False
            color = 'red'
        cprint(fmt.format(
            t, val0, val1, pd),
               color)
    return ok

##################################################

def main():
    parser = argparse.ArgumentParser(
        description="""inspiral_range cross validation

This command calculates all ranges for various PSDs with the current
code and compares them against those calculated with code from a
specified git revision.  You must be running from a git checkout of
the source for this to work.  The command will fail if it detects any
calculation differences.

By default it will attempt to determine the git reference for upstream
master for your current configuration (usually 'origin/master' or
'upstream/master').  You may specify an arbitrary git revision with
the --git-rev command.  For example, to compare against another
remote/branch use:

$ python3 -m inspiral_range.test --git-rev remote/dev-branch

or if you have uncommitted changes compare against the current head
with:

$ python3 -m gwinc.test --head

See gitrevisions(7) for various ways to refer to git revisions.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rgroup = parser.add_mutually_exclusive_group()
    rgroup.add_argument(
        '--git-rev', '-g', metavar='REV',
        help="specify specific git revision to compare against")
    rgroup.add_argument(
        '--head', '-gh', action='store_const', dest='git_rev', const='HEAD',
        help="shortcut for '--git-rev HEAD'")
    rgroup.add_argument(
        '-dt', action='store_true',
        help="compare against cache of distance_tool output'")
    args = parser.parse_args()

    if args.dt:
        ranges_ref = ranges_dt
        label = 'dt'

    else:
        try:
            if args.git_rev:
                git_rev = args.git_rev
            else:
                remote = git_find_upstream_name()
                if not remote:
                    raise SystemExit("Could not resolve git upstream remote name.")
                git_rev = '{}/master'.format(remote)
            logging.warning("git  rev: {}".format(git_rev))
            git_hash = git_rev_resolve_hash(git_rev)
            if not git_hash:
                raise SystemExit("Could not resolve git reference.")
            logging.warning("git hash: {}".format(git_hash))
            git_path = test_path('rev')
            git_extract_hash(git_hash, git_path)
            logging.warning('')
        except SystemExit as e:
            logging.error(e)
            sys.exit("Try running with '-dt' option.")

        def ranges_ref(*args, **kwargs):
            return ranges_git(git_path, *args, **kwargs)

        label = git_hash[:8]

    ok = True

    for ifo in IFOS:
        path = test_path(ifo+'.txt')

        print('{} {}:'.format(ifo, path))

        data = np.loadtxt(path)
        freq = data[:, 0]
        psd = data[:, 1]**2

        for m in [1.4, 10, 30]:
            out_ref = ranges_ref(path, m1=m, m2=m)
            params = out_ref['waveform']
            metrics_ref = out_ref['metrics']

            metrics_cur, H = all_ranges(freq, psd, **params)

            header = ' {}/{} {}'.format(
                H.params['m1'], H.params['m2'], H.params['approximant'])

            fmt = '  {:28} {:10.0f} {:10.0f} {:8.2f}'
            print('{:30} {:>10} {:>10} {:>8}'.format(
                header, label, 'current', '%d'))
            ok &= check_diff(metrics_ref, metrics_cur, fmt=fmt)

            print()

    if not ok:
        cprint("ERROR: differences greater than {}% detected".format(PD_THRESHOLD), 'red')
        sys.exit(1)


if __name__ == '__main__':
    main()
