from pycondor import Job, Dagman
from distutils.spawn import find_executable
from os.path import abspath, join
import configparser


class Node(Job):
    def add_args_from_cp(self, cp, section, set_name=None):
        """
        Parse command line options from a given section in an ini file and
        pass to the executable.
        cp: ConfigParser object
            ConfigParser object pointing to the ini file.
        section: str
            section of the ini file to add to the options.
        set_name: str
            subection name. If not None then will look for
            options of the form f"{section}-{set_name}"
        """
        args = []
        for opt in cp.options(section):
            arg = (cp.get(section, opt)).strip()
            args.append(f"--{opt} {arg}")

        if set_name:
            name = f"{section}-{set_name}"
            for opt in cp.options(name):
                arg = (cp.get(name, opt)).strip()
                args.append(f"--{opt} {arg}")
        self.add_arg(arg=" ".join(args))

    def get_request_memory(self, cp, name):
        """

        Parameters
        ----------
        cp: configparser.ConfigParser
        name: str
            name of subsection
        'request_memory' should always be in [workflow]
        but it can be overridden in an executable specific
        subsection such as [workflow-genwf-seed]
        """
        try:
            request_memory = cp.get("workflow-"+name, "request_memory")
        except:
            request_memory = cp.get("workflow", "request_memory")
        return request_memory


class GenWaveformJob(Node):
    """Waveform generator Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    set_name: str
        subsection name.
        either 'seed', 'train', 'validation' or 'test'
    idx: int
        index to append to output directory
        Default is None and won't append anything
    """

    def __init__(self, cp, section, set_name, idx=None):
        name = f"{section}-{set_name}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        request_cpus = cp.get(name, "n-cores")

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        if idx:
            submit_name = name + f"-{idx}"
        else:
            submit_name = name

        super().__init__(
            name=submit_name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section, set_name, idx)

    def add_args_from_cp(self, cp, section, set_name=None, idx=None):
        """
        overrides method to include the idx variable

        Parse command line options from a given section in an ini file and
        pass to the executable.
        cp: ConfigParser object
            ConfigParser object pointing to the ini file.
        section: str
            section of the ini file to add to the options.
        set_name: str
            subection name. If not None then will look for
            options of the form f"{section}-{set_name}"
        idx: int
            index to append to output directory ("--output-dir" option)
            Default is None and won't append anything
        """
        args = []
        for opt in cp.options(section):
            arg = (cp.get(section, opt)).strip()
            args.append(f"--{opt} {arg}")

        if set_name:
            name = f"{section}-{set_name}"
            for opt in cp.options(name):
                arg = (cp.get(name, opt)).strip()
                if opt == "output-dir":
                    if idx:
                        arg = arg+f"_{idx}"
                args.append(f"--{opt} {arg}")
        self.add_arg(arg=" ".join(args))


class CombineWaveformJob(Node):
    """Combine Waveform Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    set_name: str
        subsection name.
        either 'seed', 'train', 'validation' or 'test'
    """

    def __init__(self, cp, section, set_name):
        name = f"{section}-{set_name}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        request_cpus = 1

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        super().__init__(
            name=name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section, set_name)


class BuildReducedBasisJob(Node):
    """Build reduced basis Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    set_name: str
        subsection name.
        either 'seed', 'train', 'validation' or 'test'
    """

    def __init__(self, cp, section, set_name):
        name = f"{section}-{set_name}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        request_cpus = 1

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        super().__init__(
            name=name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section, set_name)


class GenTrainingSetJob(Node):
    """Generate training set Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    data: str
        name of data.
        'amp', 'phase', 'real', 'imag', 'freq'
    set_name: str
        subsection name.
        either 'train' or 'val'
    """

    def __init__(self, cp, section, data, set_name):
        data_set_name = f"{data}-{set_name}"
        name = f"{section}-{data_set_name}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        request_cpus = 1

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        super().__init__(
            name=name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section, data_set_name)


class FitJob(Node):
    """Fit Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    data: str
        subsection name.
        either 'amp', 'phase', 'real', 'imag', 'freq'
    """

    def __init__(self, cp, section, data):
        name = f"{section}-{data}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        request_cpus = cp.get("workflow-"+name, "request_cpus")
        if request_cpus == str(0):
            raise ValueError(
                "You have requested 0 cpus. Please request at least 1")

        try:
            request_gpus = cp.get("workflow-"+name, "request_gpus")
            extra_lines.append(f"request_gpus = {request_gpus}")
        except:
            pass
        super().__init__(
            name=name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section, data)


class EvaluateJob(Node):
    """Evaluate Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    set_name: str
        subsection name.
        either 'train', 'validation' or 'test'
    """

    def __init__(self, cp, section, set_name):
        name = f"{section}-{set_name}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        request_cpus = 1

        super().__init__(
            name=name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section, set_name)


class MakeWebpageJob(Node):
    """Make Webpage Job

    Parameters
    ----------
    cp: configparser.ConfigParser
    section: str
        name of section in cp.
        Also name of executable key in [executables]
    """

    def __init__(self, cp, section):
        name = f"{section}"

        executable = cp.get("executables", section)
        executable = find_executable(executable)

        log_dir = cp.get("workflow", "log_dir")

        request_memory = self.get_request_memory(cp, name)

        accounting_group = cp.get("workflow", "accounting_group")
        extra_lines = [f'accounting_group = {accounting_group}']

        request_cpus = 1

        super().__init__(
            name=name,
            executable=executable,
            error=abspath(join(log_dir, 'error')),
            log=abspath(join(log_dir, 'log')),
            output=abspath(join(log_dir, 'output')),
            submit=abspath(join(log_dir, 'submit')),
            request_memory=request_memory,
            request_cpus=request_cpus,
            getenv=True,
            universe="vanilla",
            extra_lines=extra_lines
        )

        self.add_args_from_cp(cp, section)
