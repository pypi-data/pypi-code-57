from fitsnap3.scrapers.scrape import Scraper
from fitsnap3.io.input import config
from fitsnap3.parallel_tools import pt
from fitsnap3.io.output import output
import numpy as np
from pandas import read_csv
from tqdm import tqdm
from random import shuffle
from os import path, listdir
import re
from _collections import defaultdict

UNPROCESSED_KEYS = ['uid']

PROPERTY_NAME_MAP = {'positions': 'pos',
                     'numbers': 'Z',
                     'charges': 'charge',
                     'symbols': 'species'}

REV_PROPERTY_NAME_MAP = dict(zip(PROPERTY_NAME_MAP.values(), PROPERTY_NAME_MAP.keys()))

all_properties = ['energy', 'forces', 'stress', 'stresses', 'dipole',
                  'charges', 'magmom', 'magmoms', 'free_energy', 'energies']


def key_val_str_to_dict(string, sep=None):
    """
    Parse an xyz properties string in a key=value and return a dict with
    various values parsed to native types.

    Accepts brackets or quotes to delimit values. Parses integers, floats
    booleans and arrays thereof. Arrays with 9 values are converted to 3x3
    arrays with Fortran ordering.

    If sep is None, string will split on whitespace, otherwise will split
    key value pairs with the given separator.

    """
    # store the closing delimiters to match opening ones
    delimiters = {
        "'": "'",
        '"': '"',
        '(': ')',
        '{': '}',
        '[': ']',
    }

    # Make pairs and process afterwards
    kv_pairs = [
        [[]]]  # List of characters for each entry, add a new list for new value
    delimiter_stack = []  # push and pop closing delimiters
    escaped = False  # add escaped sequences verbatim

    # parse character-by-character unless someone can do nested brackets
    # and escape sequences in a regex
    for char in string.strip():
        if escaped:  # bypass everything if escaped
            kv_pairs[-1][-1].extend(['\\', char])
            escaped = False
        elif delimiter_stack:  # inside brackets
            if char == delimiter_stack[-1]:  # find matching delimiter
                delimiter_stack.pop()
            elif char in delimiters:
                delimiter_stack.append(delimiters[char])  # nested brackets
            elif char == '\\':
                escaped = True  # so escaped quotes can be ignored
            else:
                kv_pairs[-1][-1].append(char)  # inside quotes, add verbatim
        elif char == '\\':
            escaped = True
        elif char in delimiters:
            delimiter_stack.append(delimiters[char])  # brackets or quotes
        elif (sep is None and char.isspace()) or char == sep:
            if kv_pairs == [[[]]]:  # empty, beginning of string
                continue
            elif kv_pairs[-1][-1] == []:
                continue
            else:
                kv_pairs.append([[]])
        elif char == '=':
            if kv_pairs[-1] == [[]]:
                del kv_pairs[-1]
            kv_pairs[-1].append([])  # value
        else:
            kv_pairs[-1][-1].append(char)

    kv_dict = {}

    for kv_pair in kv_pairs:
        if len(kv_pair) == 0:  # empty line
            continue
        elif len(kv_pair) == 1:  # default to True
            key, value = ''.join(kv_pair[0]), 'T'
        else:  # Smush anything else with kv-splitter '=' between them
            key, value = ''.join(kv_pair[0]), '='.join(
                ''.join(x) for x in kv_pair[1:])

        if key.lower() not in UNPROCESSED_KEYS:
            # Try to convert to (arrays of) floats, ints
            split_value = re.findall(r'[^\s,]+', value)
            try:
                try:
                    numvalue = np.array(split_value, dtype=int)
                except (ValueError, OverflowError):
                    # don't catch errors here so it falls through to bool
                    numvalue = np.array(split_value, dtype=float)
                if len(numvalue) == 1:
                    numvalue = numvalue[0]  # Only one number
                elif len(numvalue) == 9:
                    # special case: 3x3 matrix, fortran ordering
                    numvalue = np.array(numvalue).reshape((3, 3), order='F')
                value = numvalue
            except (ValueError, OverflowError):
                pass  # value is unchanged

            # Parse boolean values: 'T' -> True, 'F' -> False,
            #                       'T T F' -> [True, True, False]
            if isinstance(value, str):
                str_to_bool = {'T': True, 'F': False}

                try:
                    boolvalue = [str_to_bool[vpart] for vpart in
                                 re.findall(r'[^\s,]+', value)]
                    if len(boolvalue) == 1:
                        value = boolvalue[0]
                    else:
                        value = boolvalue
                except KeyError:
                    pass  # value is unchanged

        kv_dict[key] = value

    return kv_dict


