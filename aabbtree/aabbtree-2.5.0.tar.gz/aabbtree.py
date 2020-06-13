import copy
from collections import deque

__all__ = ['AABB', 'AABBTree']
__author__ = 'Kenneth (Kip) Hart'


class AABB(object):
    """Axis-aligned bounding box (AABB)

    The AABB is a d-dimensional box.

    Args:
        limits (iterable, optional): The limits of the box. These should be
            specified in the following manner::

                limits = [(xmin, xmax),
                          (ymin, ymax),
                          (zmin, zmax),
                          ...]

            The default value is None.
    """
    def __init__(self, limits=None):
        if limits is not None:
            for lims in limits:
                if len(lims) != 2 or lims[0] > lims[1]:
                    e_str = 'Limits not in (lower, upper) format: '
                    e_str += str(lims)
                    raise ValueError(e_str)

        self.limits = limits
        self._i = 0

    def __str__(self):
        return str(self.limits)

    def __repr__(self):
        return 'AABB(' + repr(self.limits) + ')'

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < len(self):
            val = self.limits[self._i]
            self._i += 1
            return val
        raise StopIteration

    def next(self):  # pragma: no cover
        """___next__ for Python 2"""
        return self.__next__()

    def __getitem__(self, key):
        return self.limits[key]

    def __len__(self):
        return len(self.limits)

    def __eq__(self, aabb):
        if not isinstance(aabb, AABB):
            return False

        if (self.limits is None) and (aabb.limits is None):
            return True
        if (self.limits is None) or (aabb.limits is None):
            return False
        if len(self.limits) != len(aabb.limits):
            return False

        for i, lims1 in enumerate(self.limits):
            lims2 = aabb[i]
            if (lims1[0] != lims2[0]) or (lims1[1] != lims2[1]):
                return False
        return True

    def __ne__(self, aabb):
        return not self.__eq__(aabb)

    @classmethod
    def merge(cls, aabb1, aabb2):
        """Merge AABB

        Find the AABB of the union of AABBs.

        Args:
            aabb1 (AABB): An AABB
            aabb2 (AABB): An AABB

        Returns:
            AABB: An AABB that contains both of the inputs
        """
        if (aabb1.limits is None) and (aabb2.limits is None):
            return cls(None)
        if aabb1.limits is None:
            return cls(aabb2.limits)
        if aabb2.limits is None:
            return cls(aabb1.limits)

        if len(aabb1.limits) != len(aabb2.limits):
            e_str = 'AABBs of different dimensions: ' + str(len(aabb1))
            e_str += ' and ' + str(len(aabb2))
            raise ValueError(e_str)

        return cls([_merge(*lims) for lims in zip(aabb1.limits, aabb2.limits)])

    @property
    def perimeter(self):
        r"""float: perimeter of AABB

        The perimeter :math:`p_n` of an AABB with side lengths
        :math:`l_1 \ldots l_n` is:

        .. math::

            p_1 &= 0 \\
            p_2 &= 2 (l_1 + l_2) \\
            p_3 &= 2 (l_1 l_2 + l_2 l_3 + l_1 l_3) \\
            p_n &= 2 \sum_{i=1}^n \prod_{j=1\neq i}^n l_j

        """
        if len(self.limits) == 1:
            return 0

        perim = 0
        side_lens = [ub - lb for lb, ub in self.limits]
        n_dim = len(side_lens)
        for i in range(n_dim):
            p_edge = 1
            for j in range(n_dim):
                if j != i:
                    p_edge *= side_lens[j]
            perim += p_edge
        return 2 * perim

    @property
    def volume(self):
        r"""float: volume of AABB

        The volume :math:`V_n` of an AABB with side lengths
        :math:`l_1 \ldots l_n` is:

        .. math::

            V_1 &= l_1 \\
            V_2 &= l_1 l_2 \\
            V_3 &= l_1 l_2 l_3 \\
            V_n &= \prod_{i=1}^n l_i

        """
        vol = 1
        for lb, ub in self.limits:
            vol *= ub - lb
        return vol

    @property
    def corners(self):
        """list: corner points of AABB"""

        n_dim = len(self.limits)
        f = '{:0' + str(n_dim) + 'b}'

        n_corners = 2 ** n_dim
        corners = []
        for i in range(n_corners):
            inds = [int(s) for s in f.format(i)]  # convert i to binary list
            corner = [self.limits[d][ind] for d, ind in enumerate(inds)]
            corners.append(corner)
        return corners

    def overlaps(self, aabb):
        """Determine if two AABBs overlap

        Args:
            aabb (AABB): The AABB to check for overlap

        Returns:
            bool: Flag set to true if the two AABBs overlap
        """
        if (self.limits is None) or (aabb.limits is None):
            return False

        for (min1, max1), (min2, max2) in zip(self.limits, aabb.limits):
            if min1 >= max2:
                return False
            if min2 >= max1:
                return False
        return True

    def overlap_volume(self, aabb):
        r"""Determine volume of overlap between AABBs

        Let :math:`\left(l_i^{(1)}, u_i^{(1)}\right)` be the i-th dimension
        lower and upper bounds for AABB 1, and let
        :math:`\left(l_i^{(2)}, u_i^{(2)}\right)` be the lower and upper bounds
        for AABB 2. The volume of overlap is:

        .. math::

            V = \prod_{i=1}^n \text{max}\left(0,
                \text{min}\left(u_i^{(1)}, u_i^{(2)}\right) -
                \text{max}\left(l_i^{(1)}, l_i^{(2)}\right)
                \right)

        Args:
            aabb (AABB): The AABB to calculate for overlap volume

        Returns:
            float: Volume of overlap
        """  # NOQA: E501

        volume = 1
        for (min1, max1), (min2, max2) in zip(self.limits, aabb.limits):
            overlap_min = max(min1, min2)
            overlap_max = min(max1, max2)
            if overlap_min >= overlap_max:
                return 0

            volume *= overlap_max - overlap_min
        return volume


