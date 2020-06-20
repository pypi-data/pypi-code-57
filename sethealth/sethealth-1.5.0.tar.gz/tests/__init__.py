import unittest
import sethealth
import os


class TestAPI(unittest.TestCase):
    def test_valid(self):
        client = sethealth.Client(
            os.environ["SETHEALTH_KEY"], os.environ["SETHEALTH_SECRET"]
        )
        token = client.getToken()
        self.assertGreater(len(token), 10)

    def test_unvalid(self):
        with self.assertRaises(sethealth.AuthException):
            client = sethealth.Client("", "")
            client.getToken()


if __name__ == "__main__":
    unittest.main()
