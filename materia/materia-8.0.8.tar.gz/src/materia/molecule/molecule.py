from __future__ import annotations
from typing import Any

import materia as mtr
import pickle
import rdkit, rdkit.Chem

__all__ = ["Molecule"]


def first(flist, default=None):
    """ Try each function in `flist` until one does not throw an exception, and
    return the return value of that function. If all functions throw exceptions,
    return `default` 

    Args: 
        flist - list of functions to try
        default - value to return if all functions fail

    Returns:
        return value of first function that does not throw exception, or
        `default` if all throw exceptions.

    TODO: Also accept a list of (f, (exceptions)) tuples, where f is the
    function as above and (exceptions) is a tuple of exceptions that f should
    expect. This allows you to still re-raise unexpected exceptions.
    """
    # from https://stackoverflow.com/a/13874877

    for f in flist:
        try:
            return f()
        except:
            continue
    else:
        return default


class Molecule:
    def __init__(self, structure) -> None:
        super().__setattr__("properties", {})
        if isinstance(structure, mtr.Structure):
            self.structure = structure
        elif isinstance(structure, str):
            self.structure = first(
                [
                    lambda: mtr.Structure.read(structure),
                    lambda: mtr.Structure.generate(smiles=structure),
                    lambda: mtr.Structure.retrieve(name=structure),
                ]
            )

        self.charge = rdkit.Chem.GetFormalCharge(self.structure.to_rdkit())
        self.multiplicity = (sum(self.structure.atomic_numbers) + self.charge) % 2 + 1

    def _from_file(self, structure):
        try:
            return mtr.Structure.read
        except:
            return False

    def save(self, filepath: str) -> None:
        """
        Pickle molecule to a given save file.

        Args:
            filepath: Path to file in which the molecule will be pickled. Can be an absolute or a relative path.
        """
        with open(mtr.expand(filepath), "wb") as f:
            pickle.dump(obj=self, file=f)

    @staticmethod
    def load(filepath: str) -> Molecule:
        """
        Load molecule from a pickle file.

        Args:
            filepath: Path to pickle file from which the molecule will be loaded. Can be an absolute or a relative path.

        Returns:
            Molecule retrieved from pickle file.

        """
        with open(mtr.expand(filepath), "rb") as f:
            mol = pickle.load(file=f)

        return mol

    def __getattr__(self, name: str) -> Any:
        if name == "properties":
            return self.properties
        try:
            return super().__getattribute__("properties")[name]
        except KeyError:
            return getattr(self.structure, name)

    def __setattr__(self, name: str, value) -> None:
        self.properties[name] = value
