# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import AbstractSet, Optional, Set

import re
from collections import namedtuple

flag_re = r"[A-Za-z0-9][A-Za-z0-9+_-]*"
useflag_re = re.compile(r"^" + flag_re + r"$")
usedep_re = (
    r"(?P<prefix>[!-]?)(?P<flag>"
    + flag_re
    + r")(?P<default>(\(\+\)|\(\-\))?)(?P<suffix>[?=]?)"
)
_usedep_re = re.compile("^" + usedep_re + "$")

op_re = r"(?P<B>(!!))?(?P<OP>([<>]=?|[<>=~]))?"
cat_re = r"((?P<C>[A-Za-z0-9][A-Za-z0-9\-]*)/)?"
ver_re = r"(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*)"
rev_re = r"(-(?P<MR>r[0-9]+))?"
repo_re = r"(::(?P<R>[A-Za-z0-9_][A-Za-z0-9_-]*(::installed)?))?"
_atom_re = re.compile(
    op_re
    + cat_re
    + r"(?P<M>(?P<MN>[A-Za-z0-9+_-]+?)(-(?P<MV>"
    + ver_re
    + r"))?)"
    + rev_re
    + repo_re
    + r"(\[(?P<USE>.*)\])?$"
)


class InvalidAtom(Exception):
    "Exception indicating an atom has invalid syntax"


class UnqualifiedAtom(Exception):
    """
    Exception indicating an atom, which was expected to be
    qualified with a category, has no category
    """

    def __init__(self, atom):
        self.atom = atom

    def __str__(self):
        return f"Atom {self.atom} was expected to have a category!"


class Atom(str):
    CM: Optional[str]
    CMN: Optional[str]
    USE: Set[str] = set()
    M: str
    MN: str
    MF: str
    MV: Optional[str]
    MR: Optional[str]
    C: Optional[str]
    R: Optional[str]
    OP: Optional[str]
    BLOCK: bool
    MVR: Optional[str]
    CMF: str

    def __init__(self, atom: str):
        match = _atom_re.match(atom)
        if not match:
            raise InvalidAtom("Invalid atom %s. Cannot parse" % (atom))

        if match.group("M") and match.group("C"):
            self.CM = match.group("C") + "/" + match.group("M")
            self.CMN = match.group("C") + "/" + match.group("MN")
        else:
            self.CM = None
            self.CMN = None

        if match.group("USE"):
            self.USE = set(match.group("USE").split(","))
            for x in self.USE:
                m = _usedep_re.match(x)
                if not m:
                    raise InvalidAtom(
                        "Invalid use dependency {} in atom {}".format(atom, x)
                    )

        if match.group("MR"):
            self.MF = match.group("M") + "-" + match.group("MR")
        else:
            self.MF = match.group("M")

        self.M = match.group("M")
        self.MN = match.group("MN")
        self.MV = match.group("MV")
        self.MR = match.group("MR")
        self.C = match.group("C")
        self.R = match.group("R")
        self.OP = match.group("OP")
        self.BLOCK = match.group("B") is not None
        self.MVR = self.MV
        if self.MR:
            self.MVR += "-" + self.MR

        if self.C:
            self.CMF = self.C + "/" + self.MF
        else:
            self.CMF = self.MF

        if self.OP is not None and self.MV is None:
            raise InvalidAtom(
                "Atom %s has a comparison operator but no version!" % (atom)
            )

    def evaluate_conditionals(self, use: AbstractSet[str]) -> "Atom":
        """
        Create an atom instance with any USE conditionals evaluated.
        @param use: The set of enabled USE flags
        @return: an atom instance with any USE conditionals evaluated
        """
        tokens = set()

        for x in self.USE:
            m = _usedep_re.match(x)

            if m is not None:
                operator = m.group("prefix") + m.group("suffix")
                flag = m.group("flag")
                default = m.group("default")
                if default is None:
                    default = ""

                if operator == "?":
                    if flag in use:
                        tokens.add(flag + default)
                elif operator == "=":
                    if flag in use:
                        tokens.add(flag + default)
                    else:
                        tokens.add("-" + flag + default)
                elif operator == "!=":
                    if flag in use:
                        tokens.add("-" + flag + default)
                    else:
                        tokens.add(flag + default)
                elif operator == "!?":
                    if flag not in use:
                        tokens.add("-" + flag + default)
                else:
                    tokens.add(x)
            else:
                raise Exception("Internal Error when processing atom conditionals")

        atom = Atom(self)
        atom.USE = tokens
        return atom

    def strip_use(self) -> "Atom":
        """Returns the equivalent of this atom with the USE dependencies removed"""
        return Atom(re.sub(r"\[.*\]", "", str(self)))


class QualifiedAtom(Atom):
    """Atoms that include categories"""

    CM: str
    CMN: str
    CMF: str
    C: str

    def __init__(self, atom: str):
        super().__init__(atom)

        if not self.C:
            raise UnqualifiedAtom(atom)


