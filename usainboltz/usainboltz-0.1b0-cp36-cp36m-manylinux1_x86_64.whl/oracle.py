# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

"""
Various oracle implementations for Boltzmann sampling.

Oracles are used to get (often approximate) values of generating functions.
Thanks to the symbolic method, functionnal equations can be derived from
grammar specifications. This module implements some mechanics to approximate
generating functions based on these equations.

Currently three oracles are implemented:

- :class:`OracleFromDict` is quite stupid ans wraps a dictionnary
  associating :py:class:`~usainboltz.grammar.Rule` to float value into an
  :class:`Oracle`
- :class:`OracleFromPaganini` use the oracle Pagagnini of [BBD2018]_
- :class:`OracleFromNewtonGF` use the oracle NewtonGF of [PSS2012]_
  (only when Sagemath and Maple installations are present)

The entry point of these algorithms is the function oracle which determines
the oracle to use given its inputs.

AUTHORS:
- Matthieu Dien (2019): initial version
- Martin Pépin (2019): initial version

.. rubric:: References

.. [BBD2018] Maciej Bendkowski, Olivier Bodini, Sergey Dovgal, 2018,
   Polynomial tuning of multiparametric combinatorial samplers, ANALCO
.. [PSS2012] Carine Pivoteau, Bruno Salvy, Michèle Soria, 2012
   Algorithms for Combinatorial Structures: Well-founded systems and
   Newton iterations, Journal of Combinatorial Theory
"""

import sys
from functools import partial, reduce

import paganini as pg
from cvxpy import SolverError

from usainboltz.grammar import (
    Atom,
    Cycle,
    Epsilon,
    Grammar,
    Marker,
    MSet,
    Product,
    RuleName,
    Seq,
    Set,
    Symbol,
    UCycle,
    Union,
)

__all__ = ["build_oracle", "OracleFromPaganini", "OracleFromDict"]


def build_oracle(sys, **kargs):
    """Build different oracles given different inputs

    EXAMPLES::
        >>> from usainboltz import *

        >>> leaf, z = Marker("leaf"), Atom()
        >>> B = RuleName("B")
        >>> g = Grammar({B: leaf + z * B * B})
        >>> build_oracle(g)
        OracleFromPaganini(B -> Union(leaf, Product(z, B, B)))

        >>> build_oracle({'B': 2, 'z': 1./4})
        OracleFromDict({'B': 2, 'z': 0.25})
    """

    if isinstance(sys, Grammar):
        return OracleFromPaganini(sys)
    elif isinstance(sys, dict):
        return OracleFromDict(sys)

    raise TypeError(
        "I do not know what to do with a system of type {}".format(type(sys))
    )


def _to_paganini_constraint(lower_size, upper_size):
    r"""Translates constraints over :py:class:`usainboltz.grammar.IteratedRule`
    into :py:class:`paganini.Constraint`"""
    if lower_size is not None and upper_size is not None:
        if lower_size == upper_size:
            return pg.eq(lower_size)
        else:
            raise ValueError("Paganini does not support mutliple constraints.")
    elif lower_size is not None:
        return pg.geq(lower_size)
    elif upper_size is not None:
        return pg.leq(upper_size)
    else:
        return None


def _to_paganini_rule(env, rule):
    r"""Recursively translates :py:class:`usainboltz.grammar.Rule`
    into :py:class:`paganini.Expr` using the environnement `env` to
    set the expectations of pagagnini `Variables`
    """
    if isinstance(rule, Epsilon):
        return pg.Expr()
    elif isinstance(rule, Symbol):  # means Atom, Marker or RuleName
        return env[rule]
    elif isinstance(rule, Union):
        return reduce(
            lambda x, y: x + y, map(partial(_to_paganini_rule, env), rule.args)
        )
    elif isinstance(rule, Product):
        return reduce(
            lambda x, y: x * y, map(partial(_to_paganini_rule, env), rule.args)
        )
    elif isinstance(rule, Seq):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.Seq(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, Set):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.Set(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, Cycle):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.Cyc(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, MSet):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.MSet(_to_paganini_rule(env, rule.arg), constraint)
    elif isinstance(rule, UCycle):
        constraint = _to_paganini_constraint(rule.lower_size, rule.upper_size)
        return pg.UCyc(_to_paganini_rule(env, rule.arg), constraint)
    #  elif isinstance(rule, PSet):
    #  raise NotImplementedError
    else:
        raise TypeError("first argument should be of type usainboltz.grammar.Rule")


