# -*- coding:utf-8 -*-
from math import ceil
from random import choice
from typing import Callable, Any, List, Tuple, Optional, Collection, Set

from geortree.coordinates import Coordinates, Rectangle

__all__ = ['GeoRTree']


class GeoRTree:
    def __init__(self,
                 max_node_capacity: int = 10,
                 coords_extractor: Callable[[Any], Coordinates] = lambda x: x):
        """A R-tree adapted to work with geographic coordinates.

        You can insert any data type in this tree (and even mix types), as long
        as the passed "coords_extractor" knows how to get the Coordinates of
        all objects you inserted.

        Mostly a convenience wrapper over GeoRTreeNode, to which it delegates
        most of the hard work.
        """
        self.root = GeoRTreeLeafNode(max_node_capacity, coords_extractor)

    def insert(self, entry):
        """Insert passed object into the tree."""
        self.root.insert(entry)
        self.root = self.root.get_root()

    def insert_all(self, entries: Collection[Any]):
        """Insert all objects of the passed collection into the tree."""
        for e in entries:
            self.insert(e)

    def remove(self, entry):
        """Removes the passed object from the tree.

        Fails silently if the entry doesn't exist.
        """
        self.root.remove(entry)
        self.root = self.root.get_root()

    def get_nearest(self, point: Coordinates, excluding=None):
        exclusion_set = excluding or set()
        return self.root.nearest_neighbor(point, exclusion_set)[0]


class GeoRTreeNode:
    """A node in the Geographic R-tree.

    Approximates all values with Cartesian geometry, as proper spherical
    geometry would take a lot of work to implement for little gain.
    Nevertheless, should give good enough results for "small" distances that
    don't cross the 180º meridian.

    References:
        https://www.cse.cuhk.edu.hk/~taoyf/course/infs4205/lec/rtree.pdf
        http://www.cs.umd.edu/~nick/papers/nnpaper.pdf (Nearest Neighbor algorithm)
    """

    def __init__(self,
                 capacity: int,
                 coords_extractor: Callable[[Any], Coordinates],
                 parent: Optional['GeoRTreeInternalNode'] = None):
        """
        :param capacity
            How many elements this box can hold without overflowing.
        :param coords_extractor
            An optional function to extract Coordinates from the elements inside
            the box if they aren't Coordinates themselves.
        :param parent
            The parent of this node in the tree. The root will obviously have this empty.
        """
        self.capacity = capacity
        self.coords_of = coords_extractor
        self.parent = parent
        if self._is_overflowing():
            raise ValueError("Node initialized with too many elements!")
        self._update_bounds()

    def contains(self, entry) -> bool:
        """Check if the coordinates of the entry are contained in the bounding box of this node.
        """
        point = self.coords_of(entry)
        return self.bounds.contains(point)

    def insert(self, entry):
        """Insert passed object into the tree."""
        raise NotImplementedError()

    def remove(self, entry):
        """Removes the passed object from the tree.

        Fails silently if the entry doesn't exist.
        """
        raise NotImplementedError()

    def nearest_neighbor(self,
                         search_point: Coordinates,
                         exclude: Set[Any],
                         limit=float('inf')) -> Tuple[Any, float]:
        """Query the tree for the entry nearest to the search point.

        Ignores entries in the 'exclude' set.
        """
        raise NotImplementedError()

    def get_area_increase(self, candidate) -> float:
        """Calculate the increase in area for this node if the passed candidate is inserted.
        """
        if self.contains(candidate):
            return 0
        new_point = self.coords_of(candidate)
        new_sw = Coordinates(min(self.bounds.sw.lat, new_point.lat),
                             min(self.bounds.sw.lng, new_point.lng))
        new_ne = Coordinates(max(self.bounds.ne.lat, new_point.lat),
                             max(self.bounds.ne.lng, new_point.lng))
        new_area = Rectangle(new_sw, new_ne).area()
        curr_area = self.bounds.area()
        return new_area - curr_area

    def get_root(self) -> 'GeoRTreeNode':
        """Return a reference to the root of this tree.

        As nodes are added and removed, the root can change.
        """
        return self if self._is_root() else self.parent.get_root()

    def _is_root(self) -> bool:
        return self.parent is None

    def _is_overflowing(self) -> bool:
        return self._get_load() > self.capacity

    def _update_bounds(self):
        """Update the bounding box for this node and its ancestors."""
        if self._get_load() == 0:
            self.bounds = Rectangle(Coordinates(0, 0), Coordinates(0, 0))
            return
        self.bounds = self._calculate_bounds()

        if not self._is_root():
            self.parent._update_bounds()

    def _handle_overflow(self):
        """Redistribute the elements of this node as to maintain the tree balanced."""
        if self._is_root():
            self.parent = GeoRTreeInternalNode(self.capacity, self.coords_of,
                                               children=[self])
        new_sibling = self._split()
        self.parent.add_child(new_sibling)

    def _best_axis_bisection(self, axis: Collection, mapping=None) -> Tuple[List, List, float]:
        """Heuristic for determining a good split for the node.

        This method is meant to be used by the actual splitting algorithm, as
        several 'axes' must be considered for the choice of a good split.
        An axis consists in the elements of the node sorted in a certain way,
        regarding their geographical position.
        """
        mapping = mapping or self.coords_of
        min_split_size = ceil(0.4*self.capacity)
        best_self, best_other = None, None
        best_sum = float('inf')
        # Iterate over all possible ways of bisecting the axis that respect
        # the 'min_split_size' condition. Choose the one that will give
        # the lowest area sum.
        for i in range(min_split_size, self.capacity-min_split_size+1):
            candidate_self = axis[:i]
            self_coords = [mapping(x) for x in candidate_self]
            candidate_other = axis[i:]
            other_coords = [mapping(x) for x in candidate_other]
            self_area = Rectangle.enclosing(self_coords).area()
            other_area = Rectangle.enclosing(other_coords).area()
            candidate_sum = self_area + other_area
            if candidate_sum < best_sum:
                best_self, best_other = candidate_self, candidate_other
                best_sum = candidate_sum
        return best_self, best_other, best_sum

    def _get_load(self) -> int:
        raise NotImplementedError()

    def _calculate_bounds(self) -> Rectangle:
        """Calculate the Minimal Bounding Rectangle that contains all entries of this node.
        """
        raise NotImplementedError()

    def _split(self) -> 'GeoRTreeNode':
        """Create a sibling node to this, and give it some of its entries."""
        raise NotImplementedError()


