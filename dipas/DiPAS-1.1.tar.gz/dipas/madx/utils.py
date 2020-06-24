"""Utilities for interfacing the MADX program and parsing MADX generated output files."""

from contextlib import nullcontext
import io
import itertools as it
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, Optional, Sequence, Tuple, Union
from typing_extensions import Literal
import warnings

import numpy as np
import pandas as pd

from .builder import write_attribute_assignment, write_command
from .parser import parse_file, Script


__all__ = ['run_file', 'run_script', 'run_orm', 'convert', 'convert_tfs', 'convert_trackone']

logger = logging.getLogger(__name__)

error_template = '''
------------------------------------------------------------

STDOUT
======

{stdout}

------------------------------------------------------------

STDERR
======

{stderr}

------------------------------------------------------------

'''


class MADXError(Exception):
    def __init__(self, script: str, stdout: str, stderr: str):
        super().__init__()
        self.script = script
        self.stdout = stdout
        self.stderr = stderr


# noinspection PyShadowingBuiltins
def run_script(script: str, results: Union[Sequence[str], Dict[str, bool]] = None,
               *, variables: Dict[str, Any] = None, format: Dict[str, Any] = None,
               parameters: Dict[str, Dict[str, Any]] = None,
               twiss: Union[Literal[True], Dict[str, Any]] = None, madx: str = None,
               wdir: Optional[str] = None) -> Dict:
    """Run the given MADX script through the MADX program.

    Parameters
    ----------
    script : str
        The MADX script to be run.
    results : list or dict, optional
        File names of generated output files that should be returned. The content of these files will be automatically
        converted based on the chosen filename. For TFS-style files this does not include the header meta data
        (prefixed by "@") by default. If the header meta data should be returned as well, a `dict` can be used,
        mapping file names to `bool` flags that indicate whether meta data for this file is requested or not.
        More generally one can also provide a dict per file name that represents the keyword arguments that will be
        passed to :func:`convert` for that particular file.
        One can also use a special syntax for requesting meta data or indicating a specific file type. The syntax for
        each file name is ``<file_name>+meta;<file_type>`` where ``+meta`` and ``;<file_type>`` are optional. For example
        ``example.tfs`` would be parsed as a TFS file without parsing meta data. Using ``example.tfs+meta`` also returns
        the meta data. Or ``example.tfs;raw`` would return the raw content of the file rather than parsing it.
        For more information about file types see :func:`convert`.
        If the `twiss` argument is given, and a file name is specified, then this will automatically be added to the
        `results` list (similar for ``twiss=True``).
    variables : dict, optional
        Used for replacing statements of the form ``key = old;`` with ``key = value;``.
    format : dict, optional
        Used for filling in format specifiers of the form ``%(key)s``.
    parameters : dict, optional
        Parameters of lattice elements. Keys should be element labels and values dicts that map attribute names to their
        values. These definitions will be inserted after the last sequence definition.
        For example ``{"qh1": {"k1": 0.1}}`` will be inserted as ``qh1->k1 = 0.1;``.
    twiss : True or dict, optional
        Parameters for the `TWISS` command. If this argument is given, then a `TWISS` command is appended at the end
        of the script. The dict keys should be parameter names, such as ``tolerance`` with corresponding values.
        The key ``"select"``, if present, should map to another dict that specifies the parameters for a preceding
        select statement. The ``flag = twiss`` parameter does not need to be specified as it will be added automatically.
        If the ``file`` parameter is specified, the file name does not need to be specified in `results`, it will be
        added automatically. If meta information of the resulting TWISS file is required, an additional ``'meta': True``
        entry in the `twiss` dict can be provided.
        If `True` then the `TWISS` command is run with MADX default parameters while saving to a file named "twiss". The
        corresponding data is returned together with the meta data. Thus specifying ``twiss=True`` is equivalent to
        ``twiss=dict(file='twiss', meta=True)``.
    madx : str, optional
        File name pointing to the MADX executable. If the `MADX` environment variable is set it takes precedence.
    wdir : str, optional
        The working directory in which the script will be run. Note that a file named "main.madx" will be created in
        that directory, overwriting any existing file with that name. If not specified then a temporary working directory
        is created.

    Returns
    -------
    output : dict
        Containing the stdout and stderr at keys "stdout" and "stderr" respectively as well as any output files
        specified in `results`, converted by :func:`convert`.

    Raises
    ------
    ValueError
        If the MADX executable cannot be resolved either via `madx` or the `MADX` environment variable.
    subprocess.CalledProcessError
        If the MADX executable returns a non-zero exit code.

    See Also
    --------
    :func:`convert` : Used for converting specified output files.
    """
    with tempfile.TemporaryDirectory() as td:
        script_name = 'main.madx'
        script_path = os.path.join(td, script_name)
        with open(script_path, 'w') as fh:
            fh.write(script)
        return run_file(script_path, results, variables=variables, format=format, parameters=parameters, twiss=twiss,
                        madx=madx, wdir=wdir)


