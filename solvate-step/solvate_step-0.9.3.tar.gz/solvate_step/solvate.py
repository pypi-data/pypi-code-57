# -*- coding: utf-8 -*-

"""A step for solvating the system using Packmol"""

import logging
import math
import os.path
import pprint

import configargparse
import mendeleev

import seamm
from seamm import data
import seamm_util
from seamm_util import ureg, Q_, units_class  # noqa: F401
from seamm_util import pdbfile
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
from seamm_util.water_models import Water
import solvate_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('solvate')


class Solvate(seamm.Node):

    def __init__(self, flowchart=None, extension=None):
        """Setup the main Solvate step

        Keyword arguments:
        """

        logger.debug('Handling arguments in Solvate {}'.format(self))

        # Argument/config parsing
        self.parser = configargparse.ArgParser(
            auto_env_var_prefix='',
            default_config_files=[
                '/etc/seamm/packmol.ini',
                '/etc/seamm/solvate.ini',
                '/etc/seamm/seamm.ini',
                '~/.seamm/packmol.ini',
                '~/.seamm/solvate.ini',
                '~/.seamm/seamm.ini',
            ]
        )

        self.parser.add_argument(
            '--solvate-configfile',
            is_config_file=True,
            default=None,
            help='a configuration file to override others'
        )

        # Options for this plugin
        self.parser.add_argument(
            "--solvate-log-level",
            default=configargparse.SUPPRESS,
            choices=[
                'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            ],
            type=str.upper,
            help="the logging level for the Solvate step"
        )

        # Options for Solvate
        self.parser.add_argument(
            '--packmol-path',
            default='',
            help='the path to the PACKMOL executable'
        )

        self.options, self.unknown = self.parser.parse_known_args()

        # Set the logging level for this module if requested
        if 'solvate_log_level' in self.options:
            logger.setLevel(self.options.solvate_log_level)

        super().__init__(
            flowchart=flowchart, title='Solvate', extension=extension
        )

        self.parameters = solvate_step.SolvateParameters()

    @property
    def version(self):
        """The semantic version of this module.
        """
        return solvate_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return solvate_step.__git_revision__

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        if not P:
            P = self.parameters.values_to_dict()

        text = 'Solvate the system'
        if P['method'][0] == '$':
            text += (
                '. Depending on {method} either make it a periodic box or '
                'spherical droplet of'
            )
        elif P['method'] == 'making periodic':
            text += ' making it a periodic system filled with'
        elif P['method'] == 'within a sphere of solvent':
            text += ' within a spherical droplet of'
        else:
            raise RuntimeError(
                "Don't recognize the method {}".format(P['method'])
            )

        if P['solvent'] == 'water':
            text += ' water, using the {water_model} model.'
        else:
            text += ' molecules of {solvent}.'

        if P['submethod'][0] == '$':
            text += ' It will be created according to {submethod}.'
        elif P['submethod'] == (
            "fixing the volume and adding a given number of molecules"
        ):
            text += (
                ' The cell volume is fixed, with {number of molecules} '
                'solvent molecules added.'
            )
        elif P['submethod'] == ("fixing the volume and filling to a density"):
            text += (
                ' The cell volume is fixed and will be filled to a density '
                'of {density}.'
            )
        elif P['submethod'] == (
            "with the density and number of molecules of solvent"
        ):
            text += (
                ' The density is {density} with {number of molecules} '
                'solvent molecules.'
            )
        elif P['submethod'] == (
            "with the density and approximate number of atoms of solvent"
        ):
            text += (
                ' The density is {density} and solvent molecules with a total '
                'of approximately {approximate number of atoms} will be used.'
            )
        else:
            raise RuntimeError(
                "Don't recognize the submethod {}".format(P['submethod'])
            )

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def run(self):
        """Solvate the system usiing PACKMOL

        To run PACKMOL we need to specify either the size of the cell for
        periodic systems or the radius of the sphere for molecules, along
        with the number of solvent molecules to use.

        Since PACKMOL does not really handle periodic systems, we will
        pack the solvent in a smaller box that fits in the actual periodic
        cell to avoid overlaps at the cell boundaries.
        """

        next_node = super().run(printer)

        # The options from command line, config file ...
        o = self.options

        packmol_exe = os.path.join(o.packmol_path, 'packmol')

        seamm_util.check_executable(
            packmol_exe, key='--packmol-path', parser=self.parser
        )

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        method = P['method']
        submethod = P['submethod']
        logger.debug('   method = {}'.format(method))
        logger.debug('submethod = {}'.format(submethod))

        # Print what we are doing
        printer.important(__(self.description_text(P), indent=self.indent))

        # Check that there is a system and get its mass, etc.
        if data.structure is None:
            logger.error('Solvate: there is no system!')
            raise RuntimeError('Solvate: there is no system to solvate!')
        else:
            system = data.structure
            atoms = system['atoms']
            # Get the molecular weight
            elements = atoms['elements']
            mass = 0.0
            for element in elements:
                mass += mendeleev.element(element).mass
            system_mass = mass * ureg.g / ureg.mol
            system_mass.ito('kg')  # Mass per 'system', in kg
            # And center of box containing the molecule
            minx, miny, minz = atoms['coordinates'][0]
            maxx, maxy, maxz = atoms['coordinates'][0]
            for x, y, z in atoms['coordinates']:
                minx = x if x < minx else minx
                maxx = x if x > maxx else maxx
                miny = y if y < miny else miny
                maxy = y if y > maxy else maxy
                minz = z if z < minz else minz
                maxz = z if z > maxz else maxz
            cx = (minx + maxx) / 2
            cy = (miny + maxy) / 2
            cz = (minz + maxz) / 2

        # And the solvent molecule(s)
        if P['solvent'] == 'water':
            model = Water.create_model(P['water_model'])
            solvent_mass = model.mass * ureg.g / ureg.mol
            solvent_mass.ito('kg')  # Mass per solvent molecule, in kg
            n_solvent_atoms = 3
            solvent_pdb = model.pdb()
            solvent_system = model.system()
        else:
            raise NotImplementedError(
                'Solvents other than water not available yet.'
            )

        if method == "within a sphere of solvent":
            # Nonperiodic case
            raise NotImplementedError(
                'Solvating with a sphere of solvent not supported yet.'
            )
        else:
            # Periodic case
            if submethod == (
                "fixing the volume and adding a given number of molecules"
            ):
                if system['periodicity'] != 3:
                    raise RuntimeError('Solvate: the system is not periodic.')
                a, b, c, alpha, beta, gamma = system['cell']
                if alpha != 90 or beta != 90 or gamma != 90:
                    raise NotImplementedError(
                        'Solvate cannot handle non-orthorhombic cells yet'
                    )
                lx = a
                ly = b
                lz = c
                n_molecules = P['number of molecules']
            elif submethod == ("fixing the volume and filling to a density"):
                if system['periodicity'] != 3:
                    raise RuntimeError('Solvate: the system is not periodic.')
                a, b, c, alpha, beta, gamma = system['cell']
                if alpha != 90 or beta != 90 or gamma != 90:
                    raise NotImplementedError(
                        'Solvate cannot handle non-orthorhombic cells yet'
                    )
                lx = a
                ly = b
                lz = c

                density = P['density']
                volume = a * b * c * math.pow(ureg.m / 1.0e10, 3)
                target_mass = density * volume
                target_mass.ito('kg')
                n_molecules = int(
                    round((target_mass - system_mass) / solvent_mass)
                )
            elif submethod == (
                "with the density and number of molecules of solvent"
            ):
                density = P['density']
                n_molecules = P['number of molecules']

                mass = system_mass + n_molecules * solvent_mass
                volume = mass / density

                lx = math.pow(volume.to('Å^3').magnitude, 1 / 3)
                ly = lx
                lz = lx

                system['periodicity'] = 3
                system['cell'] = [lx, ly, lz, 90.0, 90.0, 90.0]
            elif submethod == (
                "with the density and approximate number of atoms of solvent"
            ):
                density = P['density']
                n_molecules = int(
                    round(P['approximate number of atoms'] / n_solvent_atoms)
                )

                mass = system_mass + n_molecules * solvent_mass
                volume = mass / density

                lx = math.pow(volume.to('Å^3').magnitude, 1 / 3)
                ly = lx
                lz = lx

                system['periodicity'] = 3
                system['cell'] = [lx, ly, lz, 90.0, 90.0, 90.0]
            else:
                raise RuntimeError(
                    "Don't recognize the submethod {}".format(submethod)
                )

        # gap = P['gap'].to('Å').magnitude
        gap = 2.0

        lxp = lx - gap / 2
        lyp = ly - gap / 2
        lzp = lz - gap / 2

        dx = (lx / 2) - cx
        dy = (ly / 2) - cy
        dz = (lz / 2) - cz

        lines = []
        lines.append('tolerance {}'.format(gap))
        lines.append('output solvate.pdb')
        lines.append('filetype pdb')
        lines.append('structure system.pdb')
        lines.append('  number 1')
        lines.append('  fixed {} {} {} 0.0 0.0 0.0'.format(dx, dy, dz))
        lines.append('end structure')
        lines.append('structure solvent.pdb')
        lines.append('  number {}'.format(n_molecules))
        lines.append(
            '  inside box {l0} {l0} {l0} {} {} {}'.format(
                lxp, lyp, lzp, l0=gap / 2
            )
        )
        lines.append('end structure')
        lines.append('')

        files = {
            'system.pdb': pdbfile.from_molssi(data.structure),
            'solvent.pdb': solvent_pdb,
            'input.inp': '\n'.join(lines)
        }

        for key, value in files.items():
            logger.debug(80 * '*')
            logger.debug('File: ' + key)
            logger.debug(80 * '*')
            logger.debug('\n' + value + '\n\n')

        local = seamm.ExecLocal()
        result = local.run(
            cmd=(packmol_exe + ' < input.inp'),
            shell=True,
            files=files,
            return_files=['solvate.pdb']
        )

        tmp_files = []
        for key, value in result.items():
            if key == 'files':
                tmp_files = value
            if key in tmp_files:
                logger.debug(80 * '*')
                logger.debug('File: ' + key)
                if value['exception'] is not None:
                    logger.debug('   Exception = ' + value['exception'])
                logger.debug(80 * '*')
                logger.debug('\n' + value['data'] + '\n\n')
            elif len(str(value)) < 100:
                logger.debug(key + ': ' + str(value))
            else:
                logger.debug(80 * '*')
                logger.debug('Result: ' + key)
                logger.debug(80 * '*')
                logger.debug('\n' + str(value) + '\n\n')

        # Parse the resulting PDB file
        new_structure = pdbfile.to_molssi(result['solvate.pdb']['data'])

        logger.debug('Coordinates for the solvated system:')
        for x, y, z in new_structure['atoms']['coordinates']:
            logger.debug('{:9.4f} {:9.4f} {:9.4f}'.format(x, y, z))

        # Packmol just gives back atoms and coordinates, so we need to
        # build out the system with added solvent molecules and then
        # replace the coordinates with the new coordinates

        solvent_atoms = solvent_system['atoms']
        for molecule_id in range(n_molecules):
            first_atom = len(atoms['elements'])
            for key in atoms:
                if key in solvent_atoms:
                    if key == 'atom_types' or key == 'charges':
                        types = atoms[key]
                        solvent_types = solvent_atoms[key]
                        for type_ in types:
                            if type_ in solvent_types:
                                types[type_].extend(solvent_types[type_])
                            elif '*' in solvent_types:
                                types[type_].extend(solvent_types['*'])
                    else:
                        atoms[key].extend(solvent_atoms[key])
                else:
                    logger.warning(key + 'not in solvent_system.atoms')
                    for i in range(n_solvent_atoms):
                        atoms[key].append('')
            for i, j, order in solvent_system['bonds']:
                system['bonds'].append([first_atom + i, first_atom + j, order])

        # And the new coordinates
        atoms['coordinates'] = new_structure['atoms']['coordinates']

        string = 'Solvated the system with {nmol} solvent molecules.'
        if system['periodicity'] == 3:
            string += ' The periodic cell is {lx:.2f}x{ly:.2f}x{lz:.2f}'
            string += ' with a density of {density:.5~P}.'
        printer.important(
            __(
                string,
                indent='    ',
                lx=lx,
                ly=ly,
                lz=lz,
                nmol=n_molecules,
                density=density
            )
        )
        printer.important('')

        logger.log(
            0, 'Structure created by Packmol:\n\n' +
            pprint.pformat(data.structure)
        )

        return next_node
