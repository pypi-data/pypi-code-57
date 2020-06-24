import neuron
import nrn

object_clutter = set(['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__'])
section_clutter = set(['allseg', 'arc3d', 'cell', 'children', 'connect', 'diam3d', 'has_membrane', 'hname', 'hoc_internal_name', 'insert', 'is_pysec', 'n3d', 'name', 'orientation', 'parentseg', 'psection', 'pt3dadd', 'pt3dchange', 'pt3dclear', 'pt3dinsert', 'pt3dremove', 'pt3dstyle', 'push', 'same', 'spine3d', 'subtree', 'trueparentseg', 'uninsert', 'wholetree', 'x3d', 'y3d', 'z3d'])
section_clutter.update(object_clutter)
mechanism_clutter = set(['is_ion', 'name', 'segment'])
mechanism_clutter.update(object_clutter)

unclutter_map = {
    nrn.Mechanism: mechanism_clutter,
    nrn.Section: section_clutter
}
