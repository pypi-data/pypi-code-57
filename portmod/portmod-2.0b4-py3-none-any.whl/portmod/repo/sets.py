# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Set
import os
from portmod.globals import env
from portmod.repo.atom import Atom, atom_sat
from .profiles import get_system


def is_selected(atom):
    """
    Returns true if and only if a mod is selected

    selected mods are either system mods, or included in the world file
    """
    selected = get_set("world") | get_system()
    for selatom in selected:
        if atom_sat(atom, selatom):
            return True
    return False


def get_set(mod_set: str, parent_dir: str = env.SET_DIR) -> Set[Atom]:
    atoms: Set[Atom] = set()
    if mod_set == "selected":
        mod_set = "world"
    elif mod_set == "world":
        atoms |= get_system()

    if mod_set == "world" or mod_set == "rebuild":
        parent_dir = env.PORTMOD_LOCAL_DIR

    set_file = os.path.join(parent_dir, mod_set)
    if os.path.exists(set_file):
        with open(set_file, "r") as file:
            return atoms | set([Atom(s) for s in file.read().splitlines()])
    else:
        return atoms


def add_set(mod_set: str, atom: Atom, parent_dir: str = env.SET_DIR):
    if mod_set == "world" or mod_set == "rebuild":
        parent_dir = env.PORTMOD_LOCAL_DIR

    set_file = os.path.join(parent_dir, mod_set)
    os.makedirs(env.SET_DIR, exist_ok=True)
    if os.path.exists(set_file):
        with open(set_file, "r+") as file:
            for line in file:
                if atom in line:
                    break
            else:
                print(atom, file=file)
    else:
        with open(set_file, "a+") as file:
            print(atom, file=file)


def remove_set(mod_set: str, atom: Atom, parent_dir: str = env.SET_DIR):
    if mod_set == "world" or mod_set == "rebuild":
        parent_dir = env.PORTMOD_LOCAL_DIR

    set_file = os.path.join(parent_dir, mod_set)
    if os.path.exists(set_file):
        with open(set_file, "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if atom not in line:
                    f.write(line)
            f.truncate()
