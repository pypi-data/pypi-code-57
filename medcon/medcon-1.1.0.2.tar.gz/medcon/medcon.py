#!/usr/bin/env python
#!/usr/bin/python
# medcon DS ChRIS plugin app
#
# (c) 2016-2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import subprocess
import pudb

sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """


                    _
                   | |
 _ __ ___   ___  __| | ___  ___  _ __    _ __  _   _
| '_ ` _ \ / _ \/ _` |/ __|/ _ \| '_ \  | '_ \| | | |
| | | | | |  __/ (_| | (__| (_) | | | |_| |_) | |_| |
|_| |_| |_|\___|\__,_|\___|\___/|_| |_(_) .__/ \__, |
                                        | |     __/ |
                                        |_|    |___/




"""

Gstr_synopsis = """

    NAME

       medcon.py

    SYNOPSIS

        python medcon.py                                                \\
             -i|--inputFile <inputFile>                                 \\
            [-a|--args 'ARGS: <argsToPassTo_medcon>']                   \\
            [--do <macro>]                                              \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python medcon.py --man in out

    DESCRIPTION

        `medcon.py` coverts NIfTI volumes to DICOM files. This is a ChRIS
        conformant "DS" (Data Synthesis) plugin that wraps around the
        medcon package and provides a thin shim about that executable. Using
        the [--args 'ARGS: <args>'] CLI, a user can pass any additional
        arbitrary arguments to the underlying `medcon`.

        If running this application directly, i.e. outside of its
        docker container, please make sure that the `medcon` application
        is installed in the host system. On Ubuntu, this is typically:

                            sudo apt install medcon

        and also make sure that you are in an appropriate python virtual
        environment with necessary requirements already installed
        (see the `requirements.txt` file).

        Please note, however, that running this application from its
        docker container is the preferred method and the one documented
        here.

    ARGS

         -i|--inputFile <inputFile>
        Input file to process. This file exists within the explictly provided
        CLI positional <inputDir>.

        [-a|--args 'ARGS: <argsToPassTo_medcon>']
        Optional string of additional arguments to "pass through" to medcon.

        All the args for medcon are themselves specified at the plugin level
        with this flag. These args MUST be contained within single quotes
        (to protect them from the shell) and the quoted string MUST start with
         the required keyword 'ARGS: '.

        [--do <macro>]
        Optional argument to provide a "macro" type functionality. Using this
        argument will add the correct underlying arguments to the internal
        `medcon` binary.

        Currently available:

	        - 'nifti2dicom' : this will silently add the args
                              '-c dicom -split3d'

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. If set to '0', no output is logged to
        console. Note stderr and stdout are still captured and saved
        to the <outputdir> even if verbosity is '0'.

        [--version]
        If specified, print version number and exit.

"""


class Medcon(ChrisApp):
    DESCRIPTION             = """
    A ChRIS plugin that wraps loosely around a `medcon` binary to expose its functionality.
    """
    AUTHORS                 = 'Arushi Vyas / Rudolph Pienaar (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A DS plugin to convert NIfTI volumes to DICOM files.'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DOCUMENTATION           = 'https://github.com/FNNDSC/pl-medcon'
    VERSION                 = '1.1.0.2'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument("-a", "--args",
                          help="medcon arguments to pass",
                          type=str,
                          dest='args',
                          optional=True,
                          default="")
        self.add_argument("--do",
                          help="functionality of medcon to be used",
                          type=str,
                          dest='do',
                          optional=True,
                          default="nifti2dicom")
        self.add_argument("-i", "--inputFile", #equivalent to -f of medcon
                          help="input file",
                          type=str,
                          dest='inputFile',
                          optional=False,
                          default="")

    def job_run(self, str_cmd, options):
        """
        Running some CLI process via python is cumbersome. The typical/easy
        path of

                            os.system(str_cmd)

        is deprecated and prone to hidden complexity. The preferred
        method is via subprocess, which has a cumbersome processing
        syntax. Still, this method runs the `str_cmd` and returns the
        stderr and stdout strings as well as a returncode.

        Providing readtime output of both stdout and stderr seems
        problematic. The approach here is to provide realtime
        output on stdout and only provide stderr on process completion.

        """
        d_ret = {
            'stdout':       "",
            'stderr':       "",
            'returncode':   0
        }

        p = subprocess.Popen(
                    str_cmd.split(),
                    stdout      = subprocess.PIPE,
                    stderr      = subprocess.PIPE,
        )

        # Realtime output on stdout
        str_stdoutLine  = ""
        str_stdout      = ""
        while True:
            stdout      = p.stdout.readline()
            if p.poll() is not None:
                break
            if stdout:
                str_stdoutLine = stdout.decode()
                if int(options.verbosity):
                    print(str_stdoutLine, end = '')
                str_stdout      += str_stdoutLine
        d_ret['stdout']     = str_stdout
        d_ret['stderr']     = p.stderr.read().decode()
        d_ret['returncode'] = p.returncode
        if int(options.verbosity):
            print('\nstderr: \n%s' % d_ret['stderr'])
        return d_ret

    def job_stdwrite(self, d_job, options):
        """
        Capture the d_job entries to respective files.
        """
        for key in d_job.keys():
            with open(
                 '%s/%s' % (options.outputdir, key), "w"
            ) as f:
                f.write(str(d_job[key]))
                f.close()
        return {
            'status': True
        }

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        str_cmd     = ""
        str_verbose = ""

        l_appargs = options.args.split('ARGS:')
        if len(l_appargs) == 2:
            str_args = l_appargs[1]
        else:
            str_args = l_appargs[0]

        if len(options.do):
            if options.do == 'nifti2dicom':
                str_args += "-c dicom -split3d"

        if int(options.verbosity):
            print(Gstr_title)
            print('Version: %s' % self.get_version())
            str_verbose = "-v "

        os.chdir(options.outputdir)
        str_cmd = "medcon %s -f %s/%s %s" % (str_verbose, options.inputdir, options.inputFile, str_args)

        # Run the job and provide realtime stdout
        # and post-run stderr
        self.job_stdwrite(
            self.job_run(str_cmd, options), options
        )

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Medcon()
    chris_app.launch()