def _to_paganini_spec(grammar, weights):
    r"""Convert a :py:class:`usainboltz.grammar.Grammar` with `weights`
    over symbols into a map :py:class:`usainboltz.grammar.Rule` ->
    :py:class:`paganini.Expr` and a :py:class:`paganini.Specification`

    Example:
        >>> from usainboltz import *
        >>> eps = Epsilon();  z = Atom(); B = RuleName()
        >>> grammar = Grammar({B: eps + z * B * B})

        >>> from usainboltz.oracle import _to_paganini_spec
        >>> env, spec = _to_paganini_spec(grammar, {z:1000})
        >>> env[z], env[B]
        (var1, var0)
        >>> spec
        var0 = 1  + var1^1 var0^2
    """

    spec = pg.Specification()
    env = dict()

    for rule in set(grammar.rules.keys()):
        if rule in weights:
            env[rule] = pg.Variable(weights[rule])
        else:
            env[rule] = pg.Variable()

    z = Atom()
    if z in weights:
        env[z] = pg.Variable(weights[z])
    else:
        env[z] = pg.Variable()

    for m in grammar.markers():
        if m in weights:
            env[m] = pg.Variable(weights[m])
        else:
            env[m] = pg.Expr()

    for rulename, rule in grammar.rules.items():
        spec.add(env[rulename], _to_paganini_rule(env, rule))

    return env, spec


class Oracle:
    pass


class OracleFromPaganini(Oracle):
    r"""Build an oracle using
    `paganini <https://github.com/maciej-bendkowski/paganini>`_ : a package
    developped by M. Bendkowski and S. Dovgal

    .. todo:: add the reference to the paper
    """

    def __init__(self, grammar, sanity_checks=True):
        r"""Build an oracle from a grammar

        Args:
          grammar (:py:class:`~usainboltz.grammar.Grammar`)

          sanity_checks (bool): enable sanity checks in paganini
            tuners (``True`` by default)

        Note:
          Set ``sanity_checks`` to ``False`` only if you know what you are doing !
        """
        super(OracleFromPaganini, self).__init__()
        self.grammar = grammar
        self.pg_method = pg.Method.STRICT if sanity_checks else pg.Method.FORCE

    def _env_to_val(self, env):
        r"""Wrapper for the output of :py:meth:`tuning`
        """
        values = {
            k: float(env[k].value if isinstance(env[k], pg.Variable) else 1.0)
            for k in env
        }
        values[Epsilon] = 1.0
        return values

    def tuning(self, rule, expectations=None, singular=False):
        r"""Run the oracle's algorithm

        Args:
          rule (:py:class:`~usainboltz.grammar.Rule`): the targeted
            symbol to tune w.r.t. ``expectations``

          expectations (dict): a mapping between grammar markers and
            their targeted expectations after tuning

          singular (bool): if ``True`` run the singular tuner
            (infinite expected size) else run a tuner targeting the
            ``expectations`` given

        Returns:
            values (dict): a mapping between grammar symbols and their
            weights in the Boltzmann model

        Note:
            If ``singular`` is ``True``, then ``expectations`` should
            be should be a dictionnary with grammar names (but the
            atom) as keys and ratios (between 0 and 1) as values.

            Else, ``expectations`` should be a dictionnary with keys as
            grammar names (but ``rule``) and the values should be
            integers.

        Examples:
           Use of the singular tuner for a binary tree grammar (size
           is the number of internal nodes):

           >>> from usainboltz import *
           >>> eps = Epsilon();  z = Atom(); B = RuleName()
           >>> grammar = Grammar({B: eps + z * B * B})
           >>> o = OracleFromPaganini(grammar)
           >>> values = o.tuning(B, singular=True)
           >>> abs(values[z]-0.25) < 1e-12
           True
           >>> abs(values[B]-2.) < 1e-12
           True

           As we expect ``z`` should be :math:`\frac14` (the
           singularity of :math:`\frac{1-\sqrt{1-4z}}{2}`)
        """

        if expectations is None:
            expectations = dict()

        if rule in expectations:
            raise ValueError("You must not set any constraint over {}".format(rule))

        # Check the values of expectations w.r.t. singular or not
        if singular:
            if any(x < 0 or x > 1 for x in expectations.values()):
                raise ValueError("Ratios must be between 0 and 1")
        elif any(x < 1 for x in expectations.values()):
            raise ValueError("The expected numbers must be greater than 1")

        env, spec = _to_paganini_spec(self.grammar, expectations)

        env[rule].set_expectation(None)
        for k, v in expectations.items():
            env[k].set_expectation(v)

        try:
            if singular:
                spec.run_singular_tuner(env[Atom()], method=self.pg_method)
            else:
                spec.run_tuner(env[rule], method=self.pg_method)
        except SolverError:
            raise ValueError("Your expected sizes can not be targeted")

        return self._env_to_val(env)

    def __repr__(self):
        return "OracleFromPaganini({})".format(self.grammar)


