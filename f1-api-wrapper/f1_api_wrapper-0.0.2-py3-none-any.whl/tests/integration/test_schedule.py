import unittest
from f1.schedule import get_current_schedule
from f1.models import Schedule


class TestScheduleModule(unittest.TestCase):

    def test_schedule_class_is_returned(self):
        schedule = get_current_schedule()
        assert schedule.__class__  == Schedule
