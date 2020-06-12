"""
This module contains functions to execute certain Radiance programs with
Python. The Pyrano project is for simulating solar irradiance with Radiance,
therefore the functions here are pre-set with the Radiance parameters to
simulate the full solar spectrum and generate irradiance results (instead of
the visible spectrum with illuminance results).
"""
import subprocess

def _run_command(rad_cmd, args, stdin=None):
    '''rad_cmd=Radiance commande name string, args=list of parameters
    stdin=standard input. Returns a python CompletedProcess object'''
    out = subprocess.run([rad_cmd] + args, stdin=stdin, stdout=subprocess.PIPE)
    return out


def _stdout_to_file(stdout, file_name):
    '''Writes stdout of a subprocess to a file.'''
    # note: newline='\n' so the writen file is unix-readable LF
    with open(file_name , 'w', newline='\n', encoding='UTF-8') as f:
        f.write(stdout.decode(encoding='UTF-8'))


def obj2rad(obj_file, output_rad_file, custom_args=None):
    '''Converts an obj file to a rad file.'''
    rad_cmd = 'obj2rad'
    if custom_args is not None:
        args = custom_args
    else:
        args = ['-f', obj_file]
    output = _run_command(rad_cmd, args, stdin=None)
    if output_rad_file is not None:
        _stdout_to_file(stdout=output.stdout, file_name=output_rad_file)
    else:
        return output.stdout


def oconv(mat_rad_file, geo_rad_file, output_file=None, custom_args=None,
          stdin=None):
    '''Returns the stdout of oconv. Optionally custom arguments can be used
    instead of the predefined material and geometry rad files. If output_file
    is specified, instead of returning it as a python object, the standard
    output will be written to a file.'''
    rad_cmd = 'oconv'
    if custom_args is not None:
        args = custom_args
    else:
        args = [mat_rad_file, geo_rad_file]
    output = _run_command(rad_cmd, args, stdin)
    if output_file is not None:
        with open(output_file , 'wb') as f:
            f.write(output.stdout)
    else:
        return output.stdout


def write_skyglow(file_name, m=1):
    '''Writes a receiver surface rad file as described in:
    "Subramaniam, S., 2017. Daylighting Simulations with Radiance using
    Matrix-based Methods". file_name=name of .rad file to write, m=controls the
    further division of the sky. The basis is the Reinhart
    sky division. It works the same way as MF in radiance: m=1 gives
    the Reinhart sky with 145 sky-patches (the middle of sky segment 1 points
    to 360 degs (North), sky segment 2 is the one next to it in the
    counter-clockwise direction); m=2 divides each
    skypatch to 4 smaller skypatches except for the top one and results in 577
    sky-patches. m=4 results in 2305 sky-patches etc.'''
    with open(file_name , 'w', newline='\n') as f:
        f.write('#@rfluxmtx u=+Y h=u\n')
        f.write('void glow groundglow\n')
        for i in range(2): f.write('0\n')
        f.write('4 1 1 1 0\n')
        f.write('\n')
        f.write('groundglow source ground\n')
        for i in range(2): f.write('0\n')
        f.write('4 0 0 -1 180\n')
        f.write('\n')
        f.write('#@rfluxmtx u=+Y h=r{}\n'.format(m))
        f.write('void glow skyglow\n')
        for i in range(2): f.write('0\n')
        f.write('4 1 1 1 0\n')
        f.write('\n')
        f.write('skyglow source skydome\n')
        for i in range(2): f.write('0\n')
        f.write('4 0 0 1 180\n')


