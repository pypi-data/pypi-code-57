from pyback.strategy import Strategy


def test_init():
    """Test Strategy instances can be initialized correctly
    """

    strategy = Strategy("SMA")

    assert strategy.name == "SMA"
