import json
from ._clutter import (
    unclutter_map as _unclutter_map,
    mechanism_clutter as _mechanism_clutter,
)
try:
    from patch import transform
except ImportError:
    def transform(obj):
        if hasattr(obj, "__neuron__"):
            # Compatibility with Patched objects.
            return obj.__neuron__()
        return obj


__version__ = "0.0.1"


def unclutter(obj):
    t = type(obj)
    if t not in _unclutter_map:
        raise NotImplementedError("Don't know how to unclutter '{}'".format(t.__module__ + "." + t.__name__))
    return set(dir(obj)) - _unclutter_map[t]


def describe_model(model, collector=None, spatial=False, ignore_glia=False):
    if collector is None:
        collector = _collect_sections
    model_descr = {}
    sections = collector(model)
    for section in sections:
        sec_descr = describe_section(section, spatial=spatial, ignore_glia=ignore_glia)
        hash = _hash(sec_descr)
        if hash in model_descr:
            model_descr[hash]["count"] += 1
        else:
            model_descr[hash] = {
                "count": 1,
                "hash": hash,
                "representative": section,
                "description": sec_descr,
            }
    return model_descr


def describe_section(section, spatial=True, ignore_glia=False):
    descr = {"nseg": section.nseg, "segs": []}
    if spatial:
        descr["L"] = section.L
        descr["diam"] = section.diam
    for seg in section:
        descr["segs"].append(describe_segment(seg, ignore_glia=ignore_glia))
    return descr


def describe_segment(seg, ignore_glia=False):
    descr = {}
    for mech in seg:
        name = str(mech)
        if ignore_glia and name.startswith("glia__"):
            name = name.split("__")[2]
        descr[name] = describe_mechanism(mech)
    return descr


def describe_mechanism(mech):
    return {param: getattr(mech, param) for param in unclutter(mech)}


def _hash(obj):
    return hash(json.dumps(obj))

def _collect_sections(model):
    return model.soma + model.axon + (model.dend or model.dendrites)
