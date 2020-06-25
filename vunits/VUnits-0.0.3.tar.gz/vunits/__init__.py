# -*- coding: utf-8 -*-

####
#
# setuptools likes to see a name for the package,
# and it's best-practices to have the __version__
# present, too:
#
name = 'vunits'
__version__ = '0.0.3'

import os

def run_tests(python_command='python', buffer=False, failfast=False,
              verbose=False):
    """Run unit tests.
    
    Parameters
    ----------
        python_command : str
            Command used by terminal to run python. Default is 'python'.
        buffer : bool, optional
            The standard output and standard error streams are buffered during
            the test run. Output during a passing test is discarded. Output is
            echoed normally on test fail or error and is added to the failure
            messages. Default is False.
        failfast : bool, optional
            Stop the test run on the first error or failure. Default is False.
        verbose : bool, optional
            Verbose output. Default is False.
    """
    # Swich to test directory and run the tests
    base_path = os.getcwd()
    pmutt_path = os.path.dirname(__file__)
    test_path = os.path.join(pmutt_path, 'tests')
    os.chdir(test_path)
    test_command = '{} -m unittest'.format(python_command)
    if buffer:
        test_command += ' -b'
    if failfast:
        test_command += ' -f'
    if verbose:
        test_command += ' -v'
    os.system(test_command)
    os.chdir(base_path)