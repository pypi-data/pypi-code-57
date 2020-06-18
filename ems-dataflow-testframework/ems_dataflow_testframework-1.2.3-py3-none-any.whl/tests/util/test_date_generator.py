import datetime
import random
from unittest.mock import patch

from testframework.util.date_generator import DateGenerator


class TestDateGenerator:

    def setup_method(self, method):
        self.now = datetime.datetime(2017, 12, 12, 10, 0, 0)

    def test_fake_now_returnsNow(self):
        with patch("testframework.util.date_generator.datetime.datetime") as dt:
            dt.utcnow.return_value = self.now
            result = DateGenerator.now()

            dt.utcnow.assert_called_once()
            assert self.now == result

    def test_one_week_earlier_returnsApproximatelyOneWeekEarlierFromNow(self):
        with patch("testframework.util.date_generator.datetime.datetime") as dt:
            dt.utcnow.return_value = self.now
            result = DateGenerator.one_week_earlier()

            assert (self.now + datetime.timedelta(days=-7)) == result

    def test_get_datetime_with_offset_givenRandomHoursOffset_modifiesDatetimeWithThatValue(self):
        with patch("testframework.util.date_generator.datetime.datetime") as dt:
            dt.utcnow.return_value = self.now
            offset = random.randint(-100, 100)
            result = DateGenerator.get_datetime_with_offset(offset_hours=offset)

            assert (self.now + datetime.timedelta(hours=offset)) == result
