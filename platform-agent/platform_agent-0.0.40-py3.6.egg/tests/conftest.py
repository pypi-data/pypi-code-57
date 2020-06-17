from pytest import fixture


@fixture
def standard_coin_set():
    return [1, 2, 5, 10, 20, 50]


@fixture
def custom_coin_set():
    return [1, 3, 10, 22, 84]


@fixture
def custom_coin_set_even():
    return [2, 4, 8, 16]


@fixture
def list_of_coins():
    return [7, 7, 7, 5, 4, 3, 4, 6, 7, 7, 99]
