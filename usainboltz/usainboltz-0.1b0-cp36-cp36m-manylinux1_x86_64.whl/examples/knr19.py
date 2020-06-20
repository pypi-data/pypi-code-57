# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

from usainboltz import Atom, Generator, Grammar, Marker, RuleName, union_builder

# ---
# S-expressions to represent any kind of expression
# ---


class Sexpr:
    def __init__(self, constructor, *args):
        self.constructor = constructor
        self.args = args

    def __eq__(self, other):
        return (
            isinstance(other, Sexpr)
            and other.constructor == self.constructor
            and other.args == self.args
        )

    def __str__(self):
        if self.args:
            args = ", ".join(map(str, self.args))
            return "({}, {})".format(self.constructor, args)
        else:
            return str(self.constructor)

    def size(self):
        return 1 + sum(arg.size() for arg in self.args)


# ---
# Regular expressions
# ---

# UsainBoltz grammar
z = Atom()
a, b, eps = Marker("a"), Marker("b"), Marker("eps")
L = RuleName()
grammar = Grammar(rules={L: z * (a + b + eps + L + L * L + L * L)})
generator = Generator(grammar, L, singular=True)

# Expression constructors
atom_a = Sexpr("a")
atom_b = Sexpr("b")
atom_eps = Sexpr("eps")


def star(expr):
    return Sexpr("*", expr)


def concat(x, y):
    return Sexpr(".", x, y)


def union(x, y):
    return Sexpr("+", x, y)


pattern = Sexpr("*", atom_a, atom_b)


def is_pattern(expr):
    a = Sexpr("a")
    b = Sexpr("b")
    return expr == Sexpr("*", a, b) or expr == Sexpr("*", b, a)


def build_atom(name):
    return Sexpr(name)


def build_star(expr):
    # Simplification: (expr)** = (expr)*
    if expr.constructor == "*":
        return expr
    # Simplification: epsilon* = epsilon
    elif expr == atom_eps:
        return expr
    # Simplification (expr + epsilon)* = (expr)*
    elif expr.constructor == "+":
        epsilon = Sexpr("eps")
        lhs, rhs = expr.args
        if lhs == epsilon:
            return star(rhs)
        elif rhs == epsilon:
            return star(lhs)
        else:
            return star(expr)
    else:
        return star(expr)


def build_union(args):
    lhs, rhs = args
    # Simplification: (a+b)* + expr = (a+b)*
    if is_pattern(lhs) or is_pattern(rhs):
        return pattern
    else:
        return union(lhs, rhs)


def build_concat(args):
    return concat(*args)


def build(tupl):
    build_arg = union_builder(
        build_atom, build_atom, build_atom, build_star, build_union, build_concat
    )
    z, arg = tupl
    return build_arg(arg)


generator.set_builder(L, build)
