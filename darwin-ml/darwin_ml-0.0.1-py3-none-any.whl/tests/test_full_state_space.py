import unittest
from loguru import logger
import pandas_datareader.data as web

class TestFullStateSpace(unittest.TestCase):
    """This is a full backtest integration testing.

    Args:
        unittest: [description]
    """

    def setUp(self):
        logger.warning("download some test data from yfinance")
        logger.debug("Store that data and get the metadata id.")
        logger.success("Attach a userid")
        logger.error("Convert the data into technical analysis")
        logger.info("Convert the data into technical analysis")

    def tearDown(self):
        pass

    def test_upper(self):
        pass

    def test_isupper(self):
        pass

    def test_split(self):
        pass


if __name__ == '__main__':
    unittest.main()