def rfluxmtx(skyglow_file, sp_file, oct_file, lw=0.00001, ab=2, ad=10000,
             n=4, output_file=None, custom_args=None):
    '''Returns the stdout of rfluxmtx. skyglow_file = skyglow.rad file e.g.
    made with the write_skyglow function, sp_file = sensor point file
    containing the  x, y, z, xi, yi, zi, coordinates of the sensorpoints,
    oct_file = octree file made e.g. with the oconv function,
    lw = radiance lw parameter (it is recommended to use lw = (1)/(ad*10),
    ab = radiance ab parameter, ad = radiance ad parameter, n = number of cpu
    cores to use. <-- When these parameters are used, the rfluxmtx is set up to
    provide daylight coefficients as described in "Subramaniam, S., 2017.
    Daylighting Simulations with Radiance using Matrix-based Methods" in
    section 6.1.1.1. This way DC-s are calculated for sensor points as
    "senders". Optionally, for a more general use of rfluxmtx, custom_args can
    be used instead of the predefined ones. In that case all arguments should
    be provided as a list of strings. If output_file is specified, instead of
    returning it as a python object, the standard output will be written to a
    file.'''
    rad_cmd = 'rfluxmtx'
    if custom_args is not None:
        stdin = open(sp_file, 'r')
        args = custom_args
        output = _run_command(rad_cmd, args, stdin)
        stdin.close()
    else:
        with open(sp_file, 'r') as f:
            y = len(f.readlines())
        stdin = open(sp_file, 'r')
        args = ['-I+', '-y', str(y), '-lw', str(lw), '-ab', str(ab), '-ad',
                str(ad), '-n', str(n), '-', skyglow_file, '-i', oct_file]
        output = _run_command(rad_cmd, args, stdin)
        stdin.close()
    if output_file is not None:
        _stdout_to_file(stdout=output.stdout, file_name=output_file)
    else:
        return output.stdout


def epw2wea(epw_file, output_wea_file):
    '''Converts an epw weather file to a wea file.'''
    rad_cmd = 'epw2wea'
    args = [epw_file, output_wea_file]
    _run_command(rad_cmd, args, stdin=None)


def gendaymtx(wea_file, m, g_albedo=0.2, output_file=None, custom_args=None):
    '''Generates sky matrix from a wea file. wea_file = .wea file input,
    m = controls the further division of the sky. The basis is the Reinhart
    sky division. It works the same way as MF in radiance: m=1 gives
    the Reinhart sky with 145 sky-patches; m=2 divides each skypatch to 4 smaller skypatches
    except for the top one and results in 577 sky-patches. m=4 results in 2305
    sky-patches etc. g_albedo=ground albedo, 0 is black, 1 is white.
    output_file = output .smx file name. Optionally, for a more general use of
    rfluxmtx, custom_args can be used instead of the predefined ones. In that
    case all arguments should be provided as a list of strings. If output_file
    is specified, instead of returning it as a python object, the standard
    output will be written to a file.'''
    rad_cmd = 'gendaymtx'
    if custom_args is not None:
        args = custom_args
    else:
        args = ['-m', str(m), '-g', str(g_albedo), str(g_albedo),
                str(g_albedo), '-O1', wea_file]
    output = _run_command(rad_cmd, args, stdin=None)
    if output_file is not None:
        _stdout_to_file(stdout=output.stdout, file_name=output_file)
    else:
        return output.stdout


def calc_irradiance(dc_file, sky_mtx_file, output_file, cr=0.265, cg=0.670,
                    cb=0.065):
    '''This function pipes together dctimestep and rmtxop Radiance programs to
    calculate irradiance output from a sky matrix and daylight coefficients.
    dc_file = daylight coefficient file made with e.g. rfluxmtx function,
    sky_mtx_file = sky matrix made with e.g. gendaymtx function, output_file =
    file to write the irradiance results. cr=0.265, cg=0.670 and cb=0.065 are
    coefficients to convert the 3 RGB channels to solar irradiance.'''
    rad_cmd_dctimestep = 'dctimestep'
    args_dctimestep = [dc_file, sky_mtx_file]
    output_dctimestep = subprocess.Popen([rad_cmd_dctimestep] + args_dctimestep,
                                         stdout=subprocess.PIPE)
    rad_cmd_rmtxop = 'rmtxop'
    args_rmtxop = ['-fa', '-t', '-c', str(cr), str(cg), str(cb), '-']
    output_rmtxop = subprocess.Popen([rad_cmd_rmtxop] + args_rmtxop,
                                     stdin=output_dctimestep.stdout,
                                     stdout=subprocess.PIPE)
    output_dctimestep.stdout.close()
    output = output_rmtxop.communicate()[0]
    output_rmtxop.stdout.close()
    if output_file is not None:
        _stdout_to_file(stdout=output, file_name=output_file)
    else:
        return output