# noinspection PyShadowingBuiltins
def run_file(scripts: Union[str, Sequence[str]], results: Union[Sequence[str], Dict[str, bool]] = None,
             *, variables: Dict[str, Any] = None, format: Dict[str, Any] = None, parameters: Dict[str, Any] = None,
             twiss: Dict[str, Any] = None, madx: str = None, wdir: Optional[str] = None) -> Dict:
    """Runs a single script or a bunch of dependent scripts, with optional configuration.

    The first script specified in `scripts` is considered the entry point and is passed to the MADX executable.
    Other scripts should be invoked implicitly via ``call, file = "...";``. If there is only a single script it can be
    used directly as the first argument.

    Parameters
    ----------
    scripts : str or list of str
        A single script or a list of MADX script file names. The first item is used as the entry point. Actually the
        list can contain any file names, relative to the current working directory. These files will be copied to the
        new, temporary working directory where the script will be run (regardless of whether they are used or not). For
        example one can include error definitions that way, which are then loaded in the main script. Note that files
        within the main script which are referred to via ``call, file = ...`` or ``readtable, file = ...`` are
        auto-discovered and appended to the list of required scripts (if not already present).
    results : list or dict, optional
        See :func:`run_script`.
    variables : dict, optional
        Variables configuration for each of the scripts in `scripts`. See :func:`run_script` for more details.
    format : dict, optional
        Format values for each of the scripts in `scripts`. See :func:`run_script` for more details.
    parameters : dict, optional
        Parameter definitions for each of the scripts in `scripts`. See :func:`run_script` for more details.
    twiss : dict, optional
        Twiss command specification for each of the scripts. See :func:`run_script` for more details.
    madx : str, optional
        See :func:`run_script`.
    wdir : str, optional
        The working directory in which the `scripts` will be run. Note that any existing files with similar names as the
        ones in `scripts` will be overwritten. If not specified then a temporary working directory is created.

    Returns
    -------
    output : dict
        Containing the stdout and stderr at keys "stdout" and "stderr" respectively as well as any output files
        specified in `results`, converted by :func:`convert`.

    Raises
    ------
    ValueError
        If the MADX executable cannot be resolved either via `madx` or the `MADX` environment variable.
    :class:`MADXError`
        If the MADX executable returns a non-zero exit code. The raised error has additional attributes `script`, which
        is the content of the script that caused the error, as well as `stdout` and `stderr` which contain the MADX output.
        The ``__cause__`` of that error is set to the original `subprocess.CalledProcessError`.

    See Also
    --------
    :func:`convert` : Used for converting specified output files.
    """
    if isinstance(scripts, (str, Path)):  # Special case for single file.
        scripts = [scripts]
        script_name = Path(scripts[0]).name
        if variables is not None:
            variables = {script_name: variables}
        if format is not None:
            format = {script_name: format}
        if parameters is not None:
            parameters = {script_name: parameters}
        if twiss is not None:
            twiss = {script_name: twiss}
    if results is None:
        results = {}
    if isinstance(results, dict):
        results = {k: {'meta': v} if isinstance(v, bool) else v for k, v in results.items()}
    else:
        re_matches = [re.match(r'([^+;]+)(\+meta)?(?:;([a-z]+))?', f) for f in results]
        if any(x is None for x in re_matches):
            raise ValueError(f'Invalid result specification: {results[re_matches.index(None)]!r}')
        results = {m.group(1): {'meta': bool(m.group(2)), 'f_type': m.group(3)} for m in re_matches}
    with open(scripts[0]) as fh:
        dependencies = [x[0].strip('"\'') for x in
                        re.findall(r'(?:call|readtable)[ \t]*,[ \t]*file[ \t]*:?=[ \t]*((["\']).+\2|[^\s,;]+)',
                                   fh.read())]
    scripts.extend(set(dependencies) - set(scripts[1:]))
    madx = os.getenv('MADX') or madx
    if madx is None or not os.path.isfile(madx):
        raise ValueError('Path to MADX executable must be provided as either "MADX" environment variable or '
                         'in form of the "madx" argument')
    if variables is None:
        variables = {}
    if format is None:
        format = {}
    if parameters is None:
        parameters = {}
    if twiss is None:
        twiss = {}
    with (tempfile.TemporaryDirectory() if wdir is None else nullcontext(wdir)) as td:
        for f_path in scripts:
            shutil.copy(f_path, td)
            name = Path(f_path).name
            if name in (variables.keys() | format.keys() | parameters.keys() | twiss.keys()):
                path = os.path.join(td, name)
                with open(path) as fh:
                    content = fh.read()
                for key, value in variables.get(name, {}).items():
                    content = re.sub(rf'(?<={key})\s*(:?=)\s*.*(?=;)', rf' \1 {value!s}', content)
                if name in format:
                    content = content % format[name]
                if name in parameters:
                    parts = re.split('(?<=endsequence;)', content, flags=re.IGNORECASE)
                    parts.insert(-1, '\n\n' + '\n'.join(write_attribute_assignment(label, attr, val)
                                                        for label, attrs in parameters[name].items()
                                                        for attr, val in attrs.items()) + '\n')
                    content = ''.join(parts)
                if name in twiss:
                    f_twiss = twiss[name]
                    if f_twiss is True:
                        f_twiss = dict(file='twiss', meta=True)
                    if 'file' in f_twiss:
                        f_twiss.update(save=True)
                        if f_twiss['file'] not in results:
                            results[f_twiss['file']] = dict(meta=f_twiss.pop('meta', False))
                    if 'select' in f_twiss:
                        f_twiss['select'].update(flag='twiss')
                        content += f'\n{write_command("select", f_twiss.pop("select"))};'
                    content += f'\n{write_command("twiss", f_twiss)};'
                with open(path, 'w') as fh:
                    fh.write(content)
        try:
            cp = subprocess.run([madx, os.path.split(scripts[0])[1]],
                                capture_output=True, cwd=td, text=True, check=True)
        except subprocess.CalledProcessError as err:
            with open(os.path.join(td, scripts[0])) as fh:
                script = fh.read()
            raise MADXError(script, err.stdout, err.stderr) from err
        res = {'stdout': cp.stdout, 'stderr': cp.stderr}
        warnings_list = [w.strip() for w in re.findall(r'^\+{6} warning: (.+?)$', cp.stdout, flags=re.MULTILINE)]
        if warnings_list:
            res['warnings'] = warnings_list
            warnings.warn(f'MADX issued the following warnings: {warnings_list}')
        for name, specs in results.items():
            res[name] = convert(os.path.join(td, name), **specs)
    return res