def index2range(index, nsteps):
    """Method to convert a user given *index* option to a list of indices.

    Returns a range.
    """
    if isinstance(index, int):
        if index < 0:
            tmpsnp = nsteps + index
            trbl = range(tmpsnp, tmpsnp + 1, 1)
        else:
            trbl = range(index, index + 1, 1)
    elif isinstance(index, slice):
        start = index.start
        stop = index.stop
        step = index.step

        if start is None:
            start = 0
        elif start < 0:
            start = nsteps + start

        if step is None:
            step = 1

        if stop is None:
            stop = nsteps
        elif stop < 0:
            stop = nsteps + stop

        trbl = range(start, stop, step)
    else:
        raise RuntimeError("index2range handles integers and slices only.")
    return trbl


def read_xyz(fileobj, index=-1, properties_parser=key_val_str_to_dict):
    """
    Read from a file in Extended XYZ format

    index is the frame to read, default is last frame (index=-1).
    properties_parser is the parse to use when converting the properties line
    to a dictionary, ``extxyz.key_val_str_to_dict`` is the default and can
    deal with most use cases, ``extxyz.key_val_str_to_dict_regex`` is slightly
    faster but has fewer features.
    """
    if isinstance(fileobj, str):
        fileobj = open(fileobj)

    if not isinstance(index, int) and not isinstance(index, slice) and not isinstance(index, list):
        raise TypeError('Index argument is neither slice nor integer!')

    # If possible, build a partial index up to the last frame required
    last_frame = None
    if isinstance(index, int) and index >= 0:
        last_frame = index
    elif isinstance(index, slice):
        if index.stop is not None and index.stop >= 0:
            last_frame = index.stop

    # scan through file to find where the frames start
    fileobj.seek(0)
    frames = []
    while True:
        frame_pos = fileobj.tell()
        line = fileobj.readline()
        if line.strip() == '':
            break
        try:
            natoms = int(line)
        except ValueError:
            raise ValueError('xyz scraper: Expected xyz header but got: {}'.format(line))
        fileobj.readline()  # read comment line
        for i in range(natoms):
            fileobj.readline()
        # check for VEC
        nvec = 0
        while True:
            lastPos = fileobj.tell()
            line = fileobj.readline()
            if line.lstrip().startswith('VEC'):
                nvec += 1
                if nvec > 3:
                    raise IndexError('xyz scraper: More than 3 VECX entries')
            else:
                fileobj.seek(lastPos)
                break
        frames.append((frame_pos, natoms, nvec))
        if last_frame is not None and len(frames) > last_frame:
            break

    trbl = index2range(index, len(frames))

    for index in trbl:
        frame_pos, natoms, nvec = frames[index]
        fileobj.seek(frame_pos)
        # check for consistency with frame index table
        assert int(fileobj.readline()) == natoms
        yield _read_xyz_frame(fileobj, natoms, properties_parser, nvec)


def parse_properties(prop_str):
    """
    Parse extended XYZ properties format string

    Format is "[NAME:TYPE:NCOLS]...]", e.g. "species:S:1:pos:R:3".
    NAME is the name of the property.
    TYPE is one of R, I, S, L for real, integer, string and logical.
    NCOLS is number of columns for that property.
    """

    properties = {}
    properties_list = []
    dtypes = []
    converters = []

    fields = prop_str.split(':')

    def parse_bool(x):
        """
        Parse bool to string
        """
        return {'T': True, 'F': False,
                'True': True, 'False': False}.get(x)

    fmt_map = {'R': ('d', float),
               'I': ('i', int),
               'S': (object, str),
               'L': ('bool', parse_bool)}

    for name, ptype, cols in zip(fields[::3],
                                 fields[1::3],
                                 [int(x) for x in fields[2::3]]):
        if ptype not in ('R', 'I', 'S', 'L'):
            raise ValueError('Unknown property type: ' + ptype)
        ase_name = REV_PROPERTY_NAME_MAP.get(name, name)

        dtype, converter = fmt_map[ptype]
        if cols == 1:
            dtypes.append((name, dtype))
            converters.append(converter)
        else:
            for c in range(cols):
                dtypes.append((name + str(c), dtype))
                converters.append(converter)

        properties[name] = (ase_name, cols)
        properties_list.append(name)

    dtype = np.dtype(dtypes)
    return properties, properties_list, dtype, converters


