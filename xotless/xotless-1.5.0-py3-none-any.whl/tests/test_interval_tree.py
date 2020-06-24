#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pickle
from datetime import datetime
from hypothesis import strategies as st, given

from ..ranges import Range
from ..trees import Cell, IntervalTree
from .strategies.domains import (
    many_date_ranges,
    members_of_date_ranges,
    date_ranges,
)
from .strategies.domains import (
    many_float_ranges,
    members_of_float_ranges,
    float_ranges,
)


MORE_THAN_ONE_LIFETIME = Range.new_open_right(
    datetime(1978, 10, 21), datetime(9078, 10, 21)
)


@given(st.data(), many_date_ranges(5, outer=MORE_THAN_ONE_LIFETIME))
def test_date_interval_trees_finds_the_right_interval(data, intervals):
    cells = [Cell.from_range(r, i) for i, r in enumerate(intervals)]
    tree = IntervalTree.from_cells(cells)
    picked_cell = data.draw(st.sampled_from(cells))
    interval = Range.new_open_right(
        picked_cell.lowerbound, picked_cell.upperbound
    )
    member = data.draw(members_of_date_ranges(interval))
    assert tree[member] == (picked_cell,)
    for protocol in range(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL):
        tree = pickle.loads(pickle.dumps(tree, protocol))
        assert tree[member] == (picked_cell,)


@given(st.data(), many_float_ranges(5, outer=Range.new_open_right(-1e10, 1e10)))
def test_float_interval_trees_finds_the_right_interval(data, intervals):
    cells = [Cell.from_range(r, i) for i, r in enumerate(intervals)]
    tree = IntervalTree.from_cells(cells)
    picked_cell = data.draw(st.sampled_from(cells))
    interval = Range.new_open_right(
        picked_cell.lowerbound, picked_cell.upperbound
    )
    member = data.draw(members_of_float_ranges(interval))
    assert tree[member] == (picked_cell,)
    for protocol in range(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL):
        tree = pickle.loads(pickle.dumps(tree, protocol))
        assert tree[member] == (picked_cell,)


@given(
    st.data(),
    st.lists(
        float_ranges(
            outer=Range.new_open_right(-1e10, 1e10),
            kinds=st.just(Range.new_open_right),
        ),
        min_size=1,
        max_size=10,
    ),
)
def test_float_interval_trees_finds_only_the_right_intervals(data, intervals):
    cells = [Cell.from_range(r, i) for i, r in enumerate(intervals)]
    tree = IntervalTree.from_cells(cells)
    picked_cell = data.draw(st.sampled_from(cells))
    interval = Range.new_open_right(
        picked_cell.lowerbound, picked_cell.upperbound
    )
    member = data.draw(members_of_float_ranges(interval))
    expected = {cell for cell in cells if member in cell}
    assert set(tree[member]) == expected
    if len(cells):
        assert len(expected)
    for protocol in range(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL):
        tree = pickle.loads(pickle.dumps(tree, protocol))
        assert set(tree[member]) == expected


@given(
    st.data(),
    st.lists(
        date_ranges(
            outer=MORE_THAN_ONE_LIFETIME, kinds=st.just(Range.new_open_right)
        ),
        min_size=1,
        max_size=10,
    ),
)
def test_date_interval_trees_finds_only_the_right_intervals(data, intervals):
    cells = [Cell.from_range(r, i) for i, r in enumerate(intervals)]
    tree = IntervalTree.from_cells(cells)
    picked_cell = data.draw(st.sampled_from(cells))
    interval = Range.new_open_right(
        picked_cell.lowerbound, picked_cell.upperbound
    )
    member = data.draw(members_of_date_ranges(interval))
    expected = {cell for cell in cells if member in cell}
    assert set(tree[member]) == expected
    if len(cells):
        assert len(expected)
    for protocol in range(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL):
        tree = pickle.loads(pickle.dumps(tree, protocol))
        assert set(tree[member]) == expected
