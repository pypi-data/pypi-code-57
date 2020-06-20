# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""
Context-free grammars for Boltzmann generation.
===============================================

Grammars use the basic operators of the symbolic method of analytic
combinatorics to specify labelled or unlabelled combinatorial classes. For
instance, binary trees can be specified by ``B = leaf + Z * B * B`` which,
using the syntax implemented in this module, looks like:

Examples:
    >>> z, leaf = Atom(), Marker("leaf")
    >>> B = RuleName("B")

    >>> # Using the explicit syntax
    >>> Grammar({B: Union(leaf, Product(z, B, B))})
    B -> Union(leaf, Product(z, B, B))

    >>> # Using the syntactic sugar + and * for unions and products
    >>> Grammar({B: leaf + z * B * B})
    B -> Union(leaf, Product(z, B, B))


Note that we make the difference between

- terminal symbols of the grammar: :py:class:`Atom` (``leaf`` and ``z`` in the
  above example).
- non-terminal symbols: :py:class:`RuleName` (``B`` in the above example).

The most basic constructions of the symbolic method are the Cartesian product
:py:class:`Product` and the disjoint union :py:class:`Union`. In the example of
binary trees, disjoint union is used to decompose the class between leaves and
internal nodes. The Cartesian product is used to define internal nodes as a
pair of children, the ``z`` appearing at each internal node means that each
node counts as :math:`1` in the size of a tree.

The exhaustive list of supported constructions is given below. Detailed
explanations about each of these operators can be found on the `Wikipedia page
<https://en.wikipedia.org/wiki/Symbolic_method_(combinatorics)>`_ of the
symbolic method and in [FS2009]_.

Here are two other examples of specifications, for general plane trees,
illustrating the use of the :class:`Seq` (sequence) operator and the use of
multi-rules grammars:

Examples:
    >>> z = Atom()
    >>> T, S = RuleName("T"), RuleName("S")

    >>> # With Seq
    >>> Grammar({T: z * Seq(T)})
    T -> Product(z, Seq(T))

    >>> # Equivalent definition without Seq
    >>> nil = Epsilon()
    >>> Grammar({
    ...     T: z * S,
    ...     S: nil + T * S,
    ... })
    S -> Union(epsilon, Product(T, S))
    T -> Product(z, S)

.. todo:: Write about labeling

AUTHORS:

- Matthieu Dien (2019): initial version

- Martin Pépin (2019): initial version

.. rubric:: References

.. [FS2009] Philippe Flajolet, Robert Sedgewick, 2009, Analytic combinatorics,
   Cambridge University Press.