class FQAtom(QualifiedAtom):
    """Atoms that include all possible non-optional fields"""

    MV: str
    MVR: str
    R: str

    def __init__(self, atom: str):
        super().__init__(atom)
        assert self.MV
        assert self.R


VersionMatch = namedtuple(
    "VersionMatch", ["version", "numeric", "letter", "suffix", "revision"]
)


def suffix_gt(a_suffix: str, b_suffix: str) -> bool:
    """Returns true iff a_suffix > b_suffix"""
    suffixes = ["alpha", "beta", "pre", "rc", "p"]
    return suffixes.index(a_suffix) > suffixes.index(b_suffix)


def version_gt(version1: str, version2: str) -> bool:
    """Returns true if and only if version1 is greater than version2"""
    match1 = re.match(
        r"(?P<NUMERIC>[\d\.]+)"
        r"(?P<LETTER>[a-z])?_?"
        r"(?P<SUFFIX>([a-z]+\d*)*)"
        r"(-r(?P<REV>\d+))?",
        version1,
    )
    match2 = re.match(
        r"(?P<NUMERIC>[\d\.]+)"
        r"(?P<LETTER>[a-z])?_?"
        r"(?P<SUFFIX>([a-z]+\d*)*)"
        r"(-r(?P<REV>\d+))?",
        version2,
    )

    assert match1 is not None
    assert match2 is not None
    v_match1 = VersionMatch(
        version=version1,
        numeric=match1.group("NUMERIC").split("."),
        letter=match1.group("LETTER") or "",
        suffix=match1.group("SUFFIX") or "",
        revision=int(match1.group("REV") or "0"),
    )
    v_match2 = VersionMatch(
        version=version2,
        numeric=match2.group("NUMERIC").split("."),
        letter=match2.group("LETTER") or "",
        suffix=match2.group("SUFFIX") or "",
        revision=int(match2.group("REV") or "0"),
    )

    # Compare numeric components
    for index, val in enumerate(v_match1.numeric):
        if index >= len(v_match2.numeric):
            return True
        if int(val) > int(v_match2.numeric[index]):
            return True
        if int(val) < int(v_match2.numeric[index]):
            return False

    # Compare letter components
    if v_match1.letter > v_match2.letter:
        return True
    if v_match1.letter < v_match2.letter:
        return False

    # Compare suffixes
    if v_match1.suffix:
        a_suffixes = v_match1.suffix.split("_")
    else:
        a_suffixes = []
    if v_match2.suffix:
        b_suffixes = v_match2.suffix.split("_")
    else:
        b_suffixes = []
    for a_s, b_s in zip(a_suffixes, b_suffixes):
        asm = re.match(r"(?P<S>[a-z]+)(?P<N>\d+)?", a_s)
        bsm = re.match(r"(?P<S>[a-z]+)(?P<N>\d+)?", b_s)
        assert asm
        assert bsm
        a_suffix = asm.group("S")
        b_suffix = bsm.group("S")
        a_suffix_num = int(asm.group("N") or "0")
        b_suffix_num = int(bsm.group("N") or "0")
        if a_suffix == b_suffix:
            if b_suffix_num > a_suffix_num:
                return False
            if a_suffix_num > b_suffix_num:
                return True
        elif suffix_gt(a_suffix, b_suffix):
            return True
        else:
            return False
    # More suffixes implies an earlier version,
    # except when the suffix is _p
    if len(a_suffixes) > len(b_suffixes):
        if not a_suffixes[len(b_suffixes)].startswith("p"):
            return True
        return False
    if len(a_suffixes) < len(b_suffixes):
        if b_suffixes[len(a_suffixes)].startswith("p"):
            return False
        return True

    # Compare revisions
    if v_match1.revision > v_match2.revision:
        return True
    if v_match1.revision < v_match2.revision:
        return False

    # Equal
    return False


def atom_sat(specific: Atom, generic: Atom) -> bool:
    """
    Determines if a fully qualified atom (can only refer to a single package)
    satisfies a generic atom
    """

    if specific.MN != generic.MN:
        # Mods must have the same name
        return False

    if generic.C and (generic.C != specific.C):
        # If para defines category, it must match
        return False

    if generic.R and (generic.R != specific.R):
        # If para defines repo, it must match
        return False

    if not generic.OP:
        # Simple atom, either one version or all versions will satisfy

        # Check if version is correct
        if generic.MV and (specific.MV != generic.MV):
            return False

        # Check if revision is correct
        if generic.MR and (specific.MR != generic.MR):
            return False
    else:
        equal = specific.MVR == generic.MVR
        verequal = specific.MV == generic.MV
        lessthan = version_gt(generic.MVR, specific.MVR)
        greaterthan = version_gt(specific.MVR, generic.MVR)

        if generic.OP == "=":
            return equal
        if generic.OP == "~":
            return verequal
        if generic.OP == "<":
            return lessthan
        if generic.OP == "<=":
            return equal or lessthan
        if generic.OP == ">":
            return greaterthan
        if generic.OP == ">=":
            return equal or greaterthan

    return True
