"""Provides YAML serialization support."""

import yaml

from . import distributions, algorithms
from .repeatablerandom import RepeatableRandomSequence, RepeatableRandomSequenceState

__all__ = [
    'enable_yaml_support'
]

_has_enabled_support = False

# ---- RepeatableRandomSequence ----


def _rrs_state_representer(dumper, state: RepeatableRandomSequenceState):
    return dumper.represent_mapping(
        state.yaml_tag,
        state.as_dict())


def _rrs_state_constructor(loader, node):
    as_dict = loader.construct_mapping(node)
    return RepeatableRandomSequenceState.from_dict(as_dict)


def _rrs_representer(dumper, rrs: RepeatableRandomSequence):
    state = rrs.getstate()
    return dumper.represent_mapping(
        rrs.yaml_tag,
        state.as_dict())


def _rrs_constructor(loader, node):
    value = loader.construct_mapping(node)
    rrs = RepeatableRandomSequence.__new__(RepeatableRandomSequence)
    # N.B. _cascading needs to be initialized before setting the state
    # since __new__ does not create it.
    rrs._cascading = 0
    state = RepeatableRandomSequenceState.from_dict(value)
    rrs.setstate(state)
    return rrs


def _add_rrs_support():
    RepeatableRandomSequence.yaml_tag = u'!samplespace.rrs'
    RepeatableRandomSequenceState.yaml_tag = u'!samplespace.rrs_state'

    yaml.add_representer(RepeatableRandomSequenceState, _rrs_state_representer)
    yaml.add_constructor(RepeatableRandomSequenceState.yaml_tag, _rrs_state_constructor)
    yaml.add_representer(RepeatableRandomSequence, _rrs_representer)
    yaml.add_constructor(RepeatableRandomSequence.yaml_tag, _rrs_constructor)


# ---- Distributions ----

def _make_distribution_representer(_cls: distributions.Distribution):
    return lambda dumper, obj: \
        dumper.represent_mapping(_cls.yaml_tag, obj.as_dict())


def _make_distribution_constructor():
    return lambda loader, node: \
        distributions.distribution_from_dict(loader.construct_mapping(node, deep=True))


def _add_distributions_support():
    distributions.Distribution.yaml_tag = u'!samplespace.distribution'

    # noinspection PyProtectedMember
    for name, cls in distributions._distribution_lookup.items():
        yaml.add_representer(cls, _make_distribution_representer(cls))
        yaml.add_constructor(cls.yaml_tag, _make_distribution_constructor())


# ---- Algorithms ----

def _alias_table_representer(dumper, table):
    return dumper.represent_yaml_object(
        table.yaml_tag, table, algorithms.AliasTable)


def _alias_table_constructor(loader, node):
    return loader.construct_yaml_object(node, algorithms.AliasTable)


def _add_algorithm_support():
    algorithms.AliasTable.yaml_tag = u'!samplespace.aliastable'

    yaml.add_representer(algorithms.AliasTable, _alias_table_representer)
    yaml.add_constructor(algorithms.AliasTable.yaml_tag, _alias_table_constructor)


def enable_yaml_support(_force=False):
    """Add YAML serialization support. This function only needs to be
    called once per application."""
    global _has_enabled_support
    if _has_enabled_support and not _force:
        return

    _add_rrs_support()
    _add_distributions_support()
    _add_algorithm_support()
    _has_enabled_support = True