class AABBTree(object):
    """Static AABB Tree

    An AABB tree where the bounds of each AABB do not change.

    Args:
        aabb (AABB): An AABB
        value: The value associated with the AABB
        left (AABBTree, optional): The left branch of the tree
        right (AABBTree, optional): The right branch of the tree

    """  # NOQA: E501
    def __init__(self, aabb=AABB(), value=None, left=None, right=None):

        self.aabb = aabb
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        inp_strs = []
        if self.aabb != AABB():
            inp_strs.append('aabb=' + repr(self.aabb))

        if self.value is not None:
            inp_strs.append('value=' + repr(self.value))

        if self.left is not None:
            inp_strs.append('left=' + repr(self.left))

        if self.right is not None:
            inp_strs.append('right=' + repr(self.right))

        return 'AABBTree(' + ', '.join(inp_strs) + ')'

    def __str__(self, n=0):
        pre = n * '  '

        aabb_str = pre + 'AABB: '
        if self.aabb == AABB():
            aabb_str += 'None'
        else:
            aabb_str += str(self.aabb)

        value_str = pre + 'Value: ' + str(self.value)

        left_str = pre + 'Left:'
        if self.left is None:
            left_str += ' None'
        else:
            left_str += '\n' + self.left.__str__(n + 1)

        right_str = pre + 'Right:'
        if self.right is None:
            right_str += ' None'
        else:
            right_str += '\n' + self.right.__str__(n + 1)

        return '\n'.join([aabb_str, value_str, left_str, right_str])

    def __eq__(self, aabbtree):
        if not isinstance(aabbtree, AABBTree):
            return False

        if self.aabb != aabbtree.aabb:
            return False

        if self.is_leaf != aabbtree.is_leaf:
            return False

        return (self.left == aabbtree.left) and (self.right == aabbtree.right)

    def __ne__(self, aabbtree):
        return not self.__eq__(aabbtree)

    def __len__(self):
        if self.is_leaf:
            return int(self.aabb != AABB())
        else:
            return len(self.left) + len(self.right)

    @property
    def is_leaf(self):
        """bool: returns True if is leaf node"""
        return (self.left is None) and (self.right is None)

    @property
    def depth(self):
        """int: Depth of the tree"""
        if self.is_leaf:
            return 0
        else:
            return 1 + max(self.left.depth, self.right.depth)

    def add(self, aabb, value=None, method='volume'):
        r"""Add node to tree

        This function inserts a node into the AABB tree.
        The function chooses one of three options for adding the node to
        the tree:

            * Add it to the left side
            * Add it to the right side
            * Become a leaf node

        The cost of each option is calculated based on the *method* keyword,
        and the option with the lowest cost is chosen.

        Args:
            aabb (AABB): The AABB to add.
            value: The value associated with the AABB. Defaults to None.
            method (str): The method for deciding how to build the tree.
                Should be one of the following:

                    * volume

                **volume**
                *Costs based on total bounding volume and overlap volume*

                Let :math:`p` denote the parent, :math:`l` denote the left
                child, :math:`r` denote the right child, :math:`x` denote
                the AABB to add, and :math:`V` be the volume of an AABB.
                The three options to add :math:`x` to the left branch, add it
                to the right branch, or create a new parent.
                The cost associated with each of these options is:

                .. math::

                    C(\text{add left})      &= V(p \cup x) - V(p) +
                                               V(l \cup x) - V(l) +
                                               V((l \cup x) \cap r) \\
                    C(\text{add right})     &= V(p \cup x) - V(p) +
                                               V(r \cup x) - V(r) +
                                               V((r \cup x) \cap l) \\
                    C(\text{create parent}) &= V(p \cup x) + V(p \cap x)

                In the add-left cost, the term :math:`V(b \cup x) - V(b)` is
                the increase in parent bounding volume. The cost
                :math:`V(l \cup x) - V(l)` is the increase in left child
                bounding volume. The last term, :math:`V((l \cup x) \cap r)`
                is the overlapping volume between children if :math:`x` were
                added to the left child.
                The cost to create a new parent is the bounding volume of the
                parent and :math:`x` plus their overlap volume.

                This cost function includes the increases in bounding volumes
                and the amount of overlap- two values a balanced AABB tree
                should minimize. The cost function suits the author's current
                needs, though other applications may seek different tree
                properties. Please visit the `AABBTree repository`_ if
                interested in implementing another cost function.

        .. _`AABBTree repository`: https://github.com/kip-hart/AABBTree

        """  # NOQA: E501
        if self.aabb == AABB():
            self.aabb = aabb
            self.value = value

        elif self.is_leaf:
            self.left = copy.deepcopy(self)
            self.right = AABBTree(aabb, value)

            self.aabb = AABB.merge(self.aabb, aabb)
            self.value = None
        else:
            if method == 'volume':
                # Define merged AABBs
                branch_merge = AABB.merge(self.aabb, aabb)
                left_merge = AABB.merge(self.left.aabb, aabb)
                right_merge = AABB.merge(self.right.aabb, aabb)

                # Calculate the change in the sum of the bounding volumes
                branch_bnd_cost = branch_merge.volume

                left_bnd_cost = branch_merge.volume - self.aabb.volume
                left_bnd_cost += left_merge.volume - self.left.aabb.volume

                right_bnd_cost = branch_merge.volume - self.aabb.volume
                right_bnd_cost += right_merge.volume - self.right.aabb.volume

                # Calculate amount of overlap
                branch_olap_cost = self.aabb.overlap_volume(aabb)
                left_olap_cost = left_merge.overlap_volume(self.right.aabb)
                right_olap_cost = right_merge.overlap_volume(self.left.aabb)

                # Calculate total cost
                branch_cost = branch_bnd_cost + branch_olap_cost
                left_cost = left_bnd_cost + left_olap_cost
                right_cost = right_bnd_cost + right_olap_cost
            else:
                raise ValueError('Unrecognized method: ' + str(method))

            if branch_cost < left_cost and branch_cost < right_cost:
                self.left = copy.deepcopy(self)
                self.right = AABBTree(aabb, value)
                self.value = None
            elif left_cost < right_cost:
                self.left.add(aabb, value)
            else:
                self.right.add(aabb, value)
            self.aabb = AABB.merge(self.left.aabb, self.right.aabb)

    def does_overlap(self, aabb, method='DFS'):
        """Check for overlap

        This function checks if the limits overlap any leaf nodes in the tree.
        It returns true if there is an overlap.

        Args:
            aabb (AABB): The AABB to check.
            method (str): {'DFS'|'BFS'} Method for traversing the tree.
                Setting 'DFS' performs a depth-first search and 'BFS' performs
                a breadth-first search. Defaults to 'DFS'.

        Returns:
            bool: True if overlaps with a leaf node of tree.
        """
        if method == 'DFS':
            if self.is_leaf:
                return self.aabb.overlaps(aabb)

            left_aabb_over = self.left.aabb.overlaps(aabb)
            right_aabb_over = self.right.aabb.overlaps(aabb)

            if left_aabb_over and self.left.does_overlap(aabb):
                return True
            if right_aabb_over and self.right.does_overlap(aabb):
                return True
            return False

        if method == 'BFS':
            q = deque()
            q.append(self)
            while len(q) > 0:
                node = q.popleft()
                overlaps = node.aabb.overlaps(aabb)
                if overlaps and node.is_leaf:
                    return True
                if overlaps:
                    q.append(node.left)
                    q.append(node.right)
            return False

        e_str = "method should be 'DFS' or 'BFS', not " + str(method)
        raise ValueError(e_str)

    def overlap_aabbs(self, aabb, method='DFS'):
        """Get overlapping AABBs

        This function gets each overlapping AABB.

        Args:
            aabb (AABB): The AABB to check.
            method (str): {'DFS'|'BFS'} Method for traversing the tree.
                Setting 'DFS' performs a depth-first search and 'BFS' performs
                a breadth-first search. Defaults to 'DFS'.

        Returns:
            list: AABB objects in AABBTree that overlap with the input.
        """
        aabbs = []

        if method == 'DFS':
            is_leaf = self.is_leaf
            if is_leaf and self.does_overlap(aabb):
                aabbs.append(self.aabb)
            elif is_leaf:
                pass
            else:
                if self.left.aabb.overlaps(aabb):
                    aabbs.extend(self.left.overlap_aabbs(aabb))

                if self.right.aabb.overlaps(aabb):
                    aabbs.extend(self.right.overlap_aabbs(aabb))
        elif method == 'BFS':
            q = deque()
            q.append(self)
            while len(q) > 0:
                node = q.popleft()
                if node.aabb.overlaps(aabb):
                    if node.is_leaf:
                        aabbs.append(node.aabb)
                    else:
                        q.append(node.left)
                        q.append(node.right)
        else:
            e_str = "method should be 'DFS' or 'BFS', not " + str(method)
            raise ValueError(e_str)
        return aabbs

    def overlap_values(self, aabb, method='DFS'):
        """Get values of overlapping AABBs

        This function gets the value field of each overlapping AABB.

        Args:
            aabb (AABB): The AABB to check.
            method (str): {'DFS'|'BFS'} Method for traversing the tree.
                Setting 'DFS' performs a depth-first search and 'BFS' performs
                a breadth-first search. Defaults to 'DFS'.

        Returns:
            list: Value fields of each node that overlaps.
        """
        values = []

        if method == 'DFS':
            is_leaf = self.is_leaf
            if is_leaf and self.does_overlap(aabb):
                values.append(self.value)
            elif is_leaf:
                pass
            else:
                if self.left.aabb.overlaps(aabb):
                    values.extend(self.left.overlap_values(aabb))

                if self.right.aabb.overlaps(aabb):
                    values.extend(self.right.overlap_values(aabb))
        elif method == 'BFS':
            q = deque()
            q.append(self)
            while len(q) > 0:
                node = q.popleft()
                if node.aabb.overlaps(aabb):
                    if node.is_leaf:
                        values.append(node.value)
                    else:
                        q.append(node.left)
                        q.append(node.right)
        else:
            e_str = "method should be 'DFS' or 'BFS', not " + str(method)
            raise ValueError(e_str)
        return values


def _merge(lims1, lims2):
    lb = min(lims1[0], lims2[0])
    ub = max(lims1[1], lims2[1])

    return (lb, ub)
