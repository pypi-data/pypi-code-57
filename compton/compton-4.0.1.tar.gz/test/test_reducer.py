import pytest
from compton import (
    # Consumer,
    Orchestrator
)


def test_check():
    class A:
        pass

    with pytest.raises(
        ValueError,
        match='must be an instance of Reducer'
    ):
        Orchestrator([A()])  # type: ignore
