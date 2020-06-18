import datetime


class DateGenerator:
    @staticmethod
    def now():
        return datetime.datetime.utcnow()

    @staticmethod
    def one_week_earlier():
        return DateGenerator.get_datetime_with_offset(offset_hours = - 24 * 7)

    @staticmethod
    def get_datetime_with_offset(offset_hours: int) -> datetime.datetime:
        return DateGenerator.now() + datetime.timedelta(hours=offset_hours)