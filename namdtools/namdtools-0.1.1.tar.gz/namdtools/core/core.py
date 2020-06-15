"""
core.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>

>>> from namdtools import run_namd
>>> result = run_namd('system.namd', 'system.log'   , wait=True)
>>> print(result.log_)


>>> import namdtools
>>> config = namdtools.read_configuration('production.namd')
>>> config.run(10000)
"""

from namdtools.exceptions import NAMDError
import namdtools.options as options

import os
import pandas as pd
from subprocess import Popen


# NAMD configuration
class NAMDConfiguration:
    """
    NAMD configuration file.
    """

    def __init__(self, filename=None):
        """
        Initialize instance of NAMD configuration.

        Parameters
        ----------
        filename : str
            (Optional) Name of configuration file to read.
        """

        if filename is not None:
            self._read_configuration(filename)

    def _read_configuration(self, filename):
        """
        Read configuration file.

        Note:
        """
        # TODO does the order in which arguments are read in matter?
        pass

    def run(self, n_steps):
        """

        Parameters
        ----------
        n_steps : int

        Returns
        -------

        """

        pass


# NAMD controller
class NAMD:
    """
    Controls NAMD with Python.
    """

    # Initialize class instance
    def __init__(self, configuration_file=None, log_file=None, executable=None, wait=True):
        """
        Initialize the NAMD runner.

        Parameters
        ----------
        configuration : str or NAMDConfiguration
            (Optional) NAMD configuration. If str, the name of the configuration file for processing.
        log : str
            (Optional) Path to log file.
        executable : str or list
            (Optional) NAMD executable for command line.
        wait : bool
            Should we wait for the NAMD job to finish? Or should it run in the background? (Default: True)
        """

        # Set the NAMD configuration
        self._configuration_file = None
        if configuration_file is not None:
            self.configuration = configuration_file

        # Set the log file
        self._log_file = None
        if log_file is not None:
            # log_file = os.path.splitext(self._configuration_file)[0] + '.log'
            self.log_file = log_file

        # Set the NAMD executable
        self._executable = None
        if executable is not None:
            self.executable = executable
        else:
            self.executable = _compile_namd_executable()

        self._wait = bool(wait)
        self._process = None

    @property
    def configuration_file(self):
        """
        Get the NAMD configuration.

        Returns
        -------
        NAMDConfiguration
            NAMD configuration.
        """

        return self._configuration

    @configuration_file.setter
    def configuration_file(self, configuration_file):
        """

        Parameters
        ----------
        configuration

        Returns
        -------

        """

        if not isinstance(configuration_file, str):
            raise AttributeError('must be string')

        # if not isinstance(configuration, NAMDConfiguration):
        #     raise AttributeError('must be instance of NAMD configuration')

        self._configuration_file = configuration_file

    @property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, executable):
        """
        Set the executable.
        
        Parameters
        ----------
        executable : str or list
            NAMD command to run through subprocess.
        """

        if not isinstance(executable, (str, list)):
            raise AttributeError('must be string or list')

        self._executable = executable

    @property
    def pid(self):
        # Is job started?
        if self._process is None:
            raise NAMDError('job not found')

        # Return pid
        return self._process.pid

    @property
    def poll(self):
        """
        Check if NAMD is still running.

        Returns
        -------
        None or intb
            None if NAMD is running, return code if simulations are finished.
        """

        return None if self._process is None else self._process.poll()

    @property
    def log_(self):
        pass

    @property
    def log(self):
        """
        Logfile
        Returns
        -------

        """
        pass

    # Start simulations
    def start(self):
        """
        Start NAMD simulation.
        """

        # Check if NAMD is already running
        if self.poll():
            raise NAMDError('NAMD already running')

        # Open output file and run
        with open(self.log, 'w') as stream:
            self._process = Popen(self._executable.append(self._configuration_file), stdout=stream)

        # Should we wait?
        if self._wait:
            self._process.wait()
            if self._process.poll() != 0:
                raise NAMDError('NAMD job did not finish successfully')

    # Stop simulations
    def stop(self):
        # Check if NAMD is already running
        if self.poll():
            self._process.kill()

        # Otherwise, alert that NAMD is not running
        # TODO should this be warning?
        else:
            pass

    def status(self):
        pass


# Run namd on configuration file and write to log file
def run_namd(configuration_file, log_file, wait=True):
    """
    Run NAMD on `configuration_file` and write to `log_file`.

    Parameters
    ----------
    configuration_file : str
        Path to the NAMD configuration file.
    log_file : str
        Path to log file to write out.
    wait : bool
        Should we wait for the NAMD job to finish? Or should we launch in the background?

    Returns
    -------
    NAMD
        Instance of NAMD controller.
    """

    # Create NAMD instance and start it
    job = NAMD(configuration_file, log_file, wait=wait)
    job.start()

    # Was run successful?
    # if not job.success:
    #     raise NAMDError('failed to successfully complete')

    # Return
    return job


# Extract energy from log file
def extract_energy(log_file):
    # Initialize DataFrame information
    columns = None
    records = []

    # Read through log file and extract energy records
    with open(log_file, 'r') as stream:
        for line in stream.readlines():
            # Read first ETITLE
            if columns is None and line[:6] == 'ETITLE':
                columns = line.lower().split()[1:]

            # Save each energy record
            if line[:6] == 'ENERGY':
                records.append(line.split()[1:])

    # Return DataFrame
    return pd.DataFrame(records, columns=columns).set_index(columns[0])


def read_configuration(path):
    pass


# Compile namd command
def _compile_namd_executable(strict=True):
    """
    Compile namd executable to run through subprocess.

    Parameters
    ----------
    strict : bool
        Flag to indicate if we should strictly check that charmrun and namd executables exist.

    Returns
    -------
    list
        List of command-line arguments to send to subprocess.
    """

    # Set up dummy list to store command
    cmd = []

    # Add charmrun to command
    if options.charmrun_path is not None:
        cmd.append(_first_available([options.charmrun_path, 'charmrun']) if strict else options.charmrun_path)
        for arg in options.charmrun_args:
            cmd.append(str(arg))

    # Add namd to command
    if options.namd_path is None:
        Warning('who set options.namd to None?')
        options.namd = 'namd'
    cmd.append(_first_available([options.namd_path, 'namd.exe', 'namd']) if strict else options.namd_path)
    for arg in options.namd_args:
        cmd.append(str(arg))

    # Return
    return cmd


# Helper function to find first available existing path
def _first_available(paths):
    """
    Loop through `paths` and find the first available.

    Parameters
    ----------
    paths : list
        List of paths.

    Returns
    -------
    str
        First path found.
    """

    # Loop over all paths and return first path that exists
    for path in paths:
        if os.path.exists(path):
            return path

    # If we haven't found a path, throw an error
    raise FileNotFoundError('%s not found' % paths[-1])