def run_orm(script: str, kickers: Sequence[str], monitors: Sequence[str], *,
            kicks: Tuple[float, float] = (-0.001, 0.001),
            variables: Optional[Dict[str, Any]] = None,
            parameters: Dict[str, Dict[str, Any]] = None,
            twiss_args: Optional[Dict[str, Any]] = None,
            madx: str = None) -> pd.DataFrame:
    """Compute the Orbit Response Matrix (ORM) for the given sequence script, kickers and monitors.

    Parameters
    ----------
    script : str
        Either the file name of the script or the script itself. The script must contain the beam and the sequence
        definition.
    kickers : list of str
        Kicker labels.
    monitors : list of str
        Monitor labels.
    kicks : 2-tuple of float
        The kick strengths to be used for measuring the orbit response.
    variables : dict
        See :func:`run_script`.
    parameters : dict
        See :func:`run_script`.
    twiss_args : dict
        Additional parameters for the `TWISS` command.
    madx : str
        See :func:`run_script`.

    Returns
    -------
    orm : pd.DataFrame
        Index == monitors, columns == kickers.
    """
    if os.path.exists(script):
        with open(script) as fh:
            script = fh.read()
    if twiss_args is None:
        twiss_args = {}
    twiss_args.update(save=True, file="twiss")
    script += (
        f'\n%(kicker)s->kick = %(kicker)s->kick + (%(kick)f);'
        f'\nselect, flag = twiss, column = name, s, x, y;'
        f'\n{write_command("twiss", twiss_args)};'
    )
    rows = []
    for label in kickers:
        orbit = []
        for kick in kicks:
            twiss = run_script(script, ['twiss'],
                               format={'kicker': label, 'kick': kick}, variables=variables,
                               parameters=parameters, madx=madx)['twiss']
            twiss['NAME'] = twiss['NAME'].str.lower()
            twiss.set_index('NAME', inplace=True)
            orbit.append(twiss.loc[monitors, ['X', 'Y']].values.astype(float).T.ravel())
        rows.append((orbit[1] - orbit[0]) / (kicks[1] - kicks[0]))
    return pd.DataFrame(data=np.transpose(rows), index=pd.MultiIndex.from_product([['X', 'Y'], monitors]), columns=kickers)