class GeoRTreeLeafNode(GeoRTreeNode):
    """Node of the R-tree that contains data points."""
    def __init__(self,
                 capacity: int,
                 coords_extractor: Callable[[Any], Coordinates],
                 parent: Optional['GeoRTreeInternalNode'] = None,
                 elements: Optional[List[Any]] = None):
        self.elements = elements or list()
        super().__init__(capacity, coords_extractor, parent)

    def insert(self, entry):
        self.elements.append(entry)
        if self._is_overflowing():
            self._handle_overflow()
        elif not self.contains(entry):
            # Handling overflow will update the bounds, so we only need to do
            # it here if the insertion did NOT overflow this node AND if the new
            # element is NOT contained in the original bounds.
            self._update_bounds()

    def remove(self, entry):
        try:
            self.elements.remove(entry)
            self._update_bounds()
        except ValueError:
            # Bounding boxes can overlap, so you can end up looking in the wrong place
            pass

    def nearest_neighbor(self,
                         search_point: Coordinates,
                         exclude: Set[Any],
                         limit=float('inf')) -> Tuple[Any, float]:
        nearest = None
        min_dist = limit
        for entry in self.elements:
            if entry in exclude:
                continue
            distance = self.coords_of(entry).distance_to(search_point)
            if distance < min_dist:
                nearest = entry
                min_dist = distance
            elif distance == min_dist:
                # If the distance is the same, choose one at random.
                nearest = choice([entry, nearest])
        return nearest, min_dist

    def _get_load(self) -> int:
        return len(self.elements)

    def _calculate_bounds(self) -> Rectangle:
        return Rectangle.enclosing([self.coords_of(x) for x in self.elements])

    def _split(self) -> 'GeoRTreeNode':
        # As these nodes contain only points, we only need to consider two axes
        # for the bisection: latitude and longitude
        lat_axis = sorted(self.elements, key=lambda x: self.coords_of(x).lat)
        lat_self, lat_other, lat_sum = self._best_axis_bisection(lat_axis)
        lng_axis = sorted(self.elements, key=lambda x: self.coords_of(x).lng)
        lng_self, lng_other, lng_sum = self._best_axis_bisection(lng_axis)

        if lat_sum <= lng_sum:
            best_self, best_other = lat_self, lat_other
        else:
            best_self, best_other = lng_self, lng_other
        self.elements = best_self
        self._update_bounds()
        return GeoRTreeLeafNode(self.capacity, self.coords_of, elements=best_other)


