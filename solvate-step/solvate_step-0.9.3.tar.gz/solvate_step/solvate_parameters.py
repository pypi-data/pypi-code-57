# -*- coding: utf-8 -*-
"""Control parameters for solvating the system using PACKMOL
"""

import logging
import seamm

logger = logging.getLogger(__name__)


class SolvateParameters(seamm.Parameters):
    """The control parameters for using Packmol to solvate the system
    """

    parameters = {
        "solvent": {
            "default": "water",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                'water',
            ),
            "format_string": "s",
            "description": "Solvate with:",
            "help_text": "Solvate the system with these molecules.",
        },
        # 'another structure'
        "water_model": {
            "default": "SPC",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                'SPC',
                'SPC/E',
                'TIP3P',
                'TIP4P'
            ),
            "format_string": "s",
            "description": "Model:",
            "help_text": "The water model to use.",
        },
        "make periodic": {
            "default": "yes",
            "kind": "boolean",
            "format_string": "s",
            "enumeration": (
                "no",
                "yes"
            ),
            "description": "Make into a periodic system",
            "help_text": (
                "Make the system into a periodic system  if it is not already."
            )
        },
        "adjust volume": {
            "default": "yes",
            "kind": "boolean",
            "format_string": "s",
            "enumeration": (
                "no",
                "yes"
            ),
            "description": "Adjust the volume",
            "help_text": (
                "Adjust the periodic cell as needed."
            )
        },
        "method": {
            "default": "making periodic",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "making periodic",
                "within a sphere of solvent"
            ),
            "format_string": "s",
            "description": "Solvate, ",
            "help_text": "Determine how to solvate the system.",
        },
        "submethod": {
            "default": "fixing the volume and filling to a density",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": (
                "fixing the volume and adding a given number of molecules",
                "fixing the volume and filling to a density",
                "with the density and number of molecules of solvent",
                "with the density and approximate number of atoms of solvent"
            ),
            "format_string": "s",
            "description": "",
            "help_text": "Determine how to solvate the system.",
        },
        "volume": {
            "default": 8.0,
            "kind": "float",
            "default_units": "nm^3",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "The volume of the cell:",
            "help_text": "The volume of the target cell."
        },
        "number of molecules": {
            "default": 100,
            "kind": "integer",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "d",
            "description": "Number of molecules:",
            "help_text": ("The number of solvent molecules.")
        },
        "approximate number of atoms": {
            "default": 2000,
            "kind": "integer",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "d",
            "description": "Approximate number of atoms:",
            "help_text":
                (
                    "The approximate number of atoms in the solvent. "
                    "This will be rounded to give entire molecules"
                )
        },
        "density": {
            "default": 1.0,
            "kind": "float",
            "default_units": "g/ml",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Density:",
            "help_text": ("The target density of the cell.")
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**SolvateParameters.parameters, **defaults},
            data=data
        )
