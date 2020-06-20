# coding: utf-8

# Copyright 2019 Matthieu Dien and Martin Pépin
# Distributed under the license GNU GPL v3 or later
# See LICENSE.txt for more informations

r"""Mondrian paintings generation.

Generate a Mondrian painting from a simple grammar.

>>> from usainboltz.examples.mondrian import *

>>> grammar
canvas -> Product(window, window, window, window)
window -> Union(Product(red, z),
                Product(blue, z),
                Product(yellow, z),
                Product(white, z),
                Product(black, z),
                Product(window, window, window, window))

The image is generated in svg format using the builders mechanism.

>>> sizes = {square: (20, 30), blue: (2, 4), red: (2, 4), yellow: (2, 4), black: (2, 4)}
>>> painting = generator.sample(sizes)
>>> print(painting)  # doctest: +ELLIPSIS
<svg width="1440" height="1440" xmlns="http://www.w3.org/2000/svg">
...

.. image:: ../_static/img/mondrian.svg
   :height: 480px
   :width: 480px
   :align: center
"""

from usainboltz import (
    Atom,
    Generator,
    Grammar,
    Marker,
    OracleFromPaganini,
    RuleName,
    union_builder,
)
from usainboltz.generator import seed as generator_seed

LENGTH = 5
STROKE = 4

red, blue, yellow, white, black = (
    Marker(color) for color in ("red", "blue", "yellow", "white", "black")
)
square = Atom()
window = RuleName("window")
canvas = RuleName("canvas")

grammar = Grammar(
    {
        canvas: window * window * window * window,
        window: red * square
        + blue * square
        + yellow * square
        + white * square
        + black * square
        + window * window * window * window,
    }
)

target_colors = {white: 0.6}

oracle = OracleFromPaganini(grammar, sanity_checks=False)
generator = Generator(
    grammar, canvas, singular=True, expectations=target_colors, oracle=oracle
)


def color_builder(t):
    color, _ = t
    return (
        f'<rect width="{LENGTH}" height="{LENGTH}" fill="{color}" '
        'vector-effect="non-scaling-stroke"/>',
        1,
    )


def pack_translate_scale(t):
    block, v, s = t
    return f'<g transform="translate({v[0]} {v[1]}), scale({s})">\n{block[0]}\n</g>'


def quad_builder(windows):
    sizes = [w[1] for w in windows]
    biggest = max(sizes)
    scale_factors = [biggest / x for x in sizes]
    translations = [
        (0, 0),
        (LENGTH * biggest, 0),
        (0, LENGTH * biggest),
        (LENGTH * biggest, LENGTH * biggest),
    ]
    return (
        "\n".join(map(pack_translate_scale, zip(windows, translations, scale_factors))),
        2 * biggest,
    )


window_builder = union_builder(
    color_builder,
    color_builder,
    color_builder,
    color_builder,
    color_builder,
    quad_builder,
)


def canvas_builder(windows):
    size = ((max([w[1] for w in windows])) * LENGTH * 2 + 40) * 4
    r = f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">'
    r += f'\n<g stroke="black" stroke-width="{STROKE}"'
    r += ' transform="scale(4) translate(20 20)">\n'
    r += quad_builder(windows)[0]
    r += "</g>\n</svg>"
    return r


generator.set_builder(window, window_builder)
generator.set_builder(canvas, canvas_builder)
generator_seed(0xDEADB017)

if __name__ == "__main__":
    print(
        generator.sample(
            {square: (20, 30), blue: (2, 4), red: (2, 4), yellow: (2, 4), black: (2, 4)}
        )
    )