def _read_xyz_frame(lines, natoms, properties_parser=key_val_str_to_dict, nvec=0):
    # comment line
    line = next(lines).strip()
    if nvec > 0:
        info = {'comment': line}
    else:
        info = properties_parser(line) if line else {}

    pbc = None
    if 'pbc' in info:
        pbc = info['pbc']
        del info['pbc']
    elif 'Lattice' in info:
        # default pbc for extxyz file containing Lattice
        # is True in all directions
        pbc = [True, True, True]
    elif nvec > 0:
        # cell information given as pseudo-Atoms
        pbc = [False, False, False]

    cell = None
    if 'Lattice' in info:
        # NB: ASE cell is transpose of extended XYZ lattice
        cell = info['Lattice'].T
        del info['Lattice']
    elif nvec > 0:
        # cell information given as pseudo-Atoms
        cell = np.zeros((3, 3))

    if 'Properties' not in info:
        # Default set of properties is atomic symbols and positions only
        info['Properties'] = 'species:S:1:pos:R:3'
    properties, names, dtype, convs = parse_properties(info['Properties'])
    del info['Properties']

    data = []
    for ln in range(natoms):
        try:
            line = next(lines)
        except StopIteration:
            raise StopIteration('xyz scraper: Frame has {} atoms, expected {}'.format(len(data), natoms))
        vals = line.split()
        row = tuple([conv(val) for conv, val in zip(convs, vals)])
        data.append(row)

    try:
        data = np.array(data, dtype)
    except TypeError:
        raise TypeError('Badly formatted data or end of file reached before end of frame')

    # Read VEC entries if present
    if nvec > 0:
        for ln in range(nvec):
            try:
                line = next(lines)
            except StopIteration:
                raise StopIteration('xyz scraper: Frame has {} cell vectors, expected {}'.format(len(cell), nvec))
            entry = line.split()

            if not entry[0].startswith('VEC'):
                raise ValueError('Expected cell vector, got {}'.format(entry[0]))
            try:
                n = int(entry[0][3:])
                if n != ln + 1:
                    raise ValueError('Expected VEC{}, got VEC{}'.format(ln + 1, n))
            except Exception as err:
                output.exception(err, 'Expected VEC{}, got VEC{}'.format(ln + 1, entry[0][3:]))

            cell[ln] = np.array([float(x) for x in entry[1:]])
            pbc[ln] = True
        if nvec != pbc.count(True):
            raise ValueError('Problem with number of cell vectors')
        pbc = tuple(pbc)

    arrays = {}
    for name in names:
        ase_name, cols = properties[name]
        if cols == 1:
            value = data[name]
        else:
            value = np.vstack([data[name + str(c)]
                               for c in range(cols)]).T
        arrays[ase_name] = value

    symbols = None
    if 'symbols' in arrays:
        symbols = [s.capitalize() for s in arrays['symbols']]
        del arrays['symbols']

    numbers = None
    duplicate_numbers = None
    if 'numbers' in arrays:
        if symbols is None:
            numbers = arrays['numbers']
        else:
            duplicate_numbers = arrays['numbers']
        del arrays['numbers']

    charges = None
    if 'charges' in arrays:
        charges = arrays['charges']
        del arrays['charges']

    positions = None
    if 'positions' in arrays:
        positions = arrays['positions']
        del arrays['positions']

    atoms = Atoms(symbols=symbols,
                  positions=positions,
                  numbers=numbers,
                  charges=charges,
                  cell=cell,
                  pbc=pbc,
                  info=info)

    # Read and set constraints
    if 'move_mask' in arrays:
        if properties['move_mask'][1] == 3:
            atoms.set_constraint(
                [FixCartesian(a, mask=arrays['move_mask'][a, :]) for a in range(natoms)])
        elif properties['move_mask'][1] == 1:
            atoms.set_constraint(FixAtoms(mask=~arrays['move_mask']))
        else:
            raise NotImplementedError('Not implemented constraint')
        del arrays['move_mask']

    for name, array in arrays.items():
        atoms.new_array(name, array)

    if duplicate_numbers is not None:
        atoms.set_atomic_numbers(duplicate_numbers)

    # Load results of previous calculations into SinglePointCalculator
    results = {}
    for key in list(atoms.info.keys()):
        if key in all_properties:
            results[key] = atoms.info[key]
            # special case for stress- convert to Voigt 6-element form
            if key.startswith('stress') and results[key].shape == (3, 3):
                stress = results[key]
                stress = np.array([stress[0, 0],
                                   stress[1, 1],
                                   stress[2, 2],
                                   stress[1, 2],
                                   stress[0, 2],
                                   stress[0, 1]])
                results[key] = stress
    for key in list(atoms.arrays.keys()):
        if key in all_properties:
            results[key] = atoms.arrays[key]
    if results != {}:
        calculator = SinglePointCalculator(atoms, **results)
        atoms.set_calculator(calculator)
    return atoms


