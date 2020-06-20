from unittest import TestCase
from unittest.mock import patch, call

import peper.__main__


class TestMain(TestCase):
    def test_main(self):
        with patch("sys.argv", ["test", "jajca"]):
            peper.__main__.main()