class GeoRTreeInternalNode(GeoRTreeNode):
    """Node of the R-tree that does not contain data points.

    Only internal nodes can be parents of other nodes. This does NOT
    break the LSP because internal nodes can do anything that the generic
    nodes can. The LSP doesn't care the other way around.
    """

    def __init__(self,
                 capacity: int,
                 coords_extractor: Callable[[Any], Coordinates],
                 parent: Optional[GeoRTreeNode] = None,
                 children: Optional[List[GeoRTreeNode]] = None):
        self.children = children or list()
        super().__init__(capacity, coords_extractor, parent)

    def insert(self, entry):
        self._choose_subtree(entry).insert(entry)

    def remove(self, entry):
        for branch in self.children:
            if branch.contains(entry):
                branch.remove(entry)

    def nearest_neighbor(self,
                         search_point: Coordinates,
                         exclude: Set[Any],
                         limit=float('inf')) -> Tuple[Any, float]:
        nearest = None
        min_dist = limit
        branches = sorted(self.children,
                          key=lambda x: x.bounds.distance_to_point(search_point))
        for b in branches:
            if b.bounds.distance_to_point(search_point) > min_dist:
                break
            candidate, distance = b.nearest_neighbor(search_point, exclude, min_dist)
            if distance < min_dist:
                nearest = candidate
                min_dist = distance
        return nearest, min_dist

    def add_child(self, child: GeoRTreeNode):
        """Add a child node to this node.

        NOT to be used to add entries to the tree.
        """
        self.children.append(child)
        child.parent = self
        if self._is_overflowing():
            self._handle_overflow()
        self._update_bounds()

    def _choose_subtree(self, entry: Any) -> 'GeoRTreeNode':
        """Choose which subtree will receive the entry being added."""
        return min(self.children, key=lambda x: x.get_area_increase(entry))

    def _get_load(self) -> int:
        return len(self.children)

    def _split(self) -> 'GeoRTreeNode':
        # Bisecting rectangles is harder. We need to consider both latitude and
        # longitude for the northeast and southwest points.
        splitting_axis = [
            (sorted(self.children, key=lambda x: x.bounds.sw.lat), lambda x: x.bounds.sw),
            (sorted(self.children, key=lambda x: x.bounds.ne.lat), lambda x: x.bounds.ne),
            (sorted(self.children, key=lambda x: x.bounds.sw.lng), lambda x: x.bounds.sw),
            (sorted(self.children, key=lambda x: x.bounds.ne.lng), lambda x: x.bounds.ne)
        ]
        best_self, best_other, best_sum = None, None, float('inf')
        for axis, mapping in splitting_axis:
            ax_self, ax_other, ax_sum = self._best_axis_bisection(axis, mapping)
            if ax_sum < best_sum:
                best_self, best_other, best_sum = ax_self, ax_other, ax_sum
        self.children = best_self
        self._update_bounds()
        return GeoRTreeInternalNode(self.capacity, self.coords_of, children=best_other)

    def _calculate_bounds(self) -> Rectangle:
        south = west = float('inf')
        north = east = float('-inf')
        for x in self.children:
            north = max(north, x.bounds.ne.lat)
            east = max(east, x.bounds.ne.lng)
            south = min(south, x.bounds.sw.lat)
            west = min(west, x.bounds.sw.lng)
        return Rectangle(Coordinates(south, west), Coordinates(north, east))
