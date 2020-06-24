from collections import defaultdict
import io
import re
from typing import Iterator, List, Tuple

import numpy as np
import pandas as pd
import pint


__all__ = ['Paramodi']


class Paramodi:
    column_names = ['device', 'attribute', 'purpose', 'value', 'unit', 'parameter_name', 'original_value']

    @classmethod
    def parse(cls, f_name_or_text: str) -> pd.DataFrame:
        """Parse the given paramodi file and return the data as a pandas data frame.

        The resulting data frame has the following columns::

            device, attribute, purpose, value, unit, parameter_name, original_value

        where `device` and `attribute` are the original parameter name split at the first forward slash (``/``).
        `parameter_name` and `original_value` are the original representations of the parameter name and the parameter value.
        The first three columns serve as an index of the data frame.

        Parameters
        ----------
        f_name_or_text : str
            File name pointing to the paramodi file or the content of such a file.

        Returns
        -------
        Data frame with the above described properties.
        """
        content = f_name_or_text.splitlines()
        if len(content) == 1:
            with open(content[0]) as fh:
                content = fh.readlines()
        content = '\n'.join(';'.join(x) for line in content if not line.startswith('#') for x in cls.parse_line(line.strip()))
        df = pd.read_csv(io.StringIO(content), header=None, names=cls.column_names, sep=';', dtype=str)
        df.set_index(cls.column_names[:3], inplace=True)
        values = df.groupby(level=[0, 1, 2])['value'].apply(list).map(lambda x: x[0] if len(x) == 1 else x).values
        df = df.groupby(level=[0, 1, 2]).first()
        df['value'] = values
        return df

    @classmethod
    def parse_line(cls, line: str) -> Iterator[Tuple[str]]:
        """Parse the given line into the required column values."""
        name, value, unit, purpose = re.findall(r'(?:\[.+\]|[^,])+', line)
        device, attribute = name.split('/', 1)
        original_value = value
        if value.startswith('['):
            values = [x.strip() for x in value.lstrip('[').rstrip(']').split(',')]
        else:
            values = [value]
        for value in values:
            yield device.lower(), attribute.lower(), purpose.lower(), value, unit, name, original_value

    @classmethod
    def apply_units(cls, paramodi: pd.DataFrame) -> List[Tuple]:
        """Apply the specified units to the specified values.

        If either the value is NaN or the unit is not available (``---``) the original value is used otherwise a
        corresponding quantity is computed. This uses the ``pint`` package for assigning the units.

        Parameters
        ----------
        paramodi : pd.DataFrame
            Such as from :meth:`parse`.

        Returns
        -------
        quantities : list of (index, pint.Quantity)
            A list containing the indices and quantities wherever applicable and the original values otherwise for each
            row of the `paramodi` data frame.
        """
        ur = pint.UnitRegistry()
        return [(i, float(v) * getattr(ur, u) if (not (isinstance(v, float) and np.isnan(v)) and u != '---') else v)
                for i, v, u in zip(paramodi.index, paramodi['value'], paramodi['unit'])]

    @classmethod
    def update_madx_device_data(cls, devices: pd.DataFrame, paramodi: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """Update the given MADX device data with values from the paramodi data.

        This applies the following conversions:

        * **[SBend]**
          * ``angle`` is incremented by ``HKICK`` from the paramodi data.
        * **[Quadrupole]**
          * ``k1`` is replaced by ``KL / q.L`` where ``KL`` is from the paramodi data.
        * **[HKicker, VKicker]**
          * ``kick`` is replaced by ``HKICK`` and ``VKICK`` respectively.

        Parameters
        ----------
        devices : pd.DataFrame
            Data frame containing the MADX device data. Indices should be device labels and match those in the first
            index level of the `paramodi` data frame. Columns should be device attributes (NaN where no such attribute
            is applicable). There must be a ``"type"`` column which indicates the device type as MADX command keyword
            (e.g. "quadrupole" or "sbend").
        paramodi : pd.DataFrame
            Structure according to :meth:`parse`.

        Returns
        -------
        updated_devices : pd.DataFrame
            Data frame similar to `devices` with the relevant columns updated according to the above rules.
        updates : dict
            A dict containing the applied updates. Keys are element labels and values are dicts that map parameter
            names to their *new* (updated) value.
        """
        paramodi = paramodi.groupby(level=(0, 1)).first()
        devices = devices.to_dict(orient='index')
        updates = defaultdict(dict)
        for label, device in devices.items():
            if device['type'].lower() == 'quadrupole':
                try:
                    new_value = float(paramodi.loc[(label, 'kl'), 'value']) / device['l']
                except KeyError:
                    continue
                else:
                    device['k1'] = updates[label]['k1'] = new_value
            elif device['type'].lower() in {'sbend', 'rbend'}:
                try:
                    kick = float(paramodi.loc[(label, 'hkick'), 'value'])
                except KeyError:
                    continue
                else:
                    device['angle'] = updates[label]['angle'] = device.get('angle', 0.) + kick
                    device['dk0'] = updates[label]['dk0'] = device.get('dk0', 0.) + kick / device['l']
            elif device['type'].lower() in {'hkicker', 'vkicker'}:
                try:
                    new_value = float(paramodi.loc[(label, device['type'][:-2]), 'value'])
                except KeyError:
                    continue
                else:
                    device['kick'] = updates[label]['kick'] = new_value
        return pd.DataFrame.from_dict(devices, orient='index'), dict(updates)
