"""
Input and output from netCDF-SCM's netCDF format
"""
import os.path
import warnings

import pymagicc.io

from .definitions import (
    _SCM_TIMESERIES_META_COLUMNS,
    NAME_COMPONENTS_SEPARATOR,
    OUTPUT_PREFIX,
)
from .iris_cube_wrappers import (
    CMIP6Input4MIPsCube,
    CMIP6OutputCube,
    MarbleCMIP5Cube,
    ScmCube,
)

try:
    import iris
except ModuleNotFoundError:  # pragma: no cover # emergency valve
    from .errors import raise_no_iris_warning

    raise_no_iris_warning()


_ALL_AVAILABLE_CUBES = {
    "Scm": ScmCube,
    "MarbleCMIP5": MarbleCMIP5Cube,
    "CMIP6Input4MIPs": CMIP6Input4MIPsCube,
    "CMIP6Output": CMIP6OutputCube,
}


def save_netcdf_scm_nc(cubes, out_path):
    """
    Save a series of cubes to a `.nc` file

    Parameters
    ----------
    cubes : dict
        Dictionary of "region name"-:obj:`ScmCube` key-value pairs. The cubes will all
        be saved in the same ``.nc`` file.

    out_path : str
        Path in which to save the data
    """
    save_cubes = []
    for scm_cube in cubes.values():
        cube = scm_cube.cube
        save_cubes.append(cube)

    iris.save(save_cubes, out_path, local_keys=_SCM_TIMESERIES_META_COLUMNS)


def load_scmdataframe(path):
    """
    Load an scmdataframe from a netCDF-SCM ``.nc`` file

    Parameters
    ----------
    path : str
        Path from which to load the data

    Returns
    -------
    :obj:`ScmDataFrame`
        :obj:`ScmDataFrame` containing the data in ``path``.
    """
    helper, scm_cubes = _load_helper_and_scm_cubes(path)
    scmdf = helper.convert_scm_timeseries_cubes_to_openscmdata(scm_cubes)

    # TODO: decide whether assuming point data is a good idea or not
    return scmdf


def _load_helper_and_scm_cubes(path):
    cube_list = iris.load(path)

    loaded = ScmCube()
    scm_cubes = {}
    for v in cube_list:
        region = v.attributes["region"]
        scm_cubes[region] = ScmCube()
        scm_cubes[region].cube = v

    # take any cube as base for now, not sure how to really handle this so will
    # leave like this for now and only make this method public when I work it
    # out...
    loaded.cube = cube_list[0]

    return loaded, scm_cubes


def get_scmcube_helper(drs):
    """
    Get ScmCube helper for a given data reference syntax

    Paramters
    ---------
    drs : str
        Data reference syntax to get the helper cube for

    Returns
    -------
    :obj:`netcdf_scm.iris_cube_wrappers.ScmCube`
        Instance of sub-class of :obj:`netcdf_scm.iris_cube_wrappers.ScmCube`
        which matches the input data reference syntax

    Raises
    ------
    NotImplementedError
        ``drs`` is equal to ``"None"``

    KeyError
        ``drs`` is unrecognised
    """
    if drs == "None":
        raise NotImplementedError(
            "`drs` == 'None' is not supported yet. Please raise an issue at "
            "gitlab.com/netcdf-scm/netcdf-scm/ with your use case if you need this "
            "feature."
        )

    try:
        return _ALL_AVAILABLE_CUBES[drs]()
    except KeyError:
        raise KeyError("Unrecognised drs: {}".format(drs))


def load_mag_file(infile, drs):
    """
    Load ``.MAG`` file with automatic infilling of metadata if possible

    Parameters
    ----------
    infile : str
        File to load (use the full path for best results as this is used to
        determine the metadata)

    drs : str
        Data reference syntax to use with this file

    Returns
    -------
    :obj:`pymagicc.io.MAGICCData`
        :obj:`pymagicc.io.MAGICCData` with the data and metadata contained in
        the file.

    Warns
    -----
    UserWarning
        Some or all of the metadata couldn't be determined from ``infile``
        with the given ``drs``.
    """
    out = pymagicc.io.MAGICCData(infile)

    helper = get_scmcube_helper(drs)

    path_worked = False
    name_worked = False
    try:
        path_bits = helper.process_path(os.path.dirname(infile))
        path_worked = True

    except ValueError as e:
        warnings.warn(
            "Couldn't determine cube metadata from path with the drs '{}'.\n"
            "Error: '{}'".format(drs, e)
        )

        fname_to_check = os.path.basename(infile).replace(
            "{}{}".format(OUTPUT_PREFIX, NAME_COMPONENTS_SEPARATOR), ""
        )
        try:
            name_bits = helper.process_filename(fname_to_check)
            name_worked = True
        except ValueError as e:
            warnings.warn(
                "Couldn't determine cube metadata from filename either with "
                "the drs '{}'.\nError: '{}'".format(drs, e)
            )

    if path_worked:
        for scm_name, cmip_name in helper._scm_timeseries_id_map.items():
            try:
                out.set_meta(path_bits["{}".format(cmip_name)], scm_name)
            except KeyError:
                out.set_meta(getattr(helper, cmip_name), scm_name)

    elif name_worked:
        for scm_name, cmip_name in helper._scm_timeseries_id_map.items():
            try:
                out.set_meta(name_bits["{}".format(cmip_name)], scm_name)
            except KeyError:
                warnings.warn(
                    "Can't set metadata for '{}' from filename alone with the "
                    "drs '{}'.".format(scm_name, drs)
                )

    return out