type_dict = {'s': str, 'd': int, 'le': float}


def convert(f_name: str, f_type: Optional[Literal['madx', 'raw', 'tfs', 'trackone']] = None, meta: bool = False) \
        -> Union[pd.DataFrame, str, Script, Tuple[pd.DataFrame, Dict[str, str]]]:
    """Convert MADX output file by automatically choosing the appropriate conversion method based on the file name.

    Parameters
    ----------
    f_name : str
        If ends with "one" then a ``TRACK, ONETABLE = true`` is assumed and a `pd.DataFrame` is returned. If suffix is
        one of `{".madx", ".seq"}` then a tuple according to `madx.parse_file` is returned. Otherwise a TFS file is
        assumed and converted to a `pd.DataFrame`. If this fails the raw string content is returned. Raw string content
        can also be enforced by using the suffix `".raw"`; this supersedes the other cases.
    f_type : str
        Determines how the file should be loaded. The following types can be used:
            * "madx" -- parses the file as a MADX script, using :func:`parse_file`.
            * "raw" -- loads the raw content of the file.
            * "tfs" -- parses the file as a TFS file, using :func:`convert_tfs`.
            * "trackone" -- parses the file as a TRACKONE file, using :func:`convert_trackone`.
    meta : bool
        Indicates whether TFS meta data (prefixed with "@") should be returned in form of a dict. This is only possible
        for `trackone` and `tfs` tables.

    Returns
    -------
    The return value depends on the choice of the file name (see `f_name`).
    """
    if f_type == 'raw' or f_type is None and Path(f_name).suffix == '.raw':
        with open(f_name) as fh:
            return fh.read()
    elif f_type == 'trackone' or f_type is None and Path(f_name).name.endswith('one'):
        return convert_trackone(f_name, meta)
    elif f_type == 'madx' or f_type is None and Path(f_name).suffix in {'.madx', '.seq'}:
        return parse_file(f_name)
    elif f_type == 'tfs':
        return convert_tfs(f_name, meta)
    else:
        try:
            return convert_tfs(f_name, meta)
        except ValueError:
            with open(f_name) as fh:
                return fh.read()