"""

from functools import reduce

from usainboltz.sage_compat import Singleton, latex

__all__ = (
    "Marker",
    "Epsilon",
    "Atom",
    "Cycle",
    "Grammar",
    "MSet",
    "Product",
    "RuleName",
    "Seq",
    "Set",
    "Union",
    "UCycle",
)

# ------------------------------------------------------- #
# Fresh names generation
# ------------------------------------------------------- #


class _NameGenerator:
    def __init__(self, prefix):
        self.prefix = prefix
        self.counter = 0

    def fresh(self):
        fresh_name = "{}_{}".format(self.prefix, self.counter)
        self.counter += 1
        return fresh_name


_symbol_name_generator = _NameGenerator("_symbol")


# ------------------------------------------------------- #
# Grammar implementation
# ------------------------------------------------------- #


class Rule:
    """The super class of all grammar rules.

    Should not be instantiated directly.
    """

    def __add__(self, rhs):
        """Disjoint union of rules using the + syntax.

        Examples:
            >>> a, b, c, d = Marker("a"), Marker("b"), Marker("c"), Marker("d")

            >>> a + b
            Union(a, b)

            >>> Union(a, b) + c
            Union(a, b, c)

            >>> a + Union(b, c)
            Union(a, b, c)

            >>> Union(a, b) + Union(c, d)
            Union(a, b, c, d)
        """
        # ensure not to build unions of unions
        lhs = self.args if isinstance(self, Union) else [self]
        rhs = rhs.args if isinstance(rhs, Union) else [rhs]
        return Union(*(lhs + rhs))

    def __mul__(self, rhs):
        """Cartesian product of rules using the * syntax.

        Examples:
            >>> a, b, c, d = Marker("a"), Marker("b"), Marker("c"), Marker("d")

            >>> a * b
            Product(a, b)

            >>> Product(a, b) * c
            Product(a, b, c)

            >>> a * Product(b, c)
            Product(a, b, c)

            >>> Product(a, b) * Product(c, d)
            Product(a, b, c, d)
        """
        # ensure not to build products of products
        # ensure not to build unions of unions
        lhs = self.args if isinstance(self, Product) else [self]
        rhs = rhs.args if isinstance(rhs, Product) else [rhs]
        return Product(*(lhs + rhs))


class IteratedRule(Rule):
    """The base class for iterated constructions Seq, Set, Cycle, MSet, etc.

    Should not be instantiated directly.
    """

    # This class attribute is used for pretty-printing. It has to be set in
    # classes extending IteratedRule.
    construction_name = None

    def __init__(self, arg, leq=None, geq=None, eq=None):
        """Rule constructor.

        Args:
          arg (:py:class:`Rule`): a rule describing the elements of the
            collection.

          leq (int): constrains the collection to have size at most ``leq``.

          geq (int): constrains the collection to have size at least ``geq``.

          eq (int): constrains the collection to have size exactly ``eq``.
        """
        super(IteratedRule, self).__init__()

        assert leq is None or geq is None or geq <= leq
        assert eq is None or (leq is None and geq is None)  # eq != 0 => leq == geq == 0

        self.lower_size = None
        self.upper_size = None

        if eq is not None:
            self.lower_size = eq
            self.upper_size = eq
        else:
            self.lower_size = geq
            self.upper_size = leq

        self.arg = _to_rule(arg)

    def __repr__(self):
        if self.construction_name is None:
            raise ValueError("IteratedRule should not be used directly!")
        constraint = None
        if self.lower_size is not None:
            constraint = "{} <= .".format(self.lower_size)
            if self.upper_size is not None:
                constraint += " <= {}".format(self.upper_size)
        else:
            if self.upper_size is not None:
                constraint = ". <= {}".format(self.upper_size)
        constraint = ", {}".format(constraint) if constraint else ""
        return "{}({}{})".format(self.construction_name, self.arg, constraint)

    def _latex_(self):
        if self.construction_name is None:
            raise ValueError("IteratedRule should not be used directly!")
        constraint = None
        if self.lower_size is not None:
            constraint = r"{} \leq \cdot".format(self.lower_size)
            if self.upper_size is not None:
                constraint += r"\geq {}".format(self.upper_size)
        else:
            if self.upper_size is not None:
                constraint = r"\cdot {}".format(self.upper_size)
        constraint = "_{{{}}}".format(constraint) if constraint else ""
        return r"{{\sc {}}}\left({}\right){}".format(
            self.construction_name, latex(self.arg), constraint
        )

    def markers(self):
        """Return the set of all markers in the rule."""
        return self.arg.markers()


class Symbol(Rule):
    """Base class for all grammar symbols (Atom, RuleName, Epsilon).

    Should not be instantiated directly.
    """

    def __init__(self, name=None):
        super(Symbol, self).__init__()
        if name is None:
            name = _symbol_name_generator.fresh()
        self.name = name

    def _latex_(self):
        r"""Return the LaTeX representation of a marker.

        Examples:
            >>> u = Marker("u")
            >>> print(latex(u))
            u

            >>> v = Atom()
            >>> print(latex(v))
            z

            >>> eps = Epsilon()
            >>> print(latex(eps))
            \epsilon
        """
        nice_name = self.name
        if len(self.name) != 1:
            nice_name = r"\textrm{{{}}}".format(self.name)
        return nice_name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Symbol):
            raise TypeError("Cannot compare Symbol and {}".format(type(other)))
        return self.name < other.name

    def markers(self):
        """Return the set of all markers contained in the expression."""
        return set()


class Marker(Symbol):
    """Marker symbols.

    Examples:
        >>> Marker("u")
        u

        >>> Marker()
        _symbol_0

    Markers are similar to atoms but have size 0. They are usually used to
    mark some special places in the grammar. For instance in the following
    grammar for Motzkin tree, the marker `u` is used to mark unary nodes.

    Examples:
        >>> z, u, M = Atom(), Marker(), RuleName()
        >>> grammar = Grammar({M: z + u * z * M + z * M * M})
    """

    def markers(self):
        return {self}


class Epsilon(Singleton, Symbol):
    """The epsilon symbol.

    Epsilon is the class containing only one element of size 0.

    Note:
        There is only one instance of the Epsilon class.

    Examples:
        >>> eps1 = Epsilon()
        >>> eps2 = Epsilon()
        >>> eps1 is eps2
        True
    """

    def __init__(self):
        super(Epsilon, self).__init__("epsilon")

    def _latex_(self):
        return r"\epsilon"


class Atom(Singleton, Symbol):
    """Terminal symbol of a grammar, accounts for the size.

    Atom is the class containing only one element of size 1.

    Note:
        There is only one instance of the Atom class.

    >>> Atom()
    z

    >>> Atom() is Atom()
    True
    """

    def __init__(self):
        super(Atom, self).__init__("z")


class RuleName(Symbol):
    """Non terminal symbols of a grammar.

    Instances of this class represent recursive references to non-terminal
    symbols inside grammar rules. For instance, sequences of atoms ``z`` could
    be defined using the following grammar where the :py:class:`RuleName` ``S``
    refers to itself in its definition:

    Examples:
        >>> epsilon, z, S = Epsilon(), Atom(), RuleName("S")
        >>> Grammar({S: epsilon + z * S})
        S -> Union(epsilon, Product(z, S))
    """


def _to_rule(rule_name):
    """Cast strings to RuleNames, otherwise do nothing."""
    if isinstance(rule_name, Rule):
        return rule_name
    return RuleName(rule_name)


class Union(Rule):
    """Disjoint union of two or more rules.

    ``D = Union(A, B, C)`` corresponds to the following grammar in BNF syntax:
    ``D ::= A | B | C``

    Examples:
        >>> A, B, C = RuleName("A"), RuleName("B"), RuleName("C")

        >>> Union(A, B, C)
        Union(A, B, C)

        >>> z = Atom()
        >>> Union(z, A)
        Union(z, A)
    """

    def __init__(self, *terms):
        """Build a union of two or more rules.

        Args:
            terms (List[Rule]): list of terms of the union.
        """
        super(Union, self).__init__()

        if len(terms) < 2:
            raise ValueError("Unions should have at least two terms")
        self.args = [_to_rule(arg) for arg in terms]

    def _latex_(self):
        """Return the LaTeX representation of a union.

        Example:
            >>> A, B = RuleName("A"), RuleName("B")
            >>> print(latex(Union(A, B)))
            A + B

        """
        return " + ".join(map(latex, self.args))

    def __repr__(self):
        return "Union({})".format(", ".join(map(repr, self.args)))

    def markers(self):
        """Return the set of markers contained in the expression."""
        return reduce(lambda x, y: x | y, (arg.markers() for arg in self.args))


class Product(Rule):
    """Cartesian product of two or more rules.

    ``Product(A, B, C)`` corresponds to the following grammar in BNF syntax:
    ``_ ::= A × B × C``

    Examples:
        >>> A, B, C = RuleName("A"), RuleName("B"), RuleName("C")

        >>> Product(A, B, C)
        Product(A, B, C)

        >>> z = Atom()
        >>> Product(z, A)
        Product(z, A)
    """

    def __init__(self, *factors):
        """Build the product of two or more rules.

        Args:
            factors (List[Rule]): list of factors of the product.
        """
        super(Product, self).__init__()
        if len(factors) < 2:
            raise ValueError("Products should have at least two components")
        self.args = [_to_rule(arg) for arg in factors]

    def _latex_(self):
        r"""Return the LaTeX representation of a product.

        Examples:
            >>> A, B = RuleName("A"), RuleName("B")

            >>> print(latex(Product(A, B)))
            A \times B

        """

        def wrap_latex(rule):
            if isinstance(rule, Union):
                return "({})".format(latex(rule))
            return latex(rule)

        return r" \times ".join(map(wrap_latex, self.args))

    def __repr__(self):
        return "Product({})".format(", ".join(map(repr, self.args)))

    def markers(self):
        """Return the set of all markers contained in the expression."""
        return reduce(lambda x, y: x | y, (arg.markers() for arg in self.args))


class Seq(IteratedRule):
    """Sequences.

    The Seq construction of the symbolic method models sequences of elements.
    In the following example, Seq is used to represent binary words as
    sequences of bits.

    Example:
        >>> z, one, zero, S = Atom(), Marker("1"), Marker("0"), RuleName("S")
        >>> Grammar({S: Seq(z * (one + zero))})
        S -> Seq(Product(z, Union(1, 0)))

    The number of terms of a sequence can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z, one, zero = Atom(), Marker("1"), Marker("0")

        >>> Seq(z * (one + zero), leq=10, geq=5)
        Seq(Product(z, Union(1, 0)), 5 <= . <= 10)

        >>> Seq(z * (one + zero), leq=10)
        Seq(Product(z, Union(1, 0)), . <= 10)

        >>> Seq(z * (one + zero), geq=5)
        Seq(Product(z, Union(1, 0)), 5 <= .)
    """

    construction_name = "Seq"  # For pretty-printing.


class Set(IteratedRule):
    """Labelled sets.

    The labelled Set construction of the symbolic method models sets of
    elements. In the following example, Set is used to model labelled general
    trees.

    Example:
        >>> z, T = Atom(), RuleName("T")
        >>> Grammar({T: z * Set(T)})
        T -> Product(z, Set(T))

    The number of elements of the set can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> # sets of 5 to 10 elements
        >>> Set(z, geq=5, leq=10)
        Set(z, 5 <= . <= 10)

        >>> # sets of at least 5 elements
        >>> Set(z, geq=5)
        Set(z, 5 <= .)

        >>> # sets of at most 10 elements
        >>> Set(z, leq=10)
        Set(z, . <= 10)
    """

    construction_name = "Set"  # For pretty-printing.


class Cycle(IteratedRule):
    """Labelled cycles.

    A cycle is like a sequence whose components can be cyclically shifted. For
    instance: [a, b, c], [b, c, a] and [c, a, b] represent the same cycle. In
    the following example, Cycle is used to represent the class of permutations
    as a set of cycles:

    Example:
        >>> z, P = Atom(), RuleName("P")
        >>> Grammar({P: Set(Cycle(z))})
        P -> Set(Cycle(z))

    The number of elements of the cycle can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> Cycle(z, geq=5, leq=10)
        Cycle(z, 5 <= . <= 10)

        >>> Cycle(z, geq=5)
        Cycle(z, 5 <= .)

        >>> Cycle(z, leq=10)
        Cycle(z, . <= 10)
    """

    construction_name = "Cycle"

    def __init__(self, arg, leq=None, geq=None, eq=None):
        if leq == 0 or geq == 0:
            raise ValueError("Cycles should contain at least one component")
        super(Cycle, self).__init__(arg, leq, geq, eq)


class MSet(IteratedRule):
    """Unlabelled multi-sets.

    A multi-set is like a set where elements can occur multiple times. In the
    following example, MSet is used to represent the class of non-plane
    general trees:

    Examples:
        >>> z, T = Atom(), RuleName("T")
        >>> Grammar({T: z * MSet(T)})
        T -> Product(z, MSet(T))

    The number of elements of the multi-set can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> MSet(z, geq=5, leq=10)
        MSet(z, 5 <= . <= 10)

        >>> MSet(z, geq=5)
        MSet(z, 5 <= .)

        >>> MSet(z, leq=10)
        MSet(z, . <= 10)
    """

    construction_name = "MSet"  # For pretty-printing.


class UCycle(IteratedRule):
    """Unlabelled cycles.

    A cycle is like a sequence whose components can be cyclically shifted. For
    instance: [a, b, c], [b, c, a] and [c, a, b] represent the same cycle.

    The number of elements of the cycle can be constrained to be greater or
    smaller that some integer constants:

    Examples:
        >>> z = Atom()

        >>> UCycle(z, geq=5, leq=10)
        UCycle(z, 5 <= . <= 10)

        >>> UCycle(z, geq=5)
        UCycle(z, 5 <= .)

        >>> UCycle(z, leq=10)
        UCycle(z, . <= 10)
    """

    construction_name = "UCycle"  # For pretty-printing

    def __init__(self, arg, leq=None, geq=None, eq=None):
        if leq == 0 or geq == 0:
            raise ValueError("UCycles should contain at least one component")
        super(UCycle, self).__init__(arg, leq, geq, eq)


class Grammar:
    """Context free grammars."""

    def __init__(self, rules=None, labelled=False):
        r"""Create a grammar.

        The rules of the grammar can be either specified at grammar creation by
        feeding them to the constructor or specified later using the
        :py:meth:`add_rule` method.

        Args:
          rules (Dict[RuleName, Rule]): dictionary mapping RuleNames to Rules

        Examples:
            >>> z = Atom()

            The grammar of sequences

            >>> S = RuleName("S")
            >>> Grammar({S: Epsilon() + z * S})
            S -> Union(epsilon, Product(z, S))

            The grammar of binary trees

            >>> B = RuleName("B")
            >>> Grammar({B: Epsilon() + z * B * B})
            B -> Union(epsilon, Product(z, B, B))

            The grammar of unary-binary trees (or Motzkin trees)

            >>> g = Grammar()
            >>> T, U, B = RuleName("T"), RuleName("U"), RuleName("B")
            >>> g.add_rule(T, z + U + B)
            >>> g.add_rule(U, z * T)
            >>> g.add_rule(B, z * T * T)
            >>> g
            B -> Product(z, T, T)
            T -> Union(z, U, B)
            U -> Product(z, T)
        """
        self.rules = {}
        rules = rules or {}
        # Pass the dictionary of rules to the add_rule method, add_rule does
        # all the sanitizing work
        for name, rule in rules.items():
            self.add_rule(name, rule)
        self.labelled = labelled

    def add_rule(self, rule_name, rule):
        """Add a rule to the grammar.

        Args:
            rule_name (RuleName): a non-terminal symbol. If it was already
                defined in the grammar, it is replaced.

            rule (Rule): the rule defining ``rule_name``.

        Examples:
            >>> A, B, C = RuleName("A"), RuleName("B"), RuleName("C")
            >>> g = Grammar()
            >>> g.add_rule(A, Union(B, C))
            >>> g.rules[A]
            Union(B, C)
        """
        rule = _to_rule(rule)
        rule_name = _to_rule(rule_name)
        self.rules[rule_name] = rule

    def _latex_(self):
        r"""Return a LaTeX representation of the grammar.

        Examples:
            >>> z, u, T = Atom(), Marker("u"), RuleName("T")
            >>> g = Grammar({
            ...     T: z + u * z * T + z * T * T
            ...  })
            >>> print(latex(g))
            T = z + u \times z \times T + z \times T \times T

            >>> A, B, C, D = RuleName("A"), RuleName("B"), RuleName("C"), RuleName("D")
            >>> g = Grammar({
            ...     A: B,
            ...     B: Product(C, D)
            ... })
            >>> print(latex(g))
            \begin{cases}
            A &= B \\
            B &= C \times D
            \end{cases}
        """
        # Chose a simpler display for single-rule grammars
        if len(self.rules) <= 1:
            ((name, rule),) = self.rules.items()
            return "{} = {}".format(name, latex(rule))

        inside = " \\\\\n".join(
            "{} &= {}".format(name, latex(rule))
            for name, rule in sorted(self.rules.items())
        )
        return "\\begin{{cases}}\n{}\n\\end{{cases}}".format(inside)

    def __repr__(self):
        return "\n".join(
            "{} -> {}".format(non_terminal, expr)
            for non_terminal, expr in sorted(self.rules.items())
        )

    def markers(self):
        """Return all the markers appearing in the grammar.

        Examples:
            >>> z, u = Atom(), Marker("u")
            >>> B = RuleName("B")
            >>> g = Grammar({B: Union(u, Product(z, B, B))})
            >>> g.markers() == {u}
            True
        """
        return reduce(
            lambda x, y: x | y, (expr.markers() for expr in self.rules.values())
        )