class XYZ(Scraper):

    def __init__(self, name):
        super().__init__(name)
        self.style_vars = ['AtomType', 'Stress', 'Lattice', 'Energy', "Positions", "Forces"]
        self.array_vars = ['AtomTypes', 'Stress', 'Lattice', "Positions", "Forces"]
        if config.sections["REFERENCE"].atom_style == "spin":
            self.style_vars.append("Spins")
            self.array_vars.append("Spins")
        if config.sections["REFERENCE"].atom_style == "charge":
            self.style_vars.append("Charges")
            self.array_vars.append("Charges")
        self.styles = defaultdict(lambda: set())
        self.all_data = []
        self.style_info = {}

    def scrape_groups(self):
        self.group_types = {'name': str, 'size': float, 'eweight': float, 'fweight': float, 'vweight': float}
        group_names = [key for key in self.group_types]

        self.group_table = read_csv(config.sections["PATH"].group_file,
                                    delim_whitespace=True,
                                    comment='#',
                                    skip_blank_lines=True,
                                    names=group_names,
                                    index_col=False)

        # Remove blank lines ; skip_blank_lines doesn't seem to work.
        self.group_table = self.group_table.dropna()
        self.group_table.index = range(len(self.group_table.index))

        # Convert data types
        self.group_table = self.group_table.astype(dtype=dict(self.group_types))

        for group_info in tqdm(self.group_table.itertuples(),
                               desc="Groups",
                               position=0,
                               total=len(self.group_table),
                               disable=(not config.args.verbose),
                               ascii=True):
            group_name = group_info.name
            folder = path.join(config.sections["PATH"].datapath, group_name)
            folder_files = listdir(folder)
            for file_name in folder_files:
                if folder not in self.files:
                    self.files[folder] = []
                if "xyz" in file_name:
                    self.files[folder].append(folder + '/' + file_name)

            if len(self.files[folder]) > 1:
                raise IndexError("Too many xyz files in folder {}".format(folder))
            if len(self.files[folder]) < 1:
                raise IndexError("Too few xyz files in folder {}".format(folder))

            self.configs[folder] = np.arange(group_info.size, dtype="int").tolist()
            shuffle(self.configs[folder], pt.get_seed)
            if group_info.size < 1:
                if self.tests is None:
                    self.tests = {}
                nfiles = len(folder_files)
                nfiles_train = max(1, int(abs(group_info.size) * len(folder_files) - 0.5))
                output.screen(group_info.name, ": Gathering ", nfiles, " fitting on ", nfiles_train)
                self.tests[folder] = []
                for i in range(nfiles - nfiles_train):
                    self.tests[folder].append(self.configs[folder].pop())

    def scrape_configs(self):
        output.screen(self.files)
        for folder in self.files:
            filename = self.files[folder][0]
            with open(filename) as file:
                self.data['AtomNumbers'] = int(file.readline())

                self.data['Group'] = filename.split("/")[-2]
                self.data['File'] = filename.split("/")[-1]
                if self.group_table.isin([self.data['Group']]).any().any():
                    self.data['GroupIndex'] = \
                        self.group_table.name[self.group_table.name == self.data['Group']].index.tolist()[0]
                else:
                    raise IndexError("{} was not found in dataframe".format(self.data['Group']))

                output.screen(self.configs)
                pt.shared_arrays["number_of_atoms"].sliced_array[:self.gr] = self.data['AtomNumbers']
                self.data["QMLattice"] = self.data["Lattice"]
                del self.data["Lattice"]  # We will populate this with the lammps-normalized lattice.
                if "Label" in self.data:
                    del self.data["Label"]  # This comment line is not that useful to keep around.

                # possibly due to JSON, some configurations have integer energy values.
                if not isinstance(self.data["Energy"], float):
                    # pt.print(f"Warning: Configuration {all_index}
                    # ({group_name}/{fname_end}) gives energy as an integer")
                    self.data["Energy"] = float(self.data["Energy"])

                self._stress_conv(self.styles)
                self.data["Energy"] *= self.convert["Energy"]

                if hasattr(config.sections["ESHIFT"], 'eshift'):
                    for atom in self.data["AtomTypes"]:
                        self.data["Energy"] += config.sections["ESHIFT"].eshift[atom]

                self._rotate_coords()
                self._translate_coords()

                if self.group_table['eweight'][self.data['GroupIndex']] >= 0.0:
                    for wtype in ['eweight', 'fweight', 'vweight']:
                        self.data[wtype] = self.group_table[wtype][self.data['GroupIndex']]
                else:
                    self.data['eweight'] = np.exp(
                        (self.group_table['eweight'][self.data['GroupIndex']] - self.data["Energy"] /
                         float(natoms)) / (self.kb * float(config.sections["BISPECTRUM"].boltz)))
                    self.data['fweight'] = \
                        self.data['eweight'] * self.group_table['fweight'][self.data['GroupIndex']]
                    self.data['vweight'] = \
                        self.data['eweight'] * self.group_table['vweight'][self.data['GroupIndex']]

                self.all_data.append(self.data)

        for style_name, style_set in self.styles.items():
            assert len(style_set) == 1, "Multiple styles ({}) for {}".format(len(style_set), style_name)

        self.style_info = {k: v.pop() for k, v in self.styles.items()}

        return self.all_data
