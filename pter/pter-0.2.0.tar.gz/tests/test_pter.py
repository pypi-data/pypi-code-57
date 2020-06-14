import datetime
import unittest

from pytodotxt import Task
from pter import utils


class TestPytodoterm(unittest.TestCase):
    def test_parse_duration(self):
        text = '1h10m'
        then = utils.parse_duration(text)
        self.assertEqual(then, datetime.timedelta(hours=1, minutes=10))

    def test_update_spent(self):
        then = (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime(utils.DATETIME_FMT)
        task = Task(f'Something spent:1h10m tracking:{then}')

        self.assertTrue(utils.update_spent(task))
        self.assertEqual(task.attributes, {'spent': ['1h20m']})


if __name__ == '__main__':
    unittest.main()

