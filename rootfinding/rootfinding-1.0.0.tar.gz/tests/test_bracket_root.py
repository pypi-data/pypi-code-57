import pytest

import sys

import rootfinding

def f(x):
    f.calls += 1
    return x**2 - 1


def check_result_full(result, f):
    fcalls = f.calls
    assert result.function_calls == fcalls
    assert 0 <= result.iterations <= fcalls
    assert isinstance(result, rootfinding.Result)
    assert result.f_root == f(result.root)
    assert len(result.bracket) == 2
    assert len(result.f_bracket) == 2
    assert all(y == f(x) for x,y in zip(result.bracket, result.f_bracket))
    f.calls = fcalls


def check_result_bracketonly(result, f):
    fcalls = f.calls
    assert result.function_calls == fcalls
    assert 0 <= result.iterations <= fcalls
    assert isinstance(result, rootfinding.Result)
    assert result.root is None
    assert result.f_root is None
    assert len(result.bracket) == 2
    assert len(result.f_bracket) == 2
    assert all(y == f(x) for x,y in zip(result.bracket, result.f_bracket))
    f.calls = fcalls


def check_result_rootonly(result, f):
    fcalls = f.calls
    assert result.function_calls == fcalls
    assert 0 <= result.iterations <= fcalls
    assert isinstance(result, rootfinding.Result)
    assert result.f_root == f(result.root)
    assert result.bracket is None
    assert result.f_bracket is None
    f.calls = fcalls


def test_bracket_root():
    f.calls = 0

    result = rootfinding.bracket_root(f, (0, -0.1))

    check_result_bracketonly(result, f)
    assert result.iterations >= 1
    rootfinding.bisect(f, result.bracket, f_bracket=result.f_bracket)


def test_bracket_root_instantbracket():
    interval = (0, 2)
    f_interval = (None, f(interval[1]))
    f.calls = 0

    result = rootfinding.bracket_root(f, interval, f_interval=f_interval, maxiter=0)

    assert f.calls == 1
    check_result_bracketonly(result, f)
    rootfinding.bisect(f, result.bracket, f_bracket=result.f_bracket)


def test_bracket_root_instantroot():
    interval = (0, -1)
    f_interval = (f(interval[0]), None)
    f.calls = 0

    result = rootfinding.bracket_root(f, interval, f_interval=f_interval, ftol=0, maxiter=0)

    assert f.calls == 1
    check_result_rootonly(result, f)


def test_bracket_root_instantrootwithbracket():
    interval = (0, -1.00001)
    f_interval = (f(interval[0]), None)
    f.calls = 0

    result = rootfinding.bracket_root(f, interval, f_interval=f_interval, ftol=1e-3, maxiter=0)

    assert f.calls == 1
    check_result_full(result, f)
    rootfinding.bisect(f, result.bracket)


def test_bracket_root_iterationlimit():
    f.calls = 0

    with pytest.raises(rootfinding.IterationLimitReached) as exc_info:
        result = rootfinding.bracket_root(f, (-1, -2))

    error = exc_info.value
    assert len(error.interval) == 2
    assert len(error.f_interval) == 2
    assert all(y == f(x) for x,y in zip(error.interval, error.f_interval))

    with pytest.raises(rootfinding.NotABracketError):
        rootfinding.bisect(f, error.interval, f_bracket=error.f_interval)
