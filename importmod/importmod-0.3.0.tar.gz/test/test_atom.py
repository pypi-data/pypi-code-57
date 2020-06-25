# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from importmod.atom import parse_atom


def test_atom():
    """Basic atom parsing test"""
    assert parse_atom("Great Mod! - v2") == "great-mod-2"