def convert_tfs(f_name: str, meta: bool = False) -> Union[pd.DataFrame, Tuple[pd.DataFrame, Dict[str, str]]]:
    """Convert table in TFS (Table File System) format to pandas data frame.

    Parameters
    ----------
    f_name : str
        File name pointing to the TFS file.
    meta : bool, optional
        If `True`, return meta information prefixed by "@ " in form of a `dict`.

    Returns
    -------
    df : pd.DataFrame
        The corresponding data frame. If `meta` is `True` then a tuple containing the data frame and
        the meta data in form of a `dict` is returned.

    Raises
    ------
    ValueError
        If the given table is incomplete or if it's not presented in TFS format.
    """
    with open(f_name) as fh:
        content = fh.readlines()

    csv_content = filter(lambda x: x and not x.startswith(('@', '#')), content)
    col_names_str = next(csv_content)
    col_types_str = next(csv_content)

    if not col_names_str.startswith('* '):
        raise ValueError('Column names not found (indicated by "* ")')
    if not col_types_str.startswith('$ '):
        raise ValueError('Column types not found (indicated by "$ ")')

    col_names = re.findall('[A-Z0-9_.]+', col_names_str)
    col_types = re.findall('%(s|d|le)', col_types_str)
    columns = {n: type_dict[t] for n, t in zip(col_names, col_types)}

    csv_content = map(_replace_characters, csv_content)
    csv_content = ','.join(col_names) + '\n' + '\n'.join(csv_content)

    df = pd.read_csv(io.StringIO(csv_content), index_col=None, dtype=columns)
    if meta:
        return df, dict(map(_parse_meta, it.takewhile(lambda x: x.startswith('@'), iter(content))))
    return df


def convert_trackone(f_name: str, meta: bool = False) -> Union[pd.DataFrame, Tuple[pd.DataFrame, Dict[str, str]]]:
    """Convert "trackone" table (generated by ``TRACK, onetable = true``) to pandas data frame.

    Parameters
    ----------
    f_name : str
        File name pointing to the "trackone" file.
    meta : bool, optional
        If `True`, return meta information prefixed by "@ " in form of a `dict`.

    Returns
    -------
    df : pd.DataFrame
        The corresponding data frame, augmented by two columns "PLACE" and "LABEL" indicating
        the observation places' *number* and *label* respectively. The columns
        `[LABEL, PLACE, NUMBER, TURN]` are set as the data frame's index.
        If `meta` is `True` then a tuple containing the data frame and the meta data in form of a `dict` is returned.

    Raises
    ------
    ValueError
        If the given table is incomplete or if it's not presented in TFS format.
    """
    df = convert_tfs(f_name, meta)
    if meta:
        df, meta_dict = df

    with open(f_name) as fh:
        content = fh.readlines()

    content = filter(lambda x: x and not x.startswith('@'), content)
    next(content)  # Column names.
    next(content)  # Column types.
    place_nrs = []
    place_labels = []
    nr, label = None, None
    for line in content:
        if line.startswith('#segment'):
            __, nr, __, __, __, label = _replace_characters(line).split(',')
            continue
        place_nrs.append(nr)
        place_labels.append(label)

    df = df.assign(PLACE=pd.Series(map(int, place_nrs), index=df.index),
                   LABEL=pd.Series(place_labels, index=df.index))
    df.set_index(['LABEL', 'PLACE', 'NUMBER', 'TURN'], inplace=True)
    if meta:
        # noinspection PyUnboundLocalVariable
        return df, meta_dict
    return df


def _parse_meta(x: str) -> Tuple[str, Any]:
    """Parses one line of an output file's meta section and returns the result as a key, value pair (type converted)."""
    m = re.match(r'^@ ([A-Z0-9_.]+)\s+%(\d{2,})?(s|le)\s+(.+)$', x)
    key, __, dtype, value = m.groups()
    if dtype == 's':
        value = value.strip('"')
    return key, type_dict[dtype](value)


def _replace_characters(s: str) -> str:
    s = re.sub(r'^\s+', '', s)
    s = re.sub(r'\s+$', '', s)
    s = re.sub(r'\s+', ',', s)
    return s