class OracleFromDict(Oracle):
    def __init__(self, dict_):
        super(OracleFromDict, self).__init__()
        if not (isinstance(dict_, dict)):
            raise TypeError("The argument should be a dictionnary")

        self.dict_ = dict_

    def tuning(self, *args, **kwargs):
        return self.dict_

    def __repr__(self):
        return "OracleFromDict({})".format(self.dict_)


def _to_combstruct_constraint(lower_size, upper_size):
    r"""Translates sizes constraint over
    :py:class:`usainboltz.grammar.IteratedRule` into `combstruct`
    constraints.

    Examples:
        >>> from usainboltz import * # doctest: +SKIP
        >>> z = Atom(); S = RuleName("S") # doctest: +SKIP
        >>> o = OracleFromNewtonGF(Grammar({S: Seq(z, leq=3)})) # doctest: +SKIP
        >>> o.combstruct_spec # doctest: +SKIP
        '{S = Seq(Atom, card <= 3)}'
        >>> o = OracleFromNewtonGF(Grammar({S: Seq(z, geq=3)})) # doctest: +SKIP
        >>> o.combstruct_spec # doctest: +SKIP
        '{S = Seq(Atom, 3 <= card)}'
        >>> o = OracleFromNewtonGF(Grammar({S: Seq(z, eq=3)})) # doctest: +SKIP
        >>> o.combstruct_spec # doctest: +SKIP
        '{S = Seq(Atom, card = 3)}'
    """

    x = (lower_size, upper_size)
    if x == (None, None):
        return ""
    elif x == (lower_size, None):
        return f", {lower_size} <= card"
    elif x == (None, upper_size):
        return f", card <= {upper_size}"
    else:
        if lower_size == upper_size:
            return f", card = {upper_size}"
        else:
            print(
                "WARNING: NewtonGF may not handle constraints "
                + "over lower and upper sizes",
                file=sys.stderr,
            )
            return f", card <= {upper_size}, {lower_size} <= card"


