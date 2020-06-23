"""
General purpose tcl script creation module
"""
import typing

_opt_str = typing.Optional[str]


def create_project(file, project_name, filename, comp_name, includes, defines, standard, solution_name, part, period):
    """
    Generate a tcl script for an HLS component creation
    :param filename: name of the file containing hls code
    :param period: clock period in ns
    :param part: part code to use
    :param solution_name: name of the solution to create inside the project
    :param file: the file on which the script will be written
    :param project_name: the name of the vivado project to generate
    :param comp_name: the name of the high level component
    :param includes: list of include directories
    :param defines: list of defines
    :param standard: c++ standard code to use
    """
    file.write("open_project {}\n".format(project_name))
    file.write("set_top {}\n".format(comp_name))
    includes_str = "" if includes is None else " ".join(
        ["-I{}".format(str(s).replace("\\", "/")) for s in includes]
    )
    if defines:
        def format_def(define):
            if len(define) == 2:
                k, v = define
                return f"-D{k}={v}"
            else:
                return f"{define[0]}"

        def_str = " ".join(map(format_def, defines))
    else:
        def_str = ""
    file.write(f'add_files {filename} -cflags "-std={standard} {includes_str} {def_str}"\n')
    file.write('open_solution "{}"\n'.format(solution_name))
    file.write('set_part {{{}}} -tool vivado\n'.format(part))
    file.write('create_clock -period {} -name default\n'.format(
        period
    ))


def csynth_solution_script(file):
    """Generate a script in file for synthetizing solution solution_name of project project_name"""
    file.write('csynth_design\n')


def export_ip_script(file,
                     impl: bool,
                     hdl: str,
                     display_name: _opt_str = None,
                     descr: _opt_str = None,
                     version: _opt_str = None,
                     ip_lib: _opt_str = None,
                     vendor: _opt_str = None,
                     ):
    """Generate a script in file for exporting solution solution_name of project project_name"""
    options = [
        "-format ip_catalog",
        f"-rtl {hdl}",
        "-flow {}".format("impl" if impl else "syn")
    ]
    if display_name is not None:
        options.append(f"-display_name {display_name}")
    if descr is not None:
        options.append(f'-description "{descr}"')
    if ip_lib is not None:
        options.append(f'-library {ip_lib}')
    if vendor is not None:
        options.append(f'-vendor {vendor}')
    if version is not None:
        options.append(f'-version {version}')

    command = "export_design {}\n".format(" ".join(options))
    file.write(command)
