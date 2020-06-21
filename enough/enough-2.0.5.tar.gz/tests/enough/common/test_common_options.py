import argparse

from enough.common import options


def test_set_options():
    parser = argparse.ArgumentParser()
    assert options.set_options(parser) == parser
    args = parser.parse_args([])
    assert '/inventory/' in args.clouds
    driver = 'DRIVER'
    clouds = 'CLOUDS'
    args = parser.parse_args(['--driver', driver, '--clouds', clouds])
    assert args.clouds == clouds
    assert args.driver == driver