def _to_combstruct_rule(rule):
    r"""Recursively translates :py:class:`~usainboltz.grammar.Rule`
    into `combstruct[specification]`
    """

    if isinstance(rule, Epsilon):
        return "Epsilon"
    elif isinstance(rule, Atom):
        return "Atom"
    elif isinstance(rule, Marker):
        return "Epsilon"
    elif isinstance(rule, RuleName):
        return str(rule)
    elif isinstance(rule, Union):
        return "Union(" + ",".join(map(_to_combstruct_rule, rule.args)) + ")"
    elif isinstance(rule, Product):
        return "Prod(" + ",".join(map(_to_combstruct_rule, rule.args)) + ")"
    elif isinstance(rule, Seq):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Sequence({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, Set):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Set({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, Cycle):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Cycle({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, MSet):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Set({_to_combstruct_rule(rule.arg)}{constraint})"
    elif isinstance(rule, UCycle):
        constraint = _to_combstruct_constraint(rule.lower_size, rule.upper_size)
        return f"Cycle({_to_combstruct_rule(rule.arg)}{constraint})"
    #  elif isinstance(rule, PSet):
    #  raise NotImplementedError
    else:
        raise TypeError("first argument should be of type usainboltz.grammar.Rule")


def _to_combstruct_spec(grammar):
    spec = set()

    for marker in grammar.markers():
        spec.add(f"{marker}=Epsilon")

    for rulename, rule in grammar.rules.items():
        spec.add(f"{rulename} = {_to_combstruct_rule(rule)}")

    return "{" + ",".join(spec) + "}"


newtongf_installed = False

try:
    from sage.interfaces.maple import maple

    maple.load("combstruct")
    maple.load("NewtonGF")
    newtongf_installed = True
    __all__.append("OracleFromNewtonGF")
except ImportError:
    pass
except RuntimeError:
    pass


class OracleFromNewtonGF(Oracle):
    r"""Build an orcale using `NewtonGF
    <http://perso.ens-lyon.fr/bruno.salvy/software/the-newtongf-package/>`_

    Note:
        If you want to use OracleFormNewtonGF, please install the
        NewtonGF library for Maple into you Maple lib/ directory,
        or precise a lib/ directory to Maple i.e.
        maple('libname:=\"NewtonGF_path\",libname:')

"""

    def __init__(self, grammar):
        r"""Build an oracle from a grammar
        """

        if not newtongf_installed:
            raise ImportError(
                "You cannot use OracleFromNewtonGF because your "
                + "Sagemath, Maple or NewtonGF installation is not "
                + "consistent."
            )

        self.grammar = grammar
        self.combstruct_spec = _to_combstruct_spec(grammar)

    def tuning(self, rule, expectations=None, singular=False):
        r"""Run the oracle's algorithm

        Args:
          rule (:py:class:`~usainboltz.grammar.Rule`): the targeted
            symbol to tune w.r.t. ``expectations``

          expectations (dict): a mapping between grammar symbols and
            their targeted expectations after tuning

          singular (bool): if ``True`` run the singular tuner
            (infinite expected size) else run a tuner targeting the
            ``expectations`` given

        Returns:
            values (dict): a mapping between grammar symbols and their
            weights in the Boltzmann model

        Note:
            In the case of NewtonGF, only **univariate**
            specifications are supported, so:
            * if `expectations` is provided it must have a key corresponding
            to `~usainboltz.grammar.Atom()`,
            * the markers (see :py:class:`~usainboltz.grammar.Marker`)
            will not be handled.

        Examples:
           Use of the singular tuner for a binary tree grammar (size
           is the number of internal nodes):

           >>> from usainboltz import *
           >>> eps = Epsilon();  z = Atom(); B = RuleName()
           >>> grammar = Grammar({B: eps + z * B * B})
           >>> o = OracleFromNewtonGF(grammar) # doctest: +SKIP
           >>> values = o.tuning(B,singular=True) # doctest: +SKIP
           >>> values[z] # doctest: +SKIP
           0.25
           >>> values[B] # doctest: +SKIP
           1.999999988

           As we expect ``z`` should be :math:`\frac14` (the
           singularity of :math:`\frac{1-\sqrt{1-4z}}{2}`)

        """

        # To remove if we do the choice to autorize only one atom per grammar
        if len(self.grammar.markers()) > 0:
            print(
                "NewtonGF deals only with univariate specifications "
                + "and there are several markers in your one",
                file=sys.stderr,
            )

        labeled = "labeled" if self.grammar.labelled else "unlabeled"

        if not singular and (expectations is None or Atom() not in expectations):
            raise ValueError(
                "You must set an expectations over the size of the structure"
            )

        rho = 0
        if singular:
            rho = maple(f"Radius({self.combstruct_spec}, {labeled})")
        else:
            rho = maple(
                f"BoltzmannParameter({self.combstruct_spec}, {labeled}, {rule}, "
                + f"{expectations[Atom()]})"
            )

        oracle = maple(
            f"NumericalNewtonIteration({self.combstruct_spec}, {labeled})({rho})"
        )
        table = str().maketrans({"=": ":", "[": "{", "]": "}"})

        self.grammar_symbols = {
            str(symbol): symbol
            for symbol in self.grammar.markers() | set(self.grammar.rules)
        }

        values = eval(str(oracle).translate(table), globals(), self.grammar_symbols)
        values[Atom()] = float(rho)
        return values

    def __repr__(self):
        return "OracleFromNewtonGF({})".format(self.grammar)
