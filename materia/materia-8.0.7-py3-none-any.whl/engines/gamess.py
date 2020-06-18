from __future__ import annotations
from typing import Any, Dict, Iterable, Optional, Tuple, Union

import materia as mtr

__all__ = [
    "GAMESSBasis",
    "GAMESSContrl",
    "GAMESSDamp",
    "GAMESSDampGS",
    "GAMESSSCF",
    "GAMESSStone",
    "GAMESSStructure",
    "GAMESSSystem",
]


class GAMESSBasis:
    def __init__(
        self,
        gbasis: Optional[str] = None,
        ngauss: Optional[int] = None,
        npfunc: Optional[int] = None,
        ndfunc: Optional[int] = None,
        nffunc: Optional[int] = None,
        diffs: Optional[bool] = None,
        diffsp: Optional[bool] = None,
    ) -> None:
        self.gbasis = gbasis
        self.ngauss = ngauss
        self.npfunc = npfunc
        self.ndfunc = ndfunc
        self.nffunc = nffunc
        self.diffs = diffs
        self.diffsp = diffsp

    def _process(self, k: str, v: Any) -> Tuple[str, Any]:
        if isinstance(v, bool):
            return k, f".{str(v)}."
        return k, v

    def __str__(self) -> str:
        keywords = (self._process(k, v) for k, v in vars(self).items())
        return (
            " $basis\n"
            + " \n".join(f"{k}={v}" for k, v in keywords if v is not None)
            + "\n $end\n"
        )


class GAMESSContrl:
    def __init__(
        self,
        runtyp: Optional[str] = None,
        units: Optional[Union[str, mtr.Quantity]] = None,
        coord: Optional[str] = None,
        icut: Optional[int] = None,
        local: Optional[str] = None,
    ) -> None:
        self.runtyp = runtyp
        self.units = units
        self.coord = coord
        self.icut = icut
        self.local = local

    def _process(self, k: str, v: Any) -> Tuple[str, Any]:
        if k == "units" and isinstance(v, mtr.Quantity):
            if v == mtr.angstrom:
                return k, "angs"
            elif v == mtr.bohr:
                return k, "bohr"
            else:
                return k, None
        return k, v

    def __str__(self) -> str:
        keywords = (self._process(k, v) for k, v in vars(self).items())
        return (
            " $contrl\n"
            + " \n".join(f"{k}={v}" for k, v in keywords if v is not None)
            + "\n $end\n"
        )


class GAMESSDamp:
    def __init__(
        self,
        ifttyp: Optional[Union[int, Iterable[int]]] = None,
        iftfix: Optional[Union[int, Iterable[int]]] = None,
        thrsh: Optional[Union[float, mtr.Quantity]] = None,
    ) -> None:
        self.ifttyp = ifttyp
        self.iftfix = iftfix
        self.thrsh = thrsh

    def _process(self, k: str, v: Any) -> Tuple[str, Any]:
        if k in ("ifttyp", "iftfix"):
            try:
                return f"{k}(1)", ",".join(str(i) for i in v)
            except TypeError:
                return f"{k}(1)", v

        if k == "thrsh" and isinstance(v, mtr.Quantity):
            return k, v.convert(mtr.kcal / mtr.mol).value

        return k, v

    def __str__(self) -> str:
        keywords = (self._process(k, v) for k, v in vars(self).items())
        return (
            " $damp\n"
            + " \n".join(f"{k}={v}" for k, v in keywords if v is not None)
            + "\n $end\n"
        )


class GAMESSDampGS:
    def __init__(
        self,
        equate_symmetric_points: Optional[bool] = False,
        instructions: Optional[Iterable[str]] = None,
    ) -> None:
        self.equate_symmetric_points = equate_symmetric_points
        self.instructions = instructions or []

    def __str__(self) -> str:
        if self.equate_symmetric_points:
            raise NotImplementedError
        else:
            keywords = (self._process(k, v) for k, v in vars(self).items())
            return " $dampgs\n" + " \n".join(self.instructions) + "\n $end\n"


class GAMESSSCF:
    def __init__(
        self,
        soscf: Optional[bool] = None,
        diis: Optional[bool] = None,
        conv: Optional[float] = None,
    ) -> None:
        self.soscf = soscf
        self.diis = diis
        self.conv = conv

    def _process(self, k: str, v: Any) -> Tuple[str, Any]:
        if isinstance(v, bool):
            return k, f".{str(v)}."
        if k == "conv" and v is not None:
            return k, str(v).replace("e", "d")
        return k, v

    def __str__(self) -> str:
        keywords = (self._process(k, v) for k, v in vars(self).items())
        return (
            " $scf\n"
            + " \n".join(f"{k}={v}" for k, v in keywords if v is not None)
            + "\n $end\n"
        )


class GAMESSStone:
    def __init__(self, bigexp: Optional[int] = None) -> None:
        self.bigexp = bigexp

    def _process(self, k: str, v: Any) -> Tuple[str, Any]:
        return k, v

    def __str__(self) -> str:
        keywords = (self._process(k, v) for k, v in vars(self).items())
        return (
            " $stone\n"
            + " \n".join(f"{k}={v}" for k, v in keywords if v is not None)
            + "\n $end\n"
        )


class GAMESSStructure:
    def __init__(self, structure: mtr.Structure) -> None:
        self.structure = structure

    def __str__(self) -> str:
        return (
            " $data\n\nc1\n"
            + "\n".join(
                f"{a.atomic_symbol.lower()}{i+1} {float(a.Z)} "
                + "  ".join(str(p) for p in a.position.reshape(3,))
                for i, a in enumerate(self.structure.atoms)
            )
            + "\n $end"
        )


class GAMESSSystem:
    def __init__(
        self,
        mwords: Optional[int] = None,
        timlim: Optional[Union[float, mtr.Quantity]] = None,
    ) -> None:
        self.mwords = mwords
        self.timlim = timlim

    def _process(self, k: str, v: Any) -> Tuple[str, Any]:
        if k == "timlim" and isinstance(v, mtr.Quantity):
            return k, v.convert(mtr.minute).value

        return k, v

    def __str__(self) -> str:
        keywords = (self._process(k, v) for k, v in vars(self).items())
        return (
            " $system\n"
            + " \n".join(f"{k}={v}" for k, v in keywords if v is not None)
            + "\n $end\n"
        )
