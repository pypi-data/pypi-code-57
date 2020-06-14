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


def test_bisect():
    ftol = 4 * sys.float_info.epsilon 
    f.calls = 0

    result = rootfinding.bisect(f, (0.1, -1.5), ftol=ftol)

    check_result_full(result, f)
    assert result.f_root <= ftol
    assert pytest.approx(result.root) == -1


def test_bisect_instant():
    bracket =  (-1.00001, 1)
    f_bracket = (f(bracket[0]), None)
    f.calls = 0

    result = rootfinding.bisect(f, bracket, f_bracket=f_bracket, maxiter=0)

    assert f.calls == 1
    check_result_full(result, f)
    assert result.root == 1


def test_bisect_notabracket():
    interval = (-1.00001, -2)
    f.calls = 0

    with pytest.raises(rootfinding.NotABracketError) as exc_info:
        rootfinding.bisect(f, interval, maxiter=0)

    error = exc_info.value
    assert error.function_calls == 2
    assert len(error.f_interval) == 2
    assert all(y == f(x) for x,y in zip(interval, error.f_interval))


def test_bisect_iterationlimit():
    bracket = (0.1, -1.5)
    f.calls = 0

    with pytest.raises(rootfinding.IterationLimitReached) as exc_info:
        result = rootfinding.bisect(f, bracket, maxiter=1)

    error = exc_info.value
    assert error.function_calls == 3
    assert any(a == b for a,b in zip(bracket, error.interval))
    assert len(error.interval) == 2
    assert len(error.f_interval) == 2
    assert all(y == f(x) for x,y in zip(error.interval, error.f_interval